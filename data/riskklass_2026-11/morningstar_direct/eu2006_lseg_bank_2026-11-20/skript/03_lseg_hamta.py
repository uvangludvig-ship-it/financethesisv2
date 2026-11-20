"""Monthly share-class total net assets from LSEG Workspace (Lipper) for the ISIN list.

    python lseg_hamta.py prov        10 test funds. Tries three ways and prints what works.
    python lseg_hamta.py allt A      whole list with way A (get_data). Resumes if interrupted.
    python lseg_hamta.py allt B      whole list with way B (get_history).
    python lseg_hamta.py torr        dry run with made-up numbers, no LSEG needed.

Needs: LSEG Workspace open and logged in, and  pip install lseg-data
Files in the same folder: lseg_isin_list_2006.csv
Writes: lseg_tna_2002_2008.csv (ISIN, date, tna_usd) and lseg_missing.csv (ISIN with no data)

NOT tested against LSEG. Run "prov" first.
"""
import os
import sys
import time

import pandas as pd

START, END = "2002-12-31", "2008-12-31"
LISTA, UT, SAKNAS = "lseg_isin_list_2006.csv", "lseg_tna_2002_2008.csv", "lseg_missing.csv"
FIELD = "TR.FundTotalNetAssets"
PARAMS = {"SDate": START, "EDate": END, "Frq": "M", "Curn": "USD"}
BATCH = 50
COLS = ["ISIN", "date", "tna_usd"]


class Fake:
    """Made-up data for the dry run."""

    def open_session(self):
        pass

    def get_data(self, universe, fields, parameters=None):
        d = pd.date_range("2003-01-31", "2003-06-30", freq="ME") if parameters else pd.to_datetime(["2026-10-31"])
        rows = [(u, x, 100.0 + i) for u in universe[:-1] for i, x in enumerate(d)]
        return pd.DataFrame(rows, columns=["Instrument", "Date", "Fund Total Net Assets"])

    def get_history(self, universe, fields, start=None, end=None, interval=None, parameters=None):
        d = pd.date_range("2003-01-31", "2003-06-30", freq="ME")
        return pd.DataFrame({u: range(len(d)) for u in universe[:-1]}, index=d, dtype=float)


def session(fake=False):
    if fake:
        return Fake()
    try:
        import lseg.data as ld
    except ImportError:
        import refinitiv.data as ld
    ld.open_session()
    return ld


def tidy_a(df):
    """get_data gives one row per instrument and date."""
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=COLS)
    df = df.copy()
    df.columns = [str(c) for c in df.columns]
    inst = df.columns[0]
    datec = [c for c in df.columns if "date" in c.lower()]
    valc = [c for c in df.columns if c != inst and c not in datec]
    if not datec or not valc:
        return pd.DataFrame(columns=COLS)
    out = pd.DataFrame({
        "ISIN": df[inst].astype(str),
        "date": pd.to_datetime(df[datec[0]], errors="coerce").dt.date,
        "tna_usd": pd.to_numeric(df[valc[-1]], errors="coerce"),
    })
    return out.dropna(subset=["date", "tna_usd"])


def tidy_b(df, codes):
    """get_history gives dates as index and one column per instrument."""
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=COLS)
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [str(c[0]) for c in df.columns]
    df.columns = [str(c) for c in df.columns]
    if len(codes) == 1 and df.shape[1] == 1:
        df.columns = [codes[0]]
    out = df.reset_index().melt(id_vars=df.index.name or "index", var_name="ISIN", value_name="tna_usd")
    out = out.rename(columns={out.columns[0]: "date"})
    out["date"] = pd.to_datetime(out["date"], errors="coerce").dt.date
    out["tna_usd"] = pd.to_numeric(out["tna_usd"], errors="coerce")
    return out.dropna(subset=["date", "tna_usd"])[COLS]


