# Bytet 2023: vad hande med etiketten i privat- och institutionella klasser? Bara antal. Inga floden.
import pandas as pd, numpy as np, os
H=os.path.expanduser("~/mnt/morningstar_direct")
M=pd.read_csv(f"{H}/direct_manadspanel.csv.gz",usecols=["SecId","fundid","roll","institutionalonly","performanceid"],low_memory=False).drop_duplicates("SecId")
sri=pd.read_pickle(f"{H}/genomforbarhet/ra_sri.pkl"); hh=pd.read_pickle(f"{H}/genomforbarhet/ra_srri_hist.pkl")
P=lambda s: pd.Period(s,"M")
# gammal etikett: sista raa SRRI sep-dec 2022; ny: forsta raa SRI jan-jun 2023
h22=hh[(hh.date>="2022-09-01")&(hh.date<="2022-12-31")].sort_values("date").groupby("SecId").srri.last().rename("srri22")
h23=hh[(hh.date>="2023-02-01")&(hh.date<="2023-06-30")].sort_values("date").groupby("SecId").srri.last().rename("srri23h1")
hlast=hh.groupby("SecId").date.max().rename("srri_sista")
h2325=hh[hh.date>="2023-07-01"].groupby("SecId").size().rename("srri_n_efter_jul23")
c23=[c for c in sri.columns if P("2023-01")<=c<=P("2023-06")]; c22=[c for c in sri.columns if P("2022-07")<=c<=P("2022-12")]
sri23=sri[c23].bfill(axis=1).iloc[:,0].rename("sri23"); sri22=sri[c22].ffill(axis=1).iloc[:,-1].rename("sri_h2_22")
first=sri.notna().idxmax(axis=1).where(sri.notna().any(axis=1)).rename("sri_forsta")
E=M.set_index("SecId").join([h22,h23,hlast,h2325,sri23,sri22,first]).reset_index()
E["typ"]=np.where(E.roll=="institutionell","inst",np.where(E.institutionalonly==1,"huvud_inst","privat"))
tw=set(E[E.roll=="institutionell"].fundid)&set(E[E.typ=="privat"].fundid)
E["tvilling"]=E.fundid.isin(tw)
E.to_pickle("etiketter.pkl")
T=E[E.tvilling&E.typ.isin(["privat","inst"])]
print("tvillingfonder:",len(tw))
for typ,g in T.groupby("typ"):
    n=len(g); print(f"\n== {typ}: {n} klasser")
    print("  har SRRI sep-dec 2022:",int(g.srri22.notna().sum()),"| har ra SRI jan-jun 2023:",int(g.sri23.notna().sum()),"| har ra SRRI feb-jun 2023:",int(g.srri23h1.notna().sum()),"| nagon SRRI-post efter juli 2023:",int(g.srri_n_efter_jul23.notna().sum()))
    print("  sista SRRI-post, ar:",g.srri_sista.dt.year.value_counts().sort_index().to_dict())
    print("  forsta raa SRI, ar:",g.sri_forsta.dropna().apply(lambda p:p.year).value_counts().sort_index().to_dict(),"| saknar SRI helt:",int(g.sri_forsta.isna().sum()))
    b=g[g.srri22.notna()]
    a=(b.sri23<b.srri22).sum(); s=(b.sri23==b.srri22).sum(); u=(b.sri23>b.srri22).sum(); m=b.sri23.isna().sum()
    print(f"  av {len(b)} med SRRI 2022: SRI H1 2023 lagre {a} ({a/len(b):.0%}) | samma tal {s} ({s/len(b):.0%}) | hogre {u} | ingen SRI {m} ({m/len(b):.0%})")
    k=b[b.sri23.isna()]; print("    av dem utan SRI H1 2023: har SRRI-post feb-jun 2023:",int(k.srri23h1.notna().sum()),"| har SRRI-post efter juli 2023:",int(k.srri_n_efter_jul23.notna().sum()))
    kk=b[b.srri23h1.notna()]; print("  har BADE ny SRRI-post feb-jun 2023 och ra SRI:",int(kk.sri23.notna().sum()),"| SRRI-post 2023 = SRRI 2022:",int((kk.srri23h1==kk.srri22).sum()),"av",len(kk))
    c=g[g.sri_h2_22.notna()&g.sri23.notna()]; print("  ra SRI fanns redan andra halvaret 2022:",len(c),"| samma varde H1 2023:",int((c.sri_h2_22==c.sri23).sum()))
# inom par: samma dos?
A=T[T.typ=="privat"].drop_duplicates("fundid").set_index("fundid"); B=T[T.typ=="inst"].drop_duplicates("fundid").set_index("fundid")
J=A[["srri22","sri23"]].join(B[["srri22","sri23","srri23h1"]],lsuffix="_p",rsuffix="_i",how="inner")
ok=J.dropna(subset=["srri22_p","sri23_p"])
print("\npar dar privatklassen har bade SRRI 2022 och SRI 2023:",len(ok))
print("  inst har ocksa bada:",int(ok[["srri22_i","sri23_i"]].notna().all(axis=1).sum()),"| inst saknar SRI H1 2023:",int(ok.sri23_i.isna().sum()),"| inst saknar SRRI 2022:",int(ok.srri22_i.isna().sum()))
b=ok.dropna(subset=["srri22_i","sri23_i"]); print("  samma gamla klass i paret:",round((b.srri22_p==b.srri22_i).mean(),3),"| samma nya klass:",round((b.sri23_p==b.sri23_i).mean(),3),"| samma dos:",round(((b.srri22_p-b.sri23_p)==(b.srri22_i-b.sri23_i)).mean(),3))
