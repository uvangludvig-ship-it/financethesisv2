# Styrka och nollfordelning for tre specifikationer. For det riktiga bytet (2022 mot 2023) skrivs BARA standardfel ut.
import pandas as pd, numpy as np, os
H=os.path.expanduser("~/mnt")
E=pd.read_pickle("etiketter.pkl"); K=pd.read_pickle(f"{H}/morningstar_direct/tvillingar/tv_klasser.pkl")
E=E[E.dos.isin([0,1,2])&E.sig_w.notna()&E.srri22.notna()]
D=E.set_index("SecId")[["dos","sig_w","srri22"]]
pr=K[(K.roll=="huvudklass")&(K.institutionalonly!=1)&K.SecId.isin(D.index)].copy()
pr=pr.join(D,on="SecId"); pr["y"]=pr.t.dt.year
ins=K[K.roll=="institutionell"][["fundid","t","f"]].rename(columns={"f":"f_i"})
tw=pr.merge(ins,on=["fundid","t"]); tw["df"]=tw.f-tw.f_i
def dm(X,keys,it=60):
    X=X.copy().astype(float)
    for _ in range(it):
        for k in keys: X=X-X.groupby(k).transform("mean")
    return X
def est(A,y,Xcols,keys,clu):
    ks=[A[k].values for k in keys]
    yd=dm(A[[y]],ks).values[:,0]; Xd=dm(A[Xcols],ks).values
    XtXi=np.linalg.pinv(Xd.T@Xd); b=XtXi@Xd.T@yd; e=yd-Xd@b
    sc=pd.DataFrame(Xd*e[:,None]).groupby(A[clu].values).sum().values; G=len(sc)
    V=XtXi@(sc.T@sc)@XtXi*G/(G-1); return b[0]*12,np.sqrt(V[0,0])*12,G
def window(A,y0,idc):
    W=A[A.y.isin([y0,y0+1])].copy(); n=W.groupby([idc,"y"]).size().unstack(fill_value=0)
    ok=n[(n.get(y0,0)>=9)&(n.get(y0+1,0)>=9)].index; W=W[W[idc].isin(ok)].copy()
    W["efter"]=(W.y==y0+1).astype(float); W["ed"]=W.efter*W.dos; s=W.sig_w/10
    for k in (1,2,3): W[f"es{k}"]=W.efter*s**k
    W["tt"]=W.t.astype(str); W["tc"]=W.tt+"_"+W.cat_lag.astype(str); W["eo"]=W.efter.astype(int).astype(str)+"_"+W.srri22.astype(int).astype(str)
    return W
out=[]
for y0 in [2019,2020,2021,2022,2023,2024]:
    real=(y0==2022)
    W=window(pr.dropna(subset=["cat_lag"]),y0,"SecId")
    bM,sM,gM=est(W,"f",["ed","es1","es2","es3"],["SecId","tc"],"fundid")
    bS,sS,gS=est(W,"f",["ed"],["SecId","tc","eo"],"fundid")
    T=window(tw,y0,"SecId")
    bI,sI,gI=est(T,"df",["ed","es1","es2","es3"],["SecId","tt"],"fundid")
    bI2,sI2,_=est(T,"df",["ed"],["SecId","tt","eo"],"fundid")
    out.append((y0,real,bM,sM,gM,len(W),bS,sS,bI,sI,gI,len(T),bI2,sI2))
print("Enhet: pp av formogenheten per ar, per steg etiketten foll. Efter = det senare aret.")
print(f"{'fonster':<10}{'M b':>7}{'M se':>6}{'M t':>6} | {'S b':>7}{'S se':>6}{'S t':>6} | {'I b':>7}{'I se':>6}{'I t':>6} | {'I+S b':>7}{'se':>6}{'t':>6} | fonder M/I, obs M/I")
for (y0,real,bM,sM,gM,nM,bS,sS,bI,sI,gI,nI,bI2,sI2) in out:
    f=lambda b,s: (f"{'dold':>7}{s:6.2f}{'':>6}" if real else f"{b:+7.2f}{s:6.2f}{b/s:+6.2f}")
    print(f"{y0}-{str(y0+1)[2:]:<5}{f(bM,sM)} | {f(bS,sS)} | {f(bI,sI)} | {f(bI2,sI2)} | {gM}/{gI}, {nM}/{nI}"+("   <-- riktiga bytet, bara SE" if real else ""))
pl=[o for o in out if not o[1]]
for nm,i,j in [("M",2,3),("S",6,7),("I",8,9),("I+S",12,13)]:
    b=np.array([o[i] for o in pl]); s=np.array([o[j] for o in pl]); r=[o for o in out if o[1]][0]
    print(f"{nm}: latsasar std av b {b.std(ddof=1):.2f}, storsta |b| {abs(b).max():.2f}, storsta |t| {abs(b/s).max():.2f}, rot-medel-kvadrat {np.sqrt((b**2).mean()):.2f} | riktiga bytet SE {r[j]:.2f}, MDE {2.8*r[j]:.1f}")
# ---- 4. manad for manad, bara SE
print("\nManad for manad (dos x manadsdummy, bas dec 2022), bara standardfel, pp/ar:")
def monthly(A,y,keys,idc):
    W=A[(A.t>=pd.Period('2022-07','M'))&(A.t<=pd.Period('2023-12','M'))].copy()
    n=W.groupby(idc).size(); W=W[W[idc].isin(n[n>=15].index)].copy()
    W["tt"]=W.t.astype(str); W["tc"]=W.tt+"_"+W.cat_lag.astype(str); ms=[m for m in sorted(W.tt.unique()) if m!="2022-12"]
    for m in ms: W["d_"+m]=(W.tt==m)*W.dos
    W["efter"]=(W.t>=pd.Period('2023-01','M')).astype(float); s=W.sig_w/10
    for k in (1,2,3): W[f"es{k}"]=W.efter*s**k
    cols=["d_"+m for m in ms]+["es1","es2","es3"]; ks=[W[k].values for k in keys]
    yd=dm(W[[y]],ks).values[:,0]; Xd=dm(W[cols],ks).values; XtXi=np.linalg.pinv(Xd.T@Xd); b=XtXi@Xd.T@yd; e=yd-Xd@b
    sc=pd.DataFrame(Xd*e[:,None]).groupby(W.fundid.values).sum().values; G=len(sc); se=np.sqrt(np.diag(XtXi@(sc.T@sc)@XtXi*G/(G-1)))[:len(ms)]*12
    return se,G
seM,gM=monthly(pr.dropna(subset=["cat_lag"]),"f",["SecId","tc"],"SecId"); seI,gI=monthly(tw,"df",["SecId","tt"],"SecId")
print(f"  M: median SE {np.median(seM):.1f}, min {seM.min():.1f}, max {seM.max():.1f} (fonder {gM})")
print(f"  I: median SE {np.median(seI):.1f}, min {seI.min():.1f}, max {seI.max():.1f} (fonder {gI})")
