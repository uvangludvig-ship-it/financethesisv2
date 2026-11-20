# python3 05_koll2.py <raw16.pkl> <lseg_wide.pkl>
import sys, pandas as pd, numpy as np, warnings; warnings.filterwarnings("ignore")
x = pd.read_pickle(sys.argv[1]); R, NA, RET, st = x["R"], x["NA"], x["RET"], x["st"]
z = pd.read_pickle(sys.argv[2]); W, ms = z["W"], z["ms"]; W = W.where(W > 0); D = NA[ms].where(NA[ms] > 0); fid = st.FundId
both = W.notna() & D.notna()
ratio = (W / D).where(both).stack().dropna(); lr = np.log(ratio)
print("klassmanader i bada: %d | kvot median %.4f | inom 1 %%: %.1f %% | inom 5 %%: %.1f %% | inom 20 %%: %.1f %% | kvot > 1,5: %.1f %% | kvot < 0,67: %.1f %%" % (len(ratio), ratio.median(), 100*(lr.abs()<.01).mean(), 100*(lr.abs()<.05).mean(), 100*(lr.abs()<.2).mean(), 100*(ratio>1.5).mean(), 100*(ratio<.67).mean()))
for y, g in lr.groupby(lr.index.get_level_values(1).str[:4]): print("  ", y, "n", len(g), "inom 1 %%: %.1f | inom 5 %%: %.1f" % (100*(g.abs()<.01).mean(), 100*(g.abs()<.05).mean()))
# fondniva eller klassniva i LSEG
Ws = W.stack().dropna().rename("v").reset_index(); Ws.columns = ["SecId", "ym", "v"]; Ws["FundId"] = Ws.SecId.map(fid)
g = Ws.groupby(["FundId", "ym"]).v; Ws["k"] = g.transform("size"); Ws["nu"] = g.transform("nunique")
multi = Ws[Ws.k > 1]; fm = multi.drop_duplicates(["FundId", "ym"])
print("\nfondmanader med >= 2 klasser i LSEG: %d | alla klasser samma varde: %.1f %% | nagra samma: %.1f %%" % (len(fm), 100*(fm.nu == 1).mean(), 100*((fm.nu > 1) & (fm.nu < fm.k)).mean()))
Ds = D.stack().dropna().rename("d").reset_index(); Ds.columns = ["SecId", "ym", "d"]
j = Ws.merge(Ds, on=["SecId", "ym"]); j["dsum"] = j.groupby(["FundId", "ym"]).d.transform("sum"); j["nd"] = j.groupby(["FundId", "ym"]).d.transform("size")
s = j[(j.k > 1) & (j.nu == 1)]; o = j[(j.k > 1) & (j.nu == j.k)]
print("dar alla klasser har SAMMA LSEG-varde (n %d): kvot mot klassens Direct-varde median %.2f; inom 5 %%: %.1f %%" % (len(s), (s.v/s.d).median(), 100*(np.log(s.v/s.d).abs()<.05).mean()))
print("dar klasserna har OLIKA LSEG-varden (n %d): kvot mot klassens Direct-varde median %.3f; inom 5 %%: %.1f %%" % (len(o), (o.v/o.d).median(), 100*(np.log(o.v/o.d).abs()<.05).mean()))
one = j[j.k == 1]; print("dar bara en klass finns i LSEG (n %d): inom 5 %%: %.1f %%" % (len(one), 100*(np.log(one.v/one.d).abs()<.05).mean()))
# floden klassniva
r = RET.reindex(columns=ms) / 100
def flow(X): Xl = X.shift(1, axis=1); return 100 * (X - Xl * (1 + r)) / Xl
fL, fD = flow(W), flow(D); A = fL.stack().rename("a"); B = fD.stack().rename("b"); q = pd.concat([A, B], axis=1).dropna()
def w(c): return c.clip(c.quantile(.01), c.quantile(.99))
print("\nflode per klassmanad i bada kallor: n %d | korrelation (kapat 1/99) %.3f | medianavvikelse %.4f pp | inom 0,1 pp: %.1f %% | inom 1 pp: %.1f %%" % (len(q), np.corrcoef(w(q.a), w(q.b))[0, 1], (q.a-q.b).abs().median(), 100*((q.a-q.b).abs()<.1).mean(), 100*((q.a-q.b).abs()<1).mean()))
q["y"] = q.index.get_level_values(1).str[:4]
for y, g in q.groupby("y"): print("  ", y, "n", len(g), "korr %.3f" % np.corrcoef(w(g.a), w(g.b))[0, 1], "| inom 1 pp: %.1f %%" % (100*((g.a-g.b).abs()<1).mean()))
# stillastaende varden (samma varde flera manader i rad) i LSEG mot Direct
def stale(X): return float(((X == X.shift(1, axis=1)) & X.notna()).sum().sum() / X.notna().sum().sum())
print("\nandel manader med exakt samma varde som forra manaden: LSEG %.3f | Direct %.3f" % (stale(W), stale(D)))
