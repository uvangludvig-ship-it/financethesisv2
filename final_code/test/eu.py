"""Europa (2018-2025 i exporten; med fem ars historik fran juni 2019): ankarets test pa europeiska fonder, risksiffran som tredje signal och
ankarets Table 4 pa bytet januari 2023.
python3 test/eu.py             (laser _arbete/bd_eu_EU.pkl och bd_eu_kid.pkl)"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import ARBETE, TAL
from lib import ankartest as at
from lib.stat import ols, r2, fama_macbeth

X3 = ["star", "lab", "unad_a", "flow_l19", "lsize", "lage", "exp", "sd60"]   # betyg, risksiffra, avkastning och ankarets kontroller


def tredje_signal(d, pfx):
    """Risksiffran (lab) bredvid betyget och avkastningen."""
    h = d.dropna(subset=["lab"]).copy()
    h["lab"] = h["lab"].astype(float)
    h["star"] = h["star"].astype(float)
    # (i) marginell forklaringsgrad med tre block (dummies for betyg och risksiffra, bas betyg 1 och siffra 4)
    for k in (2, 3, 4, 5):
        h[f"s{k}"] = (h.star == k).astype(float)
    labs = [k for k in sorted(h.lab.unique()) if k != 4] if 4 in set(h.lab) else sorted(h.lab.unique())[1:]
    for k in labs:
        h[f"k{int(k)}"] = (h.lab == k).astype(float)
    S, L, A = [f"s{k}" for k in (2, 3, 4, 5)], [f"k{int(k)}" for k in labs], ["unad_a"]
    rows = []
    for nm, g in [("all", h)]:
        for wl in ("EW", "VW"):
            w = None if wl == "EW" else (g["size"] / g.groupby("ym")["size"].transform("sum")).values
            full = r2(g, "flow", A + S + L, ["ym"], w)
            rows.append([nm, wl, len(g), 100 * full, 100 * r2(g, "flow", [], ["ym"], w), 100 * (full - r2(g, "flow", S + L, ["ym"], w)),
                         100 * (full - r2(g, "flow", A + L, ["ym"], w)), 100 * (full - r2(g, "flow", A + S, ["ym"], w))])
    pd.DataFrame(rows, columns=["sample", "weights", "N", "total", "time", "returns", "ratings", "risk"]).to_csv(TAL / f"{pfx}_signal3_r2.csv", index=False)
    # (ii) linjar regression: poolad (kluster fond och manad) och Fama-MacBeth (Newey-West 6)
    g = h.dropna(subset=["flow", "cat"] + X3).reset_index(drop=True)
    rows = []

    def rad(namn, b_l, se_l, b_s, se_s, n, nf, T=""):
        rows.append([namn, 12 * b_l, 12 * se_l, b_l / se_l, 12 * (b_l - 1.96 * se_l), 12 * (b_l + 1.96 * se_l), 12 * b_s, 12 * se_s, b_s / se_s, b_l, b_l / se_l, b_s, n, nf, T])

    def fm(x, namn):
        o, B = fama_macbeth(x, "flow", X3)
        rad(namn, o["lab"][0], o["lab"][1], o["star"][0], o["star"][1], len(x), x.FundId.nunique(), len(B))
        return B

    def pool(x, namn, fe):
        r = ols(x, "flow", X3, fe=[fe])
        rad(namn, r.b["lab"], r.se["lab"], r.b["star"], r.se["star"], r.n, r.nf)

    B = fm(g, "Fama-MacBeth")
    pool(g, "Pooled, month effects", "ym")
    t = pd.DataFrame(rows, columns=["spec", "risk_pp_year", "risk_se", "risk_t", "risk_lo", "risk_hi", "star_pp_year", "star_se", "star_t",
                                    "risk_pct_month", "risk_t_month", "star_pct_month", "N", "funds", "months"])
    t["share_months_risk_positive"] = 100 * (B["lab"] > 0).mean()
    t.to_csv(TAL / f"{pfx}_signal3.csv", index=False)


def handelse2023(d, pfx):
    """Ankarets Table 4 pa januari 2023: etiketten ar risksiffran."""
    q = d.dropna(subset=["lab"]).sort_values(["FundId", "ym"]).copy()
    q["prev"] = q.groupby("FundId")["lab"].shift(1)
    s, serie = at.andel_andrad(q, "lab", "2023-01")
    s.to_csv(TAL / f"{pfx}_t4a_risk.csv", index=False); serie.to_csv(TAL / f"{pfx}_t4a_risk_serie.csv", index=False)
    h = d.dropna(subset=["lab"]).copy(); h["lab"] = h.lab.astype(int)
    at.table4b(h, {"rating": "star", "risk": "lab"}, "2022-12").to_csv(TAL / f"{pfx}_t4b_risk.csv", index=False)


def kor(panel, pfx):
    allp = pd.read_pickle(ARBETE / panel)
    d = allp[allp["in_kod"]].copy().reset_index(drop=True)
    d["star"] = d["star_c"].astype(int)          # betyget vid slutet av manad t, som i forfattarnas kod
    d["lsize"] = np.log(d["size"]); d["lage"] = np.log(d["age"].clip(lower=0.1))
    top = at.toppfonder(d)
    pd.DataFrame([[len(d), d.FundId.nunique(), d.ym.min(), d.ym.max(), int(d.lab.notna().sum())]], columns=["fund_months", "funds", "first", "last", "with_risk_number"]).to_csv(TAL / f"{pfx}_urval.csv", index=False)
    at.table1(d, [("size", "Fund size (USD million)"), ("age", "Age (years)"), ("flow", "Flow (%)"), ("flow_usd", "Flow (USD million)"), ("unad_a", "Raw excess return (%)"),
                  ("retexmkt_a", "Market-adjusted (%)"), ("capm_a", "CAPM alpha (%)"), ("ff3_a", "FF3 alpha (%)"), ("carh_a", "FFC alpha (%)"), ("star", "Star rating"), ("lab", "Risk number")]).to_csv(TAL / f"{pfx}_table1.csv", index=False)
    at.table2(d).to_csv(TAL / f"{pfx}_table2.csv", index=False)
    at.fig3(d).to_csv(TAL / f"{pfx}_fig3.csv", index=False)
    at.fig4(d, top).to_csv(TAL / f"{pfx}_fig4.csv", index=False)
    at.table3(d, top).to_csv(TAL / f"{pfx}_table3.csv", index=False)
    a, b = at.fig5a(d)
    a.to_csv(TAL / f"{pfx}_fig5a_mean.csv", index=False); b.to_csv(TAL / f"{pfx}_fig5a_coef.csv", index=False)
    # variant: Fama-Frenchs Europe-faktorer i stallet for Developed
    topE = at.toppfonder(d, [("capm_eur_a", "CAPM-Europe"), ("ff3_eur_a", "FF3-Europe"), ("carh_eur_a", "FFC-Europe")])
    at.table3(d, topE, [("Morningstar", "CAPM-Europe"), ("Morningstar", "FF3-Europe"), ("Morningstar", "FFC-Europe")]).to_csv(TAL / f"{pfx}_table3_europe_factors.csv", index=False)
    tredje_signal(d, pfx)
    handelse2023(d, pfx)


if __name__ == "__main__":
    kor("bd_eu_EU.pkl", "eu")
    kor("bd_eu_kid.pkl", "eukid")
    print("eu klar")
