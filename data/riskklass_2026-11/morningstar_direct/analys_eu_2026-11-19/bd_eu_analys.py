"""Ben-David m.fl. (2022) pa EU-data 2018-2025 (samma kod som USA) och hastkapplopningen.
Specifikation: claude/DEKLARATION_bendavid_eu_och_hastkapplopning_A1_A3_2026-11-19.md
Anvandning: python3 -I bd_eu_analys.py <panel.pkl> [kod|var]
"""
import sys
import numpy as np
import pandas as pd

tid = sys.argv[2] if len(sys.argv) > 2 else "kod"
allp = pd.read_pickle(sys.argv[1])
starcol, incol = ("star_c", "in_kod") if tid == "kod" else ("star_l", "in_var")
d = allp[allp[incol]].copy().reset_index(drop=True)
d["star"] = d[starcol].astype(int)
ym = d["ym"]
rng = np.random.default_rng(20261119)
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

say(f"# Ben-David pa EU-data 2018-2025 ({sys.argv[1]}), tidpunkt for betyget: {'kodens (betyg per slutet av t)' if tid=='kod' else 'variant (betyg per slutet av t−1)'}")
say(f"Fondmanader {len(d)}, fonder {d.FundId.nunique()}, {d.ym.min()} till {d.ym.max()} (ankaret, USA: 248 463 och 3 341, 1997-07 till 2011-12).")

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
say(f"Manader: {len(agg)} (ankaret 175).")

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

# ---------- Table 3, variant: Europe-faktorer ----------
say("\n## Table 3, variant med Europe-faktorer (flode %, t)\n\n| Par | Flode (%) | t |\n|---|---|---|")
topE = {"Morningstar": top["Morningstar"]}
for c, lab in [("capm_eur_a", "CAPM-Eur"), ("ff3_eur_a", "FF3-Eur"), ("carh_eur_a", "FFC-Eur")]:
    ok_ = d[c].notna()
    topE[lab] = ((d.groupby("ym")[c].rank(ascending=False, method="first") <= n5) & ok_).astype(float)
for A, B in [("Morningstar", "CAPM-Eur"), ("Morningstar", "FF3-Eur"), ("Morningstar", "FFC-Eur")]:
    X = pd.DataFrame({"diff": topE[A] - topE[B], "e": np.maximum(topE[A], topE[B])})
    b, se = ols(d["flow"], X, None, cl, const=True); say(f"| {A} mot {B} | {b['diff']:+.3f} | {b['diff']/se['diff']:.2f} |")

# ---------- HASTKAPPLOPNINGEN ----------
h = d.dropna(subset=["lab"]).reset_index(drop=True); h["lab"] = h["lab"].astype(int)
say(f"\n# Hastkapplopningen: riskklassen som tredje signal\nFondmanader med visad riskklass: {len(h)}, fonder {h.FundId.nunique()}. Fordelning: {h.lab.value_counts().sort_index().to_dict()}")
def blocks(g):
    S_ = pd.get_dummies(g["star"], prefix="s", drop_first=True).astype(float)
    L_ = pd.get_dummies(g["lab"], prefix="k").astype(float)
    if "k_4" in L_: L_ = L_.drop(columns="k_4")
    else: L_ = L_.iloc[:, 1:]
    return g[["unad_a"]], S_, L_
say("\n## H1: R2-uppdelning med tre block (procent). Marginellt = R2 med alla tre minus R2 utan blocket\n\n| Urval | Vikt | Fondmanader | Totalt | Tid | Avkastning marg. | Betyg marg. | Riskklass marg. |\n|---|---|---|---|---|---|---|---|")
for nm, g in [("2018-2025", h), ("2018-2022 (SRRI)", h[h.ym <= "2022-12"]), ("2023-2025 (SRI)", h[h.ym >= "2023-01"])]:
    g = g.reset_index(drop=True); A_, S_, L_ = blocks(g); ymg = g["ym"]
    for wl in ("EW", "VW"):
        w = None if wl == "EW" else g["size"] / g.groupby("ym")["size"].transform("sum")
        t0 = r2(g["flow"], None, [ymg], w); full = r2(g["flow"], pd.concat([A_, S_, L_], axis=1), [ymg], w)
        nA = r2(g["flow"], pd.concat([S_, L_], axis=1), [ymg], w); nS = r2(g["flow"], pd.concat([A_, L_], axis=1), [ymg], w); nL = r2(g["flow"], pd.concat([A_, S_], axis=1), [ymg], w)
        say(f"| {nm} | {wl} | {len(g)} | {100*full:.2f} | {100*t0:.2f} | {100*(full-nA):.2f} | {100*(full-nS):.2f} | {100*(full-nL):.2f} |")

