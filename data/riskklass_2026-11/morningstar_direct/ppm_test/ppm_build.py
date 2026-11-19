# PPM-testet: bygger panel med tva floden per fond och manad (PPM-sparare och ovriga). Inga utfall skrivs ut.
import pandas as pd, numpy as np, glob, os
H=os.path.expanduser("~/mnt")
per=lambda s: pd.PeriodIndex(s,freq="M")
# --- egenskaper per fond (huvudklass i Direct, inte institutionell)
L=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz", low_memory=False)
L=L[(L.roll=="huvudklass")&(L.institutionalonly!=1)].copy(); L["t"]=per(L.t); L=L.sort_values(["SecId","t"])
g=L.groupby("SecId"); L["star_lag"]=g.star.shift(1); L["cat_lag"]=g.cat.shift(1)
pids=set(L.performanceid.dropna())
B=pd.concat([pd.read_csv(f) for f in glob.glob(f"{H}/shof_riskklass_resultat/bas/rips_bas_*.csv")],ignore_index=True)
B=B[B.performanceId.isin(pids)].drop_duplicates(["performanceId","ym"]); B["t"]=per(B.ym); B=B.sort_values(["performanceId","t"])
B["lr"]=np.log(B.bas)-np.log(B.groupby("performanceId").bas.shift(1))
B.loc[(B.t.astype("int64")-B.groupby("performanceId").t.shift(1).astype("int64"))!=1,"lr"]=np.nan
gb=B.groupby("performanceId").lr
B["ret12"]=gb.transform(lambda x:x.shift(1).rolling(12,min_periods=12).sum())
B["ret36"]=gb.transform(lambda x:x.shift(1).rolling(36,min_periods=36).sum())
B["sig60"]=gb.transform(lambda x:x.shift(1).rolling(60,min_periods=54).std())*np.sqrt(12)*100
C=L[["fundid","performanceid","t","star_lag","cat_lag"]].merge(B[["performanceId","t","ret12","ret36","sig60"]],left_on=["performanceid","t"],right_on=["performanceId","t"],how="left").drop_duplicates(["fundid","t"])
ok=C.cat_lag.notna()
C.loc[ok,"rank12"]=C[ok].groupby(["t","cat_lag"]).ret12.rank(pct=True); C.loc[ok,"rank36"]=C[ok].groupby(["t","cat_lag"]).ret36.rank(pct=True)
# --- PPM
X=pd.read_csv(f"{H}/ftn/crosswalk_ppm_shof.csv")[["fondnr","performanceid","fundid"]].dropna(subset=["fundid"])
P=pd.read_csv(f"{H}/ppm/ppm_panel_2018_2026.csv",usecols=["fondnr","date","mv_tot","handel_netto","fondtyp","valuta"],low_memory=False)
P["t"]=per(P.date.str[:7]); P=P.sort_values(["fondnr","t"]).drop_duplicates(["fondnr","t"])
gp=P.groupby("fondnr"); P["mv_lag"]=gp.mv_tot.shift(1); P["cons"]=(P.t.astype("int64")-gp.t.shift(1).astype("int64"))==1
sp=P.groupby("fondnr").t.agg(["min","max"]); P=P.join(sp,on="fondnr")
P["since"]=P.t.astype("int64")-P["min"].astype("int64"); P["left"]=P["max"].astype("int64")-P.t.astype("int64")
P=P.merge(X,on="fondnr",how="inner")
# --- fondens totala flode och formogenhet (SHoF): en klass per fond, helst i SEK; PPM-belopp raknas om till klassens valuta
M=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz",usecols=["performanceid","fundid"]).drop_duplicates()
M=pd.concat([M,X[["performanceid","fundid"]]]).dropna().drop_duplicates("performanceid")
V=pd.concat([pd.read_csv(f,usecols=["performanceId","ym","ccy","nf_fund","nf_n","tna_fund"]) for f in glob.glob(f"{H}/shof_riskklass_resultat/val_monthly_*.csv")+glob.glob(f"{H}/shof_riskklass_resultat/privat/val_monthly_*.csv")],ignore_index=True)
V=V.merge(M,left_on="performanceId",right_on="performanceid",how="inner"); V=V[V.fundid.isin(set(P.fundid))&(V.nf_n>=10)&V.tna_fund.notna()]
V["pri"]=(V.ccy!="SEK").astype(int); V["t"]=per(V.ym)
V=V.sort_values(["fundid","t","pri","performanceId"]).drop_duplicates(["fundid","t"])
V=V.sort_values(["fundid","t"]); gv=V.groupby("fundid"); V["tna_lag"]=gv.tna_fund.shift(1); V["ccy_lag"]=gv.ccy.shift(1)
V["vcons"]=((V.t.astype("int64")-gv.t.shift(1).astype("int64"))==1)&(V.ccy==V.ccy_lag)
R=pd.read_csv(f"{H}/morningstar_direct/riksbank/riksbank_manad.csv"); R=R[R.serie.str.match(r"SEK[A-Z]{3}PMI")].copy(); R["ccy"]=R.serie.str[3:6]; R["t"]=per(R.ym); R=R.sort_values(["ccy","t"])
R["sista_lag"]=R.groupby("ccy").sista.shift(1)
D=P.merge(V[["fundid","t","ccy","nf_fund","tna_fund","tna_lag","vcons"]],on=["fundid","t"],how="left")
D=D.merge(R[["ccy","t","medel","sista_lag"]],on=["ccy","t"],how="left")
D.loc[D.ccy=="SEK",["medel","sista_lag"]]=1.0
D=D.merge(C[["fundid","t","star_lag","cat_lag","rank12","rank36","sig60"]],on=["fundid","t"],how="left")
D["hn_c"]=D.handel_netto/D.medel; D["mvlag_c"]=D.mv_lag/D.sista_lag
D["f_ppm"]=D.handel_netto/D.mv_lag*100
D["oth_lag"]=D.tna_lag-D.mvlag_c
D["f_oth"]=(D.nf_fund-D.hn_c)/D.oth_lag*100
D["share_lag"]=D.mvlag_c/D.tna_lag
D["oth_lag_sek"]=D.oth_lag*D.sista_lag
D.to_pickle("ppm_panel_test.pkl"); print("rader",len(D),"fonder",D.fondnr.nunique())
