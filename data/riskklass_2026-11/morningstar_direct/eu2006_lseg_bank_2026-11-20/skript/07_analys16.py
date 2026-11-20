"""Ben-Davids handelsetest (Table 4, Figure 5) pa oktober 2006. Enligt DEKLARATION_bendavids_handelsetest_eu_oktober_2006_preliminar_2026-11-20.
python3 -I analys06.py panel06.pkl"""
import sys, numpy as np, pandas as pd
d = pd.read_pickle(sys.argv[1]).reset_index(drop=True); betyg = pd.read_pickle(sys.argv[1].replace(".pkl", "_betyg.pkl"))
d["star"] = d["star_d"].astype(int); d["year"] = d["ym"].str[:4]
rng = np.random.default_rng(20261120); EV = "2006-10"
out = []
def say(s=""): print(s); out.append(s)
def fe_demean(X, groups, maxit=500, tol=1e-10):
    X = X.astype(float).copy()
    for _ in range(maxit):
        prev = X.copy()
        for g in groups: X = X - X.groupby(g.values).transform("mean")
        if len(groups) == 1 or np.abs((X - prev).values).max() < tol: break
    return X
def r2(y, X, groups):
    sst = np.sum((y - y.mean()) ** 2); Z = fe_demean(pd.concat([y.rename("y"), X], axis=1), groups)
    e = Z["y"].values; A = Z.drop(columns="y").values; b, *_ = np.linalg.lstsq(A, e, rcond=None); e = e - A @ b
    return 1 - np.sum(e ** 2) / sst
def ols(y, X, fe, clusters):
    Z = fe_demean(pd.concat([y.rename("y"), X], axis=1), [fe]); yt = Z["y"].values; A = Z.drop(columns="y").values
    Ai = np.linalg.inv(A.T @ A); b = Ai @ A.T @ yt; e = yt - A @ b
    def meat(cl):
        u = pd.DataFrame(A * e[:, None]).groupby(np.asarray(cl)).sum().values; G = len(u); return G / (G - 1) * u.T @ u
    inter = pd.Series(list(zip(clusters[0], clusters[1]))).astype(str).values
    V = Ai @ (meat(clusters[0]) + meat(clusters[1]) - meat(inter)) @ Ai
    return pd.Series(b, index=X.columns), pd.Series(np.sqrt(np.diag(V)), index=X.columns)

say(f"Urval: {len(d)} fondmanader, {d.FundId.nunique()} fonder, {d.ym.min()} till {d.ym.max()}. Fore (<= {EV}): {int((d.ym <= EV).sum())}; efter: {int((d.ym > EV).sum())}.")

# ---------- Test 1: Table 4A ----------
b = betyg.sort_values(["FundId", "ym"]).copy(); b["prev"] = b.groupby("FundId")["star_d"].shift(1)
q = d[["FundId", "ym", "age"]].merge(b, on=["FundId", "ym"]).dropna(subset=["star_d", "prev"]); q["ch"] = (q.star_d != q.prev).astype(float)
def t4a(qq, nm):
    m = qq.groupby("ym").ch.mean(); pre = m[m.index < EV]; post = m[m.index > EV]; ev = m.get(EV, np.nan); n = int((qq.ym == EV).sum())
    say(f"| {nm} | {100*pre.mean():.1f} % ({100*pre.std():.1f}) | **{100*ev:.1f} %** (n {n}) | {100*post.mean():.1f} % ({100*post.std():.1f}) | {100*m.drop(EV, errors='ignore').max():.1f} % ({m.drop(EV, errors='ignore').idxmax()}) |")
say("\n## Test 1 (Table 4A): andel fonder med andrat betyg\n\n| Grupp | Fore okt 2006, medel (sd) | Oktober 2006 | Efter, medel (sd) | Hogsta ovriga manad |\n|---|---|---|---|---|")
t4a(q, "Alla"); t4a(q[q.age >= 5], "Minst fem ar"); t4a(q[(q.age >= 3) & (q.age < 5)], "Tre till fem ar")
say("| Ankaret, juni 2002 | 13,9 % (3,5) | 54,2 % | 11,9 % (2,8) | |")

