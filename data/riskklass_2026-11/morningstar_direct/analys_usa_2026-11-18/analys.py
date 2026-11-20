"""Replikering av Ben-David m.fl. (2022): Table 1, Figure 3, Figure 4/Table 3 rad 1, Figure 5 A(b), Table 4, Figure 5 B.
Specifikation: claude/DEKLARATION_replikering_bendavid_usa_1999_2005_2026-11-18.md
Användning: python3 -I analys.py panel.pkl
"""
import sys
import numpy as np
import pandas as pd

d = pd.read_pickle(sys.argv[1])
alla = pd.read_pickle(sys.argv[1].replace(".pkl", "_alla.pkl"))
rng = np.random.default_rng(20261118)

# ---------- hjälpfunktioner ----------
def demean(cols, groups, w=None, tol=1e-10, maxit=500):
    """Tar bort fixa effekter (en eller flera grupperingar) med alternerande projektioner, ev. viktat."""
    X = cols.astype(float).copy()
    ww = np.ones(len(X)) if w is None else np.asarray(w, float)
    for _ in range(maxit):
        prev = X.copy()
        for gcol in groups:
            gm = (X.mul(ww, axis=0)).groupby(gcol.values).transform("sum").div(
                pd.Series(ww, index=X.index).groupby(gcol.values).transform("sum"), axis=0)
            X = X - gm
        if len(groups) == 1 or np.nanmax(np.abs((X - prev).values)) < tol:
            break
    return X

def r2(y, X, groups, w=None):
    """R² inklusive fixa effekter, mot totalvariation runt (viktat) medel."""
    ww = np.ones(len(y)) if w is None else np.asarray(w, float)
    ybar = np.average(y, weights=ww)
    sst = np.sum(ww * (y - ybar) ** 2)
    cols = pd.DataFrame({"y": y}, index=y.index)
    if X is not None:
        cols = pd.concat([cols, X], axis=1)
    if groups:
        cols = demean(cols, groups, ww)
    yt = cols["y"].values
    if X is not None:
        Xt = cols.drop(columns="y").values
        sw = np.sqrt(ww)
        b, *_ = np.linalg.lstsq(Xt * sw[:, None], yt * sw, rcond=None)
        e = yt - Xt @ b
    else:
        e = yt
    return 1 - np.sum(ww * e ** 2) / sst

def ols_fe(y, X, fe, clusters):
    """OLS med fixa effekter (en gruppering), klustrade fel (en eller två dimensioner, Cameron-Gelbach-Miller)."""
    cols = demean(pd.concat([y.rename("y"), X], axis=1), [fe])
    yt, Xt = cols["y"].values, cols.drop(columns="y").values
    XtX_inv = np.linalg.inv(Xt.T @ Xt)
    b = XtX_inv @ Xt.T @ yt
    e = yt - Xt @ b
    def meat(cl):
        u = pd.DataFrame(Xt * e[:, None]).groupby(np.asarray(cl)).sum().values
        G = u.shape[0]
        return (G / (G - 1)) * (u.T @ u)
    if len(clusters) == 1:
        M = meat(clusters[0])
    else:
        inter = pd.Series(list(zip(clusters[0], clusters[1]))).astype(str).values
        M = meat(clusters[0]) + meat(clusters[1]) - meat(inter)
    V = XtX_inv @ M @ XtX_inv
    return pd.Series(b, index=X.columns), pd.DataFrame(V, index=X.columns, columns=X.columns)

ym = d["ym"]
out = []
def say(s=""):
    print(s); out.append(s)

