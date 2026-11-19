# Test 3: bygger panel. Rör inte flödesutfallet utöver att spara det.
import pandas as pd, numpy as np, glob
B='../../'
D=pd.read_csv(B+'morningstar_direct/direct_manadspanel.csv.gz')
D=D[(D.roll=='huvudklass')&(D.institutionalonly!=1)].copy()
D['ym']=D.t
D['incep']=pd.to_datetime(D['Inception Date'],errors='coerce')
# flöden, beställning 1
V=pd.concat([pd.read_csv(f,usecols=['performanceId','ym','ccy','nf_class','tna_class']) for f in glob.glob(B+'shof_riskklass_resultat/val_monthly_*.csv')])
V=V.drop_duplicates(['performanceId','ym'])
R=pd.concat([pd.read_csv(f,usecols=['performanceId','ym','bas']) for f in glob.glob(B+'shof_riskklass_resultat/bas/rips_bas_*.csv')]).drop_duplicates(['performanceId','ym'])
P=V.merge(R,on=['performanceId','ym'],how='outer')
P=P[P.performanceId.isin(D.performanceid)]
P['per']=pd.PeriodIndex(P.ym,freq='M')
P=P.sort_values(['performanceId','per'])
g=P.groupby('performanceId')
# kontrollera att föregående rad är föregående månad
prevper=g.per.shift(1)
cont=(P.per-prevper).apply(lambda x: x.n if pd.notna(x) else np.nan)==1
P['ret']=np.where(cont,P.bas/g.bas.shift(1)-1,np.nan)
P['tna_l']=np.where(cont,g.tna_class.shift(1),np.nan)
P['flow']=P.nf_class/P.tna_l*100
P.loc[~(P.tna_l>0),'flow']=np.nan
# 18 mån exponentiell avkastning (lag 1..18), minst 12 obs
lam=0.20551497; w=np.exp(-lam*np.arange(18))
def ewr(s):
    a=s.values; out=np.full(len(a),np.nan); n=np.full(len(a),0)
    for i in range(len(a)):
        lo=max(0,i-18); seg=a[lo:i][::-1]  # lag1 först
        m=~np.isnan(seg); 
        if m.sum()>=12: out[i]=(seg[m]*w[:len(seg)][m]).sum()/w[:len(seg)][m].sum(); n[i]=m.sum()
    return pd.Series(out,index=s.index)
P['retrf_a']=g.ret.transform(ewr)*100
# volatilitet över tillgänglig historik t-36..t-1, minst 12 obs (årstakt)
P['vol']=g.ret.transform(lambda s: s.shift(1).rolling(36,min_periods=12).std()*np.sqrt(12)*100)
P['flow_l']=g.flow.transform(lambda s: s.shift(1).rolling(12,min_periods=6).mean())
P['ltna_l']=np.log(P.tna_l.where(P.tna_l>0))
P=P[['performanceId','ym','ccy','flow','retrf_a','vol','flow_l','ltna_l','tna_l']]
M=D.merge(P,left_on=['performanceid','ym'],right_on=['performanceId','ym'],how='inner')
M['per']=pd.PeriodIndex(M.ym,freq='M')
M=M.sort_values(['SecId','per'])
gg=M.groupby('SecId')
# visad klass förra månaden: SRRI före 2023, SRI från 2023
M['klass']=np.where(M.per<pd.Period('2023-01','M'),M.srri,M.sri)
prev_ok=(M.per-gg.per.shift(1)).apply(lambda x: x.n if pd.notna(x) else np.nan)==1
M['klass_l']=np.where(prev_ok,gg.klass.shift(1),np.nan)
M['star_l']=np.where(prev_ok,gg.star.shift(1),np.nan)
M['cat_l']=np.where(prev_ok,gg.cat.shift(1),np.nan)
M['age']=((M.per.dt.to_timestamp()-M.incep).dt.days/30.4375)
# får klassen någon gång en stjärna?
M['ever_star']=gg.star.transform(lambda s: s.notna().any())
first_star=M[M.star.notna()].groupby('SecId').per.min()
M['first_star']=M.SecId.map(first_star)
K=pd.read_csv(B+'morningstar_direct/direct_kostnad.csv',usecols=['SecId','kiid_avgift','priip_kostnad'])
K['avgift']=K.kiid_avgift.fillna(K.priip_kostnad)
M=M.merge(K[['SecId','avgift']],on='SecId',how='left')
M.to_pickle('panel_test3.pkl')
print(len(M),M.SecId.nunique())
