"""Anvandning: python3 -I sicksack_eu_run.py <katalog> [a1|bas]
Sicksacken pa EU-basdatan enligt DEKLARATION_sicksack_eu_preliminar_2026-11-19 (tillagg till DEKLARATION_sicksack_2026-11-19).
python3 -I sicksack_eu_run.py <katalog med panel_eu_a1.pkl, urval_eu_a1.pkl, huvudklasser_eu_a1.pkl, a1_raw.pkl>"""
import sys, numpy as np, pandas as pd
from scipy import stats

M = sys.argv[1]; T = sys.argv[2] if len(sys.argv) > 2 else "a1"; P_ = lambda s: pd.Period(s, "M")
L = pd.read_pickle(f"{M}/panel_eu_{T}.pkl"); L["fw"] *= 100; L["fw_alla"] *= 100  # andel -> procent (pp)
E = pd.read_pickle(f"{M}/urval_eu_{T}.pkl"); B = pd.read_pickle(f"{M}/huvudklasser_eu_{T}.pkl")
assert len(B) == {"a1": 3214, "bas": 4523, "b1": 4523, "full": 4863, "full2": 4818}[T], len(B)
raw = pd.read_pickle(f"{M}/" + ("a1_raw.pkl" if T == "a1" else f"{T}_raw.pkl")); raw = raw[raw.SecId.astype(str).str.match(r"^F[0-9A-Z]{9}$")].set_index("SecId")
def cumret(m0, m1):
    ps = pd.period_range(m0, m1, freq="M").astype(str)
    R = pd.DataFrame({p: pd.to_numeric(raw[f"Monthly Return {p} USD"], errors="coerce") for p in ps}, index=raw.index) / 100
    return ((1 + R).prod(axis=1) - 1).where(R.notna().all(axis=1)) * 100
E["ret12_22"] = cumret("2022-01", "2022-12"); E["ret36_22"] = cumret("2020-01", "2022-12")

def mk(sec, fundlevel=None, fcol="fw"):
    """Klassmanadsrader for klasserna sec. fundlevel: ta dos/sigma/srri22 fran fondens huvudklass."""
    A = L[L.SecId.isin(sec)].dropna(subset=[fcol, "cat"]).copy(); A["f"] = A[fcol]
    src = B.set_index("FundId") if fundlevel else E
    key = "fundid" if fundlevel else "SecId"
    cols = ["dos", "dos_smal", "sig", "srri22"] + ([] if fundlevel else ["ret12_22", "ret36_22"])
    A = A.join(src[cols], on=key)
    if fundlevel:
        A = A.join(E[["ret12_22", "ret36_22"]], on="SecId")
    A["sig_w"] = A.sig; A["cat_lag"] = A.cat; A["aktie"] = A.cat.astype(str).str.contains("Equity")
    return A

A = mk(set(B.index))
print(f"Urval: {A.SecId.nunique()} klasser, {A.fundid.nunique()} fonder, {len(A)} klassmanader 2019-2025. Dos: {B.dos.value_counts().sort_index().to_dict()}")

# ---------- skattare (oforandrade fran sicksack_run.py) ----------
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
    sc = pd.DataFrame(Zd * e[:, None]).groupby(g).sum().values; G = len(sc)
    return sc.T @ sc * G / (G - 1)

def est(W, y, X, keys):
    ks = [W[k].values for k in keys]
    D = dm(W[[y] + X].values, ks); yd = D[:, 0]; Xd = D[:, 1:]
    A_ = np.linalg.pinv(Xd.T @ Xd); b = A_ @ Xd.T @ yd; e = yd - Xd @ b
    f = W.fundid.values; t = W.tt.values; ft = (W.fundid.astype(str) + "|" + W.tt).values
    Vf = A_ @ clus(Xd, e, f) @ A_.T
    V2 = Vf + A_ @ clus(Xd, e, t) @ A_.T - A_ @ clus(Xd, e, ft) @ A_.T
    se = np.maximum(np.sqrt(np.diag(Vf)), np.sqrt(np.clip(np.diag(V2), 0, None)))
    return b * 12, se * 12, Vf * 144, W.fundid.nunique()