# ---------- Table 1 ----------
say("## Table 1 (aktiva fonder)")
say(f"Fonder {d.FundId.nunique()}, fondmånader {len(d)}, {d.ym.min()} till {d.ym.max()}")
say("| Variabel | Antal | Medel | CS std | TS std | P5 | P25 | P50 | P75 | P95 |")
say("|---|---|---|---|---|---|---|---|---|---|")
for c, lab in [("size", "Storlek (MUSD)"), ("age", "Ålder (år)"), ("flow", "Flöde (%)"), ("flow_usd", "Flöde (MUSD)"), ("signal", "Avkastning, signal (%)")]:
    x = d[c].dropna()
    cs = d.groupby("ym")[c].std().mean(); ts = d.groupby("ym")[c].mean().std()
    pc = x.quantile([.05, .25, .5, .75, .95]).values
    say(f"| {lab} | {len(x)} | {x.mean():.2f} | {cs:.2f} | {ts:.2f} | " + " | ".join(f"{v:.2f}" for v in pc) + " |")
say("Ankaret: flöde medel −0,54, CS std 2,18; storlek medel 1 472, median 411; ålder medel 16,9.")

# ---------- Figure 3 ----------
say("\n## Figure 3: R²-uppdelning (procent)")
stars = pd.get_dummies(d["star"].astype(int), prefix="s", drop_first=True).astype(float)
# diskret signal: fem grupper lika stora som stjärngrupperna samma månad
def disc(gr):
    n = gr["star"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).values
    order = gr["signal"].rank(method="first").values
    cuts = np.cumsum(n)
    return pd.Series(np.searchsorted(cuts, order, side="left") + 1, index=gr.index)
d["sig_grp"] = d.groupby("ym", group_keys=False).apply(disc)
sigd = pd.get_dummies(d["sig_grp"], prefix="g", drop_first=True).astype(float)
wv = d["tna_l"] / d.groupby("ym")["tna_l"].transform("sum")
res3 = {}
for lab, w, S in [("EW kontinuerlig", None, d[["signal"]]), ("EW diskret", None, sigd),
                  ("VW kontinuerlig", wv, d[["signal"]]), ("VW diskret", wv, sigd)]:
    y = d["flow"]
    a = r2(y, None, [ym], w); b = r2(y, S, [ym], w); c_ = r2(y, stars, [ym], w)
    dd = r2(y, pd.concat([S, stars], axis=1), [ym], w)
    ms, mr = dd - b, dd - c_
    res3[lab] = dict(total=dd, tid=a, avk=mr, betyg=ms, gem=dd - a - ms - mr)
say("| Variant | Totalt | Tid | Avkastning | Betyg | Gemensamt |")
say("|---|---|---|---|---|---|")
for k, v in res3.items():
    say(f"| {k} | {100*v['total']:.1f} | {100*v['tid']:.1f} | {100*v['avk']:.1f} | {100*v['betyg']:.1f} | {100*v['gem']:.1f} |")
say("Ankaret EW kontinuerlig: totalt cirka 19,5; tid 3,6; avkastning 5,6; betyg 6,5; gemensamt 3,8. EW diskret: avkastning 6,0, betyg 6,5. VW: totalt cirka 29; betyg 9,6–9,8.")

# ---------- Figure 4 och Table 3 rad 1 ----------
say("\n## Figure 4 och Table 3 rad 1: femstjärniga mot toppfonder efter rå avkastning")
d["top_ms"] = (d["star"] == 5).astype(float)
n5 = d.groupby("ym")["top_ms"].transform("sum")
rk = d.groupby("ym")["signal"].rank(ascending=False, method="first")
d["top_ret"] = (rk <= n5).astype(float)
say(f"Andel toppklassade per månad: {d.top_ms.mean()*100:.1f} % (ankaret 7,4 %)")
say("| Grupp | Flöde (%) | Flöde (MUSD) | Andel positiva (%) |")
say("|---|---|---|---|")
for lab, m in [("Topp Morningstar", d.top_ms == 1), ("Topp rå avkastning", d.top_ret == 1), ("Alla fonder", pd.Series(True, index=d.index))]:
    x = d[m].groupby("ym")[["flow", "flow_usd", "pos"]].mean().mean()
    say(f"| {lab} | {x.flow:.2f} | {x.flow_usd:.1f} | {100*x.pos:.1f} |")
