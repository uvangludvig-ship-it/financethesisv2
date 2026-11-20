"""Fond-manadspanel for Ben-David-replikeringen och hastkapplopningen pa EU-basdatan (LU+IE).
Samma konstruktion som claude/bd_usa_bygg_panel_full.py (USA), med:
  klasser: Morningstar Category Group = Equity och sida enligt argument (EU = saljs i EES, inte i UK; kid = alla utom rena UK)
  faktorer: Fama-French Developed (huvud) och Europe (variant), USD; RF ur respektive fil
  visad riskklass: SRRI i kraft (Surveyed KIID SRRI History) till och med dec 2022, SRI Value fran jan 2023 (senaste varde, hogst 12 man gammalt)
python3 -I bd_eu_bygg.py <tag> <sida: EU|kid> <faktorkatalog> <ut.pkl>"""
import sys, re, numpy as np, pandas as pd
T, SIDA, FK, OUT = sys.argv[1:5]
LAMBDA = 0.20551497
R0 = pd.read_pickle(f"{T}_raw.pkl").set_index("SecId"); E = pd.read_pickle(f"urval_eu_{T}.pkl")
keep = (R0["Morningstar Category Group"] == "Equity") & (E.sida.reindex(R0.index) == "EU" if SIDA == "EU" else E.sida.reindex(R0.index) != "UK")
R0 = R0[keep]; cls = R0.index; fund = R0.FundId.values
months = pd.period_range("2013-01", "2025-12", freq="M"); ms = months.astype(str); Tn = len(ms)
num = lambda c: pd.to_numeric(R0[c].astype(str).str.replace(",", ""), errors="coerce") if c in R0 else pd.Series(np.nan, index=cls)
Rm = np.column_stack([num(f"Monthly Return {m} USD") for m in ms]) / 100
NA = np.column_stack([num(f"Net Assets - share class (Monthly) {m} USD") for m in ms])
ST = np.column_stack([num(f"Morningstar Rating Overall {m}") for m in ms])
# visad riskklass per klass och manad
hist = R0["Surveyed KIID SRRI History"]
mend = pd.PeriodIndex(ms, freq="M").to_timestamp(how="end").strftime("%Y-%m-%d").values
LAB = np.full((len(cls), Tn), np.nan)
for i, s in enumerate(hist.values):
    if not isinstance(s, str): continue
    ent = sorted(re.findall(r"\[(\d{4}-\d{2}-\d{2})\]\s*(\d)", s))
    if not ent: continue
    d = np.array([e[0] for e in ent]); v = np.array([int(e[1]) for e in ent], float)
    k = np.searchsorted(d, mend, side="right") - 1
    LAB[i] = np.where(k >= 0, v[np.clip(k, 0, None)], np.nan)
sri = np.column_stack([num(f"SRI Value {m}") if f"SRI Value {m}" in R0 else pd.Series(np.nan, index=cls) for m in ms])
sri_ff = pd.DataFrame(sri).T.ffill(limit=11).T.values
j23 = list(ms).index("2023-01"); LAB[:, j23:] = sri_ff[:, j23:]

# fondaggregat
fc, fu = pd.factorize(fund); F = len(fu)
def fsum(X):
    out = np.zeros((F, Tn)); np.add.at(out, fc, np.nan_to_num(X)); return out
na_l = np.full_like(NA, np.nan); na_l[:, 1:] = NA[:, :-1]
dflow = NA - na_l * (1 + Rm)
okf = np.isfinite(dflow) & (na_l > 0)
TNA_l = fsum(np.where(okf, na_l, 0)); DF = fsum(np.where(okf, dflow, 0))
flow = np.where(TNA_l > 0, 100 * DF / TNA_l, np.nan); flow_usd = np.where(TNA_l > 0, DF / 1e6, np.nan)
okr = np.isfinite(Rm) & (na_l > 0); W = fsum(np.where(okr, na_l, 0))
ret = np.where(W > 0, fsum(np.where(okr, Rm * na_l, 0)) / np.where(W > 0, W, 1), np.nan)
okr2 = np.isfinite(Rm); n2 = fsum(okr2.astype(float)); ret_ew = np.where(n2 > 0, fsum(np.where(okr2, Rm, 0)) / np.where(n2 > 0, n2, 1), np.nan)
ret = np.where(np.isfinite(ret), ret, ret_ew) * 100
oks = np.isfinite(ST) & (NA > 0); Ws = fsum(np.where(oks, NA, 0))
star = np.where(Ws > 0, fsum(np.where(oks, ST * NA, 0)) / np.where(Ws > 0, Ws, 1), np.nan)
oks2 = np.isfinite(ST); ns2 = fsum(oks2.astype(float))
star = np.where(np.isfinite(star), star, np.where(ns2 > 0, fsum(np.where(oks2, ST, 0)) / np.where(ns2 > 0, ns2, 1), np.nan))
star_d = np.where(np.isfinite(star), np.clip(np.floor(star + 0.5), 1, 5), np.nan)
# riskklass: klassen med storst NA_{t-1} bland klasser med etikett (annars storst NA_t)
wl = np.where(np.isfinite(LAB), np.nan_to_num(na_l, nan=-1), -np.inf)
lab = np.full((F, Tn), np.nan); best = np.full((F, Tn), -np.inf)
for i in range(len(cls)):
    m = wl[i] > best[fc[i]]; best[fc[i], m] = wl[i, m]; lab[fc[i], m] = LAB[i, m]