def prep(W, t0="2021-01", t1="2024-12", dose="dos", vol="sig_w", deg=3, switch="2023-01"):
    W = W[(W.t >= P_(t0)) & (W.t <= P_(t1))].copy()
    W["efter"] = (W.t >= P_(switch)).astype(float)
    W["ed"] = W.efter * W[dose]; s = W[vol] / 10
    for k in range(1, deg + 1): W[f"es{k}"] = W.efter * s ** k
    W["tt"] = W.t.astype(str); W["tc"] = W.tt + "_" + W.cat_lag.astype(str)
    W["eo"] = W.efter.astype(int).astype(str) + "_" + W.srri22.astype(int).astype(str)
    return W

def line(nm, b, se, G, n, extra=""):
    lo, hi = b - 1.96 * se, b + 1.96 * se
    print(f"  {nm:<58}{b:+6.2f}  SE {se:4.2f}  t {b/se:+5.2f}  95 % [{lo:+6.2f}; {hi:+6.2f}]  MDE {2.8*se:4.1f}  fonder {G}  obs {n} {extra}")
    return lo, hi

ES3 = ["es1", "es2", "es3"]
def run(W, nm, X=None, keys=("SecId", "tc")):
    b, se, V, G = est(W, "f", X or (["ed"] + ES3), list(keys)); return line(nm, b[0], se[0], G, len(W))

# ---------- beskrivning ----------
W = prep(A)
g = W.groupby(["dos", "efter"]).f.mean().unstack() * 12
print("\nMEDELFLODE, pp per ar (ra medel, inga kontroller):")
print(pd.DataFrame({"fore 2021-22": g[0.0], "efter 2023-24": g[1.0], "andring": g[1.0] - g[0.0], "fonder": W.drop_duplicates("SecId").dos.value_counts().sort_index()}).round(2).to_string())

# ---------- HUVUDTEST ----------
print("\nHUVUDTEST: Efter x Dos, Efter x polynom(sigma), klass- och manad x kategori-effekter. pp per ar per steg siffran foll.")
b, se, V, G = est(W, "f", ["ed"] + ES3, ["SecId", "tc"]); lo, hi = line("beta", b[0], se[0], G, len(W))
STAR, HALF = 5.5, 2.75
print("  LASREGEL:", "utesluter noll" if (lo > 0 or hi < 0) else "innehaller noll", "|",
      "inom +-2,75: halv stjarna avvisas" if (lo > -HALF and hi < HALF) else ("inom +-5,5: en stjarna avvisas, halv stjarna kan inte avvisas" if (lo > -STAR and hi < STAR) else "ingen slutsats om storlek"))
bmain, semain = b[0], se[0]

# ---------- V1 ----------
Q = W.dropna(subset=["star_lag"])
b, se, V, G = est(Q, "f", ["star_lag", "ed"] + ES3, ["SecId", "tc"])
print("\nV1 KAND VIKT: forra manadens stjarna i huvudregressionen")
line("stjarna, per stjarna", b[0], se[0], G, len(Q)); line("beta med stjarnan", b[1], se[1], G, len(Q))
print("  V1:", "UPPFYLLT" if b[0] / se[0] >= 2 else "FALLER")

# ---------- V2 ----------
W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str)
qs = sorted(W.q.unique()); base = "2022Q4"; cols = []; pcols = []
for q in qs:
    if q == base: continue
    W["d_" + q] = (W.q == q) * W.dos; cols.append("d_" + q); s = W.sig_w / 10
    for k in (1, 2, 3): W[f"p{k}_" + q] = (W.q == q) * s ** k; pcols.append(f"p{k}_" + q)
