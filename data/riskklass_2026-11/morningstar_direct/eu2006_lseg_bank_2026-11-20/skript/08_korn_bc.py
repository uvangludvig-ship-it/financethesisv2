"""Korning B och C enligt DEKLARATION_handelsetest_eu_oktober_2006_med_lseg_formogenhet_2026-11-20.
python3 -I korn_bc.py <panel.pkl>"""
import sys
import numpy as np
import pandas as pd

d = pd.read_pickle(sys.argv[1]).reset_index(drop=True)
d["star"] = d.star_d.astype(float)
EV = "2006-10"
d["efter"] = (d.ym > EV).astype(float)
d["aldre"] = (d.age >= 5).astype(float)
out = []


def say(s=""):
    print(s)
    out.append(s)


def dem(X, g):
    return X - X.groupby(g.values).transform("mean")


def ols(g, y, xs, fe="ym"):
    g = g.dropna(subset=[y] + xs).reset_index(drop=True)
    Z = dem(g[[y] + xs].astype(float), g[fe])
    A = Z[xs].values
    yy = Z[y].values
    Ai = np.linalg.pinv(A.T @ A)
    b = Ai @ A.T @ yy
    e = yy - A @ b

    def meat(c):
        u = pd.DataFrame(A * e[:, None]).groupby(np.asarray(c)).sum().values
        G = len(u)
        return G / (G - 1) * u.T @ u

    V = Ai @ (meat(g.FundId.values) + meat(g.ym.values) - meat((g.FundId.astype(str) + "|" + g.ym).values)) @ Ai
    return pd.Series(b, index=xs), pd.Series(np.sqrt(np.clip(np.diag(V), 0, None)), index=xs), len(g), g.FundId.nunique()


def r2(y, X, gs):
    sst = np.sum((y - y.mean()) ** 2)
    Z = dem(pd.concat([y.rename("y"), X], axis=1), gs)
    e = Z.y.values
    A = Z.drop(columns="y").values
    b, *_ = np.linalg.lstsq(A, e, rcond=None)
    e = e - A @ b
    return 1 - np.sum(e ** 2) / sst


# ---------------- Korning B ----------------
for c in ("star", "unad_a"):
    d[c + "_E"] = d[c] * d.efter
    d[c + "_A"] = d[c] * d.aldre
    d[c + "_EA"] = d[c] * d.efter * d.aldre
