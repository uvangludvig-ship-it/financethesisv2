"""Del II i DEKLARATION_sicksack_eu_A1_A3_och_brusreducerad_2026-11-19: fondflode, wins 2,5/97,5, ANCOVA.
python3 -I sicksack_eu_brusred.py <ss_eu-katalog> <tag> <morningstar_direct-katalog for SHoF>"""
import sys, numpy as np, pandas as pd
from scipy import stats
D_, T, M = sys.argv[1:4]; P_ = lambda s: pd.Period(s, "M")
L = pd.read_pickle(f"{D_}/panel_eu_{T}.pkl"); E = pd.read_pickle(f"{D_}/urval_eu_{T}.pkl"); B = pd.read_pickle(f"{D_}/huvudklasser_eu_{T}.pkl")
assert len(B) == {"bas": 4523, "b1": 4523, "full": 4863}[T], len(B)

def dm(X, keys, tol=1e-9, itmax=500):
    X = np.asarray(X, float).copy(); codes = [pd.factorize(k)[0] for k in keys]; cnt = [np.bincount(c) for c in codes]
    for _ in range(itmax):
        mx = 0.0
        for c, nn in zip(codes, cnt):
            for j in range(X.shape[1]):
                m = np.bincount(c, X[:, j]) / nn; X[:, j] -= m[c]; mx = max(mx, np.abs(m).max())
        if mx < tol: break
    return X
def clus(Zd, e, g):
    sc = pd.DataFrame(Zd * e[:, None]).groupby(g).sum().values; G = len(sc); return sc.T @ sc * G / (G - 1)
def est(W, X, keys=("SecId", "tc")):
    Dd = dm(W[["f"] + X].values, [W[k].values for k in keys]); yd = Dd[:, 0]; Xd = Dd[:, 1:]
    A_ = np.linalg.pinv(Xd.T @ Xd); b = A_ @ Xd.T @ yd; e = yd - Xd @ b
    f = W.fundid.values; t = W.tt.values; ft = (W.fundid.astype(str) + "|" + W.tt).values
    Vf = A_ @ clus(Xd, e, f) @ A_.T; V2 = Vf + A_ @ clus(Xd, e, t) @ A_.T - A_ @ clus(Xd, e, ft) @ A_.T
    se = np.maximum(np.sqrt(np.diag(Vf)), np.sqrt(np.clip(np.diag(V2), 0, None)))
    return b * 12, se * 12, Vf * 144, W.fundid.nunique()
def line(nm, b, se, G, n, star=None):
    lo, hi = b - 1.96 * se, b + 1.96 * se
    s = f"  i stjarnor {b/star:+.2f} [{lo/star:+.2f}; {hi/star:+.2f}]" if star else ""
    print(f"  {nm:<56}{b:+6.2f}  SE {se:4.2f}  t {b/se:+5.2f}  95 % [{lo:+6.2f}; {hi:+6.2f}]  MDE {2.8*se:4.1f}  fonder {G}  obs {n}{s}")
    return lo, hi
def wins(s, t, lo, hi):
    q = s.groupby(t).quantile([lo, hi]).unstack(); return s.clip(t.map(q[lo]), t.map(q[hi]))

# fondflode
kid = set(E.index[~E.inst & (E.sida != "UK")])
K = L[L.SecId.isin(kid) & L.fundid.isin(set(B.FundId)) & L.stor].copy(); K["usd"] = K.f * K.na_lag
G0 = K.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index(); G0["r"] = G0.usd / G0.na
mb = B.reset_index().set_index("FundId")[["SecId", "dos", "dos_smal", "sig", "Morningstar Category", "sverige"]].rename(columns={"Morningstar Category": "cat"})
def fund_rows(w=(.025, .975)):
    G = G0.copy(); G["f"] = wins(G.r, G.t, *w) * 100
    G = G.join(mb, on="fundid").merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left")
    G["aktie"] = G.cat.astype(str).str.contains("Equity"); G["kalla"] = 0.0; return G
