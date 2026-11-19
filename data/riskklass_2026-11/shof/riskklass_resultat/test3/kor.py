# Test 3 enligt claude/DEKLARATION_test3_fonder_utan_stjarna_2026-11-17.md
import pandas as pd, numpy as np, sys
from math import erf, sqrt
M=pd.read_pickle('panel_test3.pkl')
M=M[(M.per>=pd.Period('2019-01','M'))&(M.per<=pd.Period('2025-12','M'))].copy()
M=M[M.flow.notna()]
q=M.groupby('ym').flow.transform(lambda s: s.quantile(.01)); Q=M.groupby('ym').flow.transform(lambda s: s.quantile(.99))
M=M[(M.flow>=q)&(M.flow<=Q)]
M['utan']=M.star_l.isna().astype(float)
M['klass_utan']=M.klass_l*M.utan
for s in [2,3,4,5]: M[f'st{s}']=(M.star_l==s).astype(float)
M['lage']=np.log(M.age.clip(lower=1))
M['mc']=M.ym+'|'+M.cat_l.astype(str)
def pval(t): return 2*(1-0.5*(1+erf(abs(t)/sqrt(2))))
def demean(X,fes,tol=1e-10,maxit=500):
    X=X.copy()
    codes=[pd.factorize(f)[0] for f in fes]
    for it in range(maxit):
        old=X.copy()
        for c in codes:
            cnt=np.bincount(c); 
            for j in range(X.shape[1]):
                X[:,j]-=np.bincount(c,X[:,j])[c]/cnt[c]
        if np.max(np.abs(X-old))<tol: break
    return X
def reg(df,y,xs,fes,cl='SecId'):
    d=df.dropna(subset=[y]+xs).copy()
    # släng singletons i första FE
    for f in fes:
        d=d[d.groupby(f)[f].transform('size')>1]
    Z=demean(d[[y]+xs].to_numpy(float),[d[f].to_numpy() for f in fes])
    Y,X=Z[:,0],Z[:,1:]
    keep=X.std(0)>1e-12; X=X[:,keep]; names=[x for x,k in zip(xs,keep) if k]
    XtX=np.linalg.inv(X.T@X); b=XtX@X.T@Y; u=Y-X@b
    g=pd.factorize(d[cl])[0]; G=g.max()+1
    S=np.zeros((X.shape[1],X.shape[1]))
    sc=np.zeros((G,X.shape[1])); np.add.at(sc,g,X*u[:,None]); S=sc.T@sc
    N,K=X.shape; c=G/(G-1)*(N-1)/(N-K)
    V=c*XtX@S@XtX
    return dict(b=pd.Series(b,names),V=pd.DataFrame(V,names,names),N=N,G=G,nfund=d.SecId.nunique())
def lin(r,w):  # w: dict namn->vikt
    w=pd.Series(w); est=(r['b'][w.index]*w).sum(); se=np.sqrt(w@r['V'].loc[w.index,w.index]@w)
    return est*12,se*12,est/se
ctrl=['retrf_a','flow_l','ltna_l','lage','avgift']
stars=['st2','st3','st4','st5']
fe=['mc','ccy']
def huvud(df,extra=[],fes=fe,lab=''):
    r=reg(df,'flow',['klass_l','klass_utan','utan']+stars+ctrl+extra,fes)
    a=lin(r,{'klass_l':1}); u=lin(r,{'klass_l':1,'klass_utan':1}); d=lin(r,{'klass_utan':1})
    nu=int(df.dropna(subset=['flow','klass_l']+ctrl+extra).utan.sum())
    print(f"{lab:38s} b1 (med stjärna) {a[0]:+6.2f} se {a[1]:4.2f} p {pval(a[2]):.3f} | b1+b2 (utan) {u[0]:+6.2f} se {u[1]:4.2f} p {pval(u[2]):.3f} [{u[0]-1.96*u[1]:+.2f}; {u[0]+1.96*u[1]:+.2f}] MDE {2.8*u[1]:.2f} | b2 {d[0]:+6.2f} se {d[1]:4.2f} p {pval(d[2]):.3f} | N {r['N']} klasser {r['G']}")
    return r
base=M[M.ever_star&M.klass_l.notna()&M.cat_l.notna()&M.retrf_a.notna()]
A=base[(base.age>=12)&(base.age<60)]
print('Urval: fondmånader',len(A),'utan stjärna',int(A.utan.sum()),'klasser',A.SecId.nunique())
print('Medelflöde pp/år: med stjärna',round(A[A.utan==0].flow.mean()*12,2),'utan',round(A[A.utan==1].flow.mean()*12,2))
print('Medelklass: med',round(A[A.utan==0].klass_l.mean(),2),'utan',round(A[A.utan==1].klass_l.mean(),2))
print('\n== Huvud och robusthet (pp/år per klassteg)')
huvud(A,lab='Huvud, ålder 12-59')
huvud(A,extra=['vol'],lab='R1 + volatilitet')
B=base[(base.age>=24)&(base.age<48)]; huvud(B,lab='R2 ålder 24-47')
huvud(A,fes=['mc','SecId'],lab='R3 + klasseffekter')
huvud(A[A.per<pd.Period('2023-01','M')],lab='R4 före 2023 (SRRI)')
huvud(A[A.cat_l.astype(str).str.contains('Equity')],lab='R5 aktiekategorier')
print('\n== Positiva kontroller')
Rr=A[A.utan==0]; r=reg(Rr,'flow',['star_l','klass_l']+ctrl,fe); s=lin(r,{'star_l':1})
print(f"Stjärna, delurval med stjärna: {s[0]:+.2f} pp/år per stjärna se {s[1]:.2f} t {s[2]:.1f}")
Ru=A[A.utan==1]; r=reg(Ru,'flow',['klass_l']+ctrl,fe); s=lin(r,{'retrf_a':1}); k=lin(r,{'klass_l':1})
sd=Ru.retrf_a.std()
print(f"Avkastningssignal, delurval utan stjärna: {s[0]:+.2f} pp/år per procentenhet (sd {sd:.2f}) t {s[2]:.1f}; klass i samma regression {k[0]:+.2f} se {k[1]:.2f}")
