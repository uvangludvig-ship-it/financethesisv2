"""Bytet 2023 i tva publicerade former.
A: Adelino, Cunha och Ferreira (2017, RFS) ekv. 1: Dos x Efter + fondeffekt + kategori x manad + volatilitetsdecil x manad.
B: Reuter och Zitzewitz (NBER WP 16329) avsnitt IV.F: tvarsnitt, flode 2023 pa Dos med gammal klass, volatilitet, flode 2022, kategori.
Specifikation: claude/DEKLARATION_adelino_form_och_reuter_zitzewitz_reformform_2026-11-20.md
python3 -I acf_rz_form.py <katalog med panel_eu_bas.pkl, urval_eu_bas.pkl, huvudklasser_eu_bas.pkl>"""
import sys, numpy as np, pandas as pd
from scipy import stats
M = sys.argv[1]; P_ = lambda s: pd.Period(s, "M")
L = pd.read_pickle(f"{M}/panel_eu_bas.pkl"); E = pd.read_pickle(f"{M}/urval_eu_bas.pkl"); B = pd.read_pickle(f"{M}/huvudklasser_eu_bas.pkl")
assert len(B) == 4818, len(B)

def dm(X, keys, tol=1e-9, itmax=2000):
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
    print(f"  {nm:<52}{b:+6.2f}  SE {se:4.2f}  t {b/se:+5.2f}  95 % [{lo:+6.2f}; {hi:+6.2f}]  MDE {2.8*se:4.1f}  fonder {G}  obs {n}{s}")
    return lo, hi
def wins(s, t, lo, hi):
    q = s.groupby(t).quantile([lo, hi]).unstack(); return s.clip(t.map(q[lo]), t.map(q[hi]))
def regel(lo, hi):
    return ("innehaller noll" if lo <= 0 <= hi else "utesluter noll") + " | " + (
        "tredjedel (1,6) avvisas" if (lo > -1.6 and hi < 1.6) else ("halv stjarna (2,75) avvisas" if (lo > -2.75 and hi < 2.75) else "halv stjarna avvisas inte"))

# fondflode som i sicksackens del II
kid = set(E.index[~E.inst & (E.sida != "UK")])
K = L[L.SecId.isin(kid) & L.fundid.isin(set(B.FundId)) & L.stor].copy(); K["usd"] = K.f * K.na_lag
G0 = K.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index(); G0["r"] = G0.usd / G0.na
mb = B.reset_index().set_index("FundId")[["SecId", "dos", "sig", "srri22", "Morningstar Category"]].rename(columns={"Morningstar Category": "cat"})
G0["f"] = wins(G0.r, G0.t, .025, .975) * 100; G0["f199"] = wins(G0.r, G0.t, .01, .99) * 100
A = G0.join(mb, on="fundid").merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left")
for n in (5, 10, 20):
    A[f"vd{n}"] = A.fundid.map(pd.qcut(mb.sig, n, labels=False, duplicates="drop"))
print("Dos per volatilitetsdecil (antal fonder):")
print(pd.crosstab(pd.qcut(mb.sig, 10, labels=False), mb.dos).assign(sig_min=mb.groupby(pd.qcut(mb.sig, 10, labels=False)).sig.min().round(1), sig_max=mb.groupby(pd.qcut(mb.sig, 10, labels=False)).sig.max().round(1)).to_string())

def prep(A, t0="2021-01", t1="2024-12", switch="2023-01"):
    W = A[(A.t >= P_(t0)) & (A.t <= P_(t1))].dropna(subset=["dos", "sig", "f"]).copy()
    W["efter"] = (W.t >= P_(switch)).astype(float); W["ed"] = W.efter * W.dos
    W["e1"] = W.efter * (W.dos == 1); W["e2"] = W.efter * (W.dos == 2)
    s = W.sig / 10
    for k in (1, 2, 3): W[f"es{k}"] = W.efter * s ** k
    pm = W[W.efter == 0].groupby("fundid").f.mean(); W["efpre"] = W.efter * W.fundid.map(pm).fillna(0)
    W["tt"] = W.t.astype(str); W["tc"] = W.tt + "_" + W.cat.astype(str)
    for n in (5, 10, 20): W[f"tv{n}"] = W.tt + "_" + W[f"vd{n}"].astype(str)
    return W
