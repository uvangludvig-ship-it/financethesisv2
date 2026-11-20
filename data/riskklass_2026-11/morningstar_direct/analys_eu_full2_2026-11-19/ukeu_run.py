"""UK mot EU enligt DEKLARATION_uk_mot_eu_A1_A3_2026-11-19. python3 -I ukeu_run.py <tag>"""
import sys, numpy as np, pandas as pd
from scipy import stats
T = sys.argv[1]; P_ = lambda s: pd.Period(s, "M"); STAR = 4.81
A0 = pd.read_pickle(f"ukeu_sidor_{T}.pkl")

def dm(X, keys, tol=1e-9, itmax=1000):
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
def est(W, y, X, keys):
    D = dm(W[[y] + X].values, [W[k].values for k in keys]); yd = D[:, 0]; Xd = D[:, 1:]
    A_ = np.linalg.pinv(Xd.T @ Xd); b = A_ @ Xd.T @ yd; e = yd - Xd @ b
    f = W.fundid.values; t = W.tt.values; ft = (W.fundid.astype(str) + "|" + W.tt).values
    Vf = A_ @ clus(Xd, e, f) @ A_.T; V2 = Vf + A_ @ clus(Xd, e, t) @ A_.T - A_ @ clus(Xd, e, ft) @ A_.T
    se = np.maximum(np.sqrt(np.diag(Vf)), np.sqrt(np.clip(np.diag(V2), 0, None)))
    return b * 12, se * 12, Vf * 144, W.fundid.nunique()
def line(nm, b, se, G, n):
    lo, hi = b - 1.96 * se, b + 1.96 * se
    print(f"    {nm:<50}{b:+6.2f}  SE {se:4.2f}  t {b/se:+5.2f}  95 % [{lo:+6.2f}; {hi:+6.2f}]  MDE {2.8*se:4.1f}  stjarnor [{lo/STAR:+.2f}; {hi/STAR:+.2f}]  fonder {G}  obs {n}")
    return lo, hi
def rule(lo, hi):
    return ("utesluter noll" if (lo > 0 or hi < 0) else "innehaller noll") + " | " + (
        "inom +-2,4: halv stjarna avvisas" if (lo > -2.4 and hi < 2.4) else ("inom +-4,81: en stjarna avvisas" if (lo > -STAR and hi < STAR) else "ingen slutsats"))

def prepN(A, t0="2021-01", t1="2024-12", switch="2023-01", fcol="f", drop=None, okcol="ok_main"):
    W = A[A[okcol] & (A.t >= P_(t0)) & (A.t <= P_(t1))].copy(); W["y"] = W[fcol]
    if drop: W = W[~((W.t >= P_(drop[0])) & (W.t <= P_(drop[1])))]
    W["efter"] = (W.t >= P_(switch)).astype(float); W["eu"] = (W.sida == "EU").astype(float); W["ee"] = W.efter * W.eu
    W["fs"] = W.fundid + "|" + W.sida; pm = W[W.efter == 0].groupby("fs").y.mean(); W["efpre"] = W.efter * W.fs.map(pm).fillna(0)
    W["tt"] = W.t.astype(str); W["fm"] = W.fundid + "|" + W.tt
    W = W[W.groupby("fm").sida.transform("nunique") == 2]  # bara manader dar bada sidor finns
    return W
def runN(W, nm, anc=True):
    b, se, V, G = est(W, "y", ["ee"] + (["efpre"] if anc else []), ["fs", "fm"]); return line(nm, b[0], se[0], G, len(W)), b[0]

def prepD(A, fcol="f"):
    W = A[A.ok_main & (A.t >= P_("2021-01")) & (A.t <= P_("2024-12"))]
    g = W.pivot_table(index=["fundid", "t"], columns="sida", values=fcol).dropna().reset_index(); g["d"] = g.EU - g.UK
    g = g.join(W.drop_duplicates("fundid").set_index("fundid")[["dos", "sig", "cat"]], on="fundid")
    g = g[g.dos.isin([0, 1, 2]) & g.sig.notna() & g.cat.notna()].copy()
    g["efter"] = (g.t >= P_("2023-01")).astype(float); g["ed"] = g.efter * g.dos; s = g.sig / 10
    for k in (1, 2, 3): g[f"es{k}"] = g.efter * s ** k
    pm = g[g.efter == 0].groupby("fundid").d.mean(); g["edpre"] = g.efter * g.fundid.map(pm)
    g["tt"] = g.t.astype(str); g["tc"] = g.tt + "_" + g.cat.astype(str); return g

