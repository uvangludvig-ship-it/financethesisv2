# Styrka pa latsasbyte jan 2022 (2021 mot 2022). Det riktiga bytet 2023 skattas INTE.
import pandas as pd, numpy as np
x=pd.read_pickle('alla_bas.pkl'); flow=pd.read_pickle('alla_flow.pkl'); na=pd.read_pickle('alla_na.pkl')
both=pd.read_csv('alla_fonder_med_par.csv').iloc[:,0]
x=x[x.FundId.isin(both)&x.side.isin(['UK','EU'])&(x.n_flow>=30)&(x['Inception Date']<='2021-12-31')]
fd=x[x.side=='EU'].groupby('FundId').dos.median()
P=pd.Period
def rate(ids):
    f=flow.loc[ids].sum(); a=na.loc[ids].sum().shift(1); return (f/a*1200).where(a>0)
D={}
for fid,g in x.groupby('FundId'):
    D[fid]=rate(g[g.side=='EU'].SecId)-rate(g[g.side=='UK'].SecId)
def ols_se(X,y):
    b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b; n,k=X.shape; XtXi=np.linalg.inv(X.T@X)
    V=XtXi@(X.T*(e**2))@X@XtXi*n/(n-k); return b,np.sqrt(np.diag(V))
for clip in [200,50]:
    rows=[]
    for fid,d in D.items():
        d=d.clip(-clip,clip)
        rows.append(dict(FundId=fid,dos=fd.get(fid,np.nan),dd=d[P('2022-01','M'):P('2022-12','M')].mean()-d[P('2021-01','M'):P('2021-12','M')].mean()))
    r=pd.DataFrame(rows).dropna(subset=['dd'])
    se_lvl=r.dd.std()/np.sqrt(len(r))
    rd=r.dropna(subset=['dos']); b,se=ols_se(np.column_stack([np.ones(len(rd)),rd.dos]),rd.dd.values)
    print(f'klipp ±{clip}: nivåskift EU mot UK: N={len(r)}, sd={r.dd.std():.1f}, MDE={2.8*se_lvl:.1f} | doslutning: N={len(rd)}, MDE={2.8*se[1]:.1f} pp/år per steg')
