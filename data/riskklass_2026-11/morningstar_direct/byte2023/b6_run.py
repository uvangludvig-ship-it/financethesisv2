# Bytet 2023 enligt claude/DEKLARATION_tvillingar_och_byte2023_2026-11-17.md: S (huvud), M (sido), positiv kontroll (stjarna).
import pandas as pd, numpy as np, os
H=os.path.expanduser("~/mnt")
E=pd.read_pickle("etiketter.pkl"); K=pd.read_pickle(f"{H}/morningstar_direct/tvillingar/tv_klasser.pkl")
E=E[E.dos.isin([0,1,2])&E.sig_w.notna()&E.srri22.notna()]
D=E.set_index("SecId")[["dos","sig_w","srri22"]]
pr=K[(K.roll=="huvudklass")&(K.institutionalonly!=1)&K.SecId.isin(D.index)].copy().join(D,on="SecId"); pr["y"]=pr.t.dt.year
pr=pr.dropna(subset=["cat_lag"])
def dm(X,keys,it=80):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(k).transform("mean")
    return X
def est(A,y,Xcols,keys):
    ks=[A[k].values for k in keys]; yd=dm(A[[y]],ks).values[:,0]; Xd=dm(A[Xcols],ks).values
    XtXi=np.linalg.pinv(Xd.T@Xd); b=XtXi@Xd.T@yd; e=yd-Xd@b
    sc=pd.DataFrame(Xd*e[:,None]).groupby(A.fundid.values).sum().values; G=len(sc)
    return b*12,np.sqrt(np.diag(XtXi@(sc.T@sc)@XtXi*G/(G-1)))*12,G
W=pr[pr.y.isin([2022,2023])].copy(); n=W.groupby(["SecId","y"]).size().unstack(fill_value=0)
W=W[W.SecId.isin(n[(n[2022]>=9)&(n[2023]>=9)].index)].copy()
W["efter"]=(W.y==2023).astype(float); W["ed"]=W.efter*W.dos; s=W.sig_w/10
for k in (1,2,3): W[f"es{k}"]=W.efter*s**k
W["tt"]=W.t.astype(str); W["tc"]=W.tt+"_"+W.cat_lag.astype(str); W["eo"]=W.efter.astype(int).astype(str)+"_"+W.srri22.astype(int).astype(str)
def show(nm,b,se,i,honest=None):
    h=max(se[i],honest) if honest else se[i]
    print(f"  {nm:<40}{b[i]:+6.2f}  SE {se[i]:.2f}  t {b[i]/se[i]:+5.2f}  95 % [{b[i]-1.96*se[i]:+6.2f}; {b[i]+1.96*se[i]:+6.2f}]"+(f"  | med latsasarens spridning {honest}: [{b[i]-1.96*h:+6.2f}; {b[i]+1.96*h:+6.2f}]" if honest else ""))
print(f"Urval: {W.SecId.nunique()} klasser, {W.fundid.nunique()} fonder, {len(W)} klassmanader 2022-2023. Dos: {W.drop_duplicates('SecId').dos.value_counts().sort_index().to_dict()}")
b,se,G=est(W,"f",["ed"],["SecId","tc","eo"]); print("\nS (HUVUD): Efter x Dos, klass + manad x kategori + Efter x gammal klass. pp/ar per steg siffran foll"); show("Efter x Dos",b,se,0,1.9)
b,se,G=est(W,"f",["ed","es1","es2","es3"],["SecId","tc"]); print("\nM (sido): Efter x Dos, klass + manad x kategori + Efter x polynom i volatilitet"); show("Efter x Dos",b,se,0,2.4)
Q=W.dropna(subset=["star_lag"])
b,se,G=est(Q,"f",["ed","star_lag"],["SecId","tc","eo"]); print(f"\nPositiv kontroll: S med klassens stjarna (klasser {Q.SecId.nunique()}, obs {len(Q)}, stjarnbyten i fonstret {int((Q.sort_values(['SecId','t']).groupby('SecId').star_lag.diff().abs()>0).sum())})"); show("Efter x Dos",b,se,0); show("stjarna, per stjarna",b,se,1)
