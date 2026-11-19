"""Vilken rensning sanker bruset? Bara latsasbytet januari 2021 (floden 2019-2022, inget efter dec 2022).
Rapporterar SE och MDE i stjarnor (2,8 x SE / stjarnans koefficient i samma regression). Inga beta for dosen skrivs ut.
python3 -I brus_latsas.py <katalog>"""
import sys, numpy as np, pandas as pd
M = sys.argv[1]; P_ = lambda s: pd.Period(s, "M")
L = pd.read_pickle(f"{M}/panel_eu_a1.pkl"); E = pd.read_pickle(f"{M}/urval_eu_a1.pkl"); B = pd.read_pickle(f"{M}/huvudklasser_eu_a1.pkl")
L = L[(L.t >= P_("2019-01")) & (L.t <= P_("2022-12"))].copy()
assert L.t.max() <= P_("2022-12")

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
    print(f"  {nm:<62} fonder {A.fundid.nunique():5d} | SE dos {se[1]:5.2f} | stjarna {b[0]:+6.2f} (t {b[0]/se[0]:4.1f}) | MDE i stjarnor {2.8*se[1]/b[0]:5.2f}")

base_cols = ["dos", "sig"]
def main_rows(fcol="fw", Lx=None):
    Lx = L if Lx is None else Lx
    A = Lx[Lx.SecId.isin(B.index)].copy(); A["f"] = A[fcol] * 100
    return A.join(B[base_cols], on="SecId")

print("LATSASBYTE jan 2021, 2019-20 mot 2021-22. Lagre 'MDE i stjarnor' ar battre.")
evaluate(main_rows(), "0. Som deklarerat (en klass per fond, NA >= 1 MUSD, wins 1/99)")

# 1. hogre storleksgrans
Lb = L.copy(); m = Lb.na_lag >= 10e6; Lb["f10"] = np.where(m, wins(Lb.f.where(m), Lb.t), np.nan)
evaluate(main_rows("f10", Lb), "1. NA_t-1 >= 10 MUSD")

# 2. datafel: oforandrad NA (stillastaende) och spikar som vands nasta manad
Lc = L.sort_values(["SecId", "t"]).copy()
na_t = Lc.na_lag.groupby(Lc.SecId).shift(-1)  # NA_t = nasta rads na_lag
stale = (na_t == Lc.na_lag)
fn = Lc.f.groupby(Lc.SecId).shift(-1)
spike = (Lc.f.abs() > 0.2) & (fn.abs() > 0.2) & (np.sign(Lc.f) != np.sign(fn)) & ((Lc.f + fn).abs() < 0.25 * Lc.f.abs())
bad = stale | spike | spike.groupby(Lc.SecId).shift(1, fill_value=False)
print(f"     (datafel: stillastaende NA {stale.mean():.3f}, spikar {spike.mean():.4f} av klassmanaderna)")
mm = Lc.stor & ~bad; Lc["fc"] = np.where(mm, wins(Lc.f.where(mm), Lc.t), np.nan)
evaluate(main_rows("fc", Lc), "2. Utan stillastaende NA och vanda spikar")

# 3. hardare winsorisering
Ld = L.copy(); Ld["f5"] = np.where(Ld.stor, wins(Ld.f.where(Ld.stor), Ld.t, .025, .975), np.nan)
evaluate(main_rows("f5", Ld), "3. Winsorisering 2,5/97,5 inom manad")

# 4. fondniva: dollarfloden summerade over alla KID-klasser (ej institutionella), delat med summerad NA
K = L[L.SecId.isin(E.index[~E.inst & (E.sida != "UK")]) & L.fundid.isin(set(B.FundId)) & L.stor].copy()
K["usd"] = K.f * K.na_lag
G = K.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index(); G["f"] = wins(G.usd / G.na, G.t) * 100
mb = B.reset_index().set_index("FundId")[["SecId", "dos", "sig", "Morningstar Category"]].rename(columns={"Morningstar Category": "cat"})
G = G.join(mb, on="fundid"); G = G.merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left")
evaluate(G, "4. Fondniva: alla KID-klasser summerade i dollar")

# 5. kontroll for forperiodens flodesniva (Efter x medelflode 2019-20)
def pre_ctrl(A):
    pm = A[A.efter == 0].groupby("SecId").f.mean(); A["efpre"] = A.efter * A.SecId.map(pm).fillna(0); return ["efpre"]
evaluate(main_rows(), "5. Med Efter x forperiodens medelflode", pre_ctrl)

# 6. rangmatt: percentil inom manad x kategori (0-100)
Lr = main_rows(); Lr["f"] = Lr.groupby(["t", "cat"]).f.rank(pct=True) * 100
evaluate(Lr, "6. Percentilrang inom manad x kategori")


# 8. alla klasser (sidotest 12)
allc = E.index[~E.inst & (E.sida != "UK") & E.srri22.notna() & E.sri_ny.notna() & E.dos.isin([0, 1, 2]) & E.sig.notna() & E["Morningstar Category"].notna()]
A8 = L[L.SecId.isin(allc)].copy(); A8["f"] = A8.fw * 100; A8 = A8.join(E[base_cols], on="SecId")
evaluate(A8, "8. Alla icke-institutionella klasser (sidotest 12)")

# 9. kombination: fondniva + datafel bort + forperiodskontroll
Kc = Lc[Lc.SecId.isin(E.index[~E.inst & (E.sida != "UK")]) & Lc.fundid.isin(set(B.FundId)) & Lc.stor & ~bad].copy(); Kc["usd"] = Kc.f * Kc.na_lag
G2 = Kc.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index(); G2["f"] = wins(G2.usd / G2.na, G2.t) * 100
G2 = G2.join(mb, on="fundid").merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left")
evaluate(G2, "9. Fondniva + utan datafel + forperiodskontroll", pre_ctrl)
