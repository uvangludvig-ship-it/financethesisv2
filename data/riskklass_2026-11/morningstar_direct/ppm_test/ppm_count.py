# Styrkekontroll: bara antal och standardfel. Inga punktskattningar.
import pandas as pd, numpy as np
D=pd.read_pickle("ppm_panel_test.pkl")
T0,T1=pd.Period("2019-01","M"),pd.Period("2023-12","M")
D=D[(D.t>=T0)&(D.t<=T1)]
print("PPM-fondmanader 2019-2023:",len(D),"fonder",D.fondnr.nunique())
print("med fondflode ur SHoF:",int(D.tna_lag.notna().sum()),"| valuta:",D.ccy.value_counts().to_dict())
for cc,S in D[D.share_lag.notna()].groupby("ccy"): print("  PPM-andel av fonden",cc,len(S),S.share_lag.quantile([.01,.1,.5,.9,.99]).round(4).to_dict(),"andel >1:",round((S.share_lag>1).mean(),4))
def sample(D,need_oth=True):
    m=D.cons&(D.since>=12)&(D.left>=6)&(D.mv_lag>=10e6)&D.f_ppm.notna()&D.star_lag.notna()&D.cat_lag.notna()&D.rank12.notna()&D.rank36.notna()&D.sig60.between(1,40)
    if need_oth: m&=D.vcons&(D.oth_lag_sek>=100e6)&D.f_oth.notna()&(D.share_lag<0.9)&D.ccy.isin(["SEK","EUR","USD","NOK","DKK"])
    A=D[m].copy()
    for c in (["f_ppm","f_oth"] if need_oth else ["f_ppm"]):
        lo=A.groupby("t")[c].transform(lambda x:x.quantile(.01)); hi=A.groupby("t")[c].transform(lambda x:x.quantile(.99)); A=A[(A[c]>=lo)&(A[c]<=hi)]
    return A
def dm(D,X,keys,it=80):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def ctrl(A): 
    s=A.sig60/10; return pd.DataFrame({"star":A.star_lag,"r12":A.rank12,"r12b":A.rank12**2,"r36":A.rank36,"r36b":A.rank36**2,"s1":s,"s2":s**2,"s3":s**3},index=A.index)
def se_pair(A,keys):
    Xd=dm(A,ctrl(A),keys).values; out=[]; res=[]
    XtXi=np.linalg.pinv(Xd.T@Xd)
    for c in ["f_ppm","f_oth"]:
        y=dm(A,A[[c]],keys).values[:,0]; b=XtXi@Xd.T@y; res.append(y-Xd@b)
    S=[pd.DataFrame(Xd*e[:,None]).groupby(A.fondnr.values).sum().values for e in res]; G=len(S[0]); k=G/(G-1)
    V=lambda a,b_: (XtXi@(a.T@b_)@XtXi*k)[0,0]
    se_p=np.sqrt(V(S[0],S[0]))*12; se_o=np.sqrt(V(S[1],S[1]))*12; se_d=np.sqrt(V(S[0],S[0])+V(S[1],S[1])-2*V(S[0],S[1]))*12
    return se_p,se_o,se_d
A=sample(D); A["tc"]=A.t.astype(str)+"_"+A.cat_lag; A["tf"]=A.t.astype(str)+"_"+A.fondtyp.astype(str)
print("\nGemensamt urval (bada floden):",len(A),"fondmanader,",A.fondnr.nunique(),"fonder; per ar",A.t.dt.year.value_counts().sort_index().to_dict())
n=A.groupby("tc").fondnr.transform("size"); print("  i celler manad x Morningstar-kategori med minst 2 fonder:",int((n>=2).sum()),"| kategorier:",A.cat_lag.nunique())
print("  stjarnbyten inom fond:",int((A.sort_values(['fondnr','t']).groupby('fondnr').star_lag.diff().abs()>0).sum()), "| stjarnfordelning:",A.star_lag.value_counts().sort_index().to_dict())
print("  spridning (std) i floden, procent per manad: PPM",round(A.f_ppm.std(),2),"ovriga",round(A.f_oth.std(),2))
for nm,keys in [("A fond + manad x Morningstar-kategori",["fondnr","tc"]),("B fond + manad x fondtyp (PPM)",["fondnr","tf"]),("C manad x Morningstar-kategori",["tc"])]:
    sp,so,sd=se_pair(A,keys); print(f"  {nm}: SE stjarna PPM {sp:.2f} | ovriga {so:.2f} | skillnad {sd:.2f}  -> MDE skillnad {2.8*sd:.1f} pp/ar")
A2=sample(D,False); print("\nBara PPM-flode, alla valutor:",len(A2),"fondmanader,",A2.fondnr.nunique(),"fonder")
