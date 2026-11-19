# T2: bygger fondmånadspanel for testet "fonder utan stjarnbetyg". Inga utfall skrivs ut har.
# Urval: huvudklass per fond i Direct, institutionalonly != 1. Floden ur SHoF val_monthly, kurser ur rips_bas.
import pandas as pd, numpy as np, glob, os
H=os.path.expanduser("~/mnt")
L=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz", low_memory=False)
L=L[(L.roll=="huvudklass")&(L.institutionalonly!=1)].copy()
L["t"]=pd.PeriodIndex(L.t,freq="M")
L=L.sort_values(["SecId","t"])
g=L.groupby("SecId")
L["star_lag"]=g.star.shift(1); L["cat_lag"]=g.cat.shift(1)
L["label"]=np.where(L.t<=pd.Period("2022-12","M"), L.srri, L.sri)
L["label_lag"]=L.groupby("SecId").label.shift(1)
L["incep"]=pd.to_datetime(L["Inception Date"], errors="coerce")
pids=set(L.performanceid.dropna())
# floden
fl=[]
for f in glob.glob(f"{H}/shof_riskklass_resultat/val_monthly_*.csv")+glob.glob(f"{H}/shof_riskklass_resultat/privat/val_monthly_*.csv"):
    v=pd.read_csv(f); v=v[v.performanceId.isin(pids)]; v["src"]="privat" if "/privat/" in f else "huvud"; fl.append(v)
V=pd.concat(fl,ignore_index=True).drop_duplicates(["performanceId","ym"])
V["t"]=pd.PeriodIndex(V.ym,freq="M"); V=V.sort_values(["performanceId","t"])
gv=V.groupby("performanceId")
V["tna_lag"]=gv.tna_class.shift(1); V["t_lag"]=gv.t.shift(1)
V["consec"]=(V.t.astype("int64")-V.t_lag.astype("int64"))==1
has=V[V.tna_class.notna()].groupby("performanceId").t.agg(["min","max"]).rename(columns={"min":"t0","max":"t1"})
V=V.join(has,on="performanceId")
V["m_since"]=V.t.astype("int64")-V.t0.astype("int64"); V["m_left"]=V.t1.astype("int64")-V.t.astype("int64")
lim={"SEK":100e6,"NOK":100e6,"DKK":70e6}
V["lim"]=V.ccy.map(lim).fillna(10e6)
V["f"]=V.nf_class/V.tna_lag*100
ok=V.consec&(V.m_since>=12)&(V.m_left>=6)&(V.tna_lag>=V.lim)&V.f.notna()&np.isfinite(V.f)
ok&=(V.nf_n>=10)|(V.src=="privat")   # nf_n galler fondflodet; privatfilerna har nf_n=0
V=V[ok&(V.t>=pd.Period("2019-01","M"))&(V.t<=pd.Period("2025-12","M"))].copy()
lo=V.groupby("t").f.transform(lambda x:x.quantile(.01)); hi=V.groupby("t").f.transform(lambda x:x.quantile(.99))
V=V[(V.f>=lo)&(V.f<=hi)]
# kurser
B=pd.concat([pd.read_csv(f) for f in glob.glob(f"{H}/shof_riskklass_resultat/bas/rips_bas_*.csv")],ignore_index=True)
B=B[B.performanceId.isin(pids)].drop_duplicates(["performanceId","ym"])
B["t"]=pd.PeriodIndex(B.ym,freq="M"); B=B.sort_values(["performanceId","t"])
B["lr"]=np.log(B.bas)-np.log(B.groupby("performanceId").bas.shift(1))
B["gap"]=(B.t.astype("int64")-B.groupby("performanceId").t.shift(1).astype("int64"))
B.loc[B.gap!=1,"lr"]=np.nan
gb=B.groupby("performanceId").lr
B["ret12"]=gb.transform(lambda x:x.shift(1).rolling(12,min_periods=12).sum())
B["sig12"]=gb.transform(lambda x:x.shift(1).rolling(12,min_periods=12).std())*np.sqrt(12)*100
B["ret36"]=gb.transform(lambda x:x.shift(1).rolling(36,min_periods=36).sum())
B["sig60"]=gb.transform(lambda x:x.shift(1).rolling(60,min_periods=54).std())*np.sqrt(12)*100
P=L.merge(V[["performanceId","t","f","ccy"]],left_on=["performanceid","t"],right_on=["performanceId","t"],how="inner")
P=P.merge(B[["performanceId","t","ret12","sig12","ret36","sig60"]],on=["performanceId","t"],how="left")
P["age_m"]=(P.t.dt.year-P.incep.dt.year)*12+(P.t.dt.month-P.incep.dt.month)
P["rated"]=P.star_lag.notna()
P["post"]=P.t>=pd.Period("2023-01","M")
P=P.drop_duplicates(["fundid","t"])
keep=["SecId","fundid","t","f","star_lag","cat_lag","label_lag","label","srri","sri","ret12","sig12","ret36","sig60","age_m","rated","post","ccy","vev_22"]
P[keep].to_pickle("t2_panel.pkl")
print("fondmanader",len(P),"fonder",P.fundid.nunique())