say("Ankaret: Topp Morningstar +1,16 % / cirka 37 MUSD / 67,5 %; topp rå avkastning +0,99 % / cirka 18 MUSD / 61,7 %; alla −0,49 % / cirka 0 / 35,2 %.")
say("| Utfall | Skillnad Morningstar − rå avkastning | t (kluster fond och månad) | Ankaret |")
say("|---|---|---|---|")
for c, lab, anc in [("flow", "Flöde (%)", "+0,099 (t 2,50)"), ("flow_usd", "Flöde (MUSD)", "+10,9 (t 6,27)"), ("pos", "Positivt flöde (pp)", "+7,1 (t 4,45)")]:
    b, V = ols_fe(d[c], d[["top_ms", "top_ret"]], ym, [d["FundId"].values, ym.values])
    diff = b["top_ms"] - b["top_ret"]; se = np.sqrt(V.loc["top_ms", "top_ms"] + V.loc["top_ret", "top_ret"] - 2 * V.loc["top_ms", "top_ret"])
    k = 100 if c == "pos" else 1
    say(f"| {lab} | {k*diff:+.3f} | {diff/se:.2f} | {anc} |")

# ---------- Figure 5 A(b) ----------
say("\n## Figure 5 A(b): flöde per stjärna, år för år (procent per månad)")
say("| År | Artikelns spec: stjärna + avkastning | t | Kodens kontroller | t | Fondmånader (kodspec) |")
say("|---|---|---|---|---|---|")
d["year"] = d["ym"].str[:4]
d["lsize"] = np.log(d["size"]); d["lage"] = np.log(d["age"].clip(lower=0.1))
for yr, g in d.groupby("year"):
    b, V = ols_fe(g["flow"], g[["star", "signal"]], g["ym"], [g["FundId"].values])
    gc = g.dropna(subset=["flow_l19", "sd60", "exp", "lage"])
    if len(gc) > 500:
        b2, V2 = ols_fe(gc["flow"], gc[["star", "signal", "flow_l19", "lsize", "lage", "exp", "sd60"]], gc["ym"], [gc["FundId"].values])
        s2 = f"{b2['star']:.2f} | {b2['star']/np.sqrt(V2.loc['star','star']):.1f} | {len(gc)}"
    else:
        s2 = "saknas | | "
    say(f"| {yr} | {b['star']:.2f} | {b['star']/np.sqrt(V.loc['star','star']):.1f} | {s2} |")
b, V = ols_fe(d["flow"], d[["star", "signal"]], ym, [d["FundId"].values, ym.values])
say(f"Poolat 1999–2005 (artikelns spec, kluster fond och månad): {b['star']:.3f} (t {b['star']/np.sqrt(V.loc['star','star']):.1f}). Ankaret: 0,4–0,6 varje år.")

