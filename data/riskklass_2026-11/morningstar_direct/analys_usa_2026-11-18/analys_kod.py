"""Replikering enligt TILLÄGG 1 i DEKLARATION_replikering_bendavid_usa_1999_2005_2026-11-18:
kodens tidpunkt för betyget (samma månad som flödet), Table 3 i kodens form, Figure 5 A(b) med kodens kontroller.
Kör båda tidpunkterna sida vid sida. Användning: python3 -I analys_kod.py panel.pkl
"""
import sys
import numpy as np
import pandas as pd

base = pd.read_pickle(sys.argv[1])
alla = pd.read_pickle(sys.argv[1].replace(".pkl", "_alla.pkl"))
rng = np.random.default_rng(20261118)

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

def run(d, lab):
    R = {}
    d = d.reset_index(drop=True).copy(); ym = d["ym"]
    R["n"] = (len(d), d.FundId.nunique())
    # Figure 3, EW och VW kontinuerlig
    S = pd.get_dummies(d["star"].astype(int), prefix="s", drop_first=True).astype(float)
    wv = d["tna_l"] / d.groupby("ym")["tna_l"].transform("sum")
    for nm, w in [("EW", None), ("VW", wv)]:
        a = r2(d["flow"], None, [ym], w); b = r2(d["flow"], d[["signal"]], [ym], w)
        c = r2(d["flow"], S, [ym], w); dd = r2(d["flow"], pd.concat([d[["signal"]], S], axis=1), [ym], w)
        R[f"fig3_{nm}"] = (dd, a, dd - c, dd - b, dd - a - (dd - c) - (dd - b))
    # Figure 4 och Table 3
    M = (d["star"] == 5).astype(float); n5 = M.groupby(ym).transform("sum")
    U = (d.groupby("ym")["signal"].rank(ascending=False, method="first") <= n5).astype(float)
    R["andel5"] = M.mean()
    R["fig4"] = {g: d[m].groupby("ym")[["flow", "flow_usd", "pos"]].mean().mean() for g, m in [("M", M == 1), ("U", U == 1)]}
    t3k, t3d = {}, {}
    X = pd.DataFrame({"diff": M - U, "e": np.maximum(M, U)})
    Xd = pd.DataFrame({"M": M, "U": U})
    for c in ["flow", "flow_usd", "pos"]:
        b, se = ols(d[c], X, None, [d.FundId.values, ym.values], const=True)
        t3k[c] = (b["diff"], b["diff"] / se["diff"])
        b, _ = ols(d[c], Xd, ym, [d.FundId.values, ym.values])
        # standardfel för skillnaden via kontrast
        Z = fe_demean(pd.concat([d[c].rename("y"), Xd], axis=1), [ym]); A = Z[["M", "U"]].values; yt = Z["y"].values
        Ai = np.linalg.inv(A.T @ A); bb = Ai @ A.T @ yt; e = yt - A @ bb
        def meat(cl):
            u = pd.DataFrame(A * e[:, None]).groupby(np.asarray(cl)).sum().values; G = len(u); return G / (G - 1) * u.T @ u
        inter = pd.Series(list(zip(d.FundId.values, ym.values))).astype(str).values
        V = Ai @ (meat(d.FundId.values) + meat(ym.values) - meat(inter)) @ Ai
        k = np.array([1, -1]); t3d[c] = (k @ bb, (k @ bb) / np.sqrt(k @ V @ k))
    R["t3k"], R["t3d"] = t3k, t3d
    # Figure 5 A(b), kodens kontroller, kluster fond och månad; och enkel spec
    d["year"] = d["ym"].str[:4]; d["lsize"] = np.log(d["size"]); d["lage"] = np.log(d["age"].clip(lower=0.1))
    f5 = {}
    for yr, g in d.groupby("year"):
        g = g.reset_index(drop=True)
        b, se = ols(g["flow"], g[["star", "signal"]], g["ym"], [g.FundId.values, g.ym.values])
        gc = g.dropna(subset=["flow_l19", "sd60", "exp", "lage"]).reset_index(drop=True)
        kod = None
        if len(gc) > 500:
            b2, se2 = ols(gc["flow"], gc[["star", "signal", "flow_l19", "lsize", "lage", "exp", "sd60"]], gc["ym"], [gc.FundId.values, gc.ym.values])
            kod = (b2["star"], b2["star"] / se2["star"])
        f5[yr] = ((b["star"], b["star"] / se["star"]), kod)
    R["f5a"] = f5
    # Table 4 B
    d["m_star"] = d["ym"] + "_" + d["star"].astype(int).astype(str); d["m_cat"] = d["ym"] + "_" + d["cat"]
    t4 = {}
    for nm, g in [("före", d[d.ym <= "2002-06"]), ("efter", d[d.ym >= "2002-07"])]:
        g = g.reset_index(drop=True); y = g["flow"]; X1 = g[["signal"]]
        base0 = r2(y, X1, [g["ym"]]); rs = r2(y, X1, [g["m_star"]]); rc = r2(y, X1, [g["m_cat"]]); rsc = r2(y, X1, [g["m_star"], g["m_cat"]])
        t4[nm] = (rs - base0, rc - base0, rsc - rs)
    R["t4"] = t4
    # Figure 5 B
    june = alla[alla["ym"].str.endswith("-06")][["FundId", "ym", "star_d"]].copy()
    june["year"] = june["ym"].str[:4]; june = june.rename(columns={"star_d": "star_june"})[["FundId", "year", "star_june"]]
    e = d[d["ym"].str[5:].isin(["03", "04", "05"])].merge(june, on=["FundId", "year"], how="inner")
    def spread(g, col, top, bot):
        return g.loc[g[col].isin(top), "flow"].mean() - g.loc[g[col].isin(bot), "flow"].mean()
    f5b = {}
    for nm, top, bot in [("5 mot 1", [5], [1]), ("4–5 mot 1–2", [4, 5], [1, 2])]:
        per = e.groupby("ym").apply(lambda g: spread(g, "star", top, bot) - spread(g, "star_june", top, bot))
        yrs_s = per.groupby(per.index.str[:4]).sum()
        plac = per[~per.index.str.startswith("2002")]; yrs = sorted(set(plac.index.str[:4]))
        boot = [rng.choice(plac[plac.index.str.startswith(rng.choice(yrs))].values, 3, replace=True).sum() for _ in range(10000)]
        lo, hi = np.quantile(boot, [0.01, 0.99])
        f5b[nm] = (yrs_s, lo, hi)
    R["f5b"] = f5b
    return R

