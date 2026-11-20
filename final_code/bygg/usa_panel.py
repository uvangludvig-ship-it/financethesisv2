"""Fond-månadspanel 1991–2011 med Ben-Davids signaler (rå, marknadsjusterad, CAPM, FF3, FFC).
Specifikation: claude/DEKLARATION_replikering_bendavid_usa_1997_2011_2026-11-18.md
Användning: python3 -I bygg_panel_full.py <export.csv> <faktorer.csv> <ut.pkl>
"""
import sys, re
import numpy as np
import pandas as pd

LAMBDA = 0.20551497
src, fakt, out = sys.argv[1], sys.argv[2], sys.argv[3]

df = pd.read_csv(src, encoding="latin-1", low_memory=False, dtype=str)
df.columns = [re.sub(r"\s+", " ", c.replace("\n", " ")).strip() for c in df.columns]
df = df[df["Morningstar Category Group"].eq("Equity")].copy()

def long(prefix, name):
    cs = [c for c in df.columns if c.startswith(prefix) and re.search(r"\d{4}-\d{2}", c)]
    x = df[["SecId", "FundId"] + cs].melt(id_vars=["SecId", "FundId"], var_name="c", value_name=name)
    x["ym"] = x["c"].str.extract(r"(\d{4}-\d{2})")[0]
    x[name] = pd.to_numeric(x[name].str.replace(",", ""), errors="coerce")
    return x.drop(columns="c")

p = long("Monthly Return", "r").merge(long("Net Assets - share class (Monthly)", "na"), on=["SecId", "FundId", "ym"], how="left") \
    .merge(long("Morningstar Rating Overall", "star"), on=["SecId", "FundId", "ym"], how="left")
p = p.sort_values(["SecId", "ym"]).reset_index(drop=True)
p["na_l"] = p.groupby("SecId")["na"].shift(1)
p["dflow"] = p["na"] - p["na_l"] * (1 + p["r"] / 100)

def wavg(frame, val, wcol):
    q = frame.dropna(subset=[val]).copy()
    q["w"] = q[wcol]
    has = q.groupby(["FundId", "ym"])["w"].transform(lambda s: s.notna().any())
    q.loc[~has, "w"] = 1.0
    q = q[q["w"].notna() & (q["w"] > 0)]
    g = q.assign(v=q[val] * q["w"]).groupby(["FundId", "ym"]).agg(v=("v", "sum"), w=("w", "sum")).reset_index()
    g[val] = g["v"] / g["w"]
    return g[["FundId", "ym", val]]

fr = wavg(p, "r", "na_l").rename(columns={"r": "ret"})
fs = wavg(p, "star", "na").rename(columns={"star": "star_raw"})
fs["star_d"] = np.floor(fs["star_raw"] + 0.5).clip(1, 5)
fl = p.dropna(subset=["dflow"]).groupby(["FundId", "ym"]).agg(dflow=("dflow", "sum"), tna_l=("na_l", "sum")).reset_index()
fl["flow"] = 100 * fl["dflow"] / fl["tna_l"]
fl["flow_usd"] = fl["dflow"] / 1e6

months = sorted(p["ym"].unique()); T = len(months)
funds = sorted(df["FundId"].unique()); F = len(funds)
grid = pd.MultiIndex.from_product([funds, months], names=["FundId", "ym"]).to_frame(index=False)
f = grid.merge(fr, how="left").merge(fl, how="left").merge(fs[["FundId", "ym", "star_d"]], how="left")
f = f.sort_values(["FundId", "ym"]).reset_index(drop=True)

# Faktorer
fk = pd.read_csv(fakt)
fk["ym"] = fk["yyyymm"].astype(str).str[:4] + "-" + fk["yyyymm"].astype(str).str[4:]
fk = fk.set_index("ym").loc[months]
RF = fk["RF"].values; MKT = fk["Mkt-RF"].values
FAC = {"capm": fk[["Mkt-RF"]].values, "ff3": fk[["Mkt-RF", "SMB", "HML"]].values, "carh": fk[["Mkt-RF", "SMB", "HML", "Mom"]].values}

ret = f["ret"].values.reshape(F, T)
retrf = ret - RF[None, :]
M = ~np.isnan(retrf)
Y = np.where(M, retrf, 0.0)

def rolling_betas(Xf):
    """Betor för rad t ur fönstret t-60..t-1. Två krav:
    (1) fonden har fem års avkastningshistorik, det vill säga en avkastning i månad t-60 eller tidigare
        (Barber, Huang och Odean 2016, not 8: "we require a five-year history of fund returns for inclusion");
    (2) minst 36 observationer i fönstret (ankarets kod: "if obs_used ge &min_mm", min_mm = 36).
    Returnerar F x T x k (lutningar, utan konstant)."""
    X = np.column_stack([np.ones(T), Xf])  # T x k
    k = X.shape[1]
    xx = np.einsum("ti,tj->tij", X, X)      # T x k x k
    xy_base = X                               # T x k
    Cxx = np.cumsum(M[:, :, None, None] * xx[None], axis=1)        # F x T x k x k
    Cxy = np.cumsum((Y * M)[:, :, None] * xy_base[None], axis=1)   # F x T x k
    Cn = np.cumsum(M, axis=1)
    def win(C, t):
        a = C[:, t - 1] if t - 1 >= 0 else 0
        b = C[:, t - 61] if t - 61 >= 0 else 0
        return a - b
    B = np.full((F, T, k - 1), np.nan)
    forsta = np.where(M.any(axis=1), M.argmax(axis=1), T)      # fondens första månad med avkastning
    for t in range(1, T):
        n = win(Cn, t)
        ok = (n >= 36) & (forsta <= t - 60)
        if not ok.any():
            continue
        Sxx = win(Cxx, t)[ok]; Sxy = win(Cxy, t)[ok]
        try:
            b = np.linalg.solve(Sxx, Sxy[..., None])[..., 0]
        except np.linalg.LinAlgError:
            b = np.stack([np.linalg.lstsq(Sxx[i], Sxy[i], rcond=None)[0] for i in range(len(Sxx))])
        B[ok, t, :] = b[:, 1:]
    return B

