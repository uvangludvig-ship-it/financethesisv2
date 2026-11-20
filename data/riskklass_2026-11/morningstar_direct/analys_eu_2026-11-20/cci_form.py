"""Bytet 2023 i Cornaggia, Cornaggia och Israelsens (2018, RFS) form: Steg x Efter med fondeffekter och kontroll for gammal klass.
Specifikation: claude/DEKLARATION_cornaggia_form_steg_ganger_efter_2026-11-20.md
python3 -I cci_form.py <katalog med panel_eu_bas.pkl, urval_eu_bas.pkl, huvudklasser_eu_bas.pkl>"""
import sys, numpy as np, pandas as pd
from scipy import stats
M = sys.argv[1]; P_ = lambda s: pd.Period(s, "M")
L = pd.read_pickle(f"{M}/panel_eu_bas.pkl"); E = pd.read_pickle(f"{M}/urval_eu_bas.pkl"); B = pd.read_pickle(f"{M}/huvudklasser_eu_bas.pkl")
assert len(B) == 4818, len(B)

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
def est(W, X, keys):
    Dd = dm(W[["f"] + X].values, [W[k].values for k in keys]); yd = Dd[:, 0]; Xd = Dd[:, 1:]
    A_ = np.linalg.pinv(Xd.T @ Xd); b = A_ @ Xd.T @ yd; e = yd - Xd @ b
    f = W.fundid.values; t = W.tt.values; ft = (W.fundid.astype(str) + "|" + W.tt).values
    Vf = A_ @ clus(Xd, e, f) @ A_.T; V2 = Vf + A_ @ clus(Xd, e, t) @ A_.T - A_ @ clus(Xd, e, ft) @ A_.T
    se = np.maximum(np.sqrt(np.diag(Vf)), np.sqrt(np.clip(np.diag(V2), 0, None)))
    return b * 12, se * 12, Vf * 144, W.fundid.nunique()
def line(nm, b, se, G, n, star=None):
    lo, hi = b - 1.96 * se, b + 1.96 * se
    s = f"  i stjarnor [{lo/star:+.2f}; {hi/star:+.2f}]" if star else ""
    print(f"  {nm:<50}{b:+6.2f}  SE {se:4.2f}  t {b/se:+5.2f}  95 % [{lo:+6.2f}; {hi:+6.2f}]  MDE {2.8*se:4.1f}  fonder {G}  obs {n}{s}")
    return lo, hi
def wins(s, t, lo, hi):
    q = s.groupby(t).quantile([lo, hi]).unstack(); return s.clip(t.map(q[lo]), t.map(q[hi]))

# fondflode som i sicksackens del II
kid = set(E.index[~E.inst & (E.sida != "UK")])
K = L[L.SecId.isin(kid) & L.fundid.isin(set(B.FundId)) & L.stor].copy(); K["usd"] = K.f * K.na_lag
G0 = K.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index(); G0["r"] = G0.usd / G0.na
mb = B.reset_index().set_index("FundId")[["SecId", "dos", "sig", "srri22", "Morningstar Category"]].rename(columns={"Morningstar Category": "cat"})
G0["f"] = wins(G0.r, G0.t, .025, .975) * 100
A = G0.join(mb, on="fundid").merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left")

def prep(A, t0="2021-01", t1="2024-12", switch="2023-01"):
    W = A[(A.t >= P_(t0)) & (A.t <= P_(t1))].copy()
    W["efter"] = (W.t >= P_(switch)).astype(float); W["ed"] = W.efter * W.dos
    W["ea"] = W.efter * (W.dos >= 1); W["e2"] = W.efter * (W.dos == 2)
    ks = sorted(W.srri22.dropna().unique()); kc = []
    for k in ks[1:]:
        W[f"ek{int(k)}"] = W.efter * (W.srri22 == k); kc.append(f"ek{int(k)}")
    s = W.sig / 10
    for k in (1, 2, 3): W[f"es{k}"] = W.efter * s ** k
    pm = W[W.efter == 0].groupby("fundid").f.mean(); W["efpre"] = W.efter * W.fundid.map(pm).fillna(0)
    W["tt"] = W.t.astype(str); W["tc"] = W.tt + "_" + W.cat.astype(str); return W, kc
W, KC = prep(A); FT, FC = ["fundid", "tt"], ["fundid", "tc"]
print(f"Urval: {W.fundid.nunique()} fonder, {len(W)} fondmanader 2021-2024")
g = W.groupby(["dos", "efter"]).f.mean().unstack() * 12
print("RA MEDEL pp per ar:\n" + pd.DataFrame({"fore": g[0.0], "efter": g[1.0], "andring": g[1.0] - g[0.0]}).round(2).to_string())