d["EA"] = d.efter * d.aldre
XS = ["star", "star_E", "star_A", "star_EA", "unad_a", "unad_a_E", "unad_a_A", "unad_a_EA", "aldre", "EA"]
say("## Korning B: Betyg x Efter x Aldre (b4)")
say("\n| Fonster | b1 Betyg | b2 x Efter | b3 x Aldre | **b4 x Efter x Aldre** | SE b4 | t | 95 % | MDE | Fondmanader | Fonder | varav yngre fore / efter |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
for nm, lo, hi in [("2003-01 till 2010-12 (huvud)", "2003-01", "2010-12"), ("2004-11 till 2008-10 (variant)", "2004-11", "2008-10")]:
    g = d[(d.ym >= lo) & (d.ym <= hi) & (d.age >= 3)]
    b, se, n, nf = ols(g, "flow", XS)
    yb = int(((g.aldre == 0) & (g.efter == 0)).sum())
    ya = int(((g.aldre == 0) & (g.efter == 1)).sum())
    say(f"| {nm} | {b['star']:+.3f} ({b['star']/se['star']:.1f}) | {b['star_E']:+.3f} ({b['star_E']/se['star_E']:.1f}) | {b['star_A']:+.3f} ({b['star_A']/se['star_A']:.1f}) | **{b['star_EA']:+.3f}** | {se['star_EA']:.3f} | {b['star_EA']/se['star_EA']:.2f} | [{b['star_EA']-1.96*se['star_EA']:+.3f}; {b['star_EA']+1.96*se['star_EA']:+.3f}] | {2.8*se['star_EA']:.2f} | {n} | {nf} | {yb} / {ya} |")
    # de fyra cellerna var for sig
    cells = []
    for a_ in (1, 0):
        for e_ in (0, 1):
            gg = g[(g.aldre == a_) & (g.efter == e_)]
            bb, ss, nn, _ = ols(gg, "flow", ["star", "unad_a"])
            cells.append(f"{'aldre' if a_ else 'yngre'} {'efter' if e_ else 'fore'}: {bb['star']:+.3f} (t {bb['star']/ss['star']:.1f}, n {nn})")
    say("Flode per stjarna i de fyra cellerna: " + "; ".join(cells))

# Fama-MacBeth
say("\n**Fama-MacBeth (variant ii):** tvarsnitt per manad, koefficienten for Betyg x Aldre.")
g = d[(d.ym >= "2003-01") & (d.ym <= "2010-12") & (d.age >= 3)]
rows = []
for m, gm in g.groupby("ym"):
    if (gm.aldre == 0).sum() < 30 or (gm.aldre == 1).sum() < 30:
        continue
    X = np.c_[np.ones(len(gm)), gm[["star", "star_A", "unad_a", "unad_a_A", "aldre"]].values]
    b_, *_ = np.linalg.lstsq(X, gm.flow.values, rcond=None)
    rows.append((m, b_[1], b_[2], len(gm), int((gm.aldre == 0).sum())))
fm = pd.DataFrame(rows, columns=["ym", "b_star", "b_starA", "n", "n_yngre"]).set_index("ym")


def nw(x, L=6):
    x = np.asarray(x, float)
    T = len(x)
    u = x - x.mean()
    s = u @ u / T
    for k in range(1, L + 1):
        s += 2 * (1 - k / (L + 1)) * (u[k:] @ u[:-k]) / T
    return x.mean(), np.sqrt(s / T)


pre = fm[fm.index <= EV]
post = fm[fm.index > EV]
mp, sp = nw(pre.b_starA)
ma, sa = nw(post.b_starA)
dd = ma - mp
sd_ = np.sqrt(sp ** 2 + sa ** 2)
say(f"Manader fore {len(pre)} (fran {pre.index.min()}), efter {len(post)}. Betyg x Aldre: fore {mp:+.3f} (SE {sp:.3f}), efter {ma:+.3f} (SE {sa:.3f}). **Skillnad efter minus fore {dd:+.3f} (SE {sd_:.3f}, t {dd/sd_:.2f})**, 95 % [{dd-1.96*sd_:+.3f}; {dd+1.96*sd_:+.3f}].")
m1, s1 = nw(pre.b_star)
m2, s2 = nw(post.b_star)
say(f"Betyg for yngre fonder (basnivan): fore {m1:+.3f} (SE {s1:.3f}), efter {m2:+.3f} (SE {s2:.3f}). Minsta antal yngre fonder en manad: {int(fm.n_yngre.min())}.")

# ---------------- Korning C ----------------
say("\n## Korning C: samma fonder fore och efter")
d["m_star"] = d.ym + "_" + d.star.astype(int).astype(str)


def mr(g):
    g = g.dropna(subset=["unad_a"]).reset_index(drop=True)
    return r2(g.flow, g[["unad_a"]], g.m_star) - r2(g.flow, g[["unad_a"]], g.ym)


for nm, B, A, kmin in [("18 manader pa var sida", ("2005-05", "2006-10"), ("2006-11", "2008-04"), 12), ("36 manader pa var sida", ("2003-11", "2006-10"), ("2006-11", "2009-10"), 24)]:
    nb = d[(d.ym >= B[0]) & (d.ym <= B[1])].groupby("FundId").size()
    na = d[(d.ym >= A[0]) & (d.ym <= A[1])].groupby("FundId").size()
    keep = set(nb.index[nb >= kmin]) & set(na.index[na >= kmin])
    x = d[d.FundId.isin(keep)]
    say(f"\n**{nm}** ({B[0]}..{B[1]} mot {A[0]}..{A[1]}, minst {kmin} manader i vart fonster): {len(keep)} fonder\n\n| Grupp | Fonder | R2 fore | R2 efter | Flode per stjarna fore | efter |\n|---|---|---|---|---|---|")
    for gn, g0 in [("Minst fem ar i okt 2006", x[x.inc <= "2001-10-31"]), ("Tre till fem ar i okt 2006", x[(x.inc > "2001-10-31") & (x.inc <= "2003-10-31")])]:
        gb = g0[(g0.ym >= B[0]) & (g0.ym <= B[1])]
        ga = g0[(g0.ym >= A[0]) & (g0.ym <= A[1])]
        if g0.FundId.nunique() < 20:
            say(f"| {gn} | {g0.FundId.nunique()} | for fa | | | |")
            continue
        cb = ols(gb, "flow", ["star", "unad_a"])
        ca = ols(ga, "flow", ["star", "unad_a"])
        say(f"| {gn} | {g0.FundId.nunique()} | {mr(gb):.4f} | {mr(ga):.4f} | {cb[0]['star']:+.3f} (t {cb[0]['star']/cb[1]['star']:.1f}) | {ca[0]['star']:+.3f} (t {ca[0]['star']/ca[1]['star']:.1f}) |")
open(sys.argv[1].replace(".pkl", "_res_bc.md"), "w").write("\n".join(out))