def prep(A, t0="2021-01", t1="2024-12", switch="2023-01"):
    A = A[(A.t >= P_(t0)) & (A.t <= P_(t1))].copy()
    A["efter"] = (A.t >= P_(switch)).astype(float); A["ed"] = A.efter * A.dos; s = A.sig / 10
    for k in (1, 2, 3): A[f"es{k}"] = A.efter * s ** k
    pm = A[A.efter == 0].groupby("fundid").f.mean(); A["efpre"] = A.efter * A.fundid.map(pm).fillna(0)
    A["ek"] = A.efter * A.kalla
    A["tt"] = A.t.astype(str); A["tc"] = A.tt + "_" + A.cat.astype(str); return A
ES3 = ["es1", "es2", "es3"]; XA = ["ed"] + ES3 + ["efpre"]

A = fund_rows(); W = prep(A)
print(f"Fondflode: {W.fundid.nunique()} fonder, {len(W)} fondmanader 2021-2024, {K.SecId.nunique()} klasser bidrar")
g = W.groupby(["dos", "efter"]).f.mean().unstack() * 12
print("\nMEDELFLODE, fondniva, pp per ar (ra medel):")
print(pd.DataFrame({"fore": g[0.0], "efter": g[1.0], "andring": g[1.0] - g[0.0]}).round(2).to_string())

print("\nHUVUDTEST DEL II: Efter x Dos, polynom, Efter x forperiodens flode, fond- och manad x kategori-effekter")
Q = W.dropna(subset=["star_lag"])
b, se, V, Gn = est(Q, ["star_lag"] + XA); star = b[0]
b0, se0, V0, G0n = est(W, XA); lo, hi = line("beta", b0[0], se0[0], G0n, len(W), star)
print("  LASREGEL:", "utesluter noll" if (lo > 0 or hi < 0) else "innehaller noll", "|",
      "inom +-2,75: halv stjarna avvisas" if (lo > -2.75 and hi < 2.75) else ("inom +-5,5" if (lo > -5.5 and hi < 5.5) else "ingen slutsats"))
print(f"  ANCOVA-koefficient gamma {b0[-1]/12:+.3f} (SE {se0[-1]/12:.3f})")
print("\nV1 KAND VIKT"); line("stjarna, per stjarna", b[0], se[0], Gn, len(Q)); line("beta med stjarnan", b[1], se[1], Gn, len(Q), b[0])
print("  V1:", "UPPFYLLT" if b[0] / se[0] >= 2 else "FALLER")

print("\nV2 HANDELSSTUDIE (fondflode, utan ANCOVA), bas 2022Q4")
W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str); qs = sorted(W.q.unique()); cols = []; pc = []
for q in qs:
    if q == "2022Q4": continue
    W["d_" + q] = (W.q == q) * W.dos; cols.append("d_" + q); s = W.sig / 10
    for k in (1, 2, 3): W[f"p{k}_" + q] = (W.q == q) * s ** k; pc.append(f"p{k}_" + q)
b, se, V, Gn = est(W, cols + pc)
ev = pd.DataFrame({"kvartal": [c[2:] for c in cols], "b": b[:len(cols)], "se": se[:len(cols)]}); ev["t"] = ev.b / ev.se; print(ev.round(2).to_string(index=False))
pre_i = [i for i, c in enumerate(cols) if c[2:] < "2022Q4"]; post_i = [i for i, c in enumerate(cols) if c[2:] > "2022Q4"]
def wald(ix): bb = b[ix]; w = bb @ np.linalg.pinv(V[np.ix_(ix, ix)]) @ bb; return w, stats.chi2.sf(w, len(ix))
(wp, pp), (wa, pa) = wald(pre_i), wald(post_i)
print(f"  fore: chi2 {wp:.2f}, p {pp:.3f} | efter: chi2 {wa:.2f}, p {pa:.3f} | medel fore {b[pre_i].mean():+.2f}, efter {b[post_i].mean():+.2f}")
print("  V2:", "UPPFYLLT" if pp > 0.05 else "FALLER")

print("\nV3 LATSASBYTE jan 2021 (forperiod 2019-20)")
y = A.t.dt.year; n1 = A[y.isin([2019, 2020])].groupby("fundid").size(); n2 = A[y.isin([2021, 2022])].groupby("fundid").size()
ok = set(n1.index[n1 >= 18]) & set(n2.index[n2 >= 18])
W3 = prep(A[A.fundid.isin(ok)], "2019-01", "2022-12", "2021-01"); b, se, V, Gn = est(W3, XA); lo3, hi3 = line("latsas: Efter(2021) x Dos", b[0], se[0], Gn, len(W3))
print("  V3:", "UPPFYLLT" if lo3 < 0 < hi3 else "FALLER")

