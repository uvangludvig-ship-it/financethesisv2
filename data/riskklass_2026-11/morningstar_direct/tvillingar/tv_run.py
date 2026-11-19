# Tvillingtestet enligt claude/DEKLARATION_tvillingar_och_byte2023_2026-11-17.md
import pandas as pd, numpy as np
P=pd.read_pickle("tv_klasser.pkl")
R=P[(P.roll=="huvudklass")&(P.institutionalonly!=1)]; I=P[P.roll=="institutionell"]
T=R.merge(I,on=["fundid","t"],suffixes=("_r","_i")).dropna(subset=["star_lag_r","star_lag_i"]).copy()
T["tt"]=T.t.astype(str); T["df"]=T.f_r-T.f_i; T["dstar"]=T.star_lag_r-T.star_lag_i
def dm(D,X,keys,it=80):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(D[k].values).transform("mean")
    return X
def fit(D,y,X,keys):
    yd=dm(D,D[[y]],keys).values[:,0]; Xd=dm(D,X,keys).values; XtXi=np.linalg.pinv(Xd.T@Xd); b=XtXi@Xd.T@yd; e=yd-Xd@b
    sc=pd.DataFrame(Xd*e[:,None]).groupby(D.fundid.values).sum().values; G=len(sc)
    return b*12,XtXi@(sc.T@sc)@XtXi*G/(G-1)*144,G
def ln(nm,b,V,i): 
    s=np.sqrt(V[i,i]); print(f"  {nm:<46}{b[i]:+6.2f} [{b[i]-1.96*s:+6.2f}; {b[i]+1.96*s:+6.2f}]  t {b[i]/s:+5.2f}   ({b[i]/12:+.3f} % per manad)")
# klassmanader (stack)
def side(s,inst): 
    d=T[["fundid","t","tt",f"SecId_{s}",f"f_{s}",f"star_lag_{s}",f"cat_lag_{s}",f"ret12_{s}",f"ret36_{s}","ret12_r"]].copy(); d.columns=["fundid","t","tt","SecId","f","star","cat","ret12","ret36","ret12_fund"]; d["inst"]=inst; return d
C=pd.concat([side("r",0.0),side("i",1.0)],ignore_index=True)
C["ft"]=C.fundid+"_"+C.tt; C["tc"]=C.tt+"_"+C.cat.astype(str); C["ty"]=C.tt+"_"+C.inst.astype(int).astype(str)
print(f"Urval: {len(T)} fondmanader, {T.fundid.nunique()} fonder, {len(C)} klassmanader")
C1=C.dropna(subset=["cat","ret12","ret36"])
b,V,G=fit(C1,"f",C1[["star","ret12","ret36"]],["tc"]); print(f"\nKolumn 1: manad x kategori, avkastningskontroller (klassmanader {len(C1)}, fonder {G})"); ln("egen stjarna",b,V,0)
b1=b[0]
b,V,G=fit(C1,"f",C1[["star"]],["tc"]); ln("  (utan avkastningskontroller)",b,V,0)
b,V,G=fit(C,"f",C[["star"]],["ft","SecId"]); print(f"\nKolumn 2 (HUVUD): fond x manad + klass (fonder {G})"); ln("egen stjarna",b,V,0); b2,s2=b[0],np.sqrt(V[0,0])
print(f"  kvot kolumn 2 / kolumn 1: {b2/b1:.2f}   | ovre grans kolumn 2: {b2+1.96*s2:+.2f} mot halva kolumn 1: {b1/2:+.2f}")
C3=C.dropna(subset=["ret12_fund"]).copy(); C3["ir"]=C3.inst*C3.ret12_fund
n=C3.groupby("ft").size(); C3=C3[C3.ft.isin(n[n==2].index)]
b,V,G=fit(C3,"f",C3[["star","ir"]],["ft","SecId","ty"]); print(f"\nKolumn 3: + klasstyp x manad, institutionell x avkastning 12 man (klassmanader {len(C3)})"); ln("egen stjarna",b,V,0)
X4=pd.DataFrame({"g_m2":(T.dstar<=-2)*1.0,"g_m1":(T.dstar==-1)*1.0,"g_p1":(T.dstar==1)*1.0,"g_p2":(T.dstar>=2)*1.0},index=T.index)
b,V,G=fit(T,"df",X4,["fundid","tt"]); print("\nKolumn 4: flodesskillnad privat minus inst pa stjarngap (bas: lika), par + manad")
for i,nm in enumerate(["gap -2 eller lagre (privat farre)","gap -1","gap +1","gap +2 eller hogre (privat fler)"]): ln(nm,b,V,i)
X5=T[["star_lag_r","star_lag_i"]]
b,V,G=fit(T,"df",X5,["fundid","tt"]); print("\nKolumn 5: flodesskillnaden pa var klass stjarna for sig, par + manad")
ln("privatklassens stjarna (b_privat)",b,V,0); ln("institutionellas stjarna (= -b_inst)",b,V,1)
# handelsestudie
T=T.sort_values(["fundid","t"]).reset_index(drop=True); g=T.groupby("fundid")
T["ti"]=T.t.astype("int64")
chg_r=(g.star_lag_r.diff()).fillna(0); chg_i=(g.star_lag_i.diff()).fillna(0); cons=(T.ti-g.ti.shift(1))==1
ev=T[(chg_r!=0)&cons].copy(); ev["dir"]=np.sign(chg_r[ev.index])
# tvillingens stjarna oforandrad +-3 manader
ic=T[(chg_i!=0)][["fundid","ti"]]; icd=ic.groupby("fundid").ti.apply(list).to_dict()
keep=[all(abs(t0-x)>3 for x in icd.get(f,[])) for f,t0 in zip(ev.fundid,ev.ti)]; ev=ev[keep]
print(f"\nHandelsestudie: privatklassens stjarna andras, tvillingens oforandrad +-3 man: hojningar {int((ev.dir>0).sum())}, sankningar {int((ev.dir<0).sum())}")
ks=list(range(-6,13)); cols={}
key=T.fundid+"_"+T.ti.astype(str); idx=pd.Series(T.index,index=key.values)
for d,nm in [(1,"u"),(-1,"n")]:
    E=ev[ev.dir==d]
    for k in ks:
        if k==-1: continue
        v=np.zeros(len(T)); kk=(E.fundid+"_"+(E.ti+k).astype(str)).values; hit=idx.reindex(kk).dropna().astype(int).values
        np.add.at(v,hit,1.0); cols[f"{nm}{k}"]=v
XE=pd.DataFrame(cols,index=T.index); b,V,G=fit(T,"df",XE,["fundid","tt"]); names=list(XE.columns)
def cum(pref,kset):
    w=np.array([1.0 if (n.startswith(pref) and int(n[1:]) in kset) else 0.0 for n in names]); est=w@b/12; se=np.sqrt(w@V@w)/12; return est,se
for pref,nm in [("u","hojd stjarna"),("n","sankt stjarna")]:
    e,s=cum(pref,set(range(0,13))); p,ps=cum(pref,set(range(-6,-1)))
    print(f"  {nm}: summa manad 0-12 {e:+.2f} pp av formogenheten [{e-1.96*s:+.2f}; {e+1.96*s:+.2f}] t {e/s:+.2f} | fore (manad -6 till -2) {p:+.2f} (se {ps:.2f})")
