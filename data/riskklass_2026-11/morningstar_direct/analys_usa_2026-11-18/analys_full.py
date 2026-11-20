"""Replikering av Ben-David m.fl. (2022) på USA-data juli 1997–december 2011, kodens specifikation.
Specifikation: claude/DEKLARATION_replikering_bendavid_usa_1997_2011_2026-11-18.md
Användning: python3 -I analys_full.py panel_full.pkl [kod|var]
"""
import sys
import numpy as np
import pandas as pd

tid = sys.argv[2] if len(sys.argv) > 2 else "kod"
allp = pd.read_pickle(sys.argv[1])
betyg = pd.read_pickle(sys.argv[1].replace(".pkl", "_betyg.pkl"))
starcol, incol = ("star_c", "in_kod") if tid == "kod" else ("star_l", "in_var")
d = allp[allp[incol]].copy().reset_index(drop=True)
d["star"] = d[starcol].astype(int)
ym = d["ym"]
rng = np.random.default_rng(20261118)
out = []
def say(s=""):
    print(s); out.append(s)

# ---------- hjälpfunktioner ----------
def fe_demean(X, groups, w=None, maxit=500, tol=1e-10):
    X = X.astype(float).copy(); ww = pd.Series(np.ones(len(X)) if w is None else np.asarray(w, float), index=X.index)
    for _ in range(maxit):
        prev = X.copy()
        for g in groups:
            num = X.mul(ww, axis=0).groupby(g.values).transform("sum"); den = ww.groupby(g.values).transform("sum")
            X = X - num.div(den, axis=0)
        if len(groups) == 1 or np.abs((X - prev).values).max() < tol:
            break
    return X

def r2(y, X, groups, w=None):
    ww = np.ones(len(y)) if w is None else np.asarray(w, float)
    sst = np.sum(ww * (y - np.average(y, weights=ww)) ** 2)
    Z = pd.DataFrame({"y": y}) if X is None else pd.concat([y.rename("y"), X], axis=1)
    Z = fe_demean(Z, groups, ww) if groups else Z
    e = Z["y"].values
    if X is not None:
        A = Z.drop(columns="y").values; sw = np.sqrt(ww)
        b, *_ = np.linalg.lstsq(A * sw[:, None], e * sw, rcond=None); e = e - A @ b
    return 1 - np.sum(ww * e ** 2) / sst

def ols(y, X, fe, clusters, const=False):
    Z = pd.concat([y.rename("y"), X], axis=1)
    if fe is not None:
        Z = fe_demean(Z, [fe])
    yt = Z["y"].values; A = Z.drop(columns="y").values
    if const:
        A = np.c_[np.ones(len(A)), A]
    Ai = np.linalg.inv(A.T @ A); b = Ai @ A.T @ yt; e = yt - A @ b
    def meat(cl):
        u = pd.DataFrame(A * e[:, None]).groupby(np.asarray(cl)).sum().values; G = len(u); return G / (G - 1) * u.T @ u
    if len(clusters) == 1:
        Mx = meat(clusters[0])
    else:
        inter = pd.Series(list(zip(clusters[0], clusters[1]))).astype(str).values
        Mx = meat(clusters[0]) + meat(clusters[1]) - meat(inter)
    V = Ai @ Mx @ Ai
    names = (["_cons"] if const else []) + list(X.columns)
    return pd.Series(b, index=names), pd.Series(np.sqrt(np.diag(V)), index=names)

def newey_west(y, x, lags=6):
    X = np.c_[np.ones(len(x)), x]; b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
    Xi = np.linalg.inv(X.T @ X); S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None]); S += w * (G + G.T)
    V = Xi @ S @ Xi; r2_ = 1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2)
    return b[1], b[1] / np.sqrt(V[1, 1]), r2_

say(f"# Replikering USA 1997–2011, tidpunkt för betyget: {'kodens (betyg per slutet av t)' if tid=='kod' else 'variant (betyg per slutet av t−1)'}")
say(f"Fondmånader {len(d)}, fonder {d.FundId.nunique()}, {d.ym.min()} till {d.ym.max()} (ankaret 248 463 och 3 341, 1997-07 till 2011-12).")

# ---------- Table 1 ----------
say("\n## Table 1\n\n| Variabel | Antal | Medel | CS std | TS std | P5 | P25 | P50 | P75 | P95 | Ankaret medel / CS std / P50 |\n|---|---|---|---|---|---|---|---|---|---|---|")
anc1 = {"size": "1 472 / 3 038 / 411", "age": "16,9 / 12,8 / 12,8", "flow": "−0,54 / 2,18 / −0,61", "flow_usd": "−2,6 / 52,4 / −1,2",
        "unad_a": "0,34 / 0,99 / 0,71", "retexmkt_a": "0,07 / 0,99 / 0,01", "capm_a": "0,09 / 0,95 / 0,03", "ff3_a": "−0,03 / 0,78 / −0,07", "carh_a": "−0,03 / 0,76 / −0,06"}
