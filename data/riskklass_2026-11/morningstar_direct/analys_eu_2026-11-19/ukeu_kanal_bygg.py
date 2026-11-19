"""Variabler for kanaltesten (avkastning, kostnader) i UK mot EU. Inga floden anvands.
python3 -I ukeu_kanal_bygg.py <tag>  -> ukeu_kanal_<tag>.pkl (fondniva: P per manad), ukeu_kost_<tag>.pkl"""
import sys, numpy as np, pandas as pd
T = sys.argv[1]; P_ = lambda s: pd.Period(s, "M")
R = pd.read_pickle(f"{T}_raw.pkl").set_index("SecId"); E = pd.read_pickle(f"urval_eu_{T}.pkl"); fm = pd.read_pickle("fx_month.pkl")
# fondens representativa klass: storsta icke-institutionella klass som inte ar ren UK (NA dec 2022)
rep = E[~E.inst & (E.sida != "UK") & E["Morningstar Category"].notna()].sort_values("na_dec22", ascending=False).groupby("FundId").head(1)
per = pd.period_range("2018-01", "2024-12", freq="M")
Ru = pd.DataFrame({p: pd.to_numeric(R.loc[rep.index, f"Monthly Return {p} USD"], errors="coerce") for p in per.astype(str)}, index=rep.index) / 100
def bpu(c):
    if c == "USD": return pd.Series(1.0, index=per)
    if c == "EUR": return 1 / fm["USD"].reindex(per)
    if c in fm: return (fm[c] / fm["USD"]).reindex(per)
    return None
Rb = pd.DataFrame(np.nan, index=Ru.index, columns=Ru.columns)
for c, idx in rep.groupby("cur").groups.items():
    b = bpu(c)
    if b is None: continue
    g = (b / b.shift(1)); g.index = g.index.astype(str)
    Rb.loc[idx] = (1 + Ru.loc[idx]) * g.values - 1
# 12 manaders avkastning t-12..t-1 (det diagrammet ungefar visar), och 36 manader
lg = np.log1p(Rb)
r12 = (lg.T.rolling(12, min_periods=12).sum().T).shift(1, axis=1)
r36 = (lg.T.rolling(36, min_periods=36).sum().T).shift(1, axis=1)
K = pd.DataFrame({"r12": r12.stack(future_stack=True), "r36": r36.stack(future_stack=True)}).reset_index(); K.columns = ["SecId", "t", "r12", "r36"]
K["t"] = pd.PeriodIndex(K.t, freq="M"); K = K[K.t >= P_("2019-01")]
K = K.join(rep[["FundId", "Morningstar Category"]], on="SecId").rename(columns={"FundId": "fundid", "Morningstar Category": "cat"})
for v in ("r12", "r36"):
    K["P" + v[1:]] = K.groupby(["t", "cat"])[v].rank(pct=True)
K.to_pickle(f"ukeu_kanal_{T}.pkl")
print("fonder med P12:", K.dropna(subset=["P12"]).fundid.nunique(), "| fondmanader", K.P12.notna().sum())
# kostnader: nettokostnadskvot ur senaste arsredovisning (dagens), annars lopande avgift, omsattning (dagens) for fondens storsta EU-klass
num = lambda c: pd.to_numeric(R[c].astype(str).str.replace(",", ""), errors="coerce") if c in R else pd.Series(np.nan, index=R.index)
oc = num("Annual Report Net Expense Ratio").fillna(num("Annual Report Ongoing Charge"))
to = pd.to_numeric(R["Turnover Ratio %"].astype(str).str.replace(",", ""), errors="coerce")
C = pd.DataFrame({"oc": oc, "to": to}).join(E[["FundId", "sida", "inst", "na_dec22", "cur"]])
C.to_pickle(f"ukeu_kost_{T}.pkl")
print("kostnadskvot finns:", round(C.oc.notna().mean(), 3), "| omsattning finns:", round(C.to.notna().mean(), 3))
print(C[["oc", "to"]].describe().round(2).to_string())
