import sys, pandas as pd, re, numpy as np
d = pd.read_csv(sys.argv[1], low_memory=False, encoding='utf-8-sig')
d.columns = [re.sub(r'\s+', ' ', c).strip() for c in d.columns]
print("rader totalt", len(d))
print("sista rader Name:", d.Name.tail(8).tolist())
d = d[d.SecId.astype(str).str.match(r"^F[0-9A-Z]{9}$")].copy()
print("klasser", len(d), "unika", d.SecId.nunique(), "fonder", d.FundId.nunique())
for c in ["Domicile", "Morningstar Category Group", "Investment Type", "Institutional", "Index Fund"]:
    print("\n", c, d[c].value_counts(dropna=False).head(6).to_dict())
inc = pd.to_datetime(d["Inception Date"], errors="coerce"); obs = pd.to_datetime(d["Obsolete Date"], errors="coerce")
print("\nInception:", inc.min(), inc.max(), "saknas", inc.isna().sum())
print(inc.dt.year.clip(lower=1995).value_counts().sort_index().to_dict())
print("Obsolete saknas", obs.isna().sum(), "min", obs.min(), "max", obs.max(), "fore 2003:", (obs < "2003-01-01").sum())
print(obs.dt.year.value_counts().sort_index().to_dict())
def ser(prefix):
    cols = [c for c in d.columns if c.startswith(prefix) and re.search(r'\d{4}-\d{2}', c)]
    m = {c: re.search(r'\d{4}-\d{2}', c).group(0) for c in cols}
    x = d.set_index("SecId")[cols].rename(columns=m); x = x[sorted(x.columns)]
    return x.apply(lambda s: pd.to_numeric(s.astype(str).str.replace(",", ""), errors="coerce"))
R = ser("Morningstar Rating Overall "); NA = ser("Net Assets - share class (Monthly)"); FL = ser("Estimated Share Class Net Flow"); RET = ser("Monthly Return"); FS = ser("Fund Size - comprehensive")
pd.to_pickle({"R": R, "NA": NA, "FL": FL, "RET": RET, "FS": FS, "st": d.set_index("SecId")[["FundId", "Name", "Domicile", "Inception Date", "Obsolete Date", "Institutional", "Index Fund", "Morningstar Category", "Annual Report Net Expense Ratio", "Annual Report Ongoing Charge", "Base Currency"]]}, "raw06.pkl")
fid = d.set_index("SecId").FundId
def cnt(X, m):  # serien kan saknas i exporten (flode, fund size)
    return int(X[m].notna().sum()) if m in X.columns else 0
chg = (R != R.shift(1, axis=1)) & R.notna() & R.shift(1, axis=1).notna(); both = R.notna() & R.shift(1, axis=1).notna()
print("\nmanad | betyg kl | NA kl | flode kl | avk kl | fundsize kl | betyg+NA+NA_lag kl | fonder betyg+NA | andel andrat betyg")
for i, m in enumerate(R.columns):
    if i == 0: continue
    ok = R[m].notna() & NA[m].notna() & NA.iloc[:, i-1].notna()
    if m[5:] in ("01", "04", "07", "10") or m in ("2006-09", "2006-11", "2006-12"):
        print(m, int(R[m].notna().sum()), int(NA[m].notna().sum()), cnt(FL, m), cnt(RET, m), cnt(FS, m), int(ok.sum()), fid[ok].nunique(), f"{chg[m].sum()/max(both[m].sum(),1):.1%}")
cs = (chg.sum() / both.sum().clip(lower=1))
print("\nandel andrat betyg, alla manader:"); print((cs*100).round(1).to_string())