for c, lab in [("size", "Storlek (MUSD)"), ("age", "Ålder (år)"), ("flow", "Flöde (%)"), ("flow_usd", "Flöde (MUSD)"), ("unad_a", "Rå överavk. (%)"),
               ("retexmkt_a", "Marknadsjust. (%)"), ("capm_a", "CAPM-alfa (%)"), ("ff3_a", "FF3-alfa (%)"), ("carh_a", "FFC-alfa (%)")]:
    x = d[c].dropna(); cs = d.groupby("ym")[c].std().mean(); ts = d.groupby("ym")[c].mean().std()
    pc = x.quantile([.05, .25, .5, .75, .95]).values
    say(f"| {lab} | {len(x)} | {x.mean():.2f} | {cs:.2f} | {ts:.2f} | " + " | ".join(f"{v:.2f}" for v in pc) + f" | {anc1[c]} |")

# ---------- Table 2 ----------
say("\n## Table 2, kolumn 1–5: aggregerat likaviktat flöde på aggregerat mått (z-värde), Newey-West 6\n\n| Mått | Koef. | t | R² | Ankaret |\n|---|---|---|---|---|")
agg = d.groupby("ym")[["flow", "unad_a", "retexmkt_a", "capm_a", "ff3_a", "carh_a"]].mean()
for c, lab, anc in [("unad_a", "Rå", "0,179 (4,47), R² 0,159"), ("retexmkt_a", "Marknadsjust.", "0,015 (0,26)"), ("capm_a", "CAPM", "0,018 (0,38)"),
                    ("ff3_a", "FF3", "−0,048 (−1,01)"), ("carh_a", "FFC", "−0,018 (−0,36)")]:
    z = (agg[c] - agg[c].mean()) / agg[c].std()
    b, t, rr = newey_west(agg["flow"].values, z.values)
    say(f"| {lab} | {b:+.3f} | {t:.2f} | {rr:.3f} | {anc} |")
say(f"Månader: {len(agg)} (ankaret 175).")

# ---------- Figure 3 ----------
say("\n## Figure 3: R²-uppdelning (procent)\n\n| Variant | Totalt | Tid | Avkastning | Betyg | Gemensamt | Ankaret (totalt / tid / avk / betyg / gem) |\n|---|---|---|---|---|---|---|")
S = pd.get_dummies(d["star"], prefix="s", drop_first=True).astype(float)
def disc(gr):
    n = gr["star"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).values
    order = gr["unad_a"].rank(method="first").values
    return pd.Series(np.searchsorted(np.cumsum(n), order, side="left") + 1, index=gr.index)
d["sig_grp"] = d.groupby("ym", group_keys=False).apply(disc)
G = pd.get_dummies(d["sig_grp"], prefix="g", drop_first=True).astype(float)
wv = d["size"] / d.groupby("ym")["size"].transform("sum")
anc3 = {"EW kontinuerlig": "19,4 / 3,6 / 5,6 / 6,5 / 3,8", "EW diskret": "19,8 / 3,6 / 6,0 / 6,5 / 3,8", "VW kontinuerlig": "28,9 / 5,9 / 6,8 / 9,6 / 6,7", "VW diskret": "29,0 / 5,9 / 6,9 / 9,8 / 6,5"}
for lab, w, X in [("EW kontinuerlig", None, d[["unad_a"]]), ("EW diskret", None, G), ("VW kontinuerlig", wv, d[["unad_a"]]), ("VW diskret", wv, G)]:
    a = r2(d["flow"], None, [ym], w); b = r2(d["flow"], X, [ym], w); c = r2(d["flow"], S, [ym], w); dd = r2(d["flow"], pd.concat([X, S], axis=1), [ym], w)
    say(f"| {lab} | {100*dd:.1f} | {100*a:.1f} | {100*(dd-c):.1f} | {100*(dd-b):.1f} | {100*(dd-a-(dd-c)-(dd-b)):.1f} | {anc3[lab]} |")

# ---------- Figure 4 och Table 3 ----------
top = {"Morningstar": (d["star"] == 5).astype(float)}
n5 = top["Morningstar"].groupby(ym).transform("sum")
for c, lab in [("unad_a", "Rå"), ("capm_a", "CAPM"), ("ff3_a", "FF3"), ("carh_a", "FFC")]:
    top[lab] = (d.groupby("ym")[c].rank(ascending=False, method="first") <= n5).astype(float)
