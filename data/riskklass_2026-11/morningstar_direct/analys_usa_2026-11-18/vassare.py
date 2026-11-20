"""Diagnos: vilka urvalsval for USA-replikeringen narmare ankaret? Utforskande, inte deklarerat."""
import numpy as np, pandas as pd
allp = pd.read_pickle("panel_full.pkl"); betyg = pd.read_pickle("panel_full_betyg.pkl")
base = allp[allp.in_kod].copy(); base["star"] = base.star_c.astype(int)
def ols2(y, X, f, t):
    A = np.c_[np.ones(len(X)), X.values]; Ai = np.linalg.inv(A.T @ A); b = Ai @ A.T @ y.values; e = y.values - A @ b
    def meat(c):
        u = pd.DataFrame(A * e[:, None]).groupby(np.asarray(c)).sum().values; G = len(u); return G / (G - 1) * u.T @ u
    V = Ai @ (meat(f) + meat(t) - meat(pd.Series(list(zip(f, t))).astype(str).values)) @ Ai
    return b[1], b[1] / np.sqrt(V[1, 1])
def dem(Z, g): return Z - Z.groupby(g.values).transform("mean")
def r2(y, X, g):
    sst = ((y - y.mean()) ** 2).sum(); Z = dem(pd.concat([y.rename("y"), X], axis=1), g) if X is not None else dem(y.to_frame("y"), g)
    e = Z.y.values
    if X is not None:
        A = Z.drop(columns="y").values; e = e - A @ np.linalg.lstsq(A, e, rcond=None)[0]
    return 1 - (e ** 2).sum() / sst
def rapport(d, nm):
    d = d.reset_index(drop=True); ym = d.ym
    cs = d.groupby("ym").flow.std().mean()
    top = {"M": (d.star == 5).astype(float)}; n5 = top["M"].groupby(ym).transform("sum")
    for c, l in [("unad_a", "R"), ("capm_a", "C"), ("ff3_a", "F")]: top[l] = (d.groupby("ym")[c].rank(ascending=False, method="first") <= n5).astype(float)
    t3 = {}
    for A, B in [("M", "R"), ("M", "F"), ("R", "C")]:
        X = pd.DataFrame({"diff": top[A] - top[B], "e": np.maximum(top[A], top[B])}); t3[A + B] = ols2(d.flow, X, d.FundId.values, ym.values)
    S = pd.get_dummies(d.star, prefix="s", drop_first=True).astype(float)
    a = r2(d.flow, None, ym); b = r2(d.flow, d[["unad_a"]], ym); c = r2(d.flow, S, ym); f = r2(d.flow, pd.concat([d[["unad_a"]], S], axis=1), ym)
    f4 = d[top["M"] == 1].groupby("ym").flow.mean().mean()
    # Figure 5B
    d["year"] = d.ym.str[:4]; june = betyg[betyg.ym.str.endswith("-06")].assign(year=lambda x: x.ym.str[:4]).rename(columns={"star_d": "focal"})[["FundId", "year", "focal"]]
    e = d[d.ym.str[5:].isin(["03", "04", "05"]) & (d.year >= "1998")].merge(june, on=["FundId", "year"]).dropna(subset=["focal"])
    out5 = []
    for tp, bt in [([5], [1]), ([4, 5], [1, 2])]:
        sp = lambda g, col: g.loc[g[col].isin(tp), "flow"].mean() - g.loc[g[col].isin(bt), "flow"].mean()
        per = e.groupby("ym").apply(lambda g: sp(g, "star") - sp(g, "focal"), include_groups=False); yy = per.groupby(per.index.str[:4]).sum()
        pl = yy.drop("2002"); out5.append(f"{yy['2002']:+.2f} (ovriga ar {pl.min():+.2f}..{pl.max():+.2f})")
    print(f"| {nm} | {len(d)} / {d.FundId.nunique()} | {d.flow.mean():+.2f} / {cs:.2f} | {t3['MR'][0]:+.3f} ({t3['MR'][1]:.2f}) | {t3['MF'][0]:+.3f} ({t3['MF'][1]:.2f}) | {t3['RC'][0]:+.3f} ({t3['RC'][1]:.2f}) | {100*f:.1f} / {100*(f-c):.1f} / {100*(f-b):.1f} | {f4:.2f} | {out5[0]} | {out5[1]} |")
def w(d, lo, hi):
    d = d.copy(); q = d.groupby("ym").flow.quantile([lo, hi]).unstack(); d["flow"] = d.flow.clip(d.ym.map(q[lo]), d.ym.map(q[hi])); return d
print("| Variant | Fondman / fonder | Flode medel / CS std | T3 stjarna-ra | T3 stjarna-FF3 | T3 ra-CAPM | Fig 3 tot / avk / betyg | Fig 4 femstj. | 5B 5 mot 1 | 5B 4-5 mot 1-2 |\n|---|---|---|---|---|---|---|---|---|---|")
print("| ANKARET | 248463 / 3341 | -0,54 / 2,18 | +0,099 (2,50) | +0,192 (4,85) | +0,032 (0,62) | 19,4 / 5,6 / 6,5 | 1,16 | utanfor | utanfor |")
rapport(base, "0. Nuvarande")
rapport(base[base.age >= 6.5], "1. Alder >= 78 manader")
rapport(base[base["size"] >= 50], "2. Storlek >= 50 MUSD")
rapport(base[(base.age >= 6.5) & (base["size"] >= 50)], "3. Bada")
rapport(w(base, .025, .975), "4. Kapning 2,5/97,5")
rapport(w(base, .05, .95), "5. Kapning 5/95")
rapport(w(base[base.age >= 6.5], .05, .95), "6. Alder + kapning 5/95")
print("\nSpridning per storleksgrupp (CS std):", base.assign(g=pd.qcut(base["size"], 5, labels=False)).groupby("g").flow.std().round(2).to_dict())
print("Spridning per aldersgrupp:", base.assign(g=pd.cut(base.age, [0, 5, 6.5, 10, 20, 100])).groupby("g", observed=True).flow.std().round(2).to_dict())
print("Alder/storlek median:", round(base.age.median(), 1), round(base['size'].median()), "| ankaret 12,8 / 411")
