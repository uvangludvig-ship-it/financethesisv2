# Styrkeberakning UTAN att titta pa det riktiga bytet: samma skattare pa lataasbytet jan 2022.
import pandas as pd, numpy as np
x=pd.read_pickle('par_bas.pkl'); flow=pd.read_pickle('flow.pkl'); na=pd.read_pickle('na.pkl')
both=pd.read_csv('fonder_med_par.csv').iloc[:,0]
x=x[x.FundId.isin(both)&x.side.isin(['UK','EU'])&(x.n_flow_22_23>=20)]
fd=x[x.side=='EU'].groupby('FundId').dos.median().dropna()
def side_rate(ids):
    f=flow.loc[ids].sum(); a=na.loc[ids].sum().shift(1)
    return (f/a*1200).where(a>0)   # pp per ar
rows=[]
for fid in fd.index:
    g=x[x.FundId==fid]
    eu=side_rate(g[g.side=='EU'].SecId); uk=side_rate(g[g.side=='UK'].SecId)
    d=(eu-uk).clip(-200,200)
    rows.append(dict(FundId=fid,dos=fd[fid],
      pre=d[pd.Period('2021-01','M'):pd.Period('2021-12','M')].mean(),
      post=d[pd.Period('2022-01','M'):pd.Period('2022-12','M')].mean()))
r=pd.DataFrame(rows).dropna(); r['dd']=r.post-r.pre
X=np.column_stack([np.ones(len(r)),r.dos.values]); y=r.dd.values
b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b; n,k=X.shape
XtXi=np.linalg.inv(X.T@X); V=XtXi@(X.T*(e**2))@X@XtXi*n/(n-k); se=np.sqrt(V[1,1])
print('fonder',len(r),'| SE per steg (latsasbyte 2022):',round(se,2),'| MDE 80% kraft, 5%: ',round(2.8*se,2),'pp/ar')
print('sd av dd:',round(r.dd.std(),1),'| dos-fordelning:',r.dos.value_counts().to_dict())
