"""Testen i Ben-David, Li, Rossi och Song (2022, RFS 35(4)), avsnitt 3.1 till 3.3.

Varje funktion tar en fondmanadspanel med kolumnerna
  FundId, ym ("AAAA-MM"), flow (% av formogenheten manaden fore), flow_usd (MUSD),
  star (betyg 1-5), unad_a, retexmkt_a, capm_a, ff3_a, carh_a (avkastningssignaler, %),
  size (formogenhet t-1, MUSD), age (ar), pos (1 om flodet ar positivt)
och ger tillbaka en tabell (DataFrame). Hanvisningar till ankarets kod avser
rubrikerna i forfattarnas kodfil (11.docx).
"""
import numpy as np
import pandas as pd
from .stat import ols, r2, nw_reg

SIGNALER = [("unad_a", "Raw"), ("capm_a", "CAPM"), ("ff3_a", "FF3"), ("carh_a", "FFC")]
KONTROLLER = ["unad_a", "flow_l19", "lsize", "lage", "exp", "sd60"]   # ankarets kod, "Regression for Panel A(b) of Figure 5"


def table1(d, cols):
    """Ankarets Table 1: antal, medel, tvarsnittsspridning (medel av manadsvis sd),
    tidsseriespridning (sd av manadsmedel) och percentiler."""
    rows = []
    for c, lab in cols:
        x = d[c].dropna()
        q = x.quantile([.05, .25, .5, .75, .95]).values
        rows.append([lab, len(x), x.mean(), d.groupby("ym")[c].std().mean(), d.groupby("ym")[c].mean().std(), *q])
    return pd.DataFrame(rows, columns=["variable", "N", "mean", "cs_sd", "ts_sd", "p5", "p25", "p50", "p75", "p95"])


def table2(d):
    """Ankarets Table 2, kolumn 1-5: likaviktat manadsflode pa likaviktade matt (z-varden),
    Newey-West 6 laggar. Kolumn 1: bara ra avkastning. Kolumn 2-5: ra avkastning och ett matt till
    (koden: "newey pflow_mmew100 retrf_mmew_z retexmkt_mmew_z, lag(6)" och sa vidare)."""
    agg = d.groupby("ym")[["flow", "unad_a", "retexmkt_a", "capm_a", "ff3_a", "carh_a"]].mean()
    z = (agg - agg.mean()) / agg.std()
    y = agg["flow"].values
    b, t, rr = nw_reg(y, z[["unad_a"]].values)
    rows = [["Raw", 1, b[0], t[0], np.nan, np.nan, rr, len(agg)]]
    for i, (c, lab) in enumerate([("retexmkt_a", "Market-adjusted"), ("capm_a", "CAPM"), ("ff3_a", "FF3"), ("carh_a", "FFC")]):
        b, t, rr = nw_reg(y, z[["unad_a", c]].values)
        rows.append([lab, i + 2, b[0], t[0], b[1], t[1], rr, len(agg)])
    return pd.DataFrame(rows, columns=["measure", "column", "coef_raw", "t_raw", "coef", "t", "r2", "months"])


def _diskret(d):
    """Avkastningen i fem grupper med samma antal fonder som betygen har den manaden
    (ankarets kod, "Make a discrete return variable from 1 to 5")."""
    def f(gr):
        n = gr["star"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).values
        return pd.Series(np.searchsorted(np.cumsum(n), gr["unad_a"].rank(method="first").values, side="left") + 1, index=gr.index)
    return d.groupby("ym", group_keys=False).apply(f)


def fig3(d):
    """Ankarets Figure 3: R2 for flode pa manadseffekter, avkastning och betygsdummies.
    Marginellt R2 for ett block = R2 med allt minus R2 utan blocket."""
    d = d.copy()
    for k in (2, 3, 4, 5):
        d[f"s{k}"] = (d["star"] == k).astype(float)
    grp = _diskret(d)
    for k in (2, 3, 4, 5):
        d[f"g{k}"] = (grp == k).astype(float)
    S, G = [f"s{k}" for k in (2, 3, 4, 5)], [f"g{k}" for k in (2, 3, 4, 5)]
    wv = (d["size"] / d.groupby("ym")["size"].transform("sum")).values
    rows = []
    for lab, w, X in [("EW continuous", None, ["unad_a"]), ("EW discrete", None, G), ("VW continuous", wv, ["unad_a"]), ("VW discrete", wv, G)]:
        tid = r2(d, "flow", [], ["ym"], w)
        avk = r2(d, "flow", X, ["ym"], w)
        bet = r2(d, "flow", S, ["ym"], w)
        allt = r2(d, "flow", X + S, ["ym"], w)
        rows.append([lab, allt, tid, allt - bet, allt - avk, allt - tid - (allt - bet) - (allt - avk)])
    return pd.DataFrame(rows, columns=["variant", "total", "time", "returns", "ratings", "joint"])


