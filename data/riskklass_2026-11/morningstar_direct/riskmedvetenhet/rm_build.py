# Riskmedvetenhet: bygger panel enligt claude/DEKLARATION_riskmedvetenhet_forlustrisk_2026-11-18.md (tillagget).
# Bygger pa t2_build.py. Lagger till: forlustandel 60 man, avkastning 60 man, log TNA forra manaden, flode t-19, KIID-avgift.
# Inga utfall skrivs ut har.
import pandas as pd, numpy as np, glob, os
H=os.path.expanduser("~/mnt/Downloads")
L=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz", low_memory=False)
L=L[(L.roll=="huvudklass")&(L.institutionalonly!=1)].copy()
L["t"]=pd.PeriodIndex(L.t,freq="M"); L=L.sort_values(["SecId","t"])
g=L.groupby("SecId"); L["star_lag"]=g.star.shift(1); L["cat_lag"]=g.cat.shift(1)
L["incep"]=pd.to_datetime(L["Inception Date"], errors="coerce")
pids=set(L.performanceid.dropna())
fl=[]
for f in glob.glob(f"{H}/shof_riskklass_resultat/val_monthly_*.csv")+glob.glob(f"{H}/shof_riskklass_resultat/privat/val_monthly_*.csv"):
    v=pd.read_csv(f); v=v[v.performanceId.isin(pids)]; v["src"]="privat" if "/privat/" in f else "huvud"; fl.append(v)
V=pd.concat(fl,ignore_index=True).drop_duplicates(["performanceId","ym"])
V["t"]=pd.PeriodIndex(V.ym,freq="M"); V=V.sort_values(["performanceId","t"])
gv=V.groupby("performanceId"); V["tna_lag"]=gv.tna_class.shift(1); V["t_lag"]=gv.t.shift(1)
V["consec"]=(V.t.astype("int64")-V.t_lag.astype("int64"))==1
has=V[V.tna_class.notna()].groupby("performanceId").t.agg(["min","max"]).rename(columns={"min":"t0","max":"t1"})
V=V.join(has,on="performanceId")
V["m_since"]=V.t.astype("int64")-V.t0.astype("int64"); V["m_left"]=V.t1.astype("int64")-V.t.astype("int64")
lim={"SEK":100e6,"NOK":100e6,"DKK":70e6}; V["lim"]=V.ccy.map(lim).fillna(10e6)
V["f"]=V.nf_class/V.tna_lag*100
# flode 19 manader tidigare (otrimmat, alla manader)
F19=V[V.consec&np.isfinite(V.f)][["performanceId","t","f"]].copy(); F19["t"]=F19.t+19; F19=F19.rename(columns={"f":"f19"})
ok=V.consec&(V.m_since>=12)&(V.m_left>=6)&(V.tna_lag>=V.lim)&V.f.notna()&np.isfinite(V.f)
ok&=(V.nf_n>=10)|(V.src=="privat")
V=V[ok&(V.t>=pd.Period("2019-01","M"))&(V.t<=pd.Period("2025-12","M"))].copy()
lo=V.groupby("t").f.transform(lambda x:x.quantile(.01)); hi=V.groupby("t").f.transform(lambda x:x.quantile(.99))
V=V[(V.f>=lo)&(V.f<=hi)]
V=V.merge(F19,on=["performanceId","t"],how="left")
B=pd.concat([pd.read_csv(f) for f in glob.glob(f"{H}/shof_riskklass_resultat/bas/rips_bas_*.csv")],ignore_index=True)
B=B[B.performanceId.isin(pids)].drop_duplicates(["performanceId","ym"])
B["t"]=pd.PeriodIndex(B.ym,freq="M"); B=B.sort_values(["performanceId","t"])
B["lr"]=np.log(B.bas)-np.log(B.groupby("performanceId").bas.shift(1))
B["gap"]=(B.t.astype("int64")-B.groupby("performanceId").t.shift(1).astype("int64")); B.loc[B.gap!=1,"lr"]=np.nan
B["neg"]=np.where(B.lr.notna(),(B.lr<0).astype(float),np.nan)
gb=B.groupby("performanceId")
B["ret12"]=gb.lr.transform(lambda x:x.shift(1).rolling(12,min_periods=12).sum())
B["ret36"]=gb.lr.transform(lambda x:x.shift(1).rolling(36,min_periods=36).sum())
B["ret60"]=gb.lr.transform(lambda x:x.shift(1).rolling(60,min_periods=54).sum()*60/x.shift(1).rolling(60,min_periods=54).count())
B["sig60"]=gb.lr.transform(lambda x:x.shift(1).rolling(60,min_periods=54).std())*np.sqrt(12)*100
B["loss60"]=gb.neg.transform(lambda x:x.shift(1).rolling(60,min_periods=54).mean())
P=L.merge(V[["performanceId","t","f","f19","tna_lag","ccy"]],left_on=["performanceid","t"],right_on=["performanceId","t"],how="inner")
P=P.merge(B[["performanceId","t","ret12","ret36","ret60","sig60","loss60"]],on=["performanceId","t"],how="left")
K=pd.read_csv(f"{H}/morningstar_direct/direct_kostnad.csv")[["SecId","kiid_avgift"]].drop_duplicates("SecId")
P=P.merge(K,on="SecId",how="left")
P["age_m"]=(P.t.dt.year-P.incep.dt.year)*12+(P.t.dt.month-P.incep.dt.month)
P=P.drop_duplicates(["fundid","t"])
keep=["SecId","fundid","t","f","f19","tna_lag","ccy","star_lag","cat_lag","ret12","ret36","ret60","sig60","loss60","kiid_avgift","age_m"]
P[keep].to_pickle("rm_panel.pkl")
A=P[(P.t>=pd.Period("2020-01","M"))].dropna(subset=["cat_lag","loss60","sig60","ret12","ret36","ret60","f19","tna_lag","age_m"])
print("panel",len(P),"| analysurval 2020-2025:",len(A),"fondmanader",A.fundid.nunique(),"fonder")
eq=A.cat_lag.str.contains("Equity")
print("aktiefonder:",eq.sum(),"fondmanader",A[eq].fundid.nunique(),"fonder | med stjarna:",A[eq].star_lag.notna().sum())
print("avgift saknas, andel:",round(A.kiid_avgift.isna().mean(),3))
print("loss60 beskrivning:",A.loss60.describe().round(3).to_dict())