# ---------- Table 4 ----------
say("\n## Table 4")
a = alla.sort_values(["FundId", "ym"]).copy()
a["star_d_prev"] = a.groupby("FundId")["star_d"].shift(1)
infund = set(d["FundId"])
ch = a[a["FundId"].isin(infund)].dropna(subset=["star_d", "star_d_prev"])
ch = ch[ch["ym"] >= "1999-02"]
frac = ch.assign(c=(ch.star_d != ch.star_d_prev)).groupby("ym")["c"].mean()
pre, ev, post = frac[frac.index < "2002-06"], frac.get("2002-06"), frac[frac.index > "2002-06"]
say("A. Andel fonder med ändrat betyg (betygsdatum; fonderna i urvalet)")
say(f"| Före juni 2002 | Juni 2002 | Efter juni 2002 |\n|---|---|---|\n| {100*pre.mean():.1f} % ({100*pre.std():.1f}) | {100*ev:.1f} % | {100*post.mean():.1f} % ({100*post.std():.1f}) |")
say("Ankaret: 13,9 % (3,5), 54,2 %, 11,9 % (2,8).")
say("B. Marginellt R² för att förklara flöden (regression av flöde på signal med månadseffekter)")
d["m_star"] = d["ym"] + "_" + d["star"].astype(int).astype(str)
d["m_cat"] = d["ym"] + "_" + d["cat"]
rows = {}
for lab, g in [("före", d[d.ym <= "2002-06"]), ("efter", d[d.ym >= "2002-07"])]:
    y, X = g["flow"], g[["signal"]]
    base = r2(y, X, [g["ym"]])
    rs = r2(y, X, [g["m_star"]])
    rc = r2(y, X, [g["m_cat"]])
    rsc = r2(y, X, [g["m_star"], g["m_cat"]])
    rows[lab] = (rs - base, rc - base, rsc - rs, len(g))
say("| | Före | Efter | Ankaret före | Ankaret efter |\n|---|---|---|---|---|")
say(f"| Månad × stjärna | {rows['före'][0]:.3f} | {rows['efter'][0]:.3f} | 0,073 | 0,074 |")
say(f"| Månad × kategori | {rows['före'][1]:.3f} | {rows['efter'][1]:.3f} | 0,043 | 0,015 |")
say(f"| Månad × kategori utöver månad × stjärna | {rows['före'][2]:.3f} | {rows['efter'][2]:.3f} | 0,022 | 0,014 |")
say(f"Fondmånader: före {rows['före'][3]}, efter {rows['efter'][3]}.")

# ---------- Figure 5 B, ekvation (2) ----------
say("\n## Figure 5 B: ekvation (2), mars–maj, faktiskt betyg mot junibetyg samma år")
june = alla[alla["ym"].str.endswith("-06")][["FundId", "ym", "star_d"]].copy()
june["year"] = june["ym"].str[:4]; june = june.rename(columns={"star_d": "star_june"})[["FundId", "year", "star_june"]]
e = d[d["ym"].str[5:].isin(["03", "04", "05"])].merge(june, on=["FundId", "year"], how="inner")
def spread(g, col, top, bot):
    return g.loc[g[col].isin(top), "flow"].mean() - g.loc[g[col].isin(bot), "flow"].mean()
res = {}
for lab, top, bot in [("(a) 5 mot 1", [5], [1]), ("(b) 4–5 mot 1–2", [4, 5], [1, 2])]:
    per = e.groupby("ym").apply(lambda g: spread(g, "star", top, bot) - spread(g, "star_june", top, bot))
    per.index = pd.Index(per.index, name="ym")
    yr = per.groupby(per.index.str[:4]).sum()
    plac = per[~per.index.str.startswith("2002")]
    yrs = sorted(set(plac.index.str[:4]))
    boot = []
    for _ in range(10000):
        y_ = rng.choice(yrs)
        vals = plac[plac.index.str.startswith(y_)].values
        boot.append(rng.choice(vals, 3, replace=True).sum())
    lo, hi = np.quantile(boot, [0.01, 0.99])
    res[lab] = (yr, lo, hi)
    say(f"{lab}: summa per år " + ", ".join(f"{k} {v:+.2f}" for k, v in yr.items()) + f". Placebo 1 %–99 %: [{lo:+.2f}; {hi:+.2f}]. 2002 utanför: {'ja' if (yr['2002']>hi or yr['2002']<lo) else 'nej'}.")
say(f"Fonder med junibetyg i mars–maj 2002: {e[e.year=='2002'].FundId.nunique() if 'year' in e else ''}")
say("Ankaret: tydlig topp 2002, utanför 1 %–99 %; placeboåren positiva 11, negativa 11, noll 4.")

open(sys.argv[1].replace("panel.pkl", "resultat.md"), "w").write("\n".join(out))