def toppfonder(d, signaler=SIGNALER):
    """Toppfonder per matt: lika manga som har fem stjarnor den manaden
    (ankarets kod, "Start by counting number of funds with 5 stars in each cross-section")."""
    top = {"Morningstar": (d["star"] == 5).astype(float)}
    n5 = top["Morningstar"].groupby(d["ym"]).transform("sum")
    for c, lab in signaler:
        top[lab] = ((d.groupby("ym")[c].rank(ascending=False, method="first") <= n5) & d[c].notna()).astype(float)
    return top


def fig4(d, top):
    """Ankarets Figure 4: medel over manaderna av toppgruppens medelflode."""
    rows = []
    for lab, m in list(top.items()) + [("All funds", pd.Series(1.0, index=d.index))]:
        x = d[m == 1].groupby("ym")[["flow", "flow_usd", "pos"]].mean().mean()
        rows.append([lab, x.flow, x.flow_usd, 100 * x.pos])
    return pd.DataFrame(rows, columns=["group", "flow_pct", "flow_musd", "share_positive"])


def table3(d, top, par=None):
    """Ankarets Table 3 i kodens form: utfall = a + b1 (TopA - TopB) + b2 (TopA eller TopB),
    utan manadseffekt, kluster fond och manad (koden: "reghdfe std_floww morn_gro5_m_unad_gro5
    morn5_e_unad5, noa vce(cluster yyyymm fundid2)"). b1 ar halva skillnaden i flode mellan
    fonder som bara A och bara B toppklassar."""
    namn = list(top)
    par = par or [(a, b) for i, a in enumerate(namn) for b in namn[i + 1:]]
    rows = []
    for A, B in par:
        x = d[["FundId", "ym", "flow", "flow_usd", "pos"]].copy()
        x["diff"] = top[A] - top[B]
        x["e"] = np.maximum(top[A], top[B])
        cell = [f"{A} vs {B}"]
        for c, k in [("flow", 1), ("flow_usd", 1), ("pos", 100)]:
            r = ols(x, c, ["diff", "e"], const=True)
            cell += [k * r.b["diff"], r.t["diff"]]
        rows.append(cell + [len(x)])
    return pd.DataFrame(rows, columns=["pair", "flow_pct", "t_pct", "flow_musd", "t_musd", "pos_pp", "t_pos", "N"])


def fig5a(d, kontroller=KONTROLLER):
    """Ankarets Figure 5A. (a) medelflode per betyg och kalenderar. (b) koefficienten for
    betyg (1-5) per ar: flode pa betyg, ra signal och kontroller, manadseffekt, kluster fond och manad."""
    d = d.copy()
    d["year"] = d["ym"].str[:4]
    if "size" in d:
        d["lsize"] = np.log(d["size"])
        d["lage"] = np.log(d["age"].clip(lower=0.1))
    a = d.groupby(["year", "star"])["flow"].mean().unstack().reset_index()
    rows = []
    for yr, g in d.groupby("year"):
        r = ols(g, "flow", ["star"] + list(kontroller), fe=["ym"])
        rows.append([yr, r.b["star"], r.se["star"], r.t["star"], r.n])
    return a, pd.DataFrame(rows, columns=["year", "coef", "se", "t", "N"])


def fore_efter(d, sista_fore, kontroller=KONTROLLER):
    """Regressionen bakom ankarets Figure 5A(b), skattad pa tva perioder i stallet for ar for ar:
    flode pa betyg, ra signal och kontroller, manadseffekt, kluster fond och manad.
    Skillnaden ar koefficienten pa betyg x Efter nar alla regressorer far var sin koefficient per period.
    Ankaret laser av figuren och raknar inte ut skillnaden."""
    d = d.copy()
    if "size" in d:
        d["lsize"] = np.log(d["size"]); d["lage"] = np.log(d["age"].clip(lower=0.1))
    X = ["star"] + list(kontroller)
    g = d.dropna(subset=["flow"] + X).copy()
    g["star"] = g["star"].astype(float)
    E = (g["ym"] > sista_fore).astype(float)
    f, e = ols(g[E == 0], "flow", X, fe=["ym"]), ols(g[E == 1], "flow", X, fe=["ym"])
    for x in X:
        g[x + "_E"] = g[x] * E
    r = ols(g, "flow", X + [x + "_E" for x in X], fe=["ym"])
    return pd.DataFrame([[f.b["star"], f.se["star"], e.b["star"], e.se["star"], r.b["star_E"], r.se["star_E"], r.t["star_E"], f.n, e.n, r.nf]],
                        columns=["before", "se_before", "after", "se_after", "difference", "se_difference", "t_difference", "N_before", "N_after", "funds"])