def fac(fn3, fnm):
    def rd(fn):
        rows = []
        for ln in open(fn, encoding="latin-1"):
            p = [x.strip() for x in ln.split(",")]
            if len(p) > 1 and re.fullmatch(r"\d{6}", p[0]): rows.append(p)
            elif rows and not ln.strip(): break
        return rows
    a = rd(fn3); df3 = pd.DataFrame(a, columns=["ym", "Mkt-RF", "SMB", "HML", "RF"]).set_index("ym").astype(float)
    b = rd(fnm); dfm = pd.DataFrame(b, columns=["ym", "Mom"]).set_index("ym").astype(float)
    x = df3.join(dfm); x.index = [i[:4] + "-" + i[4:] for i in x.index]; return x.reindex(ms)
FAKT = {"dev": fac(f"{FK}/Developed_3_Factors.csv", f"{FK}/Developed_MOM_Factor.csv"), "eur": fac(f"{FK}/Europe_3_Factors.csv", f"{FK}/Europe_MOM_Factor.csv")}
assert FAKT["dev"].notna().all().all(), FAKT["dev"].isna().sum()

def rolling_betas(Y, M, Xf):
    X = np.column_stack([np.ones(Tn), Xf]); k = X.shape[1]
    xx = np.einsum("ti,tj->tij", X, X)
    Cxx = np.cumsum(M[:, :, None, None] * xx[None], axis=1); Cxy = np.cumsum((Y * M)[:, :, None] * X[None], axis=1); Cn = np.cumsum(M, axis=1)
    win = lambda C, t: (C[:, t - 1] if t >= 1 else 0) - (C[:, t - 61] if t - 61 >= 0 else 0)
    B = np.full((F, Tn, k - 1), np.nan)
    forsta = np.where(M.any(axis=1), M.argmax(axis=1), Tn)      # fondens forsta manad med avkastning
    for t in range(1, Tn):
        # fem ars avkastningshistorik (Barber, Huang och Odean 2016, not 8) och minst 36 observationer (ankarets kod, min_mm)
        n = win(Cn, t); ok = (n >= 36) & (forsta <= t - 60)
        if not ok.any(): continue
        Sxx = win(Cxx, t)[ok]; Sxy = win(Cxy, t)[ok]
        try: b = np.linalg.solve(Sxx, Sxy[..., None])[..., 0]
        except np.linalg.LinAlgError: b = np.stack([np.linalg.lstsq(Sxx[i], Sxy[i], rcond=None)[0] for i in range(len(Sxx))])
        B[ok, t, :] = b[:, 1:]
    return B
wts = np.exp(-LAMBDA * np.arange(18)); Wt = wts.sum()
def cumul18(x):
    S = np.zeros_like(x); ok = np.ones_like(x, dtype=bool)
    for s in range(1, 19):
        lag = np.full_like(x, np.nan); lag[:, s:] = x[:, :-s]; ok &= ~np.isnan(lag); S += wts[s - 1] * np.nan_to_num(lag)
    o = S / Wt; o[~ok] = np.nan; return o
sig = {}
for nm, fk in FAKT.items():
    RF = fk.RF.values; MKT = fk["Mkt-RF"].values; retrf = ret - RF[None, :]; M = ~np.isnan(retrf); Y = np.where(M, retrf, 0.0)
    if nm == "dev": sig["unad_a"] = cumul18(retrf); sig["retexmkt_a"] = cumul18(retrf - MKT[None, :])
    for m, cols in {"capm": ["Mkt-RF"], "ff3": ["Mkt-RF", "SMB", "HML"], "carh": ["Mkt-RF", "SMB", "HML", "Mom"]}.items():
        Xf = fk[cols].values; B = rolling_betas(Y, M, Xf); Bn = np.full_like(B, np.nan); Bn[:, :-1] = B[:, 1:]
        a = retrf - np.einsum("ftk,tk->ft", Bn, Xf); sig[f"{m}_a" if nm == "dev" else f"{m}_eur_a"] = cumul18(a)