# Varianterna
lag = base.copy()                                   # betyg per slutet av t-1 (ursprunglig deklaration)
cur = base.drop(columns=["star"]).merge(alla[["FundId", "ym", "star_d"]].rename(columns={"star_d": "star"}), on=["FundId", "ym"], how="left")
cur = cur.dropna(subset=["star"])                   # betyg per slutet av t (kodens)
res = {"Kodens tidpunkt (betyg t)": run(cur, "kod"), "Vår tidpunkt (betyg t−1)": run(lag, "var")}

out = []
def say(s=""): print(s); out.append(s)
K, V = res["Kodens tidpunkt (betyg t)"], res["Vår tidpunkt (betyg t−1)"]
say(f"Urval: kodens tidpunkt {K['n'][0]} fondmånader ({K['n'][1]} fonder); vår {V['n'][0]} ({V['n'][1]}). Andel 5★: {100*K['andel5']:.1f} % / {100*V['andel5']:.1f} %")
say("\n| Test | Ankaret | Kodens tidpunkt | Vår tidpunkt |\n|---|---|---|---|")
for nm, anc in [("EW", "19,4 / 3,6 / 5,6 / 6,5 / 3,8"), ("VW", "28,9 / 5,9 / 6,8 / 9,6 / 6,7")]:
    f = lambda r: " / ".join(f"{100*x:.1f}" for x in r[f"fig3_{nm}"])
    say(f"| Figure 3 {nm} kont. (totalt / tid / avk / betyg / gem) | {anc} | {f(K)} | {f(V)} |")
