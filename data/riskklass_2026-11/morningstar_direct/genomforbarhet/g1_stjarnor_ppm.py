# Punkt 1, 2, 9: antal och tackning. Inga flodesutfall (bara om formogenhetsdata finns).
import pandas as pd, numpy as np, glob, os
H=os.path.expanduser("~/mnt"); per=lambda s: pd.PeriodIndex(s,freq="M")
L=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz",low_memory=False,usecols=["SecId","t","star","cat","fundid","roll","institutionalonly","performanceid","Inception Date"])
L["t"]=per(L.t)
V=pd.concat([pd.read_csv(f,usecols=["performanceId","ym","tna_class","nf_class"]) for f in glob.glob(f"{H}/shof_riskklass_resultat/val_monthly_*.csv")+glob.glob(f"{H}/shof_riskklass_resultat/privat/val_monthly_*.csv")],ignore_index=True)
V=V[V.tna_class.notna()&V.nf_class.notna()].drop_duplicates(["performanceId","ym"]); V["t"]=per(V.ym); V["has"]=True
vk=set(zip(V.performanceId,V.t.astype("int64")))
P0,P1=pd.Period("2019-01","M"),pd.Period("2025-12","M")
print("=== 1. Olika stjarnor inom samma fond")
u=L.drop_duplicates("SecId"); print("klasser per fond i Direct:",u.groupby("fundid").SecId.nunique().value_counts().to_dict())
print("huvudklasser som sjalva ar institutionella:",int((u[u.roll=="huvudklass"].institutionalonly==1).sum()),"av",int((u.roll=="huvudklass").sum()))
A=L[(L.t>=P0)&(L.t<=P1)]
h=A[A.roll=="huvudklass"][["fundid","t","star","performanceid","institutionalonly"]].rename(columns={"star":"s_h","performanceid":"p_h","institutionalonly":"io_h"})
i=A[A.roll=="institutionell"][["fundid","t","star","performanceid"]].rename(columns={"star":"s_i","performanceid":"p_i"})
B=h.merge(i,on=["fundid","t"]); print("fonder med bada klasserna:",B.fundid.nunique(),"| fondmanader:",len(B))
def rep(B,nm):
    S=B.dropna(subset=["s_h","s_i"]); d=(S.s_h-S.s_i).abs()
    ti=S.t.astype("int64")
    fl=np.array([(p,t) in vk and (p,t-1) in vk and (q,t) in vk and (q,t-1) in vk for p,q,t in zip(S.p_h,S.p_i,ti)])
    print(f"  {nm}: fondmanader med stjarna i bada {len(S)} ({S.fundid.nunique()} fonder) | lika {(d==0).mean():.3f} | skiljer 1 {(d==1).mean():.3f} | skiljer 2+ {(d>=2).mean():.3f}")
    print(f"     med formogenhet for bada klasserna (denna och forra manaden): {int(fl.sum())} fondmanader, {S[fl].fundid.nunique()} fonder; darav olika stjarna {int((fl&(d.values>0)).sum())} fondmanader i {S[fl&(d.values>0)].fundid.nunique()} fonder")
    sw=S.assign(d=(S.s_h-S.s_i)).sort_values(["fundid","t"]); ch=(sw.groupby("fundid").d.diff().abs()>0).sum(); print(f"     antal ganger skillnaden i stjarnor andras inom fond: {int(ch)}")
