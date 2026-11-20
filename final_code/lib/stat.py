"""Skattningsverktyg som alla test delar.

Allt ar vanlig minsta kvadrat. Fasta effekter tas bort genom att variablerna
centreras inom grupp (flera grupper: vaxelvis tills inget andras). Standardfelen
ar klustrade enligt Cameron, Gelbach och Miller (2011): V = V_fond + V_manad - V_fond x manad,
samma som Statas reghdfe med vce(cluster fond manad), som ankarets kod anvander.
"""
import numpy as np
import pandas as pd


def demean(M, groups, w=None, tol=1e-10, itmax=5000):
    """Centrera kolumnerna i M inom varje grupp i `groups` (lista av vektorer)."""
    M = np.array(M, dtype=float, copy=True)
    if M.ndim == 1:
        M = M[:, None]
    w = np.ones(len(M)) if w is None else np.asarray(w, float)
    codes = [pd.factorize(np.asarray(g))[0] for g in groups]
    sw = [np.bincount(c, w) for c in codes]
    for _ in range(itmax):
        mx = 0.0
        for c, s in zip(codes, sw):
            for j in range(M.shape[1]):
                m = np.bincount(c, w * M[:, j]) / s
                M[:, j] -= m[c]
                mx = max(mx, np.abs(m).max())
        if len(codes) == 1 or mx < tol:
            break
    return M


def _meat(A, e, keys):
    codes = pd.factorize(np.asarray(keys))[0]
    S = np.zeros((codes.max() + 1, A.shape[1]))
    np.add.at(S, codes, A * e[:, None])
    G = len(S)
    return G / (G - 1) * S.T @ S


class Res:
    def __init__(self, b, se, n, nf, V, names):
        self.b = pd.Series(b, index=names)
        self.se = pd.Series(se, index=names)
        self.t = self.b / self.se
        self.n, self.nf, self.V, self.names = n, nf, V, names


def ols(df, y, xs, fe=(), cluster=("FundId", "ym"), const=False):
    """OLS av y pa xs med fasta effekter `fe` och klustrade standardfel.
    cluster: en eller tva kolumner; None ger heteroskedasticitetsrobusta fel (HC1)."""
    g = df.dropna(subset=[y] + list(xs))
    Z = g[[y] + list(xs)].to_numpy(float)
    if fe:
        Z = demean(Z, [g[k].astype(str).to_numpy() for k in fe])
    yy, A = Z[:, 0], Z[:, 1:]
    if const:
        A = np.c_[np.ones(len(A)), A]
    Ai = np.linalg.pinv(A.T @ A)
    b = Ai @ A.T @ yy
    e = yy - A @ b
    if cluster is None:
        n, k = A.shape
        V = Ai @ ((A.T * e ** 2) @ A) @ Ai * n / (n - k)
    elif len(cluster) == 1:
        V = Ai @ _meat(A, e, g[cluster[0]].astype(str).to_numpy()) @ Ai
    else:
        c1 = g[cluster[0]].astype(str).to_numpy()
        c2 = g[cluster[1]].astype(str).to_numpy()
        V = Ai @ (_meat(A, e, c1) + _meat(A, e, c2) - _meat(A, e, np.char.add(np.char.add(c1, "|"), c2))) @ Ai
    names = (["_cons"] if const else []) + list(xs)
    nf = g["FundId"].nunique() if "FundId" in g else len(g)
    return Res(b, np.sqrt(np.clip(np.diag(V), 0, None)), len(g), nf, V, names)


def r2(df, y, xs, fe, w=None):
    """Forklaringsgrad for y pa xs och fasta effekter fe (R2 mot ocentrerat medel)."""
    yv = df[y].to_numpy(float)
    ww = np.ones(len(yv)) if w is None else np.asarray(w, float)
    sst = np.sum(ww * (yv - np.average(yv, weights=ww)) ** 2)
    cols = np.c_[yv, df[list(xs)].to_numpy(float)] if len(xs) else yv[:, None]
    Z = demean(cols, [df[k].astype(str).to_numpy() for k in fe], ww) if fe else cols
    e = Z[:, 0]
    if len(xs):
        sw = np.sqrt(ww)
        b = np.linalg.lstsq(Z[:, 1:] * sw[:, None], e * sw, rcond=None)[0]
        e = e - Z[:, 1:] @ b
    return 1 - np.sum(ww * e ** 2) / sst


def nw_mean(x, lags=6):
    """Medelvarde och Newey-West-standardfel (Bartlett-vikter) for en tidsserie."""
    x = np.asarray(x, float)
    T = len(x)
    u = x - x.mean()
    s = u @ u / T
    for k in range(1, lags + 1):
        s += 2 * (1 - k / (lags + 1)) * (u[k:] @ u[:-k]) / T
    return x.mean(), np.sqrt(s / T)


def nw_reg(y, x, lags=6):
    """Tidsserieregression y = a + X b med Newey-West-fel (Bartlett-vikter) och faktorn n/(n-k),
    som Statas `newey y x, lag(6)` i forfattarnas kod. x: en kolumn eller flera.
    Returnerar b (utan konstant), t och R2."""
    y = np.asarray(y, float)
    X = np.c_[np.ones(len(y)), np.asarray(x, float)]
    n, k = X.shape
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    Xi = np.linalg.inv(X.T @ X)
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += (1 - L / (lags + 1)) * (G + G.T)
    V = Xi @ S @ Xi * n / (n - k)
    return b[1:], b[1:] / np.sqrt(np.diag(V)[1:]), 1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2)


def fama_macbeth(df, y, xs, nmin=100, within=None, lags=6):
    """Fama och MacBeth (1973): tvarsnittsregression varje manad, sedan medel over manaderna
    med Newey-West-fel. within: kolumn att centrera inom (t.ex. kategori)."""
    rows = []
    for m, c in df.groupby("ym"):
        if len(c) < nmin:
            continue
        Z = c[[y] + list(xs)].astype(float)
        if within:
            Z = Z - Z.groupby(c[within].values).transform("mean")
        A = np.c_[np.ones(len(Z)), Z[list(xs)].values]
        rows.append(np.linalg.lstsq(A, Z[y].values, rcond=None)[0][1:])
    B = pd.DataFrame(rows, columns=list(xs))
    out = {k: nw_mean(B[k].values, lags) for k in xs}
    return out, B