for c, nm, k, anc in [("flow", "Table 3 flöde %", 1, "+0,099 (t 2,50)"), ("flow_usd", "Table 3 MUSD", 1, "+10,9 (t 6,27)"), ("pos", "Table 3 positivt (pp)", 100, "+7,1 (t 4,45)")]:
    say(f"| {nm}, kodens form | {anc} | {k*K['t3k'][c][0]:+.3f} (t {K['t3k'][c][1]:.2f}) | {k*V['t3k'][c][0]:+.3f} (t {V['t3k'][c][1]:.2f}) |")
for c, nm, k in [("flow", "Table 3 flöde %", 1), ("flow_usd", "Table 3 MUSD", 1), ("pos", "Table 3 positivt (pp)", 100)]:
    say(f"| {nm}, hela skillnaden med månadseffekter | | {k*K['t3d'][c][0]:+.3f} (t {K['t3d'][c][1]:.2f}) | {k*V['t3d'][c][0]:+.3f} (t {V['t3d'][c][1]:.2f}) |")
for g, nm in [("M", "Figure 4 topp Morningstar (% / MUSD / andel pos)"), ("U", "Figure 4 topp rå avkastning")]:
    f = lambda r: f"{r['fig4'][g].flow:.2f} / {r['fig4'][g].flow_usd:.1f} / {100*r['fig4'][g].pos:.1f}"
    say(f"| {nm} | {'1,16 / 37 / 67,5' if g=='M' else '0,99 / 18 / 61,7'} | {f(K)} | {f(V)} |")
for i, nm, anc in [(0, "Table 4 B månad × stjärna (före / efter)", "0,073 / 0,074"), (1, "Table 4 B månad × kategori", "0,043 / 0,015"), (2, "Table 4 B kategori utöver stjärna", "0,022 / 0,014")]:
    say(f"| {nm} | {anc} | {K['t4']['före'][i]:.3f} / {K['t4']['efter'][i]:.3f} | {V['t4']['före'][i]:.3f} / {V['t4']['efter'][i]:.3f} |")
for nm in ["5 mot 1", "4–5 mot 1–2"]:
    f = lambda r: f"2002 {r['f5b'][nm][0]['2002']:+.2f}, placebo [{r['f5b'][nm][1]:+.2f}; {r['f5b'][nm][2]:+.2f}]"
    say(f"| Figure 5 B {nm} | topp 2002 | {f(K)} | {f(V)} |")
say("\nFigure 5 A(b), stjärnans koefficient per år (kluster fond och månad)\n\n| År | Kodens tidpunkt, kodens kontroller | Kodens tidpunkt, stjärna + avk | Vår tidpunkt, kodens kontroller | Vår tidpunkt, stjärna + avk |\n|---|---|---|---|---|")
for yr in sorted(K["f5a"]):
    def fm(x): return "saknas" if x is None else f"{x[0]:.2f} (t {x[1]:.1f})"
    say(f"| {yr} | {fm(K['f5a'][yr][1])} | {fm(K['f5a'][yr][0])} | {fm(V['f5a'].get(yr,(None,None))[1])} | {fm(V['f5a'].get(yr,(None,None))[0])} |")
say("Ankaret (kodens kontroller och tidpunkt): 0,4–0,6 varje år.")
say("\nFigure 5 B, summa mars–maj per år (kodens tidpunkt)")
for nm in ["5 mot 1", "4–5 mot 1–2"]:
    say(f"{nm}: " + ", ".join(f"{k} {v:+.2f}" for k, v in K['f5b'][nm][0].items()))
open(sys.argv[1].replace("panel.pkl", "resultat_kod.md"), "w").write("\n".join(out))