Q = W.dropna(subset=["star_lag"]); b, se, V, Gn = est(Q, ["star_lag", "ed"] + KC, FC); star = b[0]
print("\nV1 stjarnan i huvudregressionen"); line("stjarna, per stjarna", b[0], se[0], Gn, len(Q)); line("beta med stjarnan", b[1], se[1], Gn, len(Q), star)

print("\nHUVUD (Panel B): Dos x Efter, Efter x gammal klass, fond- och manad x kategori-effekter")
b, se, V, Gn = est(W, ["ed"] + KC, FC); lo, hi = line("beta, pp per ar per steg", b[0], se[0], Gn, len(W), star)
print("  LASREGEL:", "innehaller noll" if lo <= 0 <= hi else "utesluter noll", "|",
      "tredjedel (1,6) avvisas" if (lo > -1.6 and hi < 1.6) else ("halv stjarna (2,75) avvisas" if (lo > -2.75 and hi < 2.75) else "halv stjarna avvisas inte"))
bmain = b[0]

print("\nOVRIGA RADER")
b, se, V, Gn = est(W, ["ea"] + KC, FC); line("A  Panel A: Sankt (dos>=1) x Efter", b[0], se[0], Gn, len(W))
W12 = W[W.dos >= 1]; b, se, V, Gn = est(W12, ["e2"] + [c for c in KC if W12[c].abs().sum() > 0], FC); line("C  Table VI: tva steg mot ett", b[0], se[0], Gn, len(W12))
b, se, V, Gn = est(W, ["ed"], FT); line("R1 ra form: fond- och manadseffekter", b[0], se[0], Gn, len(W))
b, se, V, Gn = est(W, ["ed"] + KC, FT); line("R2 R1 + Efter x gammal klass", b[0], se[0], Gn, len(W))
b, se, V, Gn = est(W, ["ed"] + KC + ["efpre"], FC); line("R3 huvud + forperiodens flode", b[0], se[0], Gn, len(W), star)
b, se, V, Gn = est(W, ["ed"] + KC + ["es1", "es2", "es3"], FC); line("R4 huvud + polynom i sigma", b[0], se[0], Gn, len(W))

print("\nV2 HANDELSSTUDIE (Dos x kvartal, gammal klass x kvartal, bas 2022Q4)")
W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str); cols = []; pc = []
ks = sorted(W.srri22.dropna().unique())[1:]
for q in sorted(W.q.unique()):
    if q == "2022Q4": continue
    W["d_" + q] = (W.q == q) * W.dos; cols.append("d_" + q)
    for k in ks: W[f"k{int(k)}_" + q] = ((W.q == q) & (W.srri22 == k)).astype(float); pc.append(f"k{int(k)}_" + q)
b, se, V, Gn = est(W, cols + pc, FC)
for i, c in enumerate(cols): print(f"  {c[2:]}  {b[i]:+6.2f}  SE {se[i]:4.2f}")
pre = [i for i, c in enumerate(cols) if c[2:] < "2022Q4"]; post = [i for i, c in enumerate(cols) if c[2:] > "2022Q4"]
def wald(ix): bb = b[ix]; w = bb @ np.linalg.pinv(V[np.ix_(ix, ix)]) @ bb; return w, stats.chi2.sf(w, len(ix))
(w1, p1), (w2, p2) = wald(pre), wald(post)
print(f"  fore: chi2 {w1:.2f}, p {p1:.3f} | efter: chi2 {w2:.2f}, p {p2:.3f} -> V2 {'UPPFYLLT' if p1 > 0.05 else 'FALLER'}")

print("\nV3 LATSASBYTE januari 2021 (2019-2022)")
W3, KC3 = prep(A, "2019-01", "2022-12", "2021-01")
n1 = W3[W3.efter == 0].groupby("fundid").size(); n2 = W3[W3.efter == 1].groupby("fundid").size()
ok = set(n1.index[n1 >= 18]) & set(n2.index[n2 >= 18]); W3 = W3[W3.fundid.isin(ok)]
b, se, V, Gn = est(W3, ["ed"] + KC3, FC); l3, h3 = line("latsasbyte", b[0], se[0], Gn, len(W3)); print("  V3:", "UPPFYLLT" if l3 <= 0 <= h3 else "FALLER")

Wv = W.copy(); Wv["f"] = Wv.f + 0.25 * Wv.ed; bv, *_ = est(Wv, ["ed"] + KC, FC)
print(f"\nVerifiering: inplanterad +3,00 ger {bv[0]-bmain:+.3f}")
