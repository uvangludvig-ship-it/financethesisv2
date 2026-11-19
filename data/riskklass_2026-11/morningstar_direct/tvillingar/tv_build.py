# Tvillingtestet: bygger panel pa klassniva for fonder med huvudklass och institutionell klass. Inga utfall skrivs ut.
import pandas as pd, numpy as np, glob, os
H=os.path.expanduser("~/mnt"); per=lambda s: pd.PeriodIndex(s,freq="M")
L=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz",low_memory=False)
L["t"]=per(L.t); L=L.sort_values(["SecId","t"]); g=L.groupby("SecId")
L["star_lag"]=g.star.shift(1); L["cat_lag"]=g.cat.shift(1)
L["label"]=np.where(L.t<=pd.Period("2022-12","M"),L.srri,L.sri); L["label_lag"]=L.groupby("SecId").label.shift(1)
L["incep"]=pd.to_datetime(L["Inception Date"],errors="coerce"); L["age_m"]=(L.t.dt.year-L.incep.dt.year)*12+(L.t.dt.month-L.incep.dt.month)
pids=set(L.performanceid.dropna())
V=pd.concat([pd.read_csv(f).assign(src="privat" if "/privat/" in f else "huvud") for f in glob.glob(f"{H}/shof_riskklass_resultat/val_monthly_*.csv")+glob.glob(f"{H}/shof_riskklass_resultat/privat/val_monthly_*.csv")],ignore_index=True)
V=V[V.performanceId.isin(pids)].drop_duplicates(["performanceId","ym"]); V["t"]=per(V.ym); V=V.sort_values(["performanceId","t"])
gv=V.groupby("performanceId"); V["tna_lag"]=gv.tna_class.shift(1); V["cons"]=(V.t.astype("int64")-gv.t.shift(1).astype("int64"))==1
has=V[V.tna_class.notna()].groupby("performanceId").t.agg(["min","max"]); V=V.join(has,on="performanceId")
V["since"]=V.t.astype("int64")-V["min"].astype("int64"); V["left"]=V["max"].astype("int64")-V.t.astype("int64")
V["lim"]=V.ccy.map({"SEK":100e6,"NOK":100e6,"DKK":70e6}).fillna(10e6); V["f"]=V.nf_class/V.tna_lag*100
ok=V.cons&(V.since>=12)&(V.left>=6)&(V.tna_lag>=V.lim)&V.f.notna()&np.isfinite(V.f)
V=V[ok&(V.t>=pd.Period("2019-01","M"))&(V.t<=pd.Period("2025-12","M"))].copy()
lo=V.groupby("t").f.transform(lambda x:x.quantile(.01)); hi=V.groupby("t").f.transform(lambda x:x.quantile(.99)); V=V[(V.f>=lo)&(V.f<=hi)]
B=pd.concat([pd.read_csv(f) for f in glob.glob(f"{H}/shof_riskklass_resultat/bas/rips_bas_*.csv")],ignore_index=True)
B=B[B.performanceId.isin(pids)].drop_duplicates(["performanceId","ym"]); B["t"]=per(B.ym); B=B.sort_values(["performanceId","t"])
B["lr"]=np.log(B.bas)-np.log(B.groupby("performanceId").bas.shift(1)); B.loc[(B.t.astype("int64")-B.groupby("performanceId").t.shift(1).astype("int64"))!=1,"lr"]=np.nan
gb=B.groupby("performanceId").lr
for k in (12,36): B[f"ret{k}"]=gb.transform(lambda x:x.shift(1).rolling(k,min_periods=k).sum())
P=L.merge(V[["performanceId","t","f","ccy","tna_lag"]],left_on=["performanceid","t"],right_on=["performanceId","t"],how="inner").merge(B[["performanceId","t","ret12","ret36"]],on=["performanceId","t"],how="left")
P[["SecId","fundid","roll","institutionalonly","t","f","ccy","tna_lag","star_lag","cat_lag","label_lag","srri","sri","age_m","ret12","ret36"]].to_pickle("tv_klasser.pkl")
print("klassmanader",len(P),"klasser",P.SecId.nunique())