def fetch(ld, codes, way):
    if way == "A":
        return tidy_a(ld.get_data(universe=codes, fields=[FIELD + ".date", FIELD], parameters=PARAMS))
    return tidy_b(ld.get_history(universe=codes, fields=[FIELD], start=START, end=END, interval="monthly",
                                 parameters={"Curn": "USD"}), codes)


def prov(fake=False):
    ld = session(fake)
    lst = pd.read_csv(LISTA)
    codes = lst.loc[lst.test10 == "yes", "ISIN"].tolist()
    names = lst.set_index("ISIN").Name
    res = pd.DataFrame(index=codes)
    res["name"] = [str(names.get(c, ""))[:34] for c in codes]
    res["closed"] = lst.set_index("ISIN").closed.reindex(codes).values
    for way in ("A", "B"):
        try:
            t = fetch(ld, codes, way)
            g = t.groupby("ISIN")
            res[f"{way}_months"] = g.size().reindex(codes).fillna(0).astype(int)
            res[f"{way}_first"] = g.date.min().reindex(codes)
            res[f"{way}_last"] = g.date.max().reindex(codes)
            res[f"{way}_first_value"] = g.tna_usd.first().reindex(codes)
            if way == "A" and len(t):
                print("\nWay A, first rows as returned:")
                print(t.head(8).to_string(index=False))
        except Exception as e:  # noqa: BLE001
            print(f"\nWay {way} failed: {type(e).__name__}: {e}")
    try:
        snap = tidy_a(ld.get_data(universe=codes, fields=[FIELD + ".date", FIELD]))
        res["latest_value"] = snap.groupby("ISIN").tna_usd.last().reindex(codes)
    except Exception as e:  # noqa: BLE001
        print(f"\nLatest value failed: {type(e).__name__}: {e}")
    pd.set_option("display.width", 250)
    print("\nRESULT (73 months is a full series):")
    print(res.to_string())
    print("\nCopy everything above and send it to Claude.")


def allt(way, fake=False):
    ld = session(fake)
    lst = pd.read_csv(LISTA)
    codes = lst["ISIN"].dropna().drop_duplicates().tolist()
    done = set()
    if os.path.exists(UT):
        done |= set(pd.read_csv(UT, usecols=["ISIN"]).ISIN.astype(str))
    if os.path.exists(SAKNAS):
        done |= set(pd.read_csv(SAKNAS).ISIN.astype(str))
    todo = [c for c in codes if c not in done]
    print(f"{len(codes)} ISIN in the list, {len(done)} already done, {len(todo)} to fetch, way {way}")
    for i in range(0, len(todo), BATCH):
        part = todo[i:i + BATCH]
        t = None
        for attempt in range(4):
            try:
                t = fetch(ld, part, way)
                break
            except Exception as e:  # noqa: BLE001
                print(f"  batch {i // BATCH + 1}: {type(e).__name__}: {e}. Waiting {10 * (attempt + 1)} s")
                time.sleep(10 * (attempt + 1))
        if t is None:
            print(f"  batch {i // BATCH + 1} skipped after four tries. Run the command again later.")
            continue
        t = t[t.ISIN.isin(part)]
        t.to_csv(UT, mode="a", header=not os.path.exists(UT), index=False)
        miss = [c for c in part if c not in set(t.ISIN)]
        if miss:
            pd.DataFrame({"ISIN": miss}).to_csv(SAKNAS, mode="a", header=not os.path.exists(SAKNAS), index=False)
        print(f"  {min(i + BATCH, len(todo))}/{len(todo)}: {t.ISIN.nunique()} of {len(part)} with data, {len(t)} rows")
        time.sleep(1)
    print(f"Done. Send {UT} and {SAKNAS} to Claude.")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "prov":
        prov()
    elif mode == "allt" and len(sys.argv) > 2 and sys.argv[2] in ("A", "B"):
        allt(sys.argv[2])
    elif mode == "torr":
        prov(fake=True)
        UT, SAKNAS = "torr_" + UT, "torr_" + SAKNAS
        allt("A", fake=True)
    else:
        print(__doc__)
