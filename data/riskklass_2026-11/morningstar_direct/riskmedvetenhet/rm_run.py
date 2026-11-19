# Riskmedvetenhet: test enligt claude/DEKLARATION_riskmedvetenhet_forlustrisk_2026-11-18.md (med tillagg).
import pandas as pd, numpy as np
P=pd.read_pickle("rm_panel.pkl")
A=P[P.t>=pd.Period("2020-01","M")].dropna(subset=["cat_lag","loss60","sig60","ret12","ret36","ret60","f19","tna_lag","age_m"]).copy()
A["tt"]=A.t.astype(str)+"_"+A.cat_lag
A["ccy"]=A.ccy.fillna("NA")
# rattelse fore tolkning: f19 ar otrimmat och har extremvarden (sma TNA). Winsoriseras 1/99 per manad.
q=A.groupby("t").f19.transform; A["f19"]=A.f19.clip(q(lambda x:x.quantile(.01)),q(lambda x:x.quantile(.99)))
def demean(D,X,keys,it=60):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def fit(D,X,keys):
    y=demean(D,D[["f"]],keys).values[:,0]; Xd=demean(D,X,keys).values
    b=np.linalg.lstsq(Xd,y,rcond=None)[0]; e=y-Xd@b; XtXi=np.linalg.pinv(Xd.T@Xd)
    sc=pd.DataFrame(Xd*e[:,None]).groupby(D.fundid.values).sum().values; G=len(sc)
    V=XtXi@(sc.T@sc)@XtXi*G/(G-1); return b*12,V*144,G
def sdw(D,c):  # sd inom kategori x manad
    r=D[c]-D.groupby("tt")[c].transform("mean"); return r.std()
def ctrl(D):
    return pd.DataFrame({"r12":D.ret12,"r36":D.ret36,"r60":D.ret60,"f19":D.f19,"ltna":np.log(D.tna_lag),
                         "lage":np.log(D.age_m.clip(lower=1)),"fee":D.kiid_avgift},index=D.index)
def line(nm,b,V,i):
    se=np.sqrt(V[i,i]); print(f"  {nm:<40}{b[i]:+6.2f} [{b[i]-1.96*se:+6.2f}; {b[i]+1.96*se:+6.2f}]  t {b[i]/se:+5.2f}")
keys=["tt","ccy"]
def block(D,title):
    sL=sdw(D,"loss60"); sS=sdw(D,"sig60")
    D=D.copy(); D["loss_s"]=D.loss60/sL; D["sig_s"]=D.sig60/sS
    print(f"\n=== {title}: {len(D)} fondmanader, {D.fundid.nunique()} fonder. 1 sd inom kat x man: forlust {sL:.3f}, svangning {sS:.2f} pp")
    b,V,G=fit(D,pd.concat([D[["loss_s"]],ctrl(D)],axis=1),keys); print("Kol 1 (huvudtest), utan stjarna:"); line("forlustrisk (per 1 sd)",b,V,0)
    R=D[D.star_lag.notna()]
    b,V,G=fit(R,pd.concat([R[["loss_s"]],ctrl(R)],axis=1),keys); print(f"Kol 1, samma delurval som kol 2 ({len(R)} obs):"); line("forlustrisk (per 1 sd)",b,V,0)
    b,V,G=fit(R,pd.concat([R[["loss_s","star_lag"]],ctrl(R)],axis=1),keys); print("Kol 2, med stjarna:"); line("forlustrisk (per 1 sd)",b,V,0); line("stjarna (positiv kontroll, per stjarna)",b,V,1)
    print(f"  halv stjarna = {b[1]/2:+.2f}")
    b,V,G=fit(D,pd.concat([D[["loss_s","sig_s"]],ctrl(D)],axis=1),keys); print("Kol 3, kapplopning, utan stjarna:"); line("forlustrisk (per 1 sd)",b,V,0); line("svangning (per 1 sd)",b,V,1)
eq=A.cat_lag.str.contains("Equity")
block(A[eq],"AKTIEFONDER (huvudurval)")
block(A,"ALLA FONDER (robusthet)")
