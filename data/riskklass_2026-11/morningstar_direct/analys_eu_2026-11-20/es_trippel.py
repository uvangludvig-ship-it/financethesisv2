"""Sicksacken med Evans och Suns kontrollgrupp: privat minus institutionell klass i samma fond.
Specifikation: claude/DEKLARATION_evans_sun_privat_mot_institutionell_2026-11-20.md
python3 -I es_trippel.py <katalog med panel_eu_bas.pkl, urval_eu_bas.pkl, huvudklasser_eu_bas.pkl>"""
import sys, numpy as np, pandas as pd
from scipy import stats
M = sys.argv[1]; P_ = lambda s: pd.Period(s, "M")
L = pd.read_pickle(f"{M}/panel_eu_bas.pkl"); E = pd.read_pickle(f"{M}/urval_eu_bas.pkl"); B = pd.read_pickle(f"{M}/huvudklasser_eu_bas.pkl")
assert len(B) == 4818, len(B)
Bf = B.reset_index().set_index("FundId")[["dos", "sig", "Morningstar Category"]].rename(columns={"Morningstar Category": "catf"})

# kandidatfonder: har institutionell klass med >= 18 flodesmanader i bada perioderna (rakning utan floden)
Ei = E[E.inst & (E.sida != "UK") & (E.n_pre >= 18) & (E.n_post >= 18)]
fonder = set(Bf.index) & set(Ei.FundId)
print(f"Fonder med institutionell klass: {len(fonder)}")

