import numpy as np, pandas as pd
P_ = lambda s: pd.Period(s, 'M')
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
    D = dm(W[["f"] + X].values, [W[k].values for k in keys]); yd = D[:, 0]; Xd = D[:, 1:]
    A_ = np.linalg.pinv(Xd.T @ Xd); b = A_ @ Xd.T @ yd; e = yd - Xd @ b
    f = W.fundid.values; t = W.tt.values; ft = (W.fundid.astype(str) + "|" + W.tt).values
    Vf = A_ @ clus(Xd, e, f) @ A_.T; V2 = Vf + A_ @ clus(Xd, e, t) @ A_.T - A_ @ clus(Xd, e, ft) @ A_.T
    se = np.maximum(np.sqrt(np.diag(Vf)), np.sqrt(np.clip(np.diag(V2), 0, None))); return b * 12, se * 12

def wins(s, t, lo=.01, hi=.99):
    q = s.groupby(t).quantile([lo, hi]).unstack(); return s.clip(t.map(q[lo]), t.map(q[hi]))

def evaluate(A, nm, extra=None):
    """A: rader SecId, fundid, t, f (pp per manad), star_lag, cat. Dos, sigma ur huvudklassen."""
    A = A.dropna(subset=["f", "cat"]).copy()
    y = A.t.dt.year; n1 = A[y.isin([2019, 2020])].groupby("SecId").size(); n2 = A[y.isin([2021, 2022])].groupby("SecId").size()
    A = A[A.SecId.isin(set(n1.index[n1 >= 18]) & set(n2.index[n2 >= 18]))]
    A["efter"] = (A.t >= P_("2021-01")).astype(float); A["ed"] = A.efter * A.dos; s = A.sig / 10
    for k in (1, 2, 3): A[f"es{k}"] = A.efter * s ** k
    A["tt"] = A.t.astype(str); A["tc"] = A.tt + "_" + A.cat.astype(str)
    X = ["ed", "es1", "es2", "es3"] + (extra(A) if extra else [])
    Q = A.dropna(subset=["star_lag"])
    b, se = est(Q, ["star_lag"] + X)
    return (A.fundid.nunique(), se[1], b[0])
    print(f"  {nm:<62} fonder {A.fundid.nunique():5d} | SE dos {se[1]:5.2f} | stjarna {b[0]:+6.2f} (t {b[0]/se[0]:4.1f}) | MDE i stjarnor {2.8*se[1]/b[0]:5.2f}")

