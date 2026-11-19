# Punkt 3, 4, 6, 7, 8: etiketternas fordelning och byten. Inga floden.
import pandas as pd, numpy as np, os
H=os.path.expanduser("~/mnt"); per=lambda s: pd.PeriodIndex(s,freq="M"); pd.set_option("display.width",200)
L=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz",low_memory=False,usecols=["SecId","t","srri","sri","cat","fundid","roll","institutionalonly","performanceid"]); L["t"]=per(L.t)
u=L.drop_duplicates("SecId").set_index("SecId"); main=set(u[u.roll=="huvudklass"].index)
sri=pd.read_pickle("ra_sri.pkl"); Hh=pd.read_pickle("ra_srri_hist.pkl"); Hh["t"]=Hh.date.dt.to_period("M")
print("=== 3. Bytet januari 2023 (huvudklasser, raa varden)")
o=Hh[(Hh.t>=pd.Period("2022-09","M"))&(Hh.t<=pd.Period("2022-12","M"))].sort_values("date").groupby("SecId").srri.last().rename("old")
o2=Hh[(Hh.t>=pd.Period("2022-11","M"))&(Hh.t<=pd.Period("2022-12","M"))].sort_values("date").groupby("SecId").srri.last()
ns=sri[[c for c in sri.columns if pd.Period("2023-01","M")<=c<=pd.Period("2023-06","M")]]; new=ns.bfill(axis=1).iloc[:,0].rename("new")
D=pd.concat([o,new],axis=1).dropna(); D=D[D.index.isin(main)]
c22=L[L.t==pd.Period("2022-12","M")].set_index("SecId").cat; D["cat"]=c22.reindex(D.index); D["akt"]=D.cat.fillna("").str.contains("Equity"); D["d"]=D.new-D.old
print("huvudklasser med SRRI sep-dec 2022 och SRI jan-jun 2023:",len(D),"(SRRI just nov-dec:",int(D.index.isin(o2.index).sum()),") | aktiekategorier:",int(D.akt.sum()))
print(pd.crosstab(D.old.astype(int),D.new.astype(int),margins=True))
def dist(x): 
    v=x.d.clip(-3,2).value_counts(normalize=True).sort_index(); return {int(k):round(float(a),3) for k,a in v.items()}
print("forandring, alla:",dist(D)); print("forandring, aktie:",dist(D[D.akt])); print("forandring, ovriga:",dist(D[~D.akt]))
for nm,X in [("alla",D),("aktie",D[D.akt])]:
    m=X.groupby("old").new.agg(lambda s:s.value_counts().iloc[0]); n=X.groupby("old").size()
    print(f"  {nm}: andel som INTE fick den vanligaste nya klassen for sin gamla klass: {1-m.sum()/n.sum():.3f}; per gammal klass:",{int(k):round(1-m[k]/n[k],3) for k in n.index})
print("  aktie, gammal klass 6 -> ny:",D[D.akt&(D.old==6)].new.value_counts().sort_index().to_dict(),"| gammal 5 -> ny:",D[D.akt&(D.old==5)].new.value_counts().sort_index().to_dict())
print("\n=== 4. Hoptryckning (visad klass inom kategori och manad, huvudklasser, minst 3 fonder)")
A=L[L.SecId.isin(main)&L.cat.notna()].copy(); A["lab"]=np.where(A.t<=pd.Period("2022-12","M"),A.srri,A.sri); A=A.dropna(subset=["lab"])
A=A[(A.t>=pd.Period("2019-01","M"))&(A.t<=pd.Period("2025-12","M"))]
g=A.groupby(["t","cat"]).lab.agg(["std","nunique","size"]).reset_index(); g=g[g["size"]>=3]; g["y"]=g.t.dt.year; g["akt"]=g.cat.str.contains("Equity")
for nm,X in [("alla kategorier",g),("aktiekategorier",g[g.akt])]:
    r=X.groupby("y").agg(std=("std","mean"),samma=("nunique",lambda s:(s==1).mean()),celler=("size","size")); print(nm); print(r.round(3).T)