idx = pd.MultiIndex.from_product([fu, ms], names=["FundId", "ym"])
f = pd.DataFrame({"ret": ret.ravel(), "flow": flow.ravel(), "flow_usd": flow_usd.ravel(), "tna_l": TNA_l.ravel(), "star_d": star_d.ravel(), "lab": lab.ravel(),
                  **{k: v.ravel() for k, v in sig.items()}}, index=idx).reset_index()
f.loc[f.tna_l <= 0, "tna_l"] = np.nan
g = f.groupby("FundId"); f["star_c"] = f.star_d; f["star_l"] = g.star_d.shift(1); f["lab_l"] = g.lab.shift(1)
f["flow_l19"] = g.flow.shift(19); f["sd60"] = g.ret.transform(lambda z: z.shift(1).rolling(60, min_periods=36).std())
st = pd.DataFrame({"FundId": R0.FundId, "inc": pd.to_datetime(R0["Inception Date"], errors="coerce"),
                   "exp": num("Annual Report Net Expense Ratio"), "idx": R0["Index Fund"].eq("Yes"), "cat": R0["Morningstar Category"]})
st["idx_known"] = R0["Index Fund"].isin(["Yes", "No"]) if "Index Fund" in R0 else False
st["idx_name"] = R0["Name"].astype(str).str.contains(r"\bIndex\b|Tracker|\bETF\b|Passive", case=False, regex=True)
sf = st.groupby("FundId").agg(inc=("inc", "min"), exp=("exp", "mean"), cat=("cat", "first"), index=("idx", "any"), known=("idx_known", "any"), iname=("idx_name", "any"))
sf["index"] = np.where(sf.known, sf["index"], sf.iname)  # flaggan saknas (B2): namnregel
print("fonder utan indexflagga (namnregel):", int((~sf.known).sum()), "| varav index enligt namn:", int((~sf.known & sf.iname).sum()))
f = f.merge(sf, left_on="FundId", right_index=True, how="left"); f["age"] = (pd.to_datetime(f.ym + "-01") - f.inc).dt.days / 365.25
f[["FundId", "ym", "lab", "star_d"]].to_pickle(OUT.replace(".pkl", "_etikett.pkl"))
s0 = f[(f.ym >= "2018-01") & (f.ym <= "2025-12")]
steps = [("flode finns", s0.flow.notna()), ("formogenhet >= 10 MUSD", s0.tna_l >= 10e6), ("alla fyra signaler", s0[["unad_a", "capm_a", "ff3_a", "carh_a"]].notna().all(axis=1)),
         ("kategori", s0.cat.notna()), ("ej indexfond", ~s0["index"].fillna(False).astype(bool)), ("betyg (kodens tidpunkt)", s0.star_c.notna())]
mask = pd.Series(True, index=s0.index); print(f"Klasser {len(cls)}, fonder {F}. Urvalskedja (fondmanader 2018-2025):")
for nm, m_ in steps:
    mask &= m_; print(f"  {nm:26s} {int(mask.sum()):>8d}  fonder {s0.loc[mask, 'FundId'].nunique()}")
vmask = pd.Series(True, index=s0.index)
for nm, m_ in steps[:-1]: vmask &= m_
vmask &= s0.star_l.notna()
print("  variant, betyg t-1:", int(vmask.sum()), "| med visad riskklass (kod):", int((mask & s0.lab.notna()).sum()))
sm = s0[mask | vmask].copy(); sm["in_kod"] = mask[mask | vmask].values; sm["in_var"] = vmask[mask | vmask].values
sm["pos"] = (sm.flow > 0).astype(float); sm["size"] = sm.tna_l / 1e6
def wins(x):
    lo, hi = x.quantile([0.01, 0.99]); return x.clip(lo, hi)
for c in ["flow", "flow_usd", "size", "age", "unad_a", "retexmkt_a", "capm_a", "ff3_a", "carh_a", "capm_eur_a", "ff3_eur_a", "carh_eur_a", "flow_l19", "sd60", "exp"]:
    sm[c] = sm.groupby("ym")[c].transform(wins)
sm = sm.reset_index(drop=True); sm.to_pickle(OUT)
print("riskklass i urvalet (kod), fordelning:", sm[sm.in_kod].lab.value_counts().sort_index().to_dict())
print("sparat", OUT, sm.shape)
