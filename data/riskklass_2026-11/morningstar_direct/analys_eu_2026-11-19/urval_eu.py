"""Urval for sicksacken (som i DEKLARATION_sicksack_eu_preliminar_2026-11-19) och balanskontroll for ANCOVA.
Anvander bara antal flodesmanader och floden till och med dec 2022.
python3 -I urval_eu.py <tag>  -> huvudklasser_eu_<tag>.pkl"""
import sys, numpy as np, pandas as pd
T = sys.argv[1]; P_ = lambda s: pd.Period(s, "M")
E = pd.read_pickle(f"urval_eu_{T}.pkl")
steps = []; m = ~E.inst & (E.sida != "UK"); steps.append(("Icke-institutionella klasser, inte rena UK", m.sum()))
m &= E.n_pre >= 18; steps.append(("minst 18 flodesmanader 2021-22 (NA_t-1 >= 1 MUSD)", m.sum()))
m &= E.n_post >= 18; steps.append(("och minst 18 2023-24", m.sum()))
m &= E.srri22.notna(); steps.append(("och SRRI i kraft vid utgangen av 2022", m.sum()))
m &= E.sri_ny.notna(); steps.append(("och SRI", m.sum()))
m &= E.dos.isin([0, 1, 2]) & E.sig.notna(); steps.append(("och dos 0, 1, 2 samt sigma", m.sum()))
m &= E["Morningstar Category"].notna(); steps.append(("och kategori", m.sum()))
for s, n in steps: print(f"{n:7d}  {s}")
B = E[m].sort_values("na_dec22", ascending=False).groupby("FundId").head(1)
print("en klass per fond:", len(B), "| dos:", B.dos.value_counts().sort_index().to_dict(), "| bred dos fran H2-22:", int(B.sri23.isna().sum()),
      "| sverige:", int(B.sverige.sum()), "| aktie:", int(B["Morningstar Category"].str.contains("Equity").sum()), "| kategorier:", B["Morningstar Category"].nunique())
print("sida:", B.sida.value_counts().to_dict())
B.to_pickle(f"huvudklasser_eu_{T}.pkl")

# balans: forperiodens medelflode (2021-22, fondniva, wins 2,5/97,5) mot dos, givet polynom och kategori
L = pd.read_pickle(f"panel_eu_{T}.pkl"); L = L[(L.t >= P_("2021-01")) & (L.t <= P_("2022-12"))]
K = L[L.SecId.isin(E.index[~E.inst & (E.sida != "UK")]) & L.fundid.isin(set(B.FundId)) & L.stor].copy(); K["usd"] = K.f * K.na_lag
G = K.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index(); G["r"] = G.usd / G.na
q = G.groupby("t").r.quantile([.025, .975]).unstack(); G["r"] = G.r.clip(G.t.map(q[.025]), G.t.map(q[.975])) * 1200
pre = G.groupby("fundid").r.mean()
C = B.set_index("FundId")[["dos", "sig", "Morningstar Category"]].join(pre.rename("pre")).dropna()
cat = pd.factorize(C["Morningstar Category"])[0]; w = lambda v: v - (np.bincount(cat, v) / np.bincount(cat))[cat]
s = C.sig.values / 10; X = np.column_stack([w(C.dos.values.astype(float)), w(s), w(s ** 2), w(s ** 3)]); y = w(C.pre.values)
XtXi = np.linalg.pinv(X.T @ X); b = XtXi @ X.T @ y; e = y - X @ b; V = XtXi @ (X.T * e ** 2) @ X @ XtXi
print(f"BALANS (ANCOVA-villkor): forperiodens flode 2021-22 pa dos | b {b[0]:+.2f} pp/ar, SE {np.sqrt(V[0,0]):.2f}, t {b[0]/np.sqrt(V[0,0]):+.2f}, fonder {len(C)}")