rep(B,"alla par"); rep(B[B.io_h!=1],"huvudklassen ar privatsparklass")
print("\n=== 2. Forsta stjarnan")
S=L.sort_values(["SecId","t"]).copy(); S["has"]=S.star.notna()
first=S[S.has].groupby("SecId").t.min().rename("t0"); st=S.groupby("SecId").t.min().rename("tmin")
F=pd.concat([first,st],axis=1).dropna(); F=F[F.t0>pd.Period("2018-01","M")]
F=F.join(u.set_index("SecId")[["performanceid","Inception Date","roll","institutionalonly"]])
F["incep"]=pd.to_datetime(F["Inception Date"],errors="coerce"); F["age"]=(F.t0.dt.year-F.incep.dt.year)*12+(F.t0.dt.month-F.incep.dt.month)
r0=S.merge(F[["t0"]],left_on=["SecId","t"],right_on=["SecId","t0"]).set_index("SecId").star; F["r0"]=r0
print("klasser vars forsta stjarna ligger efter 2018-01:",len(F)); print("  alder vid forsta stjarna, kvantiler:",F.age.quantile([.05,.25,.5,.75,.95]).to_dict())
G=F[F.age.between(30,48)]; print("  darav alder 30-48 manader (riktig forsta stjarna):",len(G),"| huvudklass, inte institutionell:",int(((G.roll=="huvudklass")&(G.institutionalonly!=1)).sum()))
print("  per ar:",G.t0.dt.year.value_counts().sort_index().to_dict()); print("  forsta betyg:",G.r0.value_counts().sort_index().to_dict())
t0=G.t0.astype("int64")
def cov(p,t,a,b): return sum((p,t+k) in vk for k in range(a,b+1))
G=G.assign(nb=[cov(p,t,-12,-1) for p,t in zip(G.performanceid,t0)],na=[cov(p,t,0,12) for p,t in zip(G.performanceid,t0)])
print("  med floden alla 12 man fore och 13 efter:",int(((G.nb==12)&(G.na==13)).sum()),"| minst 10 fore och 11 efter:",int(((G.nb>=10)&(G.na>=11)).sum()),"| minst 6 fore och 11 efter:",int(((G.nb>=6)&(G.na>=11)).sum()))
g2=G[(G.nb>=6)&(G.na>=11)]; print("  bland dem (6 fore, 11 efter): per ar",g2.t0.dt.year.value_counts().sort_index().to_dict(),"| betyg",g2.r0.value_counts().sort_index().to_dict(),"| privatspar-huvudklass",int(((g2.roll=="huvudklass")&(g2.institutionalonly!=1)).sum()))
print("\n=== 9. PPM")
X=pd.read_csv(f"{H}/ftn/crosswalk_ppm_shof.csv")[["fondnr","fundid"]].dropna()
P=pd.read_csv(f"{H}/ppm/ppm_panel_2018_2026.csv",usecols=["fondnr","date","mv_tot","handel_netto"],low_memory=False); P["t"]=per(P.date.str[:7])
P=P[(P.t>=P0)&(P.t<=pd.Period("2023-12","M"))&P.handel_netto.notna()&P.mv_tot.notna()].merge(X,on="fondnr")
print("PPM-fonder 2019-2023 med handel:",P.fondnr.nunique(),"| fondmanader",len(P))
M=L[(L.roll=="huvudklass")][["fundid","t","star","performanceid","institutionalonly"]]
Q=P.merge(M,on=["fundid","t"],how="left")
print("  med fonden i Direct:",Q[Q.performanceid.notna()].fondnr.nunique(),"| med stjarna samma manad:",Q[Q.star.notna()].fondnr.nunique(),"fonder,",int(Q.star.notna().sum()),"fondmanader")
ti=Q.t.astype("int64"); Q["fl"]=[(p,t) in vk and (p,t-1) in vk for p,t in zip(Q.performanceid,ti)]
R=Q[Q.star.notna()&Q.fl&(Q.institutionalonly!=1)]
print("  med stjarna + privatspar-huvudklass med floden samma manad:",R.fondnr.nunique(),"fonder,",len(R),"fondmanader; per ar",R.t.dt.year.value_counts().sort_index().to_dict())
R2=Q[Q.star.notna()&Q.fl]; print("  (om institutionella huvudklasser raknas med:",R2.fondnr.nunique(),"fonder,",len(R2),"fondmanader)")