tot=A.assign(y=A.t.dt.year).groupby("y").lab.agg(lambda s:s.value_counts(normalize=True).sort_index().round(2).to_dict()); print("fordelning av visad klass per ar (alla huvudklasser):"); print(tot.to_string())
print("\n=== 6. Tillverkarens skon (rå SRI mot klass ur VEV samma manad, huvudklasser)")
R=pd.read_csv(f"{H}/shof_riskklass_resultat/riskmatt/riskmatt_manad_alla.csv.gz"); R["t"]=per(R.ym)
R["kl"]=np.digitize(R.vev,[0.5,5,12,20,30,80])+1
pid=u.performanceid
S=sri.stack().rename("sri").reset_index(); S.columns=["SecId","t","sri"]; S=S[S.SecId.isin(main)]; S["pid"]=S.SecId.map(pid)
S=S.merge(R[["pid","t","vev","kl"]],on=["pid","t"],how="inner"); S["y"]=S.t.dt.year; S["d"]=np.sign(S.sri-S.kl)
T=S[S.y.between(2023,2025)]
print(T.groupby("y").d.agg(n="size",hogre=lambda s:(s>0).mean(),lika=lambda s:(s==0).mean(),lagre=lambda s:(s<0).mean()).round(3))
T2=T[T.vev.between(6,29)&~((T.vev-12).abs()<1)&~((T.vev-20).abs()<1)]; print("  langt fran granserna (VEV 6-29, minst 1 pp fran 12 och 20):",len(T2),"hogre",round((T2.d>0).mean(),3),"lika",round((T2.d==0).mean(),3),"lagre",round((T2.d<0).mean(),3))
print("\n=== 7. Klassbyten (huvudklasser)")
Hm=Hh[Hh.SecId.isin(main)].sort_values(["SecId","date"]); Hm["dd"]=Hm.groupby("SecId").srri.diff(); C=Hm[(Hm.dd.abs()>0)&Hm.date.dt.year.between(2019,2022)]
print("SRRI-byten per ar (upp/ned):",{int(y):(int((x.dd>0).sum()),int((x.dd<0).sum())) for y,x in C.groupby(C.date.dt.year)},"| fonder:",C.SecId.nunique())
Sm=sri[sri.index.isin(main)].stack().rename("sri").reset_index(); Sm.columns=["SecId","t","sri"]; Sm=Sm.sort_values(["SecId","t"]); Sm["dd"]=Sm.groupby("SecId").sri.diff(); Sm["gap"]=Sm.t.astype("int64")-Sm.groupby("SecId").t.shift(1).astype("int64")
E=Sm[(Sm.dd.abs()>0)&(Sm.t>=pd.Period("2023-03","M"))]
print("SRI-byten fran mars 2023 per ar (upp/ned):",{int(y):(int((x.dd>0).sum()),int((x.dd<0).sum())) for y,x in E.groupby(E.t.dt.year)},"| totalt",len(E),"i",E.SecId.nunique(),"klasser | storlek:",E.dd.value_counts().sort_index().to_dict())
E=E.assign(pid=E.SecId.map(pid)); Rk=R.set_index(["pid","t"]).kl
def crossed(p,t):
    v=[Rk.get((p,t+k)) for k in range(-3,4)]; v=[x for x in v if x is not None and x==x]
    return np.nan if len(v)<4 else float(len(set(v))>1)
E["cr"]=[crossed(p,t) for p,t in zip(E.pid,E.t)]
print("  med VEV-klass i fonstret +-3 man:",int(E.cr.notna().sum()),"| beraknad klass korsar en grans:",int((E.cr==1).sum()),"| korsar inte:",int((E.cr==0).sum()))
E2=E[E.cr.notna()].merge(R[["pid","t","vev"]],on=["pid","t"],how="left"); near=((E2.vev-12).abs()<1.5)|((E2.vev-20).abs()<1.5)|((E2.vev-5).abs()<1)|((E2.vev-30).abs()<2)
print("  bland dem som inte korsar: nara en grans (inom 1-2 pp):",int(((E2.cr==0)&near).sum()),"| langt fran:",int(((E2.cr==0)&~near).sum()))
print("\n=== 8. SFDR")
F=pd.read_csv(f"{H}/morningstar_direct/direct_sfdr_manad.csv.gz").set_index("SecId"); F.columns=per(F.columns)
print("klasser i filen:",len(F),"| med nagon uppgift:",int(F.notna().any(axis=1).sum()),"| huvudklasser med uppgift:",int(F[F.index.isin(main)].notna().any(axis=1).sum()),"| varden:",pd.Series(F.values.ravel()).value_counts().to_dict())
print("obs per manad (urval):",F.notna().sum().iloc[[0,6,12,18,21,22,24,30,36,48,60,67]].to_dict())
Fs=F.stack().rename("a").reset_index(); Fs.columns=["SecId","t","a"]; Fs=Fs.sort_values(["SecId","t"]); Fs["prev"]=Fs.groupby("SecId").a.shift(1); Ch=Fs[Fs.prev.notna()&(Fs.a!=Fs.prev)]
Ch=Ch.assign(riktning=Ch.prev.astype(int).astype(str)+"->"+Ch.a.astype(int).astype(str),y=Ch.t.dt.year)
print("byten, alla klasser:"); print(pd.crosstab(Ch.riktning,Ch.y,margins=True))
Cm=Ch[Ch.SecId.isin(main)]; print("byten, huvudklasser:",len(Cm),"i",Cm.SecId.nunique(),"klasser;",Cm.riktning.value_counts().to_dict())
