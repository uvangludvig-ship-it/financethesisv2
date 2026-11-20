"""USA 1997-2011: ankarets avsnitt 3.1-3.3 pa Morningstar Direct-data.
python3 test/usa.py            (laser _arbete/usa_panel.pkl, skriver final_result/tal/usa_*.csv)"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import ARBETE, TAL
from lib import ankartest as at

HANDELSE = "2002-06"


def kor():
    allp = pd.read_pickle(ARBETE / "usa_panel.pkl")
    d = allp[allp["in_kod"]].copy().reset_index(drop=True)
    d["star"] = d["star_c"].astype(int)          # betyget vid slutet av manad t, som i forfattarnas kod
    d["year"] = d["ym"].str[:4]
    spara = lambda df, namn: df.to_csv(TAL / f"usa_{namn}.csv", index=False)

    top = at.toppfonder(d)
    spara(at.table3(d, top), "table3")
    pd.DataFrame([[len(d), d.FundId.nunique(), d.ym.min(), d.ym.max()]], columns=["fund_months", "funds", "first", "last"]).to_csv(TAL / "usa_urval.csv", index=False)
    spara(at.table1(d, [("size", "Fund size (USD million)"), ("age", "Age (years)"), ("flow", "Flow (%)"), ("flow_usd", "Flow (USD million)"), ("unad_a", "Raw excess return (%)"),
                        ("retexmkt_a", "Market-adjusted (%)"), ("capm_a", "CAPM alpha (%)"), ("ff3_a", "FF3 alpha (%)"), ("carh_a", "FFC alpha (%)")]), "table1")
    spara(at.table2(d), "table2")
    spara(at.fig3(d), "fig3")
    spara(at.fig4(d, top), "fig4")
    a, b = at.fig5a(d)
    spara(a, "fig5a_mean"); spara(b, "fig5a_coef")
    spara(at.fore_efter(d, HANDELSE), "fore_efter")     # samma regression, fore och efter juni 2002

    # Table 4 Panel A: betyget mot manaden fore, inom panelen
    q = d.sort_values(["FundId", "ym"]).copy()
    q["prev"] = q.groupby("FundId")["star"].shift(1)
    s, serie = at.andel_andrad(q, "star", HANDELSE)
    spara(s, "t4a"); spara(serie, "t4a_serie")
    # Table 4 Panel B
    spara(at.table4b(d, {"rating": "star", "category": "cat"}, HANDELSE), "t4b")
    # Figure 5 Panel B: mars-maj, fokalt betyg = fondens betyg i panelen i juni samma ar
    # (koden: "if yyyymm = &yr_exp*100 + 6; focal_rating = rating", ur base_panel)
    june = d[d["ym"].str.endswith("-06")][["FundId", "year", "star"]].rename(columns={"star": "focal"})
    e = d[d["ym"].str[5:].isin(["03", "04", "05"]) & (d["year"] >= "1998")].merge(june, on=["FundId", "year"], how="inner").dropna(subset=["focal"])
    rng = np.random.default_rng(20261118)
    for nm, topp, botten in [("a_5_vs_1", [5], [1]), ("b_45_vs_12", [4, 5], [1, 2])]:
        ar, s = at.fig5b(e, topp, botten, "2002", rng)
        spara(ar, f"fig5b_ar_{nm}"); spara(s, f"fig5b_{nm}")


if __name__ == "__main__":
    kor()
    print("usa klar")
