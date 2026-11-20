"""Bygger fond-månadspanel för replikering av Ben-David m.fl. (2022) på USA-data ur Morningstar Direct.
Specifikation: claude/DEKLARATION_replikering_bendavid_usa_1999_2005_2026-11-18.md
Användning: python3 -I bygg_panel.py <export.csv> <ut.pkl>
"""
import sys, re
import numpy as np
import pandas as pd

LAMBDA = 0.20551497
INDEX_RE = r"\bIndex\b|\bIdx\b|\bIndx\b|S&P 500|Total Stock|Total Market|Extended Market|Wilshire 5000"

src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, encoding="latin-1", low_memory=False, dtype=str)
df.columns = [re.sub(r"\s+", " ", c.replace("\n", " ")).strip() for c in df.columns]
df = df[df["Morningstar Category Group"].eq("Equity")].copy()  # tar bort sammanfattningsraderna sist i filen

static = df[["SecId", "FundId", "Name", "Morningstar Category", "Inception Date", "Annual Report Net Expense Ratio"]].copy()
static["inc"] = pd.to_datetime(static["Inception Date"], errors="coerce")
static["exp"] = pd.to_numeric(static["Annual Report Net Expense Ratio"], errors="coerce")

def long(prefix, name):
    cs = [c for c in df.columns if c.startswith(prefix) and re.search(r"\d{4}-\d{2}", c)]
    x = df[["SecId", "FundId"] + cs].melt(id_vars=["SecId", "FundId"], var_name="c", value_name=name)
    x["ym"] = x["c"].str.extract(r"(\d{4}-\d{2})")[0]
    x[name] = pd.to_numeric(x[name].str.replace(",", ""), errors="coerce")
    return x.drop(columns="c")

r = long("Monthly Return", "r")
na = long("Net Assets - share class (Monthly)", "na")
st = long("Morningstar Rating Overall", "star")
p = r.merge(na, on=["SecId", "FundId", "ym"], how="left").merge(st, on=["SecId", "FundId", "ym"], how="left")
p = p.sort_values(["SecId", "ym"]).reset_index(drop=True)
p["na_l"] = p.groupby("SecId")["na"].shift(1)
p["dflow"] = p["na"] - p["na_l"] * (1 + p["r"] / 100)

# Fondavkastning: förmögenhetsviktad med förra månadens förmögenhet; likaviktad där vikter saknas (före 1999)
q = p.dropna(subset=["r"]).copy()
q["w"] = q["na_l"]
has_w = q.groupby(["FundId", "ym"])["w"].transform(lambda s: s.notna().any())
q.loc[~has_w, "w"] = 1.0
q = q.dropna(subset=["w"])
q = q[q["w"] > 0]
fr = q.assign(rw=q["r"] * q["w"]).groupby(["FundId", "ym"]).agg(rw=("rw", "sum"), w=("w", "sum")).reset_index()
fr["ret"] = fr["rw"] / fr["w"]
fr = fr[["FundId", "ym", "ret"]]

# Flöde: dollarflöde per klass summerat, delat med förra månadens förmögenhet hos samma klasser
fl = p.dropna(subset=["dflow"]).groupby(["FundId", "ym"]).agg(dflow=("dflow", "sum"), tna_l=("na_l", "sum")).reset_index()
fl["flow"] = 100 * fl["dflow"] / fl["tna_l"]
fl["flow_usd"] = fl["dflow"] / 1e6

# Stjärna per betygsdatum (slutet av månaden), förmögenhetsviktad med förmögenheten samma datum
s = p.dropna(subset=["star"]).copy()
s["w"] = s["na"]
has_w = s.groupby(["FundId", "ym"])["w"].transform(lambda z: z.notna().any())
s.loc[~has_w, "w"] = 1.0
s = s.dropna(subset=["w"])
s = s[s["w"] > 0]
fs = s.assign(sw=s["star"] * s["w"]).groupby(["FundId", "ym"]).agg(sw=("sw", "sum"), w=("w", "sum")).reset_index()
fs["star_raw"] = fs["sw"] / fs["w"]
fs["star_d"] = np.floor(fs["star_raw"] + 0.5).clip(1, 5)  # betyg daterat ym
fs = fs[["FundId", "ym", "star_d"]]

# Fondpanel på månadsrutnät
months = sorted(r["ym"].unique())
funds = df["FundId"].unique()
grid = pd.MultiIndex.from_product([funds, months], names=["FundId", "ym"]).to_frame(index=False)
f = grid.merge(fr, how="left").merge(fl, how="left").merge(fs, how="left")
f = f.sort_values(["FundId", "ym"]).reset_index(drop=True)
g = f.groupby("FundId")

# Avkastningssignal: exponentiellt viktade 18 föregående månader, alla måste finnas
wts = np.exp(-LAMBDA * np.arange(18))
lags = np.column_stack([g["ret"].shift(s_) for s_ in range(1, 19)])
ok = ~np.isnan(lags).any(axis=1)
sig = np.full(len(f), np.nan)
sig[ok] = lags[ok] @ wts / wts.sum()
f["signal"] = sig
f["star"] = g["star_d"].shift(1)        # betyget som visas under månad t (daterat t-1)
f["star_prev"] = g["star_d"].shift(2)
f["flow_l19"] = g["flow"].shift(19)
f["sd60"] = g["ret"].transform(lambda z: z.shift(1).rolling(60, min_periods=36).std())

st_f = static.groupby("FundId").agg(inc=("inc", "min"), exp=("exp", "mean"), cat=("Morningstar Category", "first"),
                                    name=("Name", lambda z: " | ".join(z.dropna())))
st_f["index"] = st_f["name"].str.contains(INDEX_RE, case=False, regex=True)
f = f.merge(st_f[["inc", "exp", "cat", "index"]], left_on="FundId", right_index=True, how="left")
f["age"] = (pd.to_datetime(f["ym"] + "-01") - f["inc"]).dt.days / 365.25

# Urval enligt deklarationen
s0 = f[(f["ym"] >= "1999-02")]
steps = [("flöde finns", s0["flow"].notna()), ("förmögenhet >= 10 MUSD", s0["tna_l"] >= 10e6),
         ("stjärna finns", s0["star"].notna()), ("signal (18 mån)", s0["signal"].notna()),
         ("kategori finns", s0["cat"].notna()), ("ej indexfond", ~s0["index"].fillna(False))]
mask = pd.Series(True, index=s0.index)
print("Urvalskedja (fondmånader):")
for nm, m in steps:
    mask &= m
    print(f"  {nm:28s} {int(mask.sum()):>8d}  fonder {s0.loc[mask, 'FundId'].nunique()}")
sm = s0[mask].copy()
print("indexfonder uteslutna (fonder):", s0.loc[s0['index'].fillna(False), 'FundId'].nunique())

sm["pos"] = (sm["flow"] > 0).astype(float)
sm["size"] = sm["tna_l"] / 1e6
def wins(x):
    lo, hi = x.quantile([0.01, 0.99])
    return x.clip(lo, hi)
for c in ["flow", "flow_usd", "signal", "size", "age", "flow_l19", "sd60", "exp"]:
    sm[c] = sm.groupby("ym")[c].transform(wins)
sm = sm.reset_index(drop=True)
sm.to_pickle(out)
# Hela fondpanelen behövs för betygsbyten (Table 4 A) och juni-betyget (ekv. 2)
f.to_pickle(out.replace(".pkl", "_alla.pkl"))
print("sparat", out, sm.shape)