# ---------- Test 2: Table 4B ----------
d["m_star"] = d["ym"] + "_" + d["star"].astype(str); d["m_cat"] = d["ym"] + "_" + d["cat"]
say("\n## Test 2 (Table 4B): marginellt R2 utover manadseffekter och ra avkastning\n\n| | Fore | Efter | Ankaret fore / efter |\n|---|---|---|---|")
res = {}
def t4b(g):
    g = g.reset_index(drop=True); y = g["flow"]; X1 = g[["unad_a"]]
    b0 = r2(y, X1, [g["ym"]]); rs = r2(y, X1, [g["m_star"]]); rc = r2(y, X1, [g["m_cat"]]); rsc = r2(y, X1, [g["m_star"], g["m_cat"]])
    return (rs - b0, rc - b0, rsc - rs, len(g), b0)
for nm, g in [("fore", d[d.ym <= EV]), ("efter", d[d.ym > EV])]: res[nm] = t4b(g)
for i, lab, anc in [(0, "Manad x betyg", "0,073 / 0,074"), (1, "Manad x kategori", "0,043 / 0,015"), (2, "Kategori utover betyg", "0,022 / 0,014")]:
    say(f"| {lab} | {res['fore'][i]:.4f} | {res['efter'][i]:.4f} | {anc} |")
say(f"Fondmanader fore {res['fore'][3]}, efter {res['efter'][3]}. R2 for basen (manad + avkastning): fore {res['fore'][4]:.4f}, efter {res['efter'][4]:.4f}.")
say("\nSamma, per aldersgrupp (manad x betyg):\n\n| Grupp | Fore | Efter | Fondmanader fore / efter |\n|---|---|---|---|")
for nm, m_ in [("Minst fem ar", d.age >= 5), ("Tre till fem ar", (d.age >= 3) & (d.age < 5))]:
    a = t4b(d[m_ & (d.ym <= EV)]); c = t4b(d[m_ & (d.ym > EV)]); say(f"| {nm} | {a[0]:.4f} | {c[0]:.4f} | {a[3]} / {c[3]} |")
say("\nSamma med lika langa fonster (17 manader pa var sida: 2005-05..2006-09 och 2006-11..2008-03), manad x betyg:")
a = t4b(d[(d.ym >= "2005-05") & (d.ym <= "2006-09")]); c = t4b(d[(d.ym >= "2006-11") & (d.ym <= "2008-03")]); say(f"fore {a[0]:.4f} (n {a[3]}), efter {c[0]:.4f} (n {c[3]})  [utforskande, ej deklarerat]")

# ---------- Test 3: Figure 5A ----------
say("\n## Test 3 (Figure 5A a): medelflode (%) per betyg och ar\n\n| Ar | 1 | 2 | 3 | 4 | 5 | Fondmanader |\n|---|---|---|---|---|---|---|")
fa = d.groupby(["year", "star"])["flow"].mean().unstack()
for yr, r_ in fa.iterrows(): say(f"| {yr} | " + " | ".join(f"{v:+.2f}" for v in r_.values) + f" | {int((d.year == yr).sum())} |")
say("\n## Test 3 (Figure 5A b): betygets koefficient per ar (flode pa betyg och ra signal, manadseffekt, kluster fond och manad)\n\n| Ar | Koef. | t | Fondmanader |\n|---|---|---|---|")
for yr, g in d.groupby("year"):
    g = g.reset_index(drop=True); b_, se = ols(g["flow"], g[["star", "unad_a"]], g["ym"], [g.FundId.values, g.ym.values]); say(f"| {yr} | {b_['star']:+.2f} | {b_['star']/se['star']:.1f} | {len(g)} |")
for nm, g in [("fore (<= 2006-10)", d[d.ym <= EV]), ("efter", d[d.ym > EV]), ("hela", d)]:
    g = g.reset_index(drop=True); b_, se = ols(g["flow"], g[["star", "unad_a"]], g["ym"], [g.FundId.values, g.ym.values]); say(f"Poolat {nm}: betyg {b_['star']:+.3f} (t {b_['star']/se['star']:.2f}), signal {b_['unad_a']:+.3f} (t {b_['unad_a']/se['unad_a']:.2f}), n {len(g)}")
say("Ankaret: 0,4-0,6 varje ar.")

