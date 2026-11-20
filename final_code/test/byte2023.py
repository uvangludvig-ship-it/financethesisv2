"""Bytet av risksiffra 1 januari 2023 (SRRI -> SRI): fick fonder vars siffra foll fler steg mer pengar?

Adelino, Cunha och Ferreira (2017, RFS 30(9), s. 3236), ekvation 1, med fond i stallet for county,
   kategori x manad i stallet for delstat x ar och volatilitetsdecil x manad i stallet for storleksdecil x ar:
     Flode(f,t) = b Dos(f) x Efter(t) + fondeffekt + kategori x manad + volatilitetsdecil x manad + e
Dos = antal steg siffran foll (0, 1, 2). Koefficienter i procentenheter av formogenheten per ar.

python3 test/byte2023.py       (laser _arbete/panel_eu_bas.pkl, urval_eu_bas.pkl, huvudklasser_eu_bas.pkl)"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import ARBETE, TAL
from lib.stat import demean, _meat

P = lambda s: pd.Period(s, "M")
L = pd.read_pickle(ARBETE / "panel_eu_bas.pkl")           # klassmanader: SecId, fundid, t, f (flode/NA), na_lag, stor, star_lag
E = pd.read_pickle(ARBETE / "urval_eu_bas.pkl")           # klasser: inst, sida, ...
B = pd.read_pickle(ARBETE / "huvudklasser_eu_bas.pkl")    # en huvudklass per fond: dos, sig (volatilitet), srri22, kategori


def est(W, X, fe):
    """OLS med fasta effekter. Standardfel klustrade pa fond (Adelino m.fl. klustrar pa enheten, county).
    Ganger 12 = procentenheter per ar."""
    Z = demean(W[["f"] + X].to_numpy(float), [W[k].to_numpy() for k in fe], tol=1e-9)
    y, A = Z[:, 0], Z[:, 1:]
    Ai = np.linalg.pinv(A.T @ A); b = Ai @ A.T @ y; e = y - A @ b
    Vf = Ai @ _meat(A, e, W.fundid.astype(str).to_numpy()) @ Ai
    return b * 12, np.sqrt(np.diag(Vf)) * 12, Vf * 144


def wins(s, t, lo, hi):
    q = s.groupby(t).quantile([lo, hi]).unstack()
    return s.clip(t.map(q[lo]), t.map(q[hi]))


# ---- fondflode: icke-institutionella klasser som inte bara saljs i UK, klasser med minst 1 MUSD manaden fore
kid = set(E.index[~E.inst & (E.sida != "UK")])
K = L[L.SecId.isin(kid) & L.fundid.isin(set(B.FundId)) & L.stor].copy()
K["usd"] = K.f * K.na_lag
G0 = K.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index()
G0["r"] = G0.usd / G0.na
G0["f"] = wins(G0.r, G0.t, .01, .99) * 100         # winsorisering 1/99 inom manad (Ben-David m.fl. 2022, s. 1733)
mb = B.reset_index().set_index("FundId")[["SecId", "dos", "sig", "srri22", "Morningstar Category"]].rename(columns={"Morningstar Category": "cat"})
A = G0.join(mb, on="fundid").merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left")
for n in (5, 10, 20):
    A[f"vd{n}"] = A.fundid.map(pd.qcut(mb.sig, n, labels=False, duplicates="drop"))


def prep(t0="2021-01", t1="2024-12", byte="2023-01"):
    W = A[(A.t >= P(t0)) & (A.t <= P(t1))].dropna(subset=["dos", "sig", "f"]).copy()
    W["efter"] = (W.t >= P(byte)).astype(float)
    W["ed"] = W.efter * W.dos
    W["e1"] = W.efter * (W.dos == 1); W["e2"] = W.efter * (W.dos == 2)
    W["tt"] = W.t.astype(str); W["tc"] = W.tt + "_" + W.cat.astype(str)
    for n in (5, 10, 20):
        W[f"tv{n}"] = W.tt + "_" + W[f"vd{n}"].astype(str)
    return W


W = prep()
FE2, FE3 = ["fundid", "tc"], ["fundid", "tc", "tv10"]
rows = []


def rad(namn, b, se, W_, k=0):
    rows.append([namn, b[k], se[k], b[k] / se[k], b[k] - 1.96 * se[k], b[k] + 1.96 * se[k], 2.8 * se[k], W_.fundid.nunique(), len(W_)])


Q = W.dropna(subset=["star_lag"])
b, se, _ = est(Q, ["star_lag", "ed"], FE3); rad("Star rating, same regression as (2)", b, se, Q, 0); rad("Fall x After with the star rating", b, se, Q, 1)
b, se, _ = est(W, ["ed"], FE3); rad("(2) Fall x After, volatility decile x month [main]", b, se, W); bmain = b[0]
b, se, _ = est(W, ["ed"], FE2); rad("(1) Fall x After, no volatility control", b, se, W)
b, se, _ = est(W, ["e1", "e2"], FE3); rad("One class x After", b, se, W, 0); rad("Two classes x After", b, se, W, 1)
t = pd.DataFrame(rows, columns=["spec", "coef", "se", "t", "lo", "hi", "mde", "funds", "N"])
t.to_csv(TAL / "byte2023_dos.csv", index=False)

# ---- handelsestudie: Dos x kvartal, bas 2022 kv 4
W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str)
cols = []
for q in sorted(W.q.unique()):
    if q != "2022Q4":
        W["d_" + q] = (W.q == q) * W.dos; cols.append("d_" + q)
b, se, V = est(W, cols, FE3)
ev = pd.DataFrame({"quarter": [c[2:] for c in cols], "coef": b, "se": se})
wald = lambda ix: stats.chi2.sf(b[ix] @ np.linalg.pinv(V[np.ix_(ix, ix)]) @ b[ix], len(ix))
ev["p_pre"] = wald([i for i, c in enumerate(cols) if c[2:] < "2022Q4"]); ev["p_post"] = wald([i for i, c in enumerate(cols) if c[2:] > "2022Q4"])
ev.to_csv(TAL / "byte2023_kvartal.csv", index=False)


# ---- beskrivning: urvalet, och medelflode per dosgrupp och manad (bilaga)
pd.crosstab(pd.qcut(mb.sig, 10, labels=False), mb.dos).to_csv(TAL / "byte2023_dos_per_decil.csv")
d1 = W.groupby("fundid").agg(dos=("dos", "first"), sig=("sig", "first")).join(W[W.t == P("2022-12")].set_index("fundid").na.rename("na_dec22"))
s = lambda x, lab: [lab, x.notna().sum(), x.mean(), x.std(), *x.quantile([.05, .25, .5, .75, .95]).values]
pd.DataFrame([s(W.f, "Flow (% per month)"), s(W.star_lag, "Star rating"), s(d1.sig, "Volatility (%, per fund)"), s(d1.dos, "Classes the number fell (per fund)"),
              s(d1.na_dec22 / 1e6, "Assets Dec 2022 (USD million, per fund)")], columns=["variable", "N", "mean", "sd", "p5", "p25", "p50", "p75", "p95"]).to_csv(TAL / "byte2023_table1.csv", index=False)
pd.DataFrame([[W.fundid.nunique(), len(W), *[int((mb.dos.reindex(W.fundid.unique()) == k).sum()) for k in (0, 1, 2)]]], columns=["funds", "fund_months", "fall0", "fall1", "fall2"]).to_csv(TAL / "byte2023_urval.csv", index=False)
W.groupby(["tt", "dos"]).f.mean().unstack().reset_index().to_csv(TAL / "byte2023_flode_per_dos.csv", index=False)
print("byte2023 klar")
