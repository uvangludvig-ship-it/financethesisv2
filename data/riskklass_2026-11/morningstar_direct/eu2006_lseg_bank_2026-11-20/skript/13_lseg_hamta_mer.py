"""More from LSEG Workspace (Lipper) for the same ISIN list as 03_lseg_hamta.py.

    python3 13_lseg_hamta_mer.py prov             10 test funds. Prints what LSEG returns. Run this first.
    python3 13_lseg_hamta_mer.py tna              net assets 1999-12 to 2002-12 for the whole list. Resumes if interrupted.
    python3 13_lseg_hamta_mer.py bolag            fund company per ISIN for the whole list. Resumes if interrupted.
    python3 13_lseg_hamta_mer.py bolag TR.Xxx     same, plus extra fields that "prov" showed exist.
    python3 13_lseg_hamta_mer.py torr             dry run with made-up numbers, no LSEG needed.

Needs: LSEG Workspace open and logged in, and the same Python as last time (pip install lseg-data).
Reads:  ../radata/lseg_isin_list_2006.csv
Writes: ../radata/lseg_tna_2000_2002.csv (ISIN, date, tna_usd), ../radata/lseg_missing_2000_2002.csv,
        ../radata/lseg_fondbolag.csv (ISIN, fund_name, fund_company, fund_company_2006, extra fields)

Verified: TR.FundTotalNetAssets with SDate/EDate/Frq/Curn worked on 20 Nov 2026 (03_lseg_hamta.py, way A).
          TR.FundCompany is named in LSEG's developer forum as the fund management company.
NOT verified: whether TR.FundCompany gives the 2006 name when SDate is set; the fields in GUESSES.
"""
import os
import sys
import time

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RA = os.path.join(HERE, "..", "radata")
LISTA = os.path.join(RA, "lseg_isin_list_2006.csv")
UT_TNA = os.path.join(RA, "lseg_tna_2000_2002.csv")
SAKNAS = os.path.join(RA, "lseg_missing_2000_2002.csv")
UT_BOLAG = os.path.join(RA, "lseg_fondbolag.csv")

START, END = "1999-12-31", "2002-12-31"   # 2002-12 overlaps the first file, as a check
TNA = "TR.FundTotalNetAssets"
PARAMS = {"SDate": START, "EDate": END, "Frq": "M", "Curn": "USD"}
REF2006 = "2006-10-31"
GUESSES = ["TR.FundPromoter", "TR.FundPromoterName", "TR.FundManagementCompany", "TR.FundAdvisor",
           "TR.FundInvestmentAdvisor", "TR.FundCompanyUltimateParent", "TR.FundTER"]
BATCH = 50


class Fake:
    """Made-up data for the dry run."""

    def open_session(self):
        pass

    def get_data(self, universe, fields, parameters=None):
        if any(f.startswith(TNA) for f in fields):
            d = pd.date_range("2000-01-31", "2000-06-30", freq="ME")
            rows = [(u, x, 100.0 + i) for u in universe[:-1] for i, x in enumerate(d)]
            return pd.DataFrame(rows, columns=["Instrument", "Date", "Fund Total Net Assets"])
        if fields[0] in GUESSES[2:]:
            raise ValueError("made-up error: unknown field")
        out = pd.DataFrame({"Instrument": universe})
        for f in fields:
            out[f] = ["Bolag " + u[-3:] + (" 2006" if parameters else "") for u in universe]
        out.iloc[-1, 1:] = None
        return out


def session(fake=False):
    if fake:
        return Fake()
    try:
        import lseg.data as ld
    except ImportError:
        import refinitiv.data as ld
    ld.open_session()
    return ld


def tidy_tna(df):
    cols = ["ISIN", "date", "tna_usd"]
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=cols)
    df = df.copy()
    df.columns = [str(c) for c in df.columns]
    inst = df.columns[0]
    datec = [c for c in df.columns if "date" in c.lower()]
    valc = [c for c in df.columns if c != inst and c not in datec]
    if not datec or not valc:
        return pd.DataFrame(columns=cols)
    out = pd.DataFrame({"ISIN": df[inst].astype(str),
                        "date": pd.to_datetime(df[datec[0]], errors="coerce").dt.date,
                        "tna_usd": pd.to_numeric(df[valc[-1]], errors="coerce")})
    return out.dropna(subset=["date", "tna_usd"])


def static(ld, codes, field, parameters=None):
    """One text field per ISIN. Returns a Series indexed by ISIN (empty strings become missing)."""
    df = ld.get_data(universe=codes, fields=[field], parameters=parameters) if parameters else ld.get_data(universe=codes, fields=[field])
    if df is None or len(df) == 0 or df.shape[1] < 2:
        return pd.Series(index=codes, dtype=object)
    s = df.drop_duplicates(df.columns[0]).set_index(df.columns[0]).iloc[:, -1]
    s = s.where(s.astype(str).str.strip().ne("") & s.notna())
    s.index = s.index.astype(str)
    return s.reindex(codes)


def retry(fn, label):
    for attempt in range(4):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            print(f"  {label}: {type(e).__name__}: {e}. Waiting {10 * (attempt + 1)} s")
            time.sleep(10 * (attempt + 1))
    print(f"  {label} skipped after four tries. Run the command again later.")
    return None


