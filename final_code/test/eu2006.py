"""Europa, oktober 2006: ankarets Table 4 och Figure 5 pa det europeiska betygsbytet.
Bara ankarets test, pa alla fonder. Inga egna test eller uppdelningar.
python3 test/eu2006.py         (laser _arbete/p_D.pkl, p_L.pkl, p_Direct.pkl)
p_D = Direct forst, LSEG fyller (huvud). p_L = LSEG forst. p_Direct = bara Direct."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import ARBETE, TAL
from lib import ankartest as at

EV = "2006-10"


def kor(panel, pfx):
    d = pd.read_pickle(ARBETE / f"{panel}.pkl").reset_index(drop=True)
    d["star"] = d["star_d"].astype(int)
    d["year"] = d["ym"].str[:4]
    spara = lambda df, namn: df.to_csv(TAL / f"{pfx}_{namn}.csv", index=False)
    spara(pd.DataFrame([[len(d), d.FundId.nunique(), d.ym.min(), d.ym.max(), int((d.ym <= EV).sum()), int((d.ym == EV).sum())]],
                       columns=["fund_months", "funds", "first", "last", "before", "funds_event_month"]), "urval")
    if pfx == "eu2006":
        spara(at.table1(d[d.ym <= "2010-12"], [("size", "Fund size (USD million)"), ("age", "Age (years)"), ("flow", "Flow (%)"), ("unad_a", "Raw excess return (%)"), ("star", "Star rating")]), "table1")

    # Table 4 Panel A: betyget mot fondens foregaende rad i panelen (koden: "lag1_rating = lag1(rating)")
    q = d.sort_values(["FundId", "ym"])[["FundId", "ym", "star"]].copy()
    q["prev"] = q.groupby("FundId")["star"].shift(1)
    s, serie = at.andel_andrad(q, "star", EV)
    spara(s, "t4a"); spara(serie, "t4a_serie")

    # Table 4 Panel B: manad x betyg (kategoriraderna hor till USA-reformens innehall och tas inte med)
    spara(at.table4b(d, {"rating": "star"}, EV), "t4b")

    # Figure 5 Panel A(b): flode pa betyg och ra signal, manadseffekt (panelen saknar ovriga kontroller)
    a, c = at.fig5a(d, kontroller=["unad_a"])
    spara(a, "fig5a_mean"); spara(c, "fig5a_coef")
    # samma regression, fore och efter oktober 2006 (hela perioden, och tva kortare)
    rows = []
    for nm, slut in [("to 2016", "2016-12"), ("to 2015", "2015-12"), ("to 2010", "2010-12")]:
        t = at.fore_efter(d[d.ym <= slut], EV, kontroller=["unad_a"]); t.insert(0, "period", nm); rows.append(t)
    spara(pd.concat(rows), "fore_efter")

    # Figure 5 Panel B: juli-september, fokalt betyg = fondens betyg i panelen i oktober samma ar
    foc = d[d["ym"].str.endswith("-10")][["FundId", "year", "star"]].rename(columns={"star": "focal"})
    e = d[d["ym"].str[5:].isin(["07", "08", "09"])].merge(foc, on=["FundId", "year"], how="inner").dropna(subset=["focal"])
    rng = np.random.default_rng(20261120)
    rows = []
    for nm, topp, botten in [("a_5_vs_1", [5], [1]), ("b_45_vs_12", [4, 5], [1, 2])]:
        ar, s = at.fig5b(e, topp, botten, "2006", rng)
        spara(ar, f"fig5b_ar_{nm}"); s.insert(0, "variant", nm); rows.append(s)
    spara(pd.concat(rows), "fig5b")


if __name__ == "__main__":
    kor("p_D", "eu2006")
    kor("p_L", "eu2006_lseg_forst")
    kor("p_Direct", "eu2006_bara_direct")
    print("eu2006 klar")