W = prep(A); FE2 = ["fundid", "tc"]; FE3 = ["fundid", "tc", "tv10"]
print(f"\nUrval: {W.fundid.nunique()} fonder, {len(W)} fondmanader 2021-2024")

print("\n===== TEST A: Adelino-formen =====")
Q = W.dropna(subset=["star_lag"]); b, se, V, Gn = est(Q, ["star_lag", "ed"], FE3); star = b[0]
print("A6 stjarnan i samma regression"); line("stjarna, per stjarna", b[0], se[0], Gn, len(Q)); line("beta med stjarnan", b[1], se[1], Gn, len(Q), star)
print("A1 HUVUD: Dos x Efter + fond + kategori x manad + volatilitetsdecil x manad")
b, se, V, Gn = est(W, ["ed"], FE3); lo, hi = line("beta, pp per ar per steg", b[0], se[0], Gn, len(W), star); print("  LASREGEL:", regel(lo, hi)); bmain = b[0]
print("OVRIGA RADER")
b, se, V, Gn = est(W, ["ed"], FE2); line("A2 utan volatilitetsdecil", b[0], se[0], Gn, len(W))
b, se, V, Gn = est(W, ["e1", "e2"], FE3); line("A3 ett steg x Efter", b[0], se[0], Gn, len(W)); line("A3 tva steg x Efter", b[1], se[1], Gn, len(W))
b, se, V, Gn = est(W, ["ed"], ["fundid", "tc", "tv5"]); line("A4 fem grupper", b[0], se[0], Gn, len(W))
b, se, V, Gn = est(W, ["ed"], ["fundid", "tc", "tv20"]); line("A4 tjugo grupper", b[0], se[0], Gn, len(W))
W5 = W.copy(); W5["f"] = W5.f199; b, se, V, Gn = est(W5, ["ed"], FE3); line("A5 winsorisering 1/99", b[0], se[0], Gn, len(W5))
b, se, V, Gn = est(W, ["ed", "es1", "es2", "es3", "efpre"], FE2); line("jfr sicksacken (polynom + flode fore)", b[0], se[0], Gn, len(W))
b, se, V, Gn = est(W, ["ed", "es1", "es2", "es3"], FE2); line("jfr sicksacken utan flode fore", b[0], se[0], Gn, len(W))
print("A7 andel av variansen i Dos x Efter som aterstar efter fasta effekter")
v0 = W.ed.var()
for nm, X, keys in [("A2 fond + kategori x manad", [], FE2), ("A1 + volatilitetsdecil x manad", [], FE3), ("+ 20 grupper", [], ["fundid", "tc", "tv20"]), ("sicksackens polynom", ["es1", "es2", "es3"], FE2)]:
    D = dm(W[["ed"] + X].values, [W[k].values for k in keys]); r = D[:, 0]
    if X: r = r - D[:, 1:] @ np.linalg.lstsq(D[:, 1:], r, rcond=None)[0]
    print(f"  {nm:<34}{100 * r.var() / v0:5.1f} %")

print("\nV1 HANDELSSTUDIE (Dos x kvartal, A1:s effekter, bas 2022Q4)")
W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str); cols = []
for q in sorted(W.q.unique()):
    if q == "2022Q4": continue
    W["d_" + q] = (W.q == q) * W.dos; cols.append("d_" + q)
b, se, V, Gn = est(W, cols, FE3)
for i, c in enumerate(cols): print(f"  {c[2:]}  {b[i]:+6.2f}  SE {se[i]:4.2f}")
pre = [i for i, c in enumerate(cols) if c[2:] < "2022Q4"]; post = [i for i, c in enumerate(cols) if c[2:] > "2022Q4"]
def wald(ix): bb = b[ix]; w = bb @ np.linalg.pinv(V[np.ix_(ix, ix)]) @ bb; return w, stats.chi2.sf(w, len(ix))
(w1, p1), (w2, p2) = wald(pre), wald(post)
print(f"  fore: chi2 {w1:.2f}, p {p1:.3f} | efter: chi2 {w2:.2f}, p {p2:.3f} -> V1 {'UPPFYLLT' if p1 > 0.05 else 'FALLER'}")