def prov(fake=False):
    ld = session(fake)
    lst = pd.read_csv(LISTA)
    codes = lst.loc[lst.test10 == "yes", "ISIN"].tolist()
    res = pd.DataFrame(index=codes)
    res["name"] = lst.set_index("ISIN").Name.reindex(codes).astype(str).str[:30].values
    try:
        t = tidy_tna(ld.get_data(universe=codes, fields=[TNA + ".date", TNA], parameters=PARAMS))
        g = t.groupby("ISIN")
        res["tna_months"] = g.size().reindex(codes).fillna(0).astype(int)
        res["tna_first"] = g.date.min().reindex(codes)
        res["tna_last"] = g.date.max().reindex(codes)
    except Exception as e:  # noqa: BLE001
        print(f"Net assets failed: {type(e).__name__}: {e}")
    for col, par in (("company_now", None), ("company_2006", {"SDate": REF2006})):
        try:
            res[col] = static(ld, codes, "TR.FundCompany", par).astype(str).str[:34].values
        except Exception as e:  # noqa: BLE001
            print(f"TR.FundCompany ({col}) failed: {type(e).__name__}: {e}")
    pd.set_option("display.width", 250)
    print("\nRESULT (37 months is a full series 1999-12 to 2002-12):")
    print(res.to_string())
    print("\nGUESSED FIELDS (how many of the 10 funds got a value, and one example):")
    for f in GUESSES:
        try:
            s = static(ld, codes, f)
            ex = str(s.dropna().iloc[0])[:50] if s.notna().any() else ""
            print(f"  {f:32s} {int(s.notna().sum()):2d} of {len(codes)}   {ex}")
        except Exception as e:  # noqa: BLE001
            print(f"  {f:32s} failed: {type(e).__name__}: {str(e)[:80]}")
    print("\nCopy everything above and send it to Claude.")


def tna(fake=False):
    ld = session(fake)
    codes = pd.read_csv(LISTA)["ISIN"].dropna().drop_duplicates().tolist()
    done = set()
    if os.path.exists(UT_TNA):
        done |= set(pd.read_csv(UT_TNA, usecols=["ISIN"]).ISIN.astype(str))
    if os.path.exists(SAKNAS):
        done |= set(pd.read_csv(SAKNAS).ISIN.astype(str))
    todo = [c for c in codes if c not in done]
    print(f"{len(codes)} ISIN in the list, {len(done)} already done, {len(todo)} to fetch")
    for i in range(0, len(todo), BATCH):
        part = todo[i:i + BATCH]
        t = retry(lambda: tidy_tna(ld.get_data(universe=part, fields=[TNA + ".date", TNA], parameters=PARAMS)), f"batch {i // BATCH + 1}")
        if t is None:
            continue
        t = t[t.ISIN.isin(part)]
        t.to_csv(UT_TNA, mode="a", header=not os.path.exists(UT_TNA), index=False)
        miss = [c for c in part if c not in set(t.ISIN)]
        if miss:
            pd.DataFrame({"ISIN": miss}).to_csv(SAKNAS, mode="a", header=not os.path.exists(SAKNAS), index=False)
        print(f"  {min(i + BATCH, len(todo))}/{len(todo)}: {t.ISIN.nunique()} of {len(part)} with data, {len(t)} rows")
        time.sleep(1)
    print(f"Done. Files: {os.path.basename(UT_TNA)} and {os.path.basename(SAKNAS)} in radata/.")


def bolag(extra, fake=False):
    ld = session(fake)
    codes = pd.read_csv(LISTA)["ISIN"].dropna().drop_duplicates().tolist()
    done = set(pd.read_csv(UT_BOLAG, usecols=["ISIN"]).ISIN.astype(str)) if os.path.exists(UT_BOLAG) else set()
    todo = [c for c in codes if c not in done]
    print(f"{len(codes)} ISIN in the list, {len(done)} already done, {len(todo)} to fetch. Extra fields: {extra or 'none'}")
    for i in range(0, len(todo), BATCH):
        part = todo[i:i + BATCH]

        def one():
            out = pd.DataFrame({"ISIN": part})
            out["fund_name"] = static(ld, part, "TR.FundName").values
            out["fund_company"] = static(ld, part, "TR.FundCompany").values
            out["fund_company_2006"] = static(ld, part, "TR.FundCompany", {"SDate": REF2006}).values
            for f in extra:
                out[f] = static(ld, part, f).values
            return out

        out = retry(one, f"batch {i // BATCH + 1}")
        if out is None:
            continue
        out.to_csv(UT_BOLAG, mode="a", header=not os.path.exists(UT_BOLAG), index=False)
        print(f"  {min(i + BATCH, len(todo))}/{len(todo)}: {int(out.fund_company.notna().sum())} of {len(part)} with fund company")
        time.sleep(1)
    print(f"Done. File: {os.path.basename(UT_BOLAG)} in radata/.")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "prov":
        prov()
    elif mode == "tna":
        tna()
    elif mode == "bolag":
        bolag(sys.argv[2:])
    elif mode == "torr":
        prov(fake=True)
        UT_TNA, SAKNAS, UT_BOLAG = (os.path.join(RA, "torr_" + os.path.basename(p)) for p in (UT_TNA, SAKNAS, UT_BOLAG))
        tna(fake=True)
        bolag(["TR.FundPromoter"], fake=True)
    else:
        print(__doc__)
