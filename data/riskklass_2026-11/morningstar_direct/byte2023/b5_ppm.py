# PPM som kontrollhylla: antal och standardfel. Ingen punktskattning for det riktiga bytet.
import pandas as pd, numpy as np, os
H=os.path.expanduser("~/mnt")
E=pd.read_pickle("etiketter.pkl"); K=pd.read_pickle(f"{H}/morningstar_direct/tvillingar/tv_klasser.pkl")
E=E[E.dos.isin([0,1,2])&E.srri22.notna()]; D=E.set_index("SecId")[["dos","sig_w","srri22"]]
pr=K[(K.roll=="huvudklass")&(K.institutionalonly!=1)&K.SecId.isin(D.index)].join(D,on="SecId")
Q=pd.read_pickle(f"{H}/morningstar_direct/ppm_test/ppm_panel_test.pkl")
Q=Q[Q.cons&(Q.since>=12)&(Q.left>=6)&(Q.mv_lag>=10e6)&Q.f_ppm.notna()].copy()
lo=Q.groupby("t").f_ppm.transform(lambda x:x.quantile(.01)); hi=Q.groupby("t").f_ppm.transform(lambda x:x.quantile(.99)); Q=Q[(Q.f_ppm>=lo)&(Q.f_ppm<=hi)]
Q=Q.sort_values("mv_lag",ascending=False).drop_duplicates(["fundid","t"])
J=pr.merge(Q[["fundid","t","f_ppm","fondnr"]],on=["fundid","t"]); J["y"]=J.t.dt.year; J["df"]=J.f-J.f_ppm
def dm(X,keys,it=60):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(k).transform("mean")
    return X
def est(A,y,Xcols,keys):
    ks=[A[k].values for k in keys]; yd=dm(A[[y]],ks).values[:,0]; Xd=dm(A[Xcols],ks).values
    XtXi=np.linalg.pinv(Xd.T@Xd); b=XtXi@Xd.T@yd; e=yd-Xd@b
    sc=pd.DataFrame(Xd*e[:,None]).groupby(A.fundid.values).sum().values; G=len(sc); return b[0]*12,np.sqrt((XtXi@(sc.T@sc)@XtXi*G/(G-1))[0,0])*12,G
def window(A,y0):
    W=A[A.y.isin([y0,y0+1])].copy(); n=W.groupby(["SecId","y"]).size().unstack(fill_value=0)
    W=W[W.SecId.isin(n[(n.get(y0,0)>=9)&(n.get(y0+1,0)>=9)].index)].copy()
    W["efter"]=(W.y==y0+1).astype(float); W["ed"]=W.efter*W.dos; W["tt"]=W.t.astype(str); return W
W=window(J,2022); u=W.drop_duplicates("SecId")
print("PPM-fonder med privatklassens flode och PPM-handel minst 9 man bade 2022 och 2023:",len(u),"| dos:",u.dos.value_counts().sort_index().to_dict())
print("  gammal klass x dos:"); print(pd.crosstab(u.srri22,u.dos))
print("  spridning (std, procent/manad): privat",round(W.f.std(),2),"PPM",round(W.f_ppm.std(),2),"skillnad",round(W.df.std(),2))
for y0 in [2019,2020,2021,2022,2023]:
    W=window(J,y0)
    if len(W)==0: continue
    b,s,G=est(W,"df",["ed"],["SecId","tt"]); b2,s2,_=est(W,"f",["ed"],["SecId","tt"]); b3,s3,_=est(W,"f_ppm",["ed"],["SecId","tt"])
    if y0==2022: print(f"{y0}-{y0+1}: privat minus PPM SE {s:.2f} (MDE {2.8*s:.1f}) | bara privat SE {s2:.2f} | bara PPM SE {s3:.2f} | fonder {G}, obs {len(W)}   <-- riktiga bytet, bara SE")
    else: print(f"{y0}-{y0+1}: privat minus PPM b {b:+.2f} se {s:.2f} t {b/s:+.2f} | bara privat b {b2:+.2f} se {s2:.2f} | bara PPM b {b3:+.2f} se {s3:.2f} | fonder {G}, obs {len(W)}")