h["lsize"] = np.log(h["size"]); h["lage"] = np.log(h["age"].clip(lower=0.1)); h["m_cat"] = h["ym"] + "_" + h["cat"]
ctrl = ["unad_a", "flow_l19", "lsize", "lage", "exp", "sd60"]
def h2(g, fe, nm):
    g = g.dropna(subset=ctrl).reset_index(drop=True)
    A_, S_, L_ = blocks(g)
    X = pd.concat([S_, L_, g[ctrl]], axis=1)
    b, se = ols(g["flow"], X, g[fe], [g.FundId.values, g.ym.values])
    # gemensamt Wald-test for riskklassdummies (med samma kovarians: berakna om)
    Z = pd.concat([g["flow"].rename("y"), X], axis=1); Z = fe_demean(Z, [g[fe]])
    yt = Z["y"].values; Am = Z.drop(columns="y").values; Ai = np.linalg.inv(Am.T @ Am); bb = Ai @ Am.T @ yt; e = yt - Am @ bb
    def meat(c_):
        u = pd.DataFrame(Am * e[:, None]).groupby(np.asarray(c_)).sum().values; G_ = len(u); return G_ / (G_ - 1) * u.T @ u
    inter = (g.FundId.astype(str) + "|" + g.ym).values
    V = Ai @ (meat(g.FundId.values) + meat(g.ym.values) - meat(inter)) @ Ai
    ix = [list(X.columns).index(c) for c in L_.columns]; wv = bb[ix] @ np.linalg.pinv(V[np.ix_(ix, ix)]) @ bb[ix]
    from scipy import stats as _st
    p = _st.chi2.sf(wv, len(ix))
    say(f"\n**H2a {nm}** ({len(g)} fondmanader, {g.FundId.nunique()} fonder). Flode i procent per manad, bas betyg 1 och riskklass 4.")
    say("| Variabel | Koef. | t |\n|---|---|---|")
    for c in list(S_.columns) + list(L_.columns) + ["unad_a", "sd60"]:
        say(f"| {c} | {b[c]:+.3f} | {b[c]/se[c]:.2f} |")
    say(f"Gemensamt test riskklassdummies: chi2 {wv:.2f}, df {len(ix)}, p {p:.3f}")
    # linjar
    XL = pd.concat([g[["star", "lab"]].astype(float), g[ctrl]], axis=1)
    b2, se2 = ols(g["flow"], XL, g[fe], [g.FundId.values, g.ym.values])
    say(f"**H2b {nm}, linjar:** riskklass {b2['lab']:+.3f} (t {b2['lab']/se2['lab']:.2f}), 95 % [{b2['lab']-1.96*se2['lab']:+.3f}; {b2['lab']+1.96*se2['lab']:+.3f}] | betyg {b2['star']:+.3f} (t {b2['star']/se2['star']:.2f}) | per ar: riskklass {12*b2['lab']:+.2f} pp, betyg {12*b2['star']:+.2f} pp | kvot riskklass/betyg {b2['lab']/b2['star']:+.2f}")
    return b2, se2
say("\n## H2: regression med betyg, riskklass, avkastning och kodens kontroller")
h2(h, "ym", "2018-2025, manadseffekt (huvud)")
h2(h, "m_cat", "2018-2025, manad x kategori")
h2(h[h.ym <= "2022-12"], "ym", "2018-2022 (SRRI), manadseffekt")
h2(h[h.ym >= "2023-01"], "ym", "2023-2025 (SRI), manadseffekt")

# verifiering: inplanterad effekt av riskklassen
hv = h.dropna(subset=ctrl).reset_index(drop=True).copy(); hv["flow"] = hv["flow"] + 0.10 * hv["lab"]
XL = pd.concat([hv[["star", "lab"]].astype(float), hv[ctrl]], axis=1); bv, sv = ols(hv["flow"], XL, hv["ym"], [hv.FundId.values, hv.ym.values])
hb = h.dropna(subset=ctrl).reset_index(drop=True); XL0 = pd.concat([hb[["star", "lab"]].astype(float), hb[ctrl]], axis=1); b0_, s0_ = ols(hb["flow"], XL0, hb["ym"], [hb.FundId.values, hb.ym.values])
say(f"\nVerifiering: inplanterad +0,100 per riskklass ger {bv['lab']:+.4f} (vantat {b0_['lab'] + 0.1:+.4f})")

open(sys.argv[1].replace(".pkl", f"_resultat_{tid}.md"), "w").write("\n".join(out))