# ---------- Test 4: Figure 5B ----------
foc = betyg[betyg["ym"].str.endswith("-10")].copy(); foc["year"] = foc["ym"].str[:4]; foc = foc.rename(columns={"star_d": "focal"})[["FundId", "year", "focal"]]
e = d[d["ym"].str[5:].isin(["07", "08", "09"])].merge(foc, on=["FundId", "year"], how="inner").dropna(subset=["focal"])
octage = d[["FundId"]].drop_duplicates().merge(d.groupby("FundId").inc.first().reset_index(), on="FundId")
e["age_oct"] = (pd.to_datetime(e["year"] + "-10-31") - e["inc"]).dt.days / 365.25
def spread(g, col, top_, bot): return g.loc[g[col].isin(top_), "flow"].mean() - g.loc[g[col].isin(bot), "flow"].mean()
def run5b(ee, top_, bot, nm):
    per = ee.groupby("ym").apply(lambda g: spread(g, "star", top_, bot) - spread(g, "focal", top_, bot), include_groups=False)
    sa = ee.groupby("ym").apply(lambda g: spread(g, "star", top_, bot), include_groups=False); sf_ = ee.groupby("ym").apply(lambda g: spread(g, "focal", top_, bot), include_groups=False)
    nmon = ee.groupby("ym").FundId.nunique(); ys = sorted(set(per.index.str[:4]))
    sw = ee.groupby("ym").apply(lambda g: (g.star != g.focal).mean(), include_groups=False)
    say(f"\n**{nm}**\n\n| Ar | Fonder per manad (min) | Andel med annat betyg i okt | Spread visat betyg | Spread oktoberbetyg | D | Jamforelsear? |\n|---|---|---|---|---|---|---|")
    yrs = {}; ok_y = []
    for y in ys:
        ix = [m for m in per.index if m.startswith(y)]; mn = int(nmon[ix].min()); full = len(ix) == 3 and not per[ix].isna().any()
        yrs[y] = per[ix].sum() if full else np.nan; isp = full and mn >= 200 and y != "2006"
        if isp: ok_y.append(y)
        say(f"| {'**'+y+'**' if y == '2006' else y} | {mn} | {100*sw[ix].mean():.0f} % | {sa[ix].sum():+.2f} | {sf_[ix].sum():+.2f} | {yrs[y]:+.2f} | {'handelsear' if y == '2006' else ('ja' if isp else 'nej')} |")
    if len(ok_y) >= 2 and "2006" in yrs and np.isfinite(yrs["2006"]):
        plac = per[[m for m in per.index if m[:4] in ok_y]]
        boot = [rng.choice(plac[plac.index.str.startswith(rng.choice(ok_y))].values, 3, replace=True).sum() for _ in range(10000)]
        lo, hi = np.quantile(boot, [0.01, 0.99]); v = yrs["2006"]
        say(f"2006: D = {v:+.2f}; placebo 1-99 % [{lo:+.2f}; {hi:+.2f}] ur {len(ok_y)} jamforelsear ({', '.join(ok_y)}); {'OVER intervallet' if v > hi else ('under intervallet' if v < lo else 'inom intervallet')}.")
        allv = sorted([yrs[y] for y in ok_y] + [v], reverse=True); say(f"Rang for 2006 bland {len(allv)} ar (storst = 1): {allv.index(v) + 1}. Storsta jamforelsear: {max(yrs[y] for y in ok_y):+.2f}; medel {np.mean([yrs[y] for y in ok_y]):+.2f}, sd {np.std([yrs[y] for y in ok_y], ddof=1):.2f}.")
    else: say("For fa jamforelsear for intervall.")
say("\n## Test 4 (Figure 5B, ekvation 2): juli-september, visat betyg mot oktoberbetyget")
run5b(e, [5], [1], "(a) 5 mot 1 stjarna, alla fonder")
run5b(e, [4, 5], [1, 2], "(b) 4-5 mot 1-2 stjarnor, alla fonder")
run5b(e[e.age_oct >= 5], [4, 5], [1, 2], "(b) 4-5 mot 1-2, fonder minst fem ar i oktober")
run5b(e[(e.age_oct >= 3) & (e.age_oct < 5)], [4, 5], [1, 2], "(b) 4-5 mot 1-2, fonder tre till fem ar (jamforelsegrupp)")
open(sys.argv[1].replace(".pkl", "_res.md"), "w").write("\n".join(out))