say(f"\n## Figure 4: toppfonder (andel toppklassade per månad {100*top['Morningstar'].mean():.1f} %, ankaret 7,4 %)\n\n| Grupp | Flöde (%) | Flöde (MUSD) | Andel positiva (%) |\n|---|---|---|---|")
for lab, m in list(top.items()) + [("Alla", pd.Series(1.0, index=d.index))]:
    x = d[m == 1].groupby("ym")[["flow", "flow_usd", "pos"]].mean().mean()
    say(f"| {lab} | {x.flow:.2f} | {x.flow_usd:.1f} | {100*x.pos:.1f} |")
say("Ankaret: Morningstar 1,16 / cirka 37 / 67,5; rå 0,99 / cirka 18 / 61,7; alla −0,49 / cirka 0 / 35,2. Övriga alfor lägre än rå.")
say("\n## Table 3: kodens form (b1 på A − B, ingen månadseffekt, kluster fond och månad)\n\n| Par | Flöde (%) | t | MUSD | t | Positivt (pp) | t | Ankaret % (t) / MUSD / pp |\n|---|---|---|---|---|---|---|---|")
anc_t3 = {("Morningstar", "Rå"): "0,099 (2,50) / 10,9 / 7,1", ("Morningstar", "CAPM"): "0,108 (2,72) / 11,0 / 7,3", ("Morningstar", "FF3"): "0,192 (4,85) / 12,3 / 10,4",
          ("Morningstar", "FFC"): "0,188 (4,73) / 12,5 / 10,0", ("Rå", "CAPM"): "0,032 (0,62) / 0,3 / 0,8", ("Rå", "FF3"): "0,207 (4,74) / 3,1 / 7,3",
          ("Rå", "FFC"): "0,195 (4,48) / 3,7 / 6,5", ("CAPM", "FF3"): "0,220 (5,06) / 3,4 / 8,0", ("CAPM", "FFC"): "0,197 (4,55) / 3,9 / 6,8", ("FF3", "FFC"): "−0,017 (−0,26) / 1,7 / −1,4"}
cl = [d.FundId.values, ym.values]
for (A, B), anc in anc_t3.items():
    X = pd.DataFrame({"diff": top[A] - top[B], "e": np.maximum(top[A], top[B])})
    cells = []
    for c, k in [("flow", 1), ("flow_usd", 1), ("pos", 100)]:
        b, se = ols(d[c], X, None, cl, const=True); cells += [f"{k*b['diff']:+.3f}", f"{b['diff']/se['diff']:.2f}"]
    say(f"| {A} mot {B} | " + " | ".join(cells) + f" | {anc} |")

# ---------- Figure 5 A ----------
d["year"] = d["ym"].str[:4]; d["lsize"] = np.log(d["size"]); d["lage"] = np.log(d["age"].clip(lower=0.1))
say("\n## Figure 5 A(a): medelflöde (%) per betyg och år\n\n| År | 1 | 2 | 3 | 4 | 5 |\n|---|---|---|---|---|---|")
fa = d.groupby(["year", "star"])["flow"].mean().unstack()
for yr, r_ in fa.iterrows():
    say(f"| {yr} | " + " | ".join(f"{v:.2f}" for v in r_.values) + " |")
say("Ankaret 2002: −1,58 / −1,26 / −0,78 / 0,05 / 1,28; 2008: −2,06 / −1,72 / −1,16 / −0,38 / 0,54.")
say("\n## Figure 5 A(b): betygets koefficient per år, kodens kontroller, kluster fond och månad\n\n| År | Koef. | t | Fondmånader |\n|---|---|---|---|")
for yr, g in d.groupby("year"):
    gc = g.dropna(subset=["flow_l19", "sd60", "exp", "lage", "lsize"]).reset_index(drop=True)
    b, se = ols(gc["flow"], gc[["star", "unad_a", "flow_l19", "lsize", "lage", "exp", "sd60"]], gc["ym"], [gc.FundId.values, gc.ym.values])
    say(f"| {yr} | {b['star']:.2f} | {b['star']/se['star']:.1f} | {len(gc)} |")
say("Ankaret: 0,4–0,6 varje år.")

