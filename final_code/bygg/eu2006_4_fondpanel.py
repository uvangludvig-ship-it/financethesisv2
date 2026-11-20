"""Fondmanadspanel 2002-12..2010-12 for handelsetestet oktober 2006. Som bd_usa_bygg_panel_full.py, bara ra signal.
python3 -I bygg06.py raw06.pkl <faktorer.csv> panel06.pkl"""
import sys, numpy as np, pandas as pd
LAMBDA = 0.20551497
x = pd.read_pickle(sys.argv[1]); R, NA, RET, st = x["R"], x["NA"], x["RET"], x["st"]
ms = list(RET.columns); T = len(ms)
def long(W, nm):
    s = W.stack().dropna()
    s.index.names = ["SecId", "ym"]; return s.rename(nm).reset_index()
PRIO = sys.argv[4]; WL = pd.read_pickle(sys.argv[5])["W"]; WL = WL.where(WL > 0)
if PRIO == "TEST": WL = WL * np.nan; PRIO = "D"
p = long(RET, "r").merge(long(NA, "naD"), on=["SecId", "ym"], how="outer").merge(long(WL, "naL"), on=["SecId", "ym"], how="outer").merge(long(R, "star"), on=["SecId", "ym"], how="outer")
grid = pd.MultiIndex.from_product([RET.index, ms], names=["SecId", "ym"]).to_frame(index=False)
p = grid.merge(p, how="left").sort_values(["SecId", "ym"]).reset_index(drop=True)
p["FundId"] = p.SecId.map(st.FundId)
for k_ in ("D", "L"): p[f"na{k_}_l"] = p.groupby("SecId")[f"na{k_}"].shift(1)
okD = p.naD.notna() & p.naD_l.notna(); okL = p.naL.notna() & p.naL_l.notna()
useD = okD if PRIO == "D" else (okD & ~okL); useL = (okL & ~okD) if PRIO == "D" else okL
first, second = ("naD", "naL") if PRIO == "D" else ("naL", "naD")
p["na"] = p[first].fillna(p[second])                      # vikt for betyget
p["na_l"] = p[first + "_l"].fillna(p[second + "_l"])        # vikt for avkastningen
p["na_f"] = np.where(useD, p.naD, np.where(useL, p.naL, np.nan)); p["na_fl"] = np.where(useD, p.naD_l, np.where(useL, p.naL_l, np.nan))
p["dflow"] = p["na_f"] - p["na_fl"] * (1 + p["r"] / 100); p["kalla"] = np.where(useD, "D", np.where(useL, "L", ""))
print("klassmanader med flode: Direct", int(useD.sum()), "| LSEG", int(useL.sum()))
def wavg(frame, val, wcol):
    q = frame.dropna(subset=[val]).copy(); q["w"] = q[wcol]
    has = q.groupby(["FundId", "ym"])["w"].transform(lambda s: s.notna().any()); q.loc[~has, "w"] = 1.0
    q = q[q["w"].notna() & (q["w"] > 0)]
    g = q.assign(v=q[val] * q["w"]).groupby(["FundId", "ym"]).agg(v=("v", "sum"), w=("w", "sum")).reset_index(); g[val] = g["v"] / g["w"]
    return g[["FundId", "ym", val]]
fr = wavg(p, "r", "na_l").rename(columns={"r": "ret"})
fs = wavg(p, "star", "na").rename(columns={"star": "star_raw"}); fs["star_d"] = np.floor(fs["star_raw"] + 0.5).clip(1, 5)
fl = p.dropna(subset=["dflow"]).groupby(["FundId", "ym"]).agg(dflow=("dflow", "sum"), tna_l=("na_fl", "sum"), andel_lseg=("kalla", lambda z: (z == "L").mean())).reset_index()
fl = fl[fl.tna_l > 0]; fl["flow"] = 100 * fl["dflow"] / fl["tna_l"]
funds = sorted(st.FundId.dropna().unique()); F = len(funds)
f = pd.MultiIndex.from_product([funds, ms], names=["FundId", "ym"]).to_frame(index=False)
f = f.merge(fr, how="left").merge(fl, how="left").merge(fs[["FundId", "ym", "star_d"]], how="left").sort_values(["FundId", "ym"]).reset_index(drop=True)
fk = pd.read_csv(sys.argv[2]); fk["ym"] = fk["yyyymm"].astype(str).str[:4] + "-" + fk["yyyymm"].astype(str).str[4:]; RF = fk.set_index("ym").loc[ms, "RF"].values
retrf = f["ret"].values.reshape(F, T) - RF[None, :]
wts = np.exp(-LAMBDA * np.arange(18)); W = wts.sum()
S = np.zeros_like(retrf); ok = np.ones_like(retrf, dtype=bool)
for s in range(1, 19):
    lag = np.full_like(retrf, np.nan); lag[:, s:] = retrf[:, :-s]; ok &= ~np.isnan(lag); S += wts[s - 1] * np.nan_to_num(lag)
# Fem ars avkastningshistorik (Barber, Huang och Odean 2016, not 8). I det fulla bygget kraver signalen for manad m
# en beta for manad m-17, och den kraver en avkastning 60 manader tidigare: forsta avkastningen senast m-77.
har = ~np.isnan(retrf); forsta = np.where(har.any(axis=1), har.argmax(axis=1), T)
ok &= (np.arange(T)[None, :] - forsta[:, None]) >= 77
sig = S / W; sig[~ok] = np.nan; f["unad_a"] = sig.reshape(-1)
st2 = st.copy(); st2["inc"] = pd.to_datetime(st2["Inception Date"], errors="coerce"); st2["idx"] = st2["Index Fund"].eq("Yes")
sf = st2.groupby("FundId").agg(inc=("inc", "min"), cat=("Morningstar Category", "first"), index=("idx", "any"))
f = f.merge(sf, left_on="FundId", right_index=True, how="left")
f["age"] = (pd.to_datetime(f["ym"] + "-01") + pd.offsets.MonthEnd(0) - f["inc"]).dt.days / 365.25
f[["FundId", "ym", "star_d"]].to_pickle(sys.argv[3].replace(".pkl", "_betyg.pkl"))
steps = [("flode finns", f["flow"].notna()), ("formogenhet >= 10 MUSD", f["tna_l"] >= 10e6), ("ra signal", f["unad_a"].notna()), ("kategori", f["cat"].notna()), ("ej indexfond", ~f["index"].fillna(False).astype(bool)), ("betyg (kodens tidpunkt)", f["star_d"].notna())]
mask = (f["ym"] >= "2003-01") & (f["ym"] <= "2016-12"); print("Urvalskedja (fondmanader 2003-01..2016-12):")
for nm, m_ in steps:
    mask &= m_; print(f"  {nm:26s} {int(mask.sum()):>8d}  fonder {f.loc[mask, 'FundId'].nunique()}")
sm = f[mask].copy(); sm["size"] = sm["tna_l"] / 1e6
def wins(z):
    lo, hi = z.quantile([0.01, 0.99]); return z.clip(lo, hi)
for c in ["flow", "unad_a", "size"]: sm[c] = sm.groupby("ym")[c].transform(wins)
sm = sm.reset_index(drop=True); sm.to_pickle(sys.argv[3])
n = sm.groupby("ym").FundId.nunique(); print("fonder per manad:", {k: int(v) for k, v in n.items() if k[5:] in ("06", "12")})
print("flode medel %.2f, tvarsnittsspridning (medel av manadsvisa sd) %.2f" % (sm.flow.mean(), sm.groupby("ym").flow.std().mean()))