print("\nV2 LATSASBYTE januari 2021 (2019-2022)")
W3 = prep(A, "2019-01", "2022-12", "2021-01")
n1 = W3[W3.efter == 0].groupby("fundid").size(); n2 = W3[W3.efter == 1].groupby("fundid").size()
ok = set(n1.index[n1 >= 18]) & set(n2.index[n2 >= 18]); W3 = W3[W3.fundid.isin(ok)]
b, se, V, Gn = est(W3, ["ed"], FE3); l3, h3 = line("latsasbyte", b[0], se[0], Gn, len(W3)); print("  V2:", "UPPFYLLT" if l3 <= 0 <= h3 else "FALLER")
Wv = W.copy(); Wv["f"] = Wv.f + 0.25 * Wv.ed; bv, *_ = est(Wv, ["ed"], FE3)
print(f"V3 inplanterad +3,00 ger {bv[0]-bmain:+.3f}")

print("\n===== TEST B: Reuter-Zitzewitz reformform (tvarsnitt) =====")
def ols_hc1(y, X):
    X = np.asarray(X, float); y = np.asarray(y, float); XtXi = np.linalg.pinv(X.T @ X); b = XtXi @ X.T @ y; e = y - X @ b
    n, k = X.shape; V = XtXi @ (X.T * e ** 2) @ X @ XtXi * n / (n - k); return b, np.sqrt(np.diag(V))
def tvar(y0, y1, c0, c1, extra=(), nmin=9, plant=0.0):
    def per(a, b_):
        g = A[(A.t >= P_(a)) & (A.t <= P_(b_))].groupby("fundid").f.agg(["mean", "size"]); return g
    y = per(y0, y1); c = per(c0, c1); nm_y = round(nmin * ((P_(y1) - P_(y0)).n + 1) / 12)
    D = mb.join(y["mean"].where(y["size"] >= nm_y).rename("y") * 12).join(c["mean"].where(c["size"] >= nmin).rename("c") * 12)
    if "star" in extra:
        s = A[A.t == P_(y0)].set_index("fundid"); D = D.join(s.star_lag.rename("star")).join(np.log(s.na).rename("lsize"))
    D = D.dropna(subset=["y", "c", "dos", "sig", "srri22", "cat"] + (["star", "lsize"] if "star" in extra else []))
    D = D[D.groupby("cat").cat.transform("size") >= 2]; D["y"] = D.y + plant * D.dos
    Xc = [D.dos, D.sig, D.c] + ([D.star, D.lsize] if "star" in extra else [])
    Xd = pd.get_dummies(D.srri22.astype(int), prefix="k", drop_first=True).astype(float)
    Z = np.column_stack(Xc + [Xd.values]); Zy = dm(np.column_stack([D.y.values, Z]), [D.cat.values])
    b, se = ols_hc1(Zy[:, 0], Zy[:, 1:]); return b, se, len(D)
b, se, n = tvar("2023-01", "2023-12", "2022-01", "2022-12"); lo, hi = line("B1 HUVUD: flode 2023 pa Dos", b[0], se[0], n, n, star)
print("  LASREGEL:", regel(lo, hi)); print(f"     volatilitet {b[1]:+.3f} (SE {se[1]:.3f}) | flode 2022 {b[2]:+.3f} (SE {se[2]:.3f})"); b1 = b[0]
b, se, n = tvar("2023-01", "2023-12", "2022-01", "2022-12", extra=("star",)); line("B2 + stjarna och log storlek", b[0], se[0], n, n); print(f"     stjarna {b[3]:+.2f} (SE {se[3]:.2f})")
b, se, n = tvar("2023-01", "2024-12", "2022-01", "2022-12"); line("B3 horisont 24 manader (per ar)", b[0], se[0], n, n)
b, se, n = tvar("2022-01", "2022-12", "2021-01", "2021-12"); l4, h4 = line("B4 falsifiering: flode 2022 pa Dos", b[0], se[0], n, n); print("  B4:", "UPPFYLLT" if l4 <= 0 <= h4 else "FALLER")
b, se, n = tvar("2023-01", "2023-12", "2022-01", "2022-12", plant=3.0); print(f"B5 inplanterad +3,00 ger {b[0]-b1:+.3f}")
