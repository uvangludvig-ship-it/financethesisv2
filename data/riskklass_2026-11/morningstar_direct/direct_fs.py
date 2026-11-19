import pandas as pd, numpy as np
L = pd.read_pickle("/home/claude/direct_out/direct_long.pkl")
srri = lambda s: np.select([s<0.5,s<2,s<5,s<10,s<15,s<25],[1,2,3,4,5,6],7)
mrm  = lambda v: np.select([v<0.5,v<5,v<12,v<20,v<30,v<80],[1,2,3,4,5,6],7)
P = L.pivot_table(index="SecId", columns="t", values=["srri","sri"], aggfunc="first")
base = L.drop_duplicates("SecId").set_index("SecId")
f = pd.DataFrame(index=base.index)
f["roll"]=base.roll; f["inst"]=base.institutionalonly; f["vev"]=base.vev_22; f["sig"]=base.sig_w_22
f["srri_act"]=P["srri"][pd.Period("2022-11","M")]
s = P["sri"].loc[:, pd.Period("2022-12","M"):pd.Period("2023-06","M")]
f["sri_act"]=s.bfill(axis=1).iloc[:,0]
f["sri_src"]=np.where(f.sri_act.notna(),"serie","saknas")
fill = f.sri_act.isna() & base.sri_cur.notna()
f.loc[fill,"sri_act"]=base.sri_cur[fill]; f.loc[fill,"sri_src"]="nuvarande"
f["srri_calc"]=srri(f.sig); f["sri_calc"]=mrm(f.vev)
f.loc[f.sig.isna(),"srri_calc"]=np.nan; f.loc[f.vev.isna(),"sri_calc"]=np.nan
f.to_csv("/home/claude/direct_out/forsta_steget_klasser.csv")
def rep(df, lab):
    a=df.dropna(subset=["srri_act","srri_calc"]); b=df.dropna(subset=["sri_act","sri_calc"])
    print(f"{lab:<38} SRRI {np.mean(a.srri_act==a.srri_calc)*100:5.1f}% (n {len(a)}), ±1 {np.mean(abs(a.srri_act-a.srri_calc)<=1)*100:5.1f}% | SRI {np.mean(b.sri_act==b.sri_calc)*100:5.1f}% (n {len(b)}), ±1 {np.mean(abs(b.sri_act-b.sri_calc)<=1)*100:5.1f}%")
m = f[f.roll=="huvudklass"]
print("=== Förstasteget: beräknad klass mot riktig klass (Morningstar Direct)")
rep(f, "alla klasser")
rep(m, "huvudklasser")
rep(m[m.inst!=1], "huvudklasser, privatsparare")
rep(m[m.sri_src=="serie"], "huvudklasser, SRI från tidsserien")
print("\n=== Nära gränserna (±3 pp), huvudklasser")
for cut,col,typ in [(12,"vev","SRI"),(20,"vev","SRI"),(10,"sig","SRRI"),(15,"sig","SRRI")]:
    w = m[(m[col]>=cut-3)&(m[col]<cut+3)]
    act = "sri_act" if typ=="SRI" else "srri_act"; calc = "sri_calc" if typ=="SRI" else "srri_calc"
    w = w.dropna(subset=[act,calc])
    above = w[col]>=cut
    print(f"{typ} gräns {cut}%: match {np.mean(w[act]==w[calc])*100:5.1f}% (n {len(w)}) | riktig klass under/över: {w[act][~above].mean():.2f} / {w[act][above].mean():.2f} | hopp {w[act][above].mean()-w[act][~above].mean():+.2f}")
print("\n=== Riktig klass mot beräknad (huvudklasser), SRI")
print(pd.crosstab(m.sri_calc, m.sri_act))
print("\n=== Riktig klass mot beräknad (huvudklasser), SRRI")
print(pd.crosstab(m.srri_calc, m.srri_act))