print("\nSIDOTEST DEL II")
b, se, V, Gn = est(W, ["ed"] + ES3); line("C1. utan ANCOVA", b[0], se[0], Gn, len(W), star)
W2 = prep(fund_rows((.01, .99))); b, se, V, Gn = est(W2, XA); line("C2. winsorisering 1/99", b[0], se[0], Gn, len(W2), star)
# C3 SHoF dar det finns
Ks = pd.read_pickle(f"{M}/tvillingar/tv_klasser.pkl"); ES = pd.read_pickle(f"{M}/byte2023/etiketter.pkl"); Ks["y"] = Ks.t.dt.year
ES["sri_ny"] = ES.sri23.fillna(ES.sri_h2_22); ES["dos_bred"] = ES.srri22 - ES.sri_ny
pm = Ks[(Ks.roll == "huvudklass") & (Ks.institutionalonly != 1)]
n = pm.groupby(["SecId", "y"]).size().unstack(fill_value=0)
keep = set(n.index[((n[2021] + n[2022]) >= 18) & ((n[2023] + n[2024]) >= 18)])
Es = ES[ES.SecId.isin(keep) & ES.srri22.notna() & ES.sri_ny.notna() & ES.dos_bred.isin([0, 1, 2]) & ES.sig_w.notna()]
hc = set(pm[pm.SecId.isin(Es.SecId) & (pm.t <= P_("2022-12"))].dropna(subset=["cat_lag"]).SecId)
Es = Es[Es.SecId.isin(hc)].set_index("SecId"); assert len(Es) == 1421
S = pm[pm.SecId.isin(Es.index)].dropna(subset=["cat_lag", "f"])[["SecId", "fundid", "t", "f", "star_lag", "cat_lag"]].rename(columns={"cat_lag": "cat"})
S["f"] = wins(S.f, S.t, .025, .975); S = S.join(Es[["dos_bred", "sig_w"]].rename(columns={"dos_bred": "dos", "sig_w": "sig"}), on="SecId"); S["kalla"] = 1.0
P = pd.concat([S, A[~A.fundid.isin(set(Es.fundid))]], ignore_index=True); WP = prep(P)
b, se, V, Gn = est(WP, XA + ["ek"]); line("C3. SHoF dar det finns, annars Direct", b[0], se[0], Gn, len(WP), star)
b, se, V, Gn = est(W[~W.sverige.astype(bool)], XA); line("C4. utan fonder till salu i Sverige", b[0], se[0], Gn, int((~W.sverige.astype(bool)).sum()), star)
b, se, V, Gn = est(W[W.aktie], XA); line("C5. bara aktiefonder", b[0], se[0], Gn, int(W.aktie.sum()), star)
# C6 kollapsad
gg = W.groupby(["fundid", "efter"]).f.mean().unstack(); C = pd.DataFrame({"dd": (gg[1.0] - gg[0.0]) * 12, "pre": gg[0.0] * 12}).join(mb[["dos", "sig", "cat"]]).dropna()
cat = pd.factorize(C.cat)[0]; w = lambda v: v - (np.bincount(cat, v) / np.bincount(cat))[cat]; s = C.sig.values / 10
X = np.column_stack([w(C.dos.values.astype(float)), w(s), w(s ** 2), w(s ** 3), w(C.pre.values)]); yv = w(C.dd.values)
XtXi = np.linalg.pinv(X.T @ X); bb = XtXi @ X.T @ yv; e = yv - X @ bb; Vv = XtXi @ (X.T * e ** 2) @ X @ XtXi * len(yv) / (len(yv) - 5 - cat.max() - 1)
print(f"  C6. kollapsad: beta {bb[0]:+.2f}  SE {np.sqrt(Vv[0,0]):.2f}  (panel {b0[0]:+.2f}, SE {se0[0]:.2f})")
# verifiering
Wp = W.copy(); Wp["f"] = Wp.f + 3.0 / 12 * Wp.ed; b, se, V, Gn = est(Wp, XA)
print(f"\nVERIFIERING: inplanterad +3,00 ger {b[0]:+.3f} (vantat {b0[0] + 3:+.3f})")