K = L[L.fundid.isin(fonder) & (L.sida != "UK") & L.stor & (L.t >= P_("2019-01")) & (L.t <= P_("2024-12"))].dropna(subset=["f", "na_lag"]).copy()
K["grp"] = np.where(K.inst, "inst", "priv"); K["usd"] = K.f * K.na_lag
G = K.groupby(["fundid", "t", "grp"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index()
G["r"] = 100 * G.usd / G.na
q = G.groupby(["t", "grp"]).r.quantile([.01, .99]).unstack()
lo_ = q[.01].reindex(pd.MultiIndex.from_frame(G[["t", "grp"]])).values; hi_ = q[.99].reindex(pd.MultiIndex.from_frame(G[["t", "grp"]])).values
G["r"] = np.clip(G.r.values, lo_, hi_)
W0 = G.pivot_table(index=["fundid", "t"], columns="grp", values="r").dropna().reset_index()
W0["D"] = W0.priv - W0.inst
W0 = W0.join(Bf, on="fundid")

def dm(X, keys, tol=1e-9, itmax=500):
    X = np.asarray(X, float).copy()
    codes = [pd.factorize(k)[0] for k in keys]; cnt = [np.bincount(c) for c in codes]
    for _ in range(itmax):
        mx = 0.0
        for c, nn in zip(codes, cnt):
            for j in range(X.shape[1]):
                m = np.bincount(c, X[:, j]) / nn; X[:, j] -= m[c]; mx = max(mx, np.abs(m).max())
        if mx < tol: break
    return X
def clus(Zd, e, g):
    sc = pd.DataFrame(Zd * e[:, None]).groupby(g).sum().values; Gn = len(sc); return sc.T @ sc * Gn / (Gn - 1)
def est(W, y, X, keys):
    D = dm(W[[y] + X].values, [W[k].values for k in keys]); yd = D[:, 0]; Xd = D[:, 1:]
    A_ = np.linalg.pinv(Xd.T @ Xd); b = A_ @ Xd.T @ yd; e = yd - Xd @ b
    f = W.fundid.values; t = W.tt.values; ft = (W.fundid.astype(str) + "|" + W.tt).values
    Vf = A_ @ clus(Xd, e, f) @ A_.T; V2 = Vf + A_ @ clus(Xd, e, t) @ A_.T - A_ @ clus(Xd, e, ft) @ A_.T
    se = np.maximum(np.sqrt(np.diag(Vf)), np.sqrt(np.clip(np.diag(V2), 0, None)))
    return b * 12, se * 12, Vf * 144, W.fundid.nunique()

def prep(W, t0, t1, switch, need=18):
    W = W[(W.t >= P_(t0)) & (W.t <= P_(t1))].copy(); W["efter"] = (W.t >= P_(switch)).astype(float)
    n1 = W[W.efter == 0].groupby("fundid").size(); n2 = W[W.efter == 1].groupby("fundid").size()
    ok = set(n1.index[n1 >= need]) & set(n2.index[n2 >= need]); W = W[W.fundid.isin(ok)].copy()
    W["ed"] = W.efter * W.dos; s = W.sig / 10
    for k in (1, 2, 3): W[f"es{k}"] = W.efter * s ** k
    W["tt"] = W.t.astype(str); W["tc"] = W.tt + "_" + W.catf.astype(str)
    return W
ES3 = ["es1", "es2", "es3"]
def line(nm, b, se, G, n):
    lo, hi = b - 1.96 * se, b + 1.96 * se
    print(f"  {nm:<52}{b:+6.2f}  SE {se:4.2f}  t {b/se:+5.2f}  95 % [{lo:+6.2f}; {hi:+6.2f}]  MDE {2.8*se:4.1f}  fonder {G}  obs {n}")
    return lo, hi

W = prep(W0, "2021-01", "2024-12", "2023-01")
print(f"Urval: {W.fundid.nunique()} fonder, {len(W)} fondmanader. Dos: {W.drop_duplicates('fundid').dos.value_counts().sort_index().to_dict()}")
g = W.groupby(["dos", "efter"])[["priv", "inst", "D"]].mean().unstack() * 12
print("\nRA MEDEL, pp per ar:\n" + g.round(2).to_string())

print("\nHUVUDTEST: D = privat minus institutionell; Efter x Dos + Efter x polynom(sigma); fond- och manad x kategori-effekter")
b, se, V, G_ = est(W, "D", ["ed"] + ES3, ["fundid", "tc"]); lo, hi = line("beta (pp per ar per steg)", b[0], se[0], G_, len(W))
print("  LASREGEL:", "innehaller noll" if lo <= 0 <= hi else ("positiv och signifikant" if lo > 0 else "negativ och signifikant"),
      "| halv stjarna (2,75) avvisas" if (lo > -2.75 and hi < 2.75) else "| halv stjarna avvisas inte",
      "| tredjedel (1,6) avvisas" if (lo > -1.6 and hi < 1.6) else "| tredjedel avvisas inte")

print("\nSIDOTEST")
b, se, V, G1 = est(W, "D", ["ed"] + ES3, ["fundid", "tt"]); line("S1 bara manadseffekter", b[0], se[0], G1, len(W))
b, se, V, G1 = est(W, "D", ["ed"], ["fundid", "tc"]); line("S2 utan polynom i sigma", b[0], se[0], G1, len(W))
b, se, V, G1 = est(W, "priv", ["ed"] + ES3, ["fundid", "tc"]); line("S3a privatflodet ensamt", b[0], se[0], G1, len(W))
b, se, V, G1 = est(W, "inst", ["ed"] + ES3, ["fundid", "tc"]); line("S3b institutionella flodet ensamt", b[0], se[0], G1, len(W))

# V2 handelsstudie
W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str); base = "2022Q4"; cols = []; pcols = []
for qq in sorted(W.q.unique()):
    if qq == base: continue
    W["d_" + qq] = (W.q == qq) * W.dos; cols.append("d_" + qq); s = W.sig / 10
    for k in (1, 2, 3): W[f"p{k}_" + qq] = (W.q == qq) * s ** k; pcols.append(f"p{k}_" + qq)
b, se, V, G1 = est(W, "D", cols + pcols, ["fundid", "tc"])
print("\nV2 HANDELSSTUDIE (Dos x kvartal, bas 2022Q4), pp per ar:")
for i, c in enumerate(cols): print(f"  {c[2:]}  {b[i]:+6.2f}  SE {se[i]:4.2f}")
pre = [i for i, c in enumerate(cols) if c[2:] < base]; post = [i for i, c in enumerate(cols) if c[2:] > base]
def wald(ix): bb = b[ix]; w = bb @ np.linalg.pinv(V[np.ix_(ix, ix)]) @ bb; return w, stats.chi2.sf(w, len(ix))
w1, p1 = wald(pre); w2, p2 = wald(post)
print(f"  fore: chi2 {w1:.2f}, p {p1:.3f} | efter: chi2 {w2:.2f}, p {p2:.3f}  -> V2 {'UPPFYLLT' if p1 > 0.05 else 'FALLER'}")

# V3 latsasbyte
W3 = prep(W0, "2019-01", "2022-12", "2021-01")
b, se, V, G3 = est(W3, "D", ["ed"] + ES3, ["fundid", "tc"]); l3, h3 = line("V3 latsasbyte jan 2021", b[0], se[0], G3, len(W3))
print("  V3:", "UPPFYLLT" if l3 <= 0 <= h3 else "FALLER")

# verifiering
Wv = W.copy(); Wv["D"] = Wv.D + (3.0 / 12) * Wv.ed
b0, *_ = est(W, "D", ["ed"] + ES3, ["fundid", "tc"]); bv, *_ = est(Wv, "D", ["ed"] + ES3, ["fundid", "tc"])
print(f"\nVerifiering: inplanterad +3,00 ger {bv[0]-b0[0]:+.3f} (vantat +3,000)")
