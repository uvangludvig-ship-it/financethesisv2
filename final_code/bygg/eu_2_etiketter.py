"""Etiketter och volatilitet for sicksacken pa EU-basdatan. Anvander inga floden.
python3 -I bygg_etiketter_eu.py <a1_raw.pkl> <fx_month.pkl>"""
import sys, re, numpy as np, pandas as pd

D = pd.read_pickle(sys.argv[1]); fm = pd.read_pickle(sys.argv[2])
D = D[D.SecId.astype(str).str.match(r"^F[0-9A-Z]{9}$")].copy().set_index("SecId")
CUR = {"Euro": "EUR", "US Dollar": "USD", "Pound Sterling": "GBP", "Swiss Franc": "CHF", "Singapore Dollar": "SGD",
       "Yen": "JPY", "Australian Dollar": "AUD", "Swedish Krona": "SEK", "Hong Kong Dollar": "HKD",
       "Norwegian Krone": "NOK", "Zloty": "PLN", "Canadian Dollar": "CAD", "Rand": "ZAR", "Czech Koruna": "CZK",
       "Offshore Chinese Yuan": "CNY", "Danish Krone": "DKK", "Hungarian Forint": "HUF", "New Zealand Dollar": "NZD"}
D["cur"] = D["Base Currency"].map(CUR)

# SRRI i kraft vid utgangen av 2022 (senaste posten under 2022)
def srri_at(s, start="2022-01-01", end="2022-12-31"):
    if not isinstance(s, str): return np.nan
    ok = [(d, int(v)) for d, v in re.findall(r"\[(\d{4}-\d{2}-\d{2})\]\s*(\d)", s) if start <= d <= end]
    return ok[-1][1] if ok else np.nan
D["srri22"] = D["Surveyed KIID SRRI History"].map(srri_at)

# SRI: forsta varde jan-jun 2023, annars sista jul-dec 2022 (bred dos)
mon = pd.period_range("2018-01", "2025-12", freq="M").astype(str)
S = pd.DataFrame({m: pd.to_numeric(D[f"SRI Value {m}"], errors="coerce") for m in mon}, index=D.index)
D["sri23"] = S.loc[:, "2023-01":"2023-06"].bfill(axis=1).iloc[:, 0]
D["sri_h2_22"] = S.loc[:, "2022-07":"2022-12"].ffill(axis=1).iloc[:, -1]
D["sri_ny"] = D.sri23.fillna(D.sri_h2_22)
D["dos"] = D.srri22 - D.sri_ny          # bred dos (huvud)
D["dos_smal"] = D.srri22 - D.sri23

# Volatilitet: manadsavkastning i basvaluta 2018-01..2022-12 (USD-avkastning omraknad med ECB)
rm = pd.period_range("2017-12", "2022-12", freq="M")
R = pd.DataFrame({p: pd.to_numeric(D[f"Monthly Return {p} USD"], errors="coerce") for p in rm[1:].astype(str)}, index=D.index) / 100
fxm = fm.reindex(rm)
def base_per_usd(c):
    if c == "USD": return pd.Series(1.0, index=rm)
    if c == "EUR": return 1 / fxm["USD"]
    if c in fxm: return fxm[c] / fxm["USD"]
    return None
sig = pd.Series(np.nan, index=D.index); sig_usd = R.std(axis=1).where(R.notna().sum(axis=1) >= 48) * np.sqrt(12) * 100
for c, idx in D.groupby("cur").groups.items():
    b = base_per_usd(c)
    if b is None: continue
    g = (b / b.shift(1)).iloc[1:]; g.index = g.index.astype(str)
    Rb = (1 + R.loc[idx, g.index]) * g.values - 1
    sig.loc[idx] = Rb.std(axis=1).where(Rb.notna().sum(axis=1) >= 48) * np.sqrt(12) * 100
D["sig"] = sig; D["sig_usd"] = sig_usd
D["srri_f"] = pd.cut(D.sig, [-1, .5, 2, 5, 10, 15, 25, 1e9], right=False, labels=False) + 1

cols = ["FundId", "Name", "Inception Date", "cur", "Domicile", "Institutional", "Index Fund", "Morningstar Category", "Country Available for Sale",
        "srri22", "sri23", "sri_h2_22", "sri_ny", "dos", "dos_smal", "sig", "sig_usd", "srri_f"]
D[cols].to_pickle(sys.argv[3] if len(sys.argv) > 3 else "etiketter_eu_a1.pkl")
print("klasser", len(D), "| srri22", D.srri22.notna().sum(), "| sri_ny", D.sri_ny.notna().sum(), "| sig", D.sig.notna().sum())
m = D.srri22.notna() & D.srri_f.notna()
print("SRRI-klass ur sig i basvaluta = visad SRRI 2022:", round((D.srri_f == D.srri22)[m].mean(), 3), "inom ett steg:", round(((D.srri_f - D.srri22).abs() <= 1)[m].mean(), 3))
f_usd = pd.cut(D.sig_usd, [-1, .5, 2, 5, 10, 15, 25, 1e9], right=False, labels=False) + 1
print("samma med USD-sigma:", round((f_usd == D.srri22)[m].mean(), 3))
