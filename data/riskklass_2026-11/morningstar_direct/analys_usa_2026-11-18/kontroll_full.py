# Oberoende kontroll: (1) alfor med explicit loop för 25 slumpade fonder, (2) Figure 3 EW och Table 3 rad 1 med explicita dummies/OLS.
import sys, re, numpy as np, pandas as pd
d=pd.read_pickle('panel_full.pkl'); d=d[d.in_kod].reset_index(drop=True)
src=sys.argv[1]
df=pd.read_csv(src,encoding='latin-1',low_memory=False,dtype=str); df.columns=[re.sub(r'\s+',' ',c.replace('\n',' ')).strip() for c in df.columns]
df=df[df['Morningstar Category Group'].eq('Equity')]
fk=pd.read_csv('faktorer/usa_ff3_mom_1986_2011.csv'); fk['ym']=fk.yyyymm.astype(str).str[:4]+'-'+fk.yyyymm.astype(str).str[4:]; fk=fk.set_index('ym')
rng=np.random.default_rng(1); fids=rng.choice(d.FundId.unique(),25,replace=False)
rc=[c for c in df.columns if c.startswith('Monthly Return')]; nc=[c for c in df.columns if c.startswith('Net Assets - share class (Monthly)')]
months=[re.search(r'\d{4}-\d{2}',c).group(0) for c in rc]
lam=0.20551497; w=np.exp(-lam*np.arange(18))
maxdiff=0; n=0
for fid in fids:
    sub=df[df.FundId==fid]
    R=sub[rc].apply(lambda s: pd.to_numeric(s.str.replace(',',''),errors='coerce')).values; NA=sub[nc].apply(lambda s: pd.to_numeric(s.str.replace(',',''),errors='coerce')).values
    T=len(months); ret=np.full(T,np.nan)
    for t in range(T):
        r=R[:,t]; wl=NA[:,t-1] if t>0 else np.full(len(r),np.nan); ok=~np.isnan(r)
        if not ok.any(): continue
        ww=np.where(ok & ~np.isnan(wl) & (wl>0), wl, np.nan)
        ret[t]=np.nansum(r*ww)/np.nansum(ww) if np.isfinite(ww).any() else r[ok].mean()
    rf=fk.loc[months,'RF'].values; y=ret-rf; X=fk.loc[months,['Mkt-RF']].values
    beta=np.full(T,np.nan)
    for t in range(1,T):
        lo=max(0,t-60); yy=y[lo:t]; xx=X[lo:t,0]; ok=~np.isnan(yy)
        if ok.sum()>=36: beta[t]=np.polyfit(xx[ok],yy[ok],1)[0]
    a=np.full(T,np.nan); a[:-1]=y[:-1]-beta[1:]*X[:-1,0]
    for _,row in d[d.FundId==fid].iterrows():
        t=months.index(row.ym); v=a[t-18:t][::-1]
        mine=(w*v).sum()/w.sum()
        if np.isfinite(mine) and np.isfinite(row.capm_a):
            # panelvärdet är winsoriserat; jämför bara där det inte kapats
            q=d[d.ym==row.ym].capm_a
            if q.min()<row.capm_a<q.max(): maxdiff=max(maxdiff,abs(mine-row.capm_a)); n+=1
print('CAPM-alfa, explicit loop mot panel: största avvikelse', round(maxdiff,8),'över',n,'fondmånader')
M=pd.get_dummies(d.ym).astype(float).values; S=pd.get_dummies(d.star_c.astype(int),drop_first=True).astype(float).values; yv=d.flow.values
def R2(Z): b,*_=np.linalg.lstsq(Z,yv,rcond=None); e=yv-Z@b; return 1-e@e/((yv-yv.mean())@(yv-yv.mean()))
a=R2(M); b=R2(np.c_[M,d.unad_a]); c=R2(np.c_[M,S]); dd=R2(np.c_[M,d.unad_a,S])
print('Figure 3 EW: totalt %.1f tid %.1f avk %.1f betyg %.1f'%(100*dd,100*a,100*(dd-c),100*(dd-b)))
Mt=(d.star_c==5).astype(float); n5=Mt.groupby(d.ym).transform('sum'); U=(d.groupby('ym').unad_a.rank(ascending=False,method='first')<=n5).astype(float)
Z=np.c_[np.ones(len(d)),Mt-U,np.maximum(Mt,U)]; bb=np.linalg.lstsq(Z,yv,rcond=None)[0]
print('Table 3 Morningstar mot rå, b1: %.3f'%bb[1], ' halva skillnaden bara-M mot bara-U: %.3f'%((d.flow[(Mt==1)&(U==0)].mean()-d.flow[(Mt==0)&(U==1)].mean())/2))
