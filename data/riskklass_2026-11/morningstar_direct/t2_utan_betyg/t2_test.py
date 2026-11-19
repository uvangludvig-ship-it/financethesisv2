# T2: test enligt claude/DEKLARATION_T2_fonder_utan_stjarnbetyg_2026-11-17.md
import pandas as pd, numpy as np
P=pd.read_pickle("t2_panel.pkl")
A=P.dropna(subset=["cat_lag","label_lag","ret12","sig12","age_m"]).copy()
A=A[A.sig12.between(0.5,60)]
A["tt"]=A.t.astype(str)+"_"+A.cat_lag
A["rank12"]=A.groupby(["t","cat_lag"]).ret12.rank(pct=True)
ever=P.groupby("fundid").rated.max(); A["ever"]=A.fundid.map(ever)
def demean(D,X,keys,it=80):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def fit(D,X,keys):
    y=demean(D,D[["f"]],keys).values[:,0]; Xd=demean(D,X,keys).values
    b=np.linalg.lstsq(Xd,y,rcond=None)[0]; e=y-Xd@b; XtXi=np.linalg.pinv(Xd.T@Xd)
    sc=pd.DataFrame(Xd*e[:,None]).groupby(D.fundid.values).sum().values; G=len(sc)
    V=XtXi@(sc.T@sc)@XtXi*G/(G-1); return b*12,V*144,G
def ctrl(D):
    po=D.post.astype(float); s=D.sig12/10
    return pd.DataFrame({"r1":D.rank12,"r2":D.rank12**2,"s1":s,"s2":s**2,"s3":s**3,"s1p":s*po,"s2p":s**2*po,"s3p":s**3*po,"age":np.log(D.age_m.clip(lower=1))},index=D.index)
def line(nm,b,V,i):
    se=np.sqrt(V[i,i]); print(f"  {nm:<34}{b[i]:+6.2f} [{b[i]-1.96*se:+6.2f}; {b[i]+1.96*se:+6.2f}]  t {b[i]/se:+5.2f}")
def run(D,keys,title):
    r=D.rated.astype(float); u=1-r
    X=pd.concat([pd.DataFrame({"lab_r":D.label_lag*r,"lab_u":D.label_lag*u,"star":D.star_lag.fillna(0)*r,"unr":u},index=D.index),ctrl(D)],axis=1)
    b,V,G=fit(D,X,keys)
    print(f"\n{title}  (fonder {G}, obs {len(D)}, utan betyg {int(u.sum())})")
    line("stjarna (positiv kontroll)",b,V,2); line("klass, med betyg (b_m)",b,V,0); line("klass, utan betyg (b_u)",b,V,1)
    d=b[1]-b[0]; sd=np.sqrt(V[1,1]+V[0,0]-2*V[0,1]); print(f"  {'skillnad b_u - b_m':<34}{d:+6.2f} [{d-1.96*sd:+6.2f}; {d+1.96*sd:+6.2f}]  t {d/sd:+5.2f}")
run(A,["fundid","tt"],"A (huvud): fond + manad x kategori")
run(A,["tt"],"B: manad x kategori")
# tillagg 2: unga mot ovriga utan betyg
r=A.rated.astype(float); y=((~A.rated)&(A.age_m<36)).astype(float); o=((~A.rated)&(A.age_m>=36)).astype(float)
X=pd.concat([pd.DataFrame({"lab_r":A.label_lag*r,"lab_y":A.label_lag*y,"lab_o":A.label_lag*o,"star":A.star_lag.fillna(0)*r,"uy":y,"uo":o},index=A.index),ctrl(A)],axis=1)
for nm,keys in [("A",["fundid","tt"]),("B",["tt"])]:
    b,V,G=fit(A,X,keys); print(f"\nTillagg 2, spec {nm}: utan betyg, yngre an 36 man ({int(y.sum())} obs) och ovriga ({int(o.sum())} obs)")
    line("klass, utan betyg, yngre an 36",b,V,1); line("klass, utan betyg, ovriga",b,V,2)
# tillagg 3: utan fonder som aldrig har betyg
D=A[A.ever].copy()
run(D,["fundid","tt"],"Tillagg 3, spec A: utan fonder som aldrig har betyg")