b, se, V, G = est(W, "f", cols + pcols, ["SecId", "tc"])
print("\nV2 HANDELSSTUDIE per kvartal (Dos x kvartal, bas 2022Q4, polynom x kvartal):")
ev = pd.DataFrame({"kvartal": [c[2:] for c in cols], "b": b[:len(cols)], "se": se[:len(cols)]}); ev["t"] = ev.b / ev.se
print(ev.round(2).to_string(index=False)); ev.to_csv(f"sicksack_eu_handelsstudie_{T}.csv", index=False)
pre_i = [i for i, c in enumerate(cols) if c[2:] < base]; post_i = [i for i, c in enumerate(cols) if c[2:] > base]
def wald(idx):
    bb = b[idx]; VV = V[np.ix_(idx, idx)]; w = bb @ np.linalg.pinv(VV) @ bb; return w, stats.chi2.sf(w, len(idx))
wpre, ppre = wald(pre_i); wpost, ppost = wald(post_i)
print(f"  gemensamt test, {len(pre_i)} kvartal FORE: chi2 {wpre:.2f}, p {ppre:.3f} | {len(post_i)} kvartal EFTER: chi2 {wpost:.2f}, p {ppost:.3f}")
print(f"  medel av koefficienterna fore {b[pre_i].mean():+.2f}, efter {b[post_i].mean():+.2f}")
print("  V2:", "UPPFYLLT" if ppre > 0.05 else "FALLER")

# ---------- V3 ----------
print("\nV3 LATSASBYTE januari 2021 (2019-20 mot 2021-22)")
y = A.t.dt.year; n1 = A[y.isin([2019, 2020])].groupby("SecId").size(); n2 = A[y.isin([2021, 2022])].groupby("SecId").size()
ok = set(n1.index[n1 >= 18]) & set(n2.index[n2 >= 18])
W3 = prep(A[A.SecId.isin(ok)], "2019-01", "2022-12", switch="2021-01"); lo3, hi3 = run(W3, "latsasbyte: Efter(2021) x Dos")
print("  V3:", "UPPFYLLT" if (lo3 < 0 < hi3) else "FALLER")

# ---------- sidotest ----------
print("\nSIDOTEST")
print(" 1. Instrument: utgar (VEV saknas)")
print(" 2. Inom gammal klass"); run(W, "Efter x Dos, Efter x gammal klass-effekter", ["ed"], ("SecId", "tc", "eo"))
print(" 3. Institutionella klasser i samma fonder")
ii = E[E.inst & (E.sida != "UK") & E.FundId.isin(set(B.FundId)) & (E.n_pre >= 18) & (E.n_post >= 18)].index
WI = prep(mk(set(ii), fundlevel=True)); run(WI, "institutionella klasser: Efter x Dos (fondens dos)")
print(" 3b. Rena UK-klasser i samma fonder")
uu = E[(E.sida == "UK") & E.FundId.isin(set(B.FundId)) & (E.n_pre >= 18) & (E.n_post >= 18)].index
WU = prep(mk(set(uu), fundlevel=True)); run(WU, "rena UK-klasser: Efter x Dos (fondens dos)")
WUp = W[W.fundid.isin(set(WU.fundid))]; run(WUp, "KID-klasserna i samma fonder")
print(" 4. Fonster")
run(prep(A, "2022-01", "2023-12"), "12 fore / 12 efter (2022 mot 2023)")
run(prep(A, "2021-01", "2025-12"), "24 fore / 36 efter (till dec 2025)")
print(" 5. Smal dos"); run(prep(A[A.dos_smal.isin([0, 1, 2])], dose="dos_smal"), "bara SRI forsta halvaret 2023")
print(" 6. Bara aktiefonder"); run(W[W.aktie], "aktiefonder"); run(W[~W.aktie], "ovriga fonder (utforskande)")
print(" 7. Kontroller")
Wc = W.copy(); Wc["er12"] = Wc.efter * Wc.ret12_22.fillna(Wc.ret12_22.mean()); Wc["er36"] = Wc.efter * Wc.ret36_22.fillna(Wc.ret36_22.mean())
Wc["er36m"] = Wc.efter * Wc.ret36_22.isna(); sd = []
for k in (1, 2, 4, 5): Wc[f"st{k}"] = (Wc.star_lag == k).astype(float); sd.append(f"st{k}")
Wc["st0"] = Wc.star_lag.isna().astype(float); sd.append("st0")
run(Wc, "med Efter x avkastning 12 och 36 man, stjarndummies", ["ed"] + ES3 + ["er12", "er36", "er36m"] + sd)
print(" 8. Form"); run(prep(A, deg=4), "fjardegradspolynom", ["ed", "es1", "es2", "es3", "es4"])
print(" 9. Bara dos 1 mot 2"); run(W[W.dos.isin([1, 2])], "dos 1 mot 2")
print(" 11. Utan fonder till salu i Sverige"); run(W[~W.sverige], "inte till salu i Sverige")
print(" 12. Alla icke-institutionella klasser")
allc = E[~E.inst & (E.sida != "UK") & (E.n_pre >= 18) & (E.n_post >= 18) & E.srri22.notna() & E.sri_ny.notna() & E.dos.isin([0, 1, 2]) & E.sig.notna() & E["Morningstar Category"].notna()].index
run(prep(mk(set(allc))), "alla klasser, kluster pa fond")
print(" 13. Ingen storleksgrans"); run(prep(mk(set(B.index), fcol="fw_alla")), "NA_t-1 utan 1 MUSD-grans")