for lev in (2, 1, 3):
    A = A0[A0.niva == lev]
    print(f"\n================ NIVA {lev}{' (HUVUDNIVA)' if lev == 2 else ''} ================")
    W = prepN(A)
    mm = W.groupby(["sida", "efter"]).y.mean().unstack() * 12
    print(f"  Ra medelfloden pp/ar: EU fore {mm.loc['EU',0.0]:+.2f} efter {mm.loc['EU',1.0]:+.2f} | UK fore {mm.loc['UK',0.0]:+.2f} efter {mm.loc['UK',1.0]:+.2f}")
    print("  HUVUDTEST N (nivaskift, Efter x EU, ANCOVA, fond x sida och fond x manad)")
    (lo, hi), bN = runN(W, "beta N"); print("    LASREGEL:", rule(lo, hi))
    print("  HUVUDTEST D (dos inom par, gap EU minus UK)")
    g = prepD(A); b, se, V, G = est(g, "d", ["ed", "es1", "es2", "es3", "edpre"], ["fundid", "tc"]); lo, hi = line("beta D (per steg)", b[0], se[0], G, len(g)); print("    LASREGEL:", rule(lo, hi))
    # V2
    W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str); cols = []
    for q in sorted(W.q.unique()):
        if q == "2022Q4": continue
        W["e_" + q] = (W.q == q) * W.eu; cols.append("e_" + q)
    b, se, V, G = est(W, "y", cols, ["fs", "fm"])
    pre = [i for i, c in enumerate(cols) if c[2:] < "2022Q4"]; post = [i for i, c in enumerate(cols) if c[2:] > "2022Q4"]
    def wald(ix): bb = b[ix]; w = bb @ np.linalg.pinv(V[np.ix_(ix, ix)]) @ bb; return w, stats.chi2.sf(w, len(ix))
    (wp, pp), (wa, pa) = wald(pre), wald(post)
    print("  V2 HANDELSSTUDIE (EU x kvartal, bas 2022Q4):  " + "  ".join(f"{c[2:]} {b[i]:+.1f}({se[i]:.1f})" for i, c in enumerate(cols)))
    print(f"    fore: chi2 {wp:.2f} p {pp:.3f} | efter: chi2 {wa:.2f} p {pa:.3f} | V2: {'UPPFYLLT' if pp > 0.05 else 'FALLER'}")
    # V3
    W3 = prepN(A, "2019-01", "2022-12", "2021-01", okcol="ok_pl"); (lo3, hi3), _ = runN(W3, "V3 latsasbyte jan 2021"); print(f"    V3: {'UPPFYLLT' if lo3 < 0 < hi3 else 'FALLER'}")
    print("  SIDOTEST")
    runN(W, "U1 utan ANCOVA", anc=False)
    runN(prepN(A, fcol="f1"), "U2 winsorisering 1/99")
    runN(prepN(A, drop=("2022-09", "2023-03")), "U3 utan sep 2022 - mar 2023")
    runN(prepN(A, "2022-01", "2023-12"), "U4 12 fore / 12 efter")
    runN(prepN(A, "2021-01", "2025-12"), "U5 24 fore / 36 efter")
    runN(prepN(A, "2021-01", "2023-06"), "U6 efter = jan-jun 2023")
    We = W[W.cat.astype(str).str.contains("Equity")]; runN(We, "U7 aktiefonder")
    gg = W.groupby(["fundid", "sida", "efter"]).y.mean().unstack(); gap = (gg.xs("EU", level="sida") - gg.xs("UK", level="sida")).dropna() * 12
    dd = gap[1.0] - gap[0.0]; x = gap[0.0] - gap[0.0].mean(); X = np.column_stack([np.ones(len(dd)), x]); XtXi = np.linalg.inv(X.T @ X)
    bb = XtXi @ X.T @ dd.values; e = dd.values - X @ bb; Vv = XtXi @ (X.T * e ** 2) @ X @ XtXi
    print(f"    U8 kollapsad: skift {bb[0]:+.2f}  SE {np.sqrt(Vv[0,0]):.2f}  (panel {bN:+.2f}) fonder {len(dd)}")
    Wp = W.copy(); Wp["y"] = Wp.y + 3.0 / 12 * Wp.ee; b, se, V, G = est(Wp, "y", ["ee", "efpre"], ["fs", "fm"])
    print(f"  VERIFIERING: inplanterad +3,00 ger {b[0]:+.3f} (vantat {bN + 3:+.3f})")
