_h = open('/home/claude/scripts/horse.py').read(); exec(_h[:_h.index('# calibrate monthly sigma')])
bas["ret36"]=g.transform(lambda x: x.shift(1).rolling(36, min_periods=36).sum())
FR3 = pd.read_pickle("/home/claude/direct_out/FR3.pkl")
L = pd.read_pickle("/home/claude/direct_out/direct_long.pkl")
M = L[L.roll=="huvudklass"].sort_values(["SecId","t"]).copy()
M["star_lag"]=M.groupby("SecId").star.shift(1)
M["cat_lag"]=M.groupby("SecId").cat.shift(1)
P = FR3.drop(columns=["star","cat"],errors="ignore").merge(M[["fundid","t","star_lag","cat_lag"]].drop_duplicates(["fundid","t"]), on=["fundid","t"], how="left")
P = P.merge(bas[["fundid","t","sig60","ret12","ret36"]], on=["fundid","t"], how="left")
P = P.dropna(subset=["cat_lag","ret12","ret36","sig60"]).copy()
P = P[P.sig60.between(1,40)]
P["rank12"]=P.groupby(["t","cat_lag"]).ret12.rank(pct=True)
P["rank36"]=P.groupby(["t","cat_lag"]).ret36.rank(pct=True)
P["unit"]=P.fundid; P["tt"]=P.t.astype(str)+"_"+P.cat_lag
pp = P.post.astype(float)
def ols(df, Xdf, ycol="f"):
    yd=demean(df, df[[ycol]])[ycol].values; Xd=demean(df, Xdf).values
    b=np.linalg.lstsq(Xd,yd,rcond=None)[0]; e=yd-Xd@b; XtXi=np.linalg.inv(Xd.T@Xd)
    sc=pd.DataFrame(Xd*e[:,None]).groupby(df.fundid.values).sum().values; G=len(sc)
    V=XtXi@(sc.T@sc)@XtXi*G/(G-1); return b, np.sqrt(np.diag(V)), G
def ctrl(D):
    X = pd.DataFrame(index=D.index)
    for k in (1,2): X[f"r12_{k}"]=D.rank12**k; X[f"r36_{k}"]=D.rank36**k
    for k in (1,2,3):
        s=(D.sig60/10)**k; X[f"s{k}"]=s; X[f"s{k}p"]=s*D.post.astype(float)
    return X
def show(nm, b, se, i, G, n):
    print(f"  {nm:<34} {b[i]*12:+6.2f} pp/år [{(b[i]-1.96*se[i])*12:+6.2f}, {(b[i]+1.96*se[i])*12:+6.2f}]  t {b[i]/se[i]:+5.2f} | fonder {G}, obs {n}")
S = P.dropna(subset=["star_lag"]).copy()
print("=== Positiv kontroll: stjärnor (förra månaden) och flöden")
print("    fond-effekter + månad x kategori-effekter, kontroll för 12/36-mån avkastningsrang i kategorin och risknivå; kluster per fond")
b,se,G = ols(S, pd.concat([pd.DataFrame({"star":S.star_lag}), ctrl(S)],axis=1)); show("per stjärna", b, se, 0, G, len(S))
b0,se0,G0 = ols(S, pd.DataFrame({"star":S.star_lag})); show("per stjärna, utan avkastningskontroller", b0, se0, 0, G0, len(S))
A = S.dropna(subset=["label"]).copy()
X = pd.concat([pd.DataFrame({"star":A.star_lag, "label":A.label}), ctrl(A)],axis=1)
b,se,G = ols(A, X)
print("\n=== Samma regression, båda etiketterna samtidigt")
show("stjärna, per stjärna", b, se, 0, G, len(A))
show("risksiffra (riktig), per klass", b, se, 1, G, len(A))
# label only inside post period: SRI changes after the switch (no switch variation)
Q = A[A.t>=pd.Period("2023-03","M")].copy()
Xq = pd.concat([pd.DataFrame({"star":Q.star_lag,"label":Q.label}), ctrl(Q).drop(columns=[c for c in ctrl(Q).columns if c.endswith("p")])],axis=1)
b,se,G = ols(Q, Xq)
print("\n=== Bara 2023-03 och framåt (risksiffran varierar bara när fondbolaget byter SRI)")
show("stjärna, per stjärna", b, se, 0, G, len(Q))
show("risksiffra (riktig), per klass", b, se, 1, G, len(Q))
ch = Q.sort_values(["fundid","t"]).groupby("fundid").label.apply(lambda s:(s.diff().abs()>0).sum())
print(f"  SRI-byten efter mars 2023: {int(ch.sum())} byten i {int((ch>0).sum())} fonder")
sc = S.sort_values(["fundid","t"]).groupby("fundid").star_lag.apply(lambda s:(s.diff().abs()>0).sum())
print(f"  stjärnbyten: {int(sc.sum())} byten i {int((sc>0).sum())} fonder")
