# Dos vid bytet: antal per gammal klass och volatilitetsband. Bara antal.
import pandas as pd, numpy as np, os
H=os.path.expanduser("~/mnt")
E=pd.read_pickle("etiketter.pkl")
R=pd.read_csv(f"{H}/shof_riskklass_resultat/riskmatt/riskmatt_manad_alla.csv.gz"); R=R[R.ym=="2022-12"].drop_duplicates("pid").set_index("pid")
E["sig_w"]=E.performanceid.map(R.sig_w); E["vev"]=E.performanceid.map(R.vev)
E["dos"]=E.srri22-E.sri23
K=pd.read_pickle(f"{H}/morningstar_direct/tvillingar/tv_klasser.pkl")
K["y"]=K.t.dt.year
n=K.groupby(["SecId","y"]).size().unstack(fill_value=0)
E["fl2223"]=E.SecId.map(((n.get(2022,0)>=9)&(n.get(2023,0)>=9)))
E["fl2223"]=E.fl2223.fillna(False).astype(bool)
# tvilling med floden samma manader
pr=K[(K.roll=="huvudklass")&(K.institutionalonly!=1)][["fundid","t","f","SecId"]]; ins=K[K.roll=="institutionell"][["fundid","t","f"]]
T=pr.merge(ins,on=["fundid","t"],suffixes=("_p","_i")); T["y"]=T.t.dt.year
m=T.groupby(["SecId","y"]).size().unstack(fill_value=0)
E["tv2223"]=E.SecId.map(((m.get(2022,0)>=9)&(m.get(2023,0)>=9))).fillna(False).astype(bool)
E.to_pickle("etiketter.pkl")
P=E[(E.roll=="huvudklass")&(E.institutionalonly!=1)&E.srri22.notna()&E.sri23.notna()].copy()
print("privata huvudklasser med ra SRRI sep-dec 2022 och ra SRI jan-jun 2023:",len(P),"| dos:",P.dos.value_counts().sort_index().to_dict())
print("\nGammal klass x dos (antal):"); print(pd.crosstab(P.srri22,P.dos))
P["band"]=pd.cut(P.sig_w,[0,10,12,15,20,25,30,200],right=False,labels=["<10","10-12","12-15","15-20","20-25","25-30",">30"])
print("\nVolatilitetsband (sig_w dec 2022) x dos:"); print(pd.crosstab(P.band,P.dos,margins=True))
print("saknar sig_w:",int(P.sig_w.isna().sum()))
print("\nVantat enligt sagtanden: 10-12 tva steg, 12-15 ett, 15-20 tva, 20-25 ett, 25-30 tva. Andel med vantad dos per band:")
exp={"10-12":2,"12-15":1,"15-20":2,"20-25":1,"25-30":2}
for b,d in exp.items():
    g=P[P.band==b]; print(f"  {b}: {int((g.dos==d).sum())} av {len(g)} ({(g.dos==d).mean():.0%})")
Q=P[P.dos.isin([0,1,2])]
print("\nMed floden minst 9 man bade 2022 och 2023 (gammal klass x dos):"); print(pd.crosstab(Q[Q.fl2223].srri22,Q[Q.fl2223].dos,margins=True))
print("\n... och med institutionell tvilling med floden samma manader:"); print(pd.crosstab(Q[Q.tv2223].srri22,Q[Q.tv2223].dos,margins=True))
print("\nSamma, per band:"); print(pd.crosstab(Q[Q.fl2223].band,Q[Q.fl2223].dos,margins=True)); print(pd.crosstab(Q[Q.tv2223].band,Q[Q.tv2223].dos,margins=True))
