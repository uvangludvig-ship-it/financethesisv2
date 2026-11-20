"""Klassmanadspanel for sicksacken pa EU-basdatan.
python3 -I bygg_panel_eu.py <a1_raw.pkl> <etiketter_eu_a1.pkl>  -> panel_eu_a1.pkl, urval_eu_a1.pkl
Skriver inga flodesvarden till skarmen."""
import sys, re, numpy as np, pandas as pd

D = pd.read_pickle(sys.argv[1]); E = pd.read_pickle(sys.argv[2]); TAG = sys.argv[3] if len(sys.argv) > 3 else "a1"
D = D[D.SecId.astype(str).str.match(r"^F[0-9A-Z]{9}$")].set_index("SecId")
EEA = set("Austria Belgium Bulgaria Croatia Cyprus Czechia Denmark Estonia Finland France Germany Greece Hungary Ireland Italy "
          "Latvia Lithuania Luxembourg Malta Netherlands Poland Portugal Romania Slovakia Slovenia Spain Sweden Iceland Norway Liechtenstein".split())
av = E["Country Available for Sale"].fillna("").str.split(";").apply(lambda l: {x.strip() for x in l if x.strip()})
uk = av.apply(lambda s: "United Kingdom" in s)
n_eea = pd.Series([len(s & (EEA - {d})) for s, d in zip(av, E.Domicile.fillna(""))], index=E.index)
E["sida"] = np.where(uk & (n_eea == 0), "UK", np.where(~uk & (n_eea > 0), "EU", np.where(uk, "bada", "ingen")))
E["sverige"] = av.apply(lambda s: "Sweden" in s)
E["inst"] = E.Institutional.eq("Yes")

per = pd.period_range("2018-12", "2025-12", freq="M")
NA = pd.DataFrame({p: pd.to_numeric(D[f"Net Assets - share class (Monthly) {p} USD"].astype(str).str.replace(",", ""), errors="coerce") for p in per.astype(str)}, index=D.index)
R = pd.DataFrame({p: pd.to_numeric(D[f"Monthly Return {p} USD"].astype(str).str.replace(",", ""), errors="coerce") for p in per.astype(str)}, index=D.index) / 100
ST = pd.DataFrame({p: pd.to_numeric(D.get(f"Morningstar Rating Overall {p}"), errors="coerce") for p in per.astype(str)}, index=D.index)
lagNA = NA.shift(1, axis=1)
F = (NA - lagNA * (1 + R)) / lagNA
F = F.where(lagNA > 0)
L = pd.DataFrame({"f": F.stack(future_stack=True), "na_lag": lagNA.stack(future_stack=True), "star_lag": ST.shift(1, axis=1).stack(future_stack=True)})
L = L.dropna(subset=["f"]).reset_index(); L.columns = ["SecId", "t", "f", "na_lag", "star_lag"]
L["t"] = pd.PeriodIndex(L.t, freq="M"); L = L[L.t >= pd.Period("2019-01", "M")]
L["stor"] = L.na_lag >= 1e6
# winsorisering 1/99 inom manad, separat for huvudregeln (na_lag >= 1 MUSD) och utan storleksgrans
for nm, m in [("fw", L.stor), ("fw_alla", pd.Series(True, index=L.index))]:
    q = L[m].groupby("t").f.quantile([.01, .99]).unstack()
    lo = L.t.map(q[.01]); hi = L.t.map(q[.99])
    L[nm] = np.where(m, L.f.clip(lo, hi), np.nan)
L = L.join(E[["FundId", "Morningstar Category", "sida", "sverige", "inst"]], on="SecId").rename(columns={"FundId": "fundid", "Morningstar Category": "cat"})
L.to_pickle(f"panel_eu_{TAG}.pkl")

# antal flodesmanader per period (bara tillganglighet, inga varden)
Ls = L[L.stor]
y = Ls.t.dt.year
n_pre = Ls[y.isin([2021, 2022])].groupby("SecId").size(); n_post = Ls[y.isin([2023, 2024])].groupby("SecId").size()
E["n_pre"] = n_pre.reindex(E.index).fillna(0); E["n_post"] = n_post.reindex(E.index).fillna(0)
E["na_dec22"] = NA["2022-12"]
E.to_pickle(f"urval_eu_{TAG}.pkl")
print("panel", len(L), "klassmanader;", L.SecId.nunique(), "klasser")
