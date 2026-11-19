import pandas as pd, numpy as np, re
d = pd.read_pickle("/home/claude/direct_raw/direct_alla.pkl")
pr = pd.concat([pd.read_csv("/mnt/user-data/outputs/direct/direct_prioritet.csv").assign(lista="prioritet"), pd.read_csv("/mnt/user-data/outputs/direct/direct_resten.csv").assign(lista="resten")], ignore_index=True).drop_duplicates("secid")
d = d.merge(pr, left_on="SecId", right_on="secid", how="left")
months = pd.period_range("2018-01","2026-10",freq="M")
def ts(prefix):
    cols=[c for c in d.columns if str(c).startswith(prefix+"_")]
    m = d[cols].copy(); m.columns=[pd.Period(c.split("_")[-1][:7],"M") for c in cols]; m.index=d.SecId.values
    return m
sri = ts("SRI Value").apply(pd.to_numeric, errors="coerce")
star = ts("Morningstar Rating Overall").apply(pd.to_numeric, errors="coerce")
cat = ts("Morningstar Category")
cat = cat.replace({"-":np.nan,"—":np.nan})
# SRRI history -> monthly as-of (only entries up to 2022-12-31 used for the pre period)
def parse_hist(h):
    return [(pd.Timestamp(a), int(b)) for a,b in re.findall(r"\[(\d{4}-\d\d-\d\d)\]\s*(\d)", str(h))]
rows=[]
for sid,h in zip(d.SecId, d["Surveyed KIID SRRI History"]):
    for dt,v in parse_hist(h): rows.append((sid,dt,v))
H = pd.DataFrame(rows, columns=["SecId","date","srri"])
H["t"]=H.date.dt.to_period("M")
H = H.sort_values(["SecId","date"]).groupby(["SecId","t"]).srri.last()
srri_m = H.unstack().reindex(columns=months)
srri_m = srri_m.ffill(axis=1)
# SRI monthly: forward-fill observed values; use current SRI (with its date) when the series is empty
sri_m = sri.reindex(columns=months).ffill(axis=1)
cur = pd.to_numeric(d.set_index("SecId")["PRIIPS KID Summary Risk Indicator"], errors="coerce")
curdate = pd.to_datetime(d.set_index("SecId")["SRI Value Date"], errors="coerce")
star_m = star.reindex(columns=months)
long = []
for name, M in [("srri",srri_m),("sri",sri_m),("star",star_m)]:
    s = M.stack(future_stack=True); s.name=name; long.append(s)
L = pd.concat(long, axis=1).reset_index(); L.columns=["SecId","t","srri","sri","star"]
cl = cat.reindex(columns=months).stack(future_stack=True).rename("cat").reset_index(); cl.columns=["SecId","t","cat"]
L = L.merge(cl, on=["SecId","t"], how="left")
L["sri_cur"]=L.SecId.map(cur); L["sri_cur_date"]=L.SecId.map(curdate)
L = L.merge(d[["SecId","ISIN_x","performanceid","fundid","roll","institutionalonly","vev_22","sig_w_22","lista","Obsolete Date","Inception Date"]], on="SecId", how="left")
L.to_pickle("/home/claude/direct_out/direct_long.pkl")
print("classes", L.SecId.nunique(), "rows", len(L))
print("share with any SRI obs:", sri.notna().any(axis=1).mean().round(3), "| current SRI:", cur.notna().mean().round(3), "| any SRRI hist:", d["Surveyed KIID SRRI History"].astype(str).str.contains(r"\[").mean().round(3), "| stars any:", star.notna().any(axis=1).mean().round(3))