def andel_andrad(q, kol, handelse):
    """Ankarets Table 4 Panel A: andel fonder vars etikett skiljer sig fran manaden fore.
    q: rader (FundId, ym, etikett, prev). Ger sammanfattning och manadsserie."""
    q = q.dropna(subset=[kol, "prev"]).copy()
    q["ch"] = (q[kol] != q["prev"]).astype(float)
    m = q.groupby("ym")["ch"].mean()
    fore, efter = q[q.ym < handelse], q[q.ym > handelse]
    s = pd.DataFrame([[100 * fore.ch.mean(), 100 * m[m.index < handelse].std(), 100 * m.get(handelse, np.nan), int((q.ym == handelse).sum()),
                       100 * efter.ch.mean(), 100 * m[m.index > handelse].std(), 100 * m[m.index < handelse].mean(), 100 * m[m.index > handelse].mean()]],
                     columns=["before", "before_sd", "event", "event_n", "after", "after_sd", "before_mean_of_months", "after_mean_of_months"])
    return s, (100 * m).rename("share").reset_index()


def _utan_ensamma(g, fe):
    """Tar bort observationer som ar ensamma i sin grupp, upprepat tills inga finns kvar.
    Sa gor Statas reghdfe, som forfattarna anvander."""
    while True:
        ens = np.zeros(len(g), bool)
        for k in fe:
            ens |= (g.groupby(k)[k].transform("size") == 1).values
        if not ens.any():
            return g
        g = g[~ens]


def table4b(d, etiketter, sista_fore, kontroll="unad_a"):
    """Ankarets Table 4 Panel B: marginellt R2 for manad x etikett utover manadseffekter,
    med ra avkastning som kontroll (koden: "reghdfe std_floww retrf_a if af_j02 == 0, a(yyyymm)"
    mot "a(month_rating)"; R2 i den andra minus R2 i den forsta). etiketter: dict namn -> kolumn.
    Sista raden for tva etiketter: den andra utover den forsta."""
    d = d.copy()
    for nm, c in etiketter.items():
        d["m_" + nm] = d["ym"] + "_" + d[c].astype(str)
    R = lambda g, fe: r2(_utan_ensamma(g, fe), "flow", [kontroll], fe)
    rows = []
    for per, g in [("before", d[d.ym <= sista_fore]), ("after", d[d.ym > sista_fore])]:
        bas = R(g, ["ym"])
        r = {"period": per, "N": len(g), "base": bas}
        for nm in etiketter:
            r[nm] = R(g, ["m_" + nm]) - bas
            r["dropped_" + nm] = len(g) - len(_utan_ensamma(g, ["m_" + nm]))
        ks = list(etiketter)
        if len(ks) >= 2:
            r[f"{ks[1]}_beyond_{ks[0]}"] = R(g, ["m_" + ks[0], "m_" + ks[1]]) - R(g, ["m_" + ks[0]])
        rows.append(r)
    return pd.DataFrame(rows)


def _spread(g, col, topp, botten):
    return g.loc[g[col].isin(topp), "flow"].mean() - g.loc[g[col].isin(botten), "flow"].mean()


def fig5b(e, topp, botten, handelsear, rng, minst_fonder=None, n_boot=10000):
    """Ankarets ekvation 2 och Figure 5B. e: fondmanader i de tre manaderna fore handelsemanaden,
    varje ar, med kolumnerna star (visat betyg) och focal (betyget i handelsemanaden samma ar).
      D_m = [flode(topp) - flode(botten)] sorterat pa visat betyg
          - [flode(topp) - flode(botten)] sorterat pa focal;      D_ar = summan over de tre manaderna.
    Jamforelsear: alla andra ar med tre fullstandiga manader (och minst `minst_fonder` fonder per manad).
    Intervall: dra ett jamforelsear, dra tre av dess manader med aterlaggning, summera; 10 000 ganger;
    1:a och 99:e percentilen."""
    per = e.groupby("ym").apply(lambda g: _spread(g, "star", topp, botten) - _spread(g, "focal", topp, botten), include_groups=False)
    nmon = e.groupby("ym")["FundId"].nunique()
    rows, ok = [], []
    for y in sorted(set(per.index.str[:4])):
        ix = [m for m in per.index if m.startswith(y)]
        full = len(ix) == 3 and not per[ix].isna().any()
        D = per[ix].sum() if full else np.nan
        jfr = full and y != handelsear and (minst_fonder is None or nmon[ix].min() >= minst_fonder)
        if jfr:
            ok.append(y)
        rows.append([y, int(nmon[ix].min()), D, "event" if y == handelsear else ("yes" if jfr else "no")])
    ar = pd.DataFrame(rows, columns=["year", "min_funds", "D", "comparison"])
    plac = per[[m for m in per.index if m[:4] in ok]]
    boot = [rng.choice(plac[plac.index.str.startswith(rng.choice(ok))].values, 3, replace=True).sum() for _ in range(n_boot)]
    lo, hi = np.quantile(boot, [0.01, 0.99])
    v = float(ar.loc[ar.year == handelsear, "D"].iloc[0])
    alla = sorted(list(ar.loc[ar.comparison == "yes", "D"]) + [v], reverse=True)
    s = pd.DataFrame([[v, lo, hi, "above" if v > hi else ("below" if v < lo else "inside"), alla.index(v) + 1, len(alla),
                       ar.loc[ar.comparison == "yes", "D"].max()]], columns=["D_event", "lo", "hi", "position", "rank", "of", "max_comparison"])
    return ar, s
