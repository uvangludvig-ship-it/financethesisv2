# T2 styrkekontroll: bara antal och standardfel. Ingen punktskattning skrivs ut.
import pandas as pd, numpy as np
P=pd.read_pickle("t2_panel.pkl")
A=P.dropna(subset=["cat_lag","label_lag","ret12","sig12","age_m"]).copy()
A=A[A.sig12.between(0.5,60)]
print("analysurval:",len(A),"fondmanader,",A.fundid.nunique(),"fonder")
print(A.groupby("rated").agg(obs=("f","size"),fonder=("fundid","nunique")))
U=A[~A.rated]
print("\nUtan betyg, efter alder (manader):")
print(pd.cut(U.age_m,[-1,23,35,47,59,119,999]).value_counts().sort_index())
print("Utan betyg per ar:"); print(U.t.dt.year.value_counts().sort_index().to_dict())
print("Utan betyg, vanligaste kategorier:"); print(U.cat_lag.value_counts().head(12))
# har fonden nagonsin betyg?
ever=P.groupby("fundid").rated.max()
U=U.assign(ever=U.fundid.map(ever))
print("\nUtan betyg: fondmanader i fonder som senare/nagon gang har betyg:",int(U.ever.sum()),"| aldrig betyg:",int((~U.ever).sum()),"| fonder aldrig betyg:",U[~U.ever].fundid.nunique())
# klassbyten inom perioder utan betyg (exkl. skalbytet jan 2023)
def changes(D):
    D=D.sort_values(["fundid","t"]); d=D.groupby("fundid").label_lag.diff()
    return int(((d.abs()>0)&(D.t!=pd.Period("2023-02","M"))&(D.t!=pd.Period("2023-01","M"))).sum())
print("klassbyten (exkl. skalbytet): utan betyg",changes(A[~A.rated]),"| med betyg",changes(A[A.rated]))
print("spridning i visad klass inom kategori x manad (std av avvikelse): utan",round((U.label_lag-U.groupby(['t','cat_lag']).label_lag.transform('mean')).std(),3),
      "| med",round((A[A.rated].label_lag-A[A.rated].groupby(['t','cat_lag']).label_lag.transform('mean')).std(),3))
# --- standardfel utan punktskattning
def demean(D,X,keys,it=60):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def se_only(D,X,keys):
    y=demean(D,D[["f"]],keys).values[:,0]; Xd=demean(D,X,keys).values
    b=np.linalg.lstsq(Xd,y,rcond=None)[0]; e=y-Xd@b; XtXi=np.linalg.pinv(Xd.T@Xd)
    sc=pd.DataFrame(Xd*e[:,None]).groupby(D.fundid.values).sum().values; G=len(sc)
    V=XtXi@(sc.T@sc)@XtXi*G/(G-1); return np.sqrt(np.diag(V))
A["tt"]=A.t.astype(str)+"_"+A.cat_lag
r=A.rated.astype(float); u=1-r; po=A.post.astype(float)
A["rank12"]=A.groupby(["t","cat_lag"]).ret12.rank(pct=True)
X=pd.DataFrame({"lab_r":A.label_lag*r,"lab_u":A.label_lag*u,"star":A.star_lag.fillna(0)*r,"unr":u,
   "r1":A.rank12,"r2":A.rank12**2,"s1":A.sig12/10,"s2":(A.sig12/10)**2,"s3":(A.sig12/10)**3,
   "s1p":A.sig12/10*po,"s2p":(A.sig12/10)**2*po,"s3p":(A.sig12/10)**3*po,"age":np.log(A.age_m.clip(lower=1))},index=A.index)
for nm,keys in [("A: fond + manad x kategori",["fundid","tt"]),("B: manad x kategori",["tt"])]:
    se=se_only(A,X,keys)*12
    print(f"\n{nm}: SE (pp/ar) klass med betyg {se[0]:.2f} | klass utan betyg {se[1]:.2f} | stjarna {se[2]:.2f}")
    print(f"   MDE 80 % (2,8 x SE): med {2.8*se[0]:.1f} | utan {2.8*se[1]:.1f}")
