"""Korning enligt DEKLARATION_bankagda_mot_fristaende_fondbolag_2026-11-20."""
import sys
import warnings
import numpy as np
import pandas as pd
sys.path.insert(0, "/home/claude/bank")
import importlib.util as _u; _s = _u.spec_from_file_location("klass", __file__.replace("12_kor_bank.py", "11_klass.py")); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m); klassa = _m.klassa

warnings.filterwarnings("ignore")
out = []


def say(s=""):
    print(s)
    out.append(s)


def dem(X, g):
    return X - X.groupby(g.values).transform("mean")


def ols(g, y, xs, fe):
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


def nw(x, L=6):
    x = np.asarray(x, float)
    T = len(x)
    u = x - x.mean()
    s = u @ u / T
    for k in range(1, L + 1):
        s += 2 * (1 - k / (L + 1)) * (u[k:] @ u[:-k]) / T
    return x.mean(), np.sqrt(s / T)


def huvud(d, namn):
    d = d.copy()
    d["bank"] = (d.grp2 == "B").astype(float)
    d["star_B"] = d.star * d.bank
    d["sig_B"] = d.unad_a * d.bank
    d["fe"] = d.ym + "_" + d.grp2
    XS = ["star", "star_B", "unad_a", "sig_B"]
    b, se, n, nf = ols(d, "flow", XS, "fe")
    t = b / se
    say(f"| {namn} | {b['star']:+.3f} ({t['star']:.1f}) | **{b['star_B']:+.3f}** | {se['star_B']:.3f} | {t['star_B']:.2f} | [{b['star_B']-1.96*se['star_B']:+.3f}; {b['star_B']+1.96*se['star_B']:+.3f}] | {2.8*se['star_B']:.2f} | {b['unad_a']:+.3f} ({t['unad_a']:.1f}) | {b['sig_B']:+.3f} ({t['sig_B']:.2f}) | {n} | {nf} |")
    return b, se


def fmb(d):
    d = d.copy()
    d["bank"] = (d.grp2 == "B").astype(float)
    rows = []
    for m, gm in d.dropna(subset=["flow", "star", "unad_a"]).groupby("ym"):
        if (gm.bank == 1).sum() < 30 or (gm.bank == 0).sum() < 30:
            continue
        X = np.c_[np.ones(len(gm)), gm.bank, gm.star, gm.star * gm.bank, gm.unad_a, gm.unad_a * gm.bank]
        b_, *_ = np.linalg.lstsq(X, gm.flow.values, rcond=None)
        rows.append((m, b_[2], b_[3], b_[4], b_[5]))
    f = pd.DataFrame(rows, columns=["ym", "star", "star_B", "sig", "sig_B"])
    r = {c: nw(f[c]) for c in ["star", "star_B", "sig", "sig_B"]}
    return r, len(f)


def panel(d, titel, extra=None):
    say(f"\n## {titel}")
    say("\n**Flode per stjarna i varje grupp for sig** (flode pa betyg och signal, manadseffekter, kluster fond och manad)\n")
    say("| Grupp | Per stjarna | SE | t | Signal | t | Fondmanader | Fonder |\n|---|---|---|---|---|---|---|---|")
    for gname in ["B", "F", "O", "oklassad"]:
        g = d[d.grp == gname]
        b, se, n, nf = ols(g, "flow", ["star", "unad_a"], "ym")
        say(f"| {gname} | {b['star']:+.3f} | {se['star']:.3f} | {b['star']/se['star']:.1f} | {b['unad_a']:+.3f} | {b['unad_a']/se['unad_a']:.1f} | {n} | {nf} |")
    say("\n**Huvudtest och varianter**\n")
    say("| Test | b1 Betyg (t) | **b2 Betyg x Bank** | SE | t | 95 % | MDE | c1 Signal (t) | c2 Signal x Bank (t) | Fondmanader | Fonder |\n|---|---|---|---|---|---|---|---|---|---|---|")
    m = d[d.grp.isin(["B", "F"])].assign(grp2=lambda x: x.grp)
    huvud(m, "Huvud: B mot F")
    v2 = d[d.grp.isin(["B", "F", "O"])].assign(grp2=lambda x: np.where(x.grp == "B", "B", "F"))
    huvud(v2, "Variant 2: B mot F+O")
    v3 = m[~m.us]
    huvud(v3, "Variant 3: utan JPMorgan, Goldman Sachs, Morgan Stanley")
    if extra is not None:
        e = extra[extra.grp.isin(["B", "F"])].assign(grp2=lambda x: x.grp)
        huvud(e, "Variant 4: 2003-2016, samma klassning")
    r, T = fmb(m)
    say(f"\n**Variant 1, Fama-MacBeth** ({T} manader, Newey-West 6 laggar): b1 Betyg {r['star'][0]:+.3f} (SE {r['star'][1]:.3f}, t {r['star'][0]/r['star'][1]:.1f}); **b2 Betyg x Bank {r['star_B'][0]:+.3f} (SE {r['star_B'][1]:.3f}, t {r['star_B'][0]/r['star_B'][1]:.2f})**, 95 % [{r['star_B'][0]-1.96*r['star_B'][1]:+.3f}; {r['star_B'][0]+1.96*r['star_B'][1]:+.3f}]; c1 Signal {r['sig'][0]:+.3f} (t {r['sig'][0]/r['sig'][1]:.1f}); c2 Signal x Bank {r['sig_B'][0]:+.3f} (t {r['sig_B'][0]/r['sig_B'][1]:.2f}).")


# ---------- Panel 1 ----------
st = pd.read_pickle("/home/claude/eu2006/lang/raw16.pkl")["st"]
nm = st.dropna(subset=["FundId"]).groupby("FundId").Name.first()
fb = pd.read_pickle("/home/claude/bank/fb.pkl").join(nm)
g, us = klassa(fb, 2006)
p = pd.read_pickle("/home/claude/lseg/an/p_D.pkl").reset_index(drop=True)
p["star"] = p.star_d.astype(float)
p["grp"] = p.FundId.map(g).fillna("oklassad")
p["us"] = p.FundId.map(us).fillna(False).astype(bool)
p1 = p[(p.ym >= "2003-01") & (p.ym <= "2010-12")]
say("# RESULTAT: bankagda mot fristaende fondbolag (korning 20 november 2026)")
panel(p1, "Panel 1: Europa 2003-01 till 2010-12, agande oktober 2006", extra=p)

# ---------- Panel 2 ----------
fb2 = pd.read_pickle("/home/claude/bank/fb_1825.pkl")
g2, us2 = klassa(fb2, 2022)
q = pd.read_pickle("/home/claude/slut/full2/bd_eu_EU_full2.pkl").reset_index(drop=True)
q["star"] = q.star_d.astype(float)
q["grp"] = q.FundId.map(g2).fillna("oklassad")
q["us"] = q.FundId.map(us2).fillna(False).astype(bool)
panel(q, "Panel 2: Europa 2018-01 till 2025-12, agande december 2022")
open("/home/claude/bank/res_bank.md", "w").write("\n".join(out))
