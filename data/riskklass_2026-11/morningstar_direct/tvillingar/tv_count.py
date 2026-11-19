# Styrka for tvillingtestet: bara antal och standardfel. Inga punktskattningar.
import pandas as pd, numpy as np
P=pd.read_pickle("tv_klasser.pkl")
R=P[(P.roll=="huvudklass")&(P.institutionalonly!=1)]; I=P[P.roll=="institutionell"]
T=R.merge(I,on=["fundid","t"],suffixes=("_r","_i"))
print("fondmanader med flode i bada klasserna:",len(T),"fonder",T.fundid.nunique())
S=T.dropna(subset=["star_lag_r","star_lag_i"]).copy()
S["dstar"]=S.star_lag_r-S.star_lag_i; S["df"]=S.f_r-S.f_i
print("... och stjarna i bada:",len(S),"fonder",S.fundid.nunique(),"| per ar",S.t.dt.year.value_counts().sort_index().to_dict())
print("stjarngap (privat minus inst):",S.dstar.value_counts().sort_index().to_dict())
print("samma valuta:",round((S.ccy_r==S.ccy_i).mean(),3),"| samma kategori:",round((S.cat_lag_r==S.cat_lag_i).mean(),3))
S=S.sort_values(["fundid","t"]); ch=S.groupby("fundid").dstar.diff().abs()>0
print("gapet andras inom par:",int(ch.sum()),"ganger i",S[ch].fundid.nunique(),"fonder")
dr=S.groupby("fundid").star_lag_r.diff().fillna(0)!=0; di=S.groupby("fundid").star_lag_i.diff().fillna(0)!=0
print("bara privatklassens stjarna andras:",int((dr&~di).sum()),"| bara institutionellas:",int((di&~dr).sum()),"| bada samtidigt:",int((dr&di).sum()))
print("alder i manader: privat median",S.age_m_r.median(),"inst median",S.age_m_i.median(),"| andel dar institutionella ar yngre:",round((S.age_m_i<S.age_m_r).mean(),3))
print("spridning: flode privat",round(S.f_r.std(),2),"inst",round(S.f_i.std(),2),"skillnad",round(S.df.std(),2),"| korrelation privat-inst flode",round(S.f_r.corr(S.f_i),3))
def dm(D,X,keys,it=60):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def se(D,y,X,keys):
    yd=dm(D,D[[y]],keys).values[:,0]; Xd=dm(D,X,keys).values; XtXi=np.linalg.pinv(Xd.T@Xd); b=XtXi@Xd.T@yd; e=yd-Xd@b
    sc=pd.DataFrame(Xd*e[:,None]).groupby(D.fundid.values).sum().values; G=len(sc); return np.sqrt(np.diag(XtXi@(sc.T@sc)@XtXi*G/(G-1)))*12
S["tt"]=S.t.astype(str)
X=pd.DataFrame({"dstar":S.dstar},index=S.index)
print("\nSE for stjarngapets koefficient (pp/ar per stjarna), flodesskillnad privat minus inst:")
for nm,keys in [("par + manad (huvud)",["fundid","tt"]),("bara manad",["tt"])]:
    s=se(S,"df",X,keys)[0]; print(f"  {nm}: SE {s:.2f} -> MDE {2.8*s:.1f}")
S["dr12"]=S.ret12_r-S.ret12_i
Q=S.dropna(subset=["dr12"]); X2=pd.DataFrame({"dstar":Q.dstar,"dr12":Q.dr12},index=Q.index)
s=se(Q,"df",X2,["fundid","tt"])[0]; print(f"  par + manad + skillnad i 12 man avkastning: SE {s:.2f} -> MDE {2.8*s:.1f}  (obs {len(Q)})")
# unga institutionella klasser utan stjarna bredvid en gammal privatklass med stjarna
Y=T[T.star_lag_r.notna()&T.star_lag_i.isna()]; print("\nprivat har stjarna, institutionella saknar:",len(Y),"fondmanader,",Y.fundid.nunique(),"fonder; omvant:",len(T[T.star_lag_i.notna()&T.star_lag_r.isna()]))
# 2023: behöll institutionella klasser SRRI?
try:
    h=pd.read_pickle("../genomforbarhet/ra_srri_hist.pkl"); print("\nra_srri_hist kolumner:",list(h.columns)[:8],len(h))
except Exception as e: print("ra_srri_hist:",e)