# ---------- kollapsad regression och permutation ----------
Bs = B.set_index(B.index)
gg = W.groupby(["SecId", "efter"]).f.mean().unstack(); dd = (gg[1.0] - gg[0.0]) * 12
C = pd.DataFrame({"dd": dd}).join(E[["dos", "sig", "srri22", "Morningstar Category"]]); C["s"] = C.sig / 10; C["s2"] = C.s ** 2; C["s3"] = C.s ** 3
catc = pd.factorize(C["Morningstar Category"])[0]
def within(v): return v - (np.bincount(catc, v) / np.bincount(catc))[catc]
yv = within(C.dd.values); Pm = np.column_stack([within(C[c].values) for c in ["s", "s2", "s3"]])
def coll(dose):
    X = np.column_stack([within(dose), Pm]); XtXi = np.linalg.pinv(X.T @ X); bb = XtXi @ X.T @ yv; e = yv - X @ bb
    Vv = XtXi @ (X.T * e ** 2) @ X @ XtXi * len(yv) / (len(yv) - 4 - catc.max() - 1); return bb[0], np.sqrt(Vv[0, 0])
bc, sc_ = coll(C.dos.values.astype(float))
print("\nKONTROLLRAKNING (kollapsad)")
print(f"  beta {bc:+.2f}  SE {sc_:.2f}  t {bc/sc_:+.2f}  95 % [{bc-1.96*sc_:+.2f}; {bc+1.96*sc_:+.2f}]   (panel: {bmain:+.2f}, SE {semain:.2f})")
print(" 10. Permutationstest (2 000 dragningar inom gammal SRRI)")
rng = np.random.default_rng(20261119); grp = C.srri22.values; dv = C.dos.values.astype(float); idx = [np.where(grp == k)[0] for k in np.unique(grp)]; perm = np.empty(2000)
for r in range(2000):
    d2 = dv.copy()
    for ii_ in idx: d2[ii_] = rng.permutation(dv[ii_])
    perm[r] = coll(d2)[0]
print(f"  faktiskt beta {bc:+.2f} | blandade: medel {perm.mean():+.2f}, std {perm.std():.2f}, 2,5-97,5 % [{np.percentile(perm,2.5):+.2f}; {np.percentile(perm,97.5):+.2f}] | tvasidigt p {np.mean(np.abs(perm) >= abs(bc)):.3f}")

# ---------- verifiering: inplanterad effekt ----------
Wp = W.copy(); Wp["f"] = Wp.f + 3.0 / 12 * Wp.ed
b, se, V, G = est(Wp, "f", ["ed"] + ES3, ["SecId", "tc"])
print(f"\nVERIFIERING: inplanterad +3,00 ger {b[0]:+.3f} (vantat {bmain + 3:+.3f})")
