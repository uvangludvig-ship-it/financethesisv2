# Test enligt claude/DEKLARATION_globbytet_2019_2026-11-18.md
import pandas as pd, numpy as np
P=pd.read_pickle("../t2_utan_betyg/t2_panel.pkl")
G=pd.read_csv("glober_manad.csv.gz")
g=G.pivot_table(index='SecId',columns='ym',values='glob')
dG=(g['2019-09']-g['2019-08']).dropna().rename('dG')
g08=g['2019-08'].rename('g08'); g09=g['2019-09'].rename('g09')
def demean(D,X,keys,it=60):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def fit(D,X,keys):
    y=demean(D,D[["f"]],keys).values[:,0]; Xd=demean(D,X,keys).values
    b=np.linalg.lstsq(Xd,y,rcond=None)[0]; e=y-Xd@b; XtXi=np.linalg.pinv(Xd.T@Xd)
    sc=pd.DataFrame(Xd*e[:,None]).groupby(D.fundid.values).sum().values; G_=len(sc)
    V=XtXi@(sc.T@sc)@XtXi*G_/(G_-1); return b*12,V*144,G_
def line(nm,b,V,i):
    se=np.sqrt(V[i,i]); print(f"  {nm:<34}{b[i]:+6.2f} [{b[i]-1.96*se:+6.2f}; {b[i]+1.96*se:+6.2f}]  t {b[i]/se:+5.2f}  (MDE~{2.8*se:.2f})")
keys=["fundid","tt"]
# ---- globbytet 2019
pre=pd.period_range("2019-04","2019-08",freq="M"); post=pd.period_range("2019-10","2020-02",freq="M")
D=P[P.t.isin(pre.append(post))].merge(dG,left_on="SecId",right_index=True).merge(g08,left_on="SecId",right_index=True).merge(g09,left_on="SecId",right_index=True)
D=D.dropna(subset=["cat_lag"]).copy(); D["tt"]=D.t.astype(str)+"_"+D.cat_lag; D["post"]=D.t.isin(post).astype(float)
D["star"]=D.star_lag.fillna(0); D["nostar"]=D.star_lag.isna().astype(float)
print(f"GLOBER 2019: {len(D)} fondmanader, {D.fundid.nunique()} fonder. dG-fordelning:", D.drop_duplicates('fundid').dG.value_counts().sort_index().to_dict())
X=pd.DataFrame({"dGpost":D.dG*D.post,"star":D.star,"nostar":D.nostar},index=D.index)
b,V,_=fit(D,X,keys); print("Huvudtest (pp/ar per glob):"); line("dG x efter",b,V,0); line("stjarna (positiv kontroll)",b,V,1)
# handelsestudie
ms=[m for m in pre.append(post) if str(m)!="2019-08"]
X=pd.DataFrame({str(m):D.dG*(D.t==m) for m in ms},index=D.index); X["star"]=D.star; X["nostar"]=D.nostar
b,V,_=fit(D,X,keys); print("Handelsestudie (bas aug 2019):")
for i,m in enumerate(ms): line(str(m),b,V,i)
# ytterlagen
E5=((D.g09==5)&(D.g08<5)).astype(float); L5=((D.g08==5)&(D.g09<5)).astype(float); E1=((D.g09==1)&(D.g08>1)).astype(float); L1=((D.g08==1)&(D.g09>1)).astype(float)
X=pd.DataFrame({"in5":E5*D.post,"ut5":L5*D.post,"in1":E1*D.post,"ut1":L1*D.post,"star":D.star,"nostar":D.nostar},index=D.index)
b,V,_=fit(D,X,keys); print("Ytterlagen (pp/ar):")
for i,n in enumerate(["gick in i 5","lamnade 5","gick in i 1","lamnade 1"]): line(n,b,V,i)
print("  antal fonder:",{n:int(v[D.post==1].groupby(D.fundid[D.post==1]).max().sum()) for n,v in [("in5",E5),("ut5",L5),("in1",E1),("ut1",L1)]})
# ---- risksiffran 2023, samma design
s=P.pivot_table(index="SecId",columns="t",values="label")
dS=(s[pd.Period("2022-12","M")]-s[pd.Period("2023-02","M")]).dropna().rename("dS")
pre2=pd.period_range("2022-08","2022-12",freq="M"); post2=pd.period_range("2023-02","2023-06",freq="M")
E=P[P.t.isin(pre2.append(post2))].merge(dS,left_on="SecId",right_index=True).dropna(subset=["cat_lag"]).copy()
E["tt"]=E.t.astype(str)+"_"+E.cat_lag; E["post"]=E.t.isin(post2).astype(float); E["star"]=E.star_lag.fillna(0); E["nostar"]=E.star_lag.isna().astype(float)
print(f"\nRISKSIFFRAN 2023 (redan sedd handelse): {len(E)} fondmanader, {E.fundid.nunique()} fonder. dS:", E.drop_duplicates('fundid').dS.value_counts().sort_index().to_dict())
X=pd.DataFrame({"dSpost":E.dS*E.post,"star":E.star,"nostar":E.nostar},index=E.index)
b,V,_=fit(E,X,keys); line("sankning (steg) x efter",b,V,0); line("stjarna",b,V,1)