# ---------- Table 4 ----------
q = d.sort_values(["FundId", "ym"]).copy()
q["prev"] = q.groupby("FundId")["star"].shift(1)
q = q.dropna(subset=["prev"]); q["ch"] = (q["star"] != q["prev"]).astype(float)
grp = np.where(q.ym < "2002-06", "före", np.where(q.ym == "2002-06", "juni", "efter"))
fr_ = q.assign(g=grp).groupby(["g", "ym"])["ch"].mean()
say("\n## Table 4 A: andel med ändrat betyg\n\n| Före juni 2002 | Juni 2002 | Efter juni 2002 | Ankaret |\n|---|---|---|---|")
say(f"| {100*q[grp=='före'].ch.mean():.1f} % ({100*fr_['före'].std():.1f}) | {100*q[grp=='juni'].ch.mean():.1f} % | {100*q[grp=='efter'].ch.mean():.1f} % ({100*fr_['efter'].std():.1f}) | 13,9 % (3,5) / 54,2 % / 11,9 % (2,8) |")
d["m_star"] = d["ym"] + "_" + d["star"].astype(str); d["m_cat"] = d["ym"] + "_" + d["cat"]
say("\n## Table 4 B: marginellt R²\n\n| | Före | Efter | Ankaret före / efter |\n|---|---|---|---|")
res = {}
for nm, g in [("före", d[d.ym <= "2002-06"]), ("efter", d[d.ym > "2002-06"])]:
    g = g.reset_index(drop=True); y = g["flow"]; X1 = g[["unad_a"]]
    b0 = r2(y, X1, [g["ym"]]); rs = r2(y, X1, [g["m_star"]]); rc = r2(y, X1, [g["m_cat"]]); rsc = r2(y, X1, [g["m_star"], g["m_cat"]])
    res[nm] = (rs - b0, rc - b0, rsc - rs, len(g))
for i, lab, anc in [(0, "Månad × betyg", "0,073 / 0,074"), (1, "Månad × kategori", "0,043 / 0,015"), (2, "Kategori utöver betyg", "0,022 / 0,014")]:
    say(f"| {lab} | {res['före'][i]:.3f} | {res['efter'][i]:.3f} | {anc} |")
say(f"Fondmånader före {res['före'][3]} (ankaret 51 322), efter {res['efter'][3]} (ankaret 197 141).")

# ---------- Figure 5 B ----------
june = betyg[betyg["ym"].str.endswith("-06")].copy(); june["year"] = june["ym"].str[:4]
june = june.rename(columns={"star_d": "focal"})[["FundId", "year", "focal"]]
e = d[d["ym"].str[5:].isin(["03", "04", "05"]) & (d["year"] >= "1998")].merge(june, on=["FundId", "year"], how="inner").dropna(subset=["focal"])
def spread(g, col, top_, bot):
    return g.loc[g[col].isin(top_), "flow"].mean() - g.loc[g[col].isin(bot), "flow"].mean()
say("\n## Figure 5 B: ekvation (2), summa mars–maj per år\n\n| År | 5 mot 1 | 4–5 mot 1–2 |\n|---|---|---|")
per = {}
for nm, top_, bot in [("a", [5], [1]), ("b", [4, 5], [1, 2])]:
    per[nm] = e.groupby("ym").apply(lambda g: spread(g, "star", top_, bot) - spread(g, "focal", top_, bot))
yrs_a = per["a"].groupby(per["a"].index.str[:4]).sum(); yrs_b = per["b"].groupby(per["b"].index.str[:4]).sum()
for yr in yrs_a.index:
    say(f"| {'**'+yr+'**' if yr=='2002' else yr} | {yrs_a[yr]:+.2f} | {yrs_b[yr]:+.2f} |")
for nm, yrs_s in [("a", yrs_a), ("b", yrs_b)]:
    plac = per[nm][~per[nm].index.str.startswith("2002")]; ys = sorted(set(plac.index.str[:4]))
    boot = [rng.choice(plac[plac.index.str.startswith(rng.choice(ys))].values, 3, replace=True).sum() for _ in range(10000)]
    lo, hi = np.quantile(boot, [0.01, 0.99])
    p_ = (yrs_s.drop("2002") > 0.05).sum(); n_ = (yrs_s.drop("2002") < -0.05).sum(); z_ = len(yrs_s) - 1 - p_ - n_
    say(f"Panel {nm}: 2002 = {yrs_s['2002']:+.2f}; placebo 1 %–99 % [{lo:+.2f}; {hi:+.2f}]; utanför: {'ja' if yrs_s['2002']>hi else 'nej'}; placeboår positiva {p_}, negativa {n_}, nära noll {z_} (ankaret 11 / 11 / 4).")

open(sys.argv[1].replace("panel_full.pkl", f"resultat_full_{tid}.md"), "w").write("\n".join(out))
