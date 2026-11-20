"""Avstamning LSEG (Lipper TNA) mot Direct (Net Assets - share class). Inga floden sorteras pa betyg."""
import sys, pandas as pd, numpy as np
# python3 04_koll_lseg.py <lseg_tna.csv(.gz)> <lseg_missing.csv> <lseg_isin_list_2006.csv> <raw16.pkl> <ut: lseg_wide.pkl>
L = pd.read_csv(sys.argv[1]); M = pd.read_csv(sys.argv[2])
lst = pd.read_csv(sys.argv[3])
print("rader", len(L), "| ISIN med data", L.ISIN.nunique(), "| ISIN utan data", M.ISIN.nunique(), "| listan", len(lst))
L["date"] = pd.to_datetime(L.date); L["ym"] = L.date.dt.strftime("%Y-%m")
print("datum:", L.date.min().date(), "till", L.date.max().date(), "| negativa/noll:", int((L.tna_usd <= 0).sum()))
dup = L.duplicated(["ISIN", "ym"]).sum(); print("flera varden samma manad:", int(dup))
L = L.sort_values(["ISIN", "date"]).drop_duplicates(["ISIN", "ym"], keep="last")
n = L.groupby("ISIN").size(); print("manader per ISIN: median", n.median(), "| kvartiler", n.quantile([.1, .25, .75, .9]).tolist())
print("forsta manad per ISIN, fordelning per ar:", L.groupby("ISIN").ym.min().str[:4].value_counts().sort_index().to_dict())
a = lst.set_index("ISIN"); got = a.index.isin(L.ISIN)
print("\ntackning per prio (andel ISIN med nagon data):"); print(pd.crosstab(a.prio, got, normalize="index").round(3).to_string())
print("tackning levande/nedlagda:"); print(pd.crosstab(a.closed, got, normalize="index").round(3).to_string())
x = pd.read_pickle(sys.argv[4]); R, NA, RET, st = x["R"], x["NA"], x["RET"], x["st"]
sec = a.SecId; W = L.assign(SecId=L.ISIN.map(sec)).pivot(index="SecId", columns="ym", values="tna_usd")
ms = [m for m in W.columns if m in NA.columns]; W = W.reindex(index=NA.index, columns=ms); D = NA[ms]
both = W.notna() & D.notna(); print("\nklassmanader med bade LSEG och Direct:", int(both.sum().sum()), "| klasser:", int(both.any(axis=1).sum()))
ratio = (W / D).where(both).stack(); lr = np.log(ratio)
print("kvot LSEG/Direct: median %.4f | 5-95 %%: %.3f - %.3f | inom 1 %%: %.1f %% | inom 5 %%: %.1f %% | inom 20 %%: %.1f %%" % (ratio.median(), ratio.quantile(.05), ratio.quantile(.95), 100 * (lr.abs() < .01).mean(), 100 * (lr.abs() < .05).mean(), 100 * (lr.abs() < .2).mean()))
print("kvot per ar (median, andel inom 5 %):", {y: (round(g.median(), 3), round(float((np.log(g).abs() < .05).mean()), 3)) for y, g in ratio.groupby(ratio.index.get_level_values(1).str[:4])})
# ar LSEG pa klass- eller fondniva? identiska varden mellan klasser i samma fond samma manad
Ws = W.stack().rename("v").reset_index(); Ws["FundId"] = Ws.SecId.map(st.FundId); g = Ws.groupby(["FundId", "ym"]).v; k = g.transform("size"); same = g.transform("nunique") == 1
print("fondmanader med flera klasser i LSEG: andel dar alla klasser har exakt samma varde: %.3f" % same[k > 1].mean())
# floden: klassniva, Directs avkastning
r = RET.reindex(columns=ms) / 100
def flow(X): Xl = X.shift(1, axis=1); return 100 * (X - Xl * (1 + r)) / Xl
fL, fD = flow(W), flow(D); ok = fL.notna() & fD.notna(); A = fL.where(ok).stack(); B = fD.where(ok).stack()
def w(z): return z.clip(z.quantile(.01), z.quantile(.99))
print("\nflode per klassmanad i bada kallor: n %d | korrelation (kapat 1/99) %.3f | medianavvikelse %.3f pp | andel inom 0,5 pp %.1f %%" % (len(A), np.corrcoef(w(A), w(B))[0, 1], (A - B).abs().median(), 100 * ((A - B).abs() < .5).mean()))
# vinst i tackning
C = D.combine_first(W); fid = st.FundId
print("\nmanad | betygsatta klasser | med Direct | med Direct eller LSEG | fonder anvandbara: Direct | Direct+LSEG")
for m in ["2003-06", "2003-12", "2004-06", "2004-12", "2005-03", "2005-06", "2005-12", "2006-06", "2006-09", "2006-10", "2006-12", "2007-06", "2007-12", "2008-06", "2008-12"]:
    i = ms.index(m); p = ms[i - 1]; rt = R[m].notna()
    u1 = rt & D[m].notna() & D[p].notna(); u2 = rt & C[m].notna() & C[p].notna()
    print(m, int(rt.sum()), int((rt & D[m].notna()).sum()), int((rt & C[m].notna()).sum()), fid[u1].nunique(), fid[u2].nunique())
pd.to_pickle({"W": W, "ms": ms}, sys.argv[5])
