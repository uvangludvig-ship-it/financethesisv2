# PPM-testet enligt claude/DEKLARATION_PPM_stjarnan_visas_inte_2026-11-17.md
import pandas as pd, numpy as np
D=pd.read_pickle("ppm_panel_test.pkl"); D=D[(D.t>=pd.Period("2019-01","M"))&(D.t<=pd.Period("2023-12","M"))]
def sample(D,need_oth=True):
    m=D.cons&(D.since>=12)&(D.left>=6)&(D.mv_lag>=10e6)&D.f_ppm.notna()&D.star_lag.notna()&D.cat_lag.notna()&D.rank12.notna()&D.rank36.notna()&D.sig60.between(1,40)
    if need_oth: m&=D.vcons&(D.oth_lag_sek>=100e6)&D.f_oth.notna()&(D.share_lag<0.9)&D.ccy.isin(["SEK","EUR","USD","NOK","DKK"])
    A=D[m].copy()
    for c in (["f_ppm","f_oth"] if need_oth else ["f_ppm"]):
        lo=A.groupby("t")[c].transform(lambda x:x.quantile(.01)); hi=A.groupby("t")[c].transform(lambda x:x.quantile(.99)); A=A[(A[c]>=lo)&(A[c]<=hi)]
    A["tc"]=A.t.astype(str)+"_"+A.cat_lag; A["tf"]=A.t.astype(str)+"_"+A.fondtyp.astype(str); return A
def dm(D,X,keys,it=100):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def ctrl(A):
    s=A.sig60/10; return pd.DataFrame({"star":A.star_lag,"r12":A.rank12,"r12b":A.rank12**2,"r36":A.rank36,"r36b":A.rank36**2,"s1":s,"s2":s**2,"s3":s**3},index=A.index)
def ci(b,se): return f"{b:+6.2f} [{b-1.96*se:+6.2f}; {b+1.96*se:+6.2f}]  t {b/se:+5.2f}"
def run(A,keys,title,cols=("f_ppm","f_oth")):
    Xd=dm(A,ctrl(A),keys).values; XtXi=np.linalg.pinv(Xd.T@Xd); B=[];S=[]
    for c in cols:
        y=dm(A,A[[c]],keys).values[:,0]; b=XtXi@Xd.T@y; B.append(b[0]*12); S.append(pd.DataFrame(Xd*(y-Xd@b)[:,None]).groupby(A.fondnr.values).sum().values)
    G=len(S[0]); k=G/(G-1); V=lambda a,c:(XtXi@(a.T@c)@XtXi*k)[0,0]*144
    print(f"\n{title}  (fonder {G}, fondmanader {len(A)})")
    print("  stjarna, PPM-flodet (s_P)      ",ci(B[0],np.sqrt(V(S[0],S[0]))))
    if len(cols)==2:
        print("  stjarna, ovrigas flode (s_O)   ",ci(B[1],np.sqrt(V(S[1],S[1]))))
        d=B[1]-B[0]; sd=np.sqrt(V(S[0],S[0])+V(S[1],S[1])-2*V(S[0],S[1])); print("  skillnad s_O - s_P             ",ci(d,sd))
A=sample(D)
run(A,["fondnr","tc"],"A (huvud): fond + manad x Morningstar-kategori")
run(A,["fondnr","tf"],"B: fond + manad x PPM-fondtyp")
run(A,["tc"],"C: manad x Morningstar-kategori")
A2=sample(D,False); run(A2,["fondnr","tc"],"Tillagg 3: bara PPM-flodet, alla PPM-fonder med stjarna, spec A",cols=("f_ppm",))
