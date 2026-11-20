# Table 3 rad 1 enligt författarnas kod (reghdfe ..., noa vce(cluster yyyymm fundid)): ingen månadseffekt,
# regressorer (M − U) och M_e_U. Definitionen av M_e_U står inte i koden: körs som max(M,U) och som M+U.
import numpy as np, pandas as pd
d=pd.read_pickle('panel.pkl')
M=(d.star==5).astype(float); n5=M.groupby(d.ym).transform('sum')
U=(d.groupby('ym').signal.rank(ascending=False,method='first')<=n5).astype(float)
def ols2(y,X,c1,c2):
    X=np.c_[np.ones(len(y)),X]; XtXi=np.linalg.inv(X.T@X); b=XtXi@X.T@y; e=y-X@b
    def meat(cl):
        u=pd.DataFrame(X*e[:,None]).groupby(np.asarray(cl)).sum().values; G=len(u); return G/(G-1)*u.T@u
    inter=pd.Series(list(zip(c1,c2))).astype(str).values
    V=XtXi@(meat(c1)+meat(c2)-meat(inter))@XtXi; return b,np.sqrt(np.diag(V))
for lab,E in [('E = max(M,U)',np.maximum(M,U)),('E = M+U',M+U)]:
    for c,k in [('flow',1),('flow_usd',1),('pos',100)]:
        b,se=ols2(d[c].values,np.c_[M-U,E],d.FundId.values,d.ym.values)
        print(f"{lab:14s} {c:9s} koef (M−U) {k*b[1]:+.3f}  t {b[1]/se[1]:.2f}")
print('andel fondmånader där båda är topp:', round(((M==1)&(U==1)).mean()*100,2),'%; bara M', round(((M==1)&(U==0)).mean()*100,2),'%; bara U', round(((M==0)&(U==1)).mean()*100,2),'%')