wts = np.exp(-LAMBDA * np.arange(18)); W = wts.sum()
def cumul18(x):
    """Signal för flödesmånad t: viktat medel av x(t-1)..x(t-18); alla måste finnas."""
    S = np.zeros_like(x); ok = np.ones_like(x, dtype=bool)
    for s in range(1, 19):
        lag = np.full_like(x, np.nan); lag[:, s:] = x[:, :-s]
        ok &= ~np.isnan(lag); S += wts[s - 1] * np.nan_to_num(lag)
    out_ = S / W; out_[~ok] = np.nan
    return out_

sig = {"unad_a": cumul18(retrf), "retexmkt_a": cumul18(retrf - MKT[None, :])}
for m, Xf in FAC.items():
    B = rolling_betas(Xf)
    # alfa för månad tau använder betan i rad tau+1 (fönster tau-59..tau), som i koden
    Bn = np.full_like(B, np.nan); Bn[:, :-1] = B[:, 1:]
    a = retrf - np.einsum("ftk,tk->ft", Bn, Xf)
    sig[f"{m}_a"] = cumul18(a)
    print(m, "alfor med värde:", int(np.isfinite(a).sum()))
for k, v in sig.items():
    f[k] = v.reshape(-1)

g = f.groupby("FundId")
f["star_c"] = f["star_d"]                 # kodens tidpunkt: betyg per slutet av t
f["star_l"] = g["star_d"].shift(1)        # variant: betyg per slutet av t-1
f["flow_l19"] = g["flow"].shift(19)
f["sd60"] = g["ret"].transform(lambda z: z.shift(1).rolling(60, min_periods=36).std())

st = df[["SecId", "FundId", "Morningstar Category", "Inception Date", "Annual Report Net Expense Ratio", "Index Fund"]].copy()
st["inc"] = pd.to_datetime(st["Inception Date"], errors="coerce")
st["exp"] = pd.to_numeric(st["Annual Report Net Expense Ratio"], errors="coerce")
st["idx"] = st["Index Fund"].eq("Yes")
sf = st.groupby("FundId").agg(inc=("inc", "min"), exp=("exp", "mean"), cat=("Morningstar Category", "first"), index=("idx", "any"))
f = f.merge(sf, left_on="FundId", right_index=True, how="left")
f["age"] = (pd.to_datetime(f["ym"] + "-01") - f["inc"]).dt.days / 365.25

s0 = f[(f["ym"] >= "1997-07") & (f["ym"] <= "2011-12")]
steps = [("flöde finns", s0["flow"].notna()), ("förmögenhet >= 10 MUSD", s0["tna_l"] >= 10e6),
         ("alla fyra signaler", s0[["unad_a", "capm_a", "ff3_a", "carh_a"]].notna().all(axis=1)),
         ("kategori", s0["cat"].notna()), ("ej indexfond", ~s0["index"].fillna(False)),
         ("betyg (kodens tidpunkt)", s0["star_c"].notna())]
mask = pd.Series(True, index=s0.index)
print("Urvalskedja (fondmånader):")
for nm, m_ in steps:
    mask &= m_
    print(f"  {nm:26s} {int(mask.sum()):>8d}  fonder {s0.loc[mask, 'FundId'].nunique()}")
base_mask = mask.copy()
# Variantens urval: samma filter men betyget per t-1
vmask = pd.Series(True, index=s0.index)
for nm, m_ in steps[:-1]:
    vmask &= m_
vmask &= s0["star_l"].notna()
print("  variant, betyg t-1:", int(vmask.sum()))
sm = s0[base_mask | vmask].copy()
sm["in_kod"] = base_mask[base_mask | vmask].values
sm["in_var"] = vmask[base_mask | vmask].values
sm["pos"] = (sm["flow"] > 0).astype(float)
sm["size"] = sm["tna_l"] / 1e6
def wins(x):
    lo, hi = x.quantile([0.01, 0.99]); return x.clip(lo, hi)
for c in ["flow", "flow_usd", "size", "age", "unad_a", "retexmkt_a", "capm_a", "ff3_a", "carh_a", "flow_l19", "sd60", "exp"]:
    sm[c] = sm.groupby("ym")[c].transform(wins)
sm = sm.reset_index(drop=True)
sm.to_pickle(out)
f[["FundId", "ym", "star_d"]].to_pickle(out.replace(".pkl", "_betyg.pkl"))
print("sparat", out, sm.shape)
