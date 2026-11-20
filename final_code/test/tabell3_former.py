"""Ankarets Table 3 i fyra former, for att visa vad valet av form gor.
python3 test/tabell3_former.py     (laser _arbete/usa_panel.pkl och bd_eu_EU.pkl)

Forfattarnas kod kor
    reghdfe std_floww morn_gro5_m_unad_gro5 morn5_e_unad5, noa vce(cluster yyyymm fundid2)
Den forsta regressorn ar TopA - TopB (definierad i koden). Den andra, morn5_e_unad5, definieras
inte i den kod vi har. Huvudtalen tolkar den som "toppklassad av nagon av de tva" (max).
Har provas ocksa "av bada" (produkt) och "antal" (summa), samt den tryckta textens form
(s. 1744): flode pa de tva indikatorerna med manadseffekter, skillnaden mellan koefficienterna.

Textens form racknas sa har. Med c_A TopA + c_B TopB = ((c_A-c_B)/2)(TopA-TopB) + ((c_A+c_B)/2)(TopA+TopB)
ar koefficienten pa (TopA-TopB) lika med halva skillnaden och har samma t-varde som skillnaden.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import ARBETE, TAL
from lib import ankartest as at
from lib.stat import ols

PAR = [("Morningstar", "Raw"), ("Morningstar", "CAPM"), ("Morningstar", "FF3"), ("Morningstar", "FFC"), ("Raw", "CAPM"), ("Raw", "FF3")]


def former(d, top):
    rows = []
    for A, B in PAR:
        x = d[["FundId", "ym", "flow"]].copy()
        x["diff"] = top[A] - top[B]
        x["either"] = np.maximum(top[A], top[B])
        x["both"] = top[A] * top[B]
        x["sum"] = top[A] + top[B]
        rad = [f"{A} vs {B}", float((x["both"] == 1).sum() / (top[A] == 1).sum())]
        for andra in ("either", "both", "sum"):
            r = ols(x, "flow", ["diff", andra], const=True)
            rad += [r.b["diff"], r.t["diff"]]
        r = ols(x, "flow", ["diff", "sum"], fe=["ym"])          # textens form
        rad += [2 * r.b["diff"], r.t["diff"]]
        rows.append(rad)
    return pd.DataFrame(rows, columns=["pair", "overlap", "b_either", "t_either", "b_both", "t_both", "b_sum", "t_sum", "text_difference", "t_text"])


def las(panel):
    allp = pd.read_pickle(ARBETE / panel)
    d = allp[allp["in_kod"]].copy().reset_index(drop=True)
    d["star"] = d["star_c"].astype(int)
    return d


if __name__ == "__main__":
    for panel, pfx in [("usa_panel.pkl", "usa"), ("bd_eu_EU.pkl", "eu")]:
        d = las(panel)
        t = former(d, at.toppfonder(d))
        t.to_csv(TAL / f"{pfx}_table3_former.csv", index=False)
        print(pfx); print(t.round(3).to_string(index=False))
    print("tabell3_former klar")
