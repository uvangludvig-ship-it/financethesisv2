"""Bygger tabeller (.tex) och figurer (.pdf) ur talen i final_result/tal/.
python3 tabeller_figurer.py
Inga tal skrivs for hand har, utom ankarets egna (ur den tryckta artikeln, sidnummer anges i final.tex)."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from config import TAL, UT

T, F = UT / "tabeller", UT / "figurer"
L = lambda namn: pd.read_csv(TAL / f"{namn}.csv")
f = lambda x, d=2: "" if pd.isna(x) else f"{x:.{d}f}".replace("-", "$-$")
ff = lambda x, d=2: "" if pd.isna(x) else f"{x:,.{d}f}".replace("-", "$-$")
tp = lambda t, d=2: "" if pd.isna(t) else f"({t:.{d}f})".replace("-", "$-$")
n0 = lambda x: "" if pd.isna(x) else f"{int(round(x)):,}"


def manadstext(ym):
    """'2019-06' -> 'June 2019'."""
    return pd.Period(ym, "M").strftime("%B %Y")


def skriv(namn, rader):
    (T / f"{namn}.tex").write_text("\n".join(rader) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ ankarets tal (Ben-David m.fl. 2022)
ANK_T1 = {"Fund size (USD million)": (1472, 3038, 411), "Age (years)": (16.9, 12.8, 12.8), "Flow (%)": (-0.54, 2.18, -0.61), "Flow (USD million)": (-2.6, 52.4, -1.2),
          "Raw excess return (%)": (0.34, 0.99, 0.71), "Market-adjusted (%)": (0.07, 0.99, 0.01), "CAPM alpha (%)": (0.09, 0.95, 0.03), "FF3 alpha (%)": (-0.03, 0.78, -0.07), "FFC alpha (%)": (-0.03, 0.76, -0.06)}
ANK_T3 = {"Morningstar vs Raw": (0.099, 2.50, 10.9, 7.1), "Morningstar vs CAPM": (0.108, 2.72, 11.0, 7.3), "Morningstar vs FF3": (0.192, 4.85, 12.3, 10.4), "Morningstar vs FFC": (0.188, 4.73, 12.5, 10.0),
          "Raw vs CAPM": (0.032, 0.62, 0.3, 0.8), "Raw vs FF3": (0.207, 4.74, 3.1, 7.3), "Raw vs FFC": (0.195, 4.48, 3.7, 6.5), "CAPM vs FF3": (0.220, 5.06, 3.4, 8.0),
          "CAPM vs FFC": (0.197, 4.55, 3.9, 6.8), "FF3 vs FFC": (-0.017, -0.26, 1.7, -1.4)}
ANK_T3_T = {"Morningstar vs Raw": (6.27, 4.45), "Morningstar vs CAPM": (6.26, 4.57), "Morningstar vs FF3": (7.19, 6.55), "Morningstar vs FFC": (7.09, 6.26), "Raw vs CAPM": (0.37, 0.41),
            "Raw vs FF3": (2.84, 4.41), "Raw vs FFC": (2.69, 3.97), "CAPM vs FF3": (2.99, 4.71), "CAPM vs FFC": (2.79, 4.07), "FF3 vs FFC": (0.85, -0.56)}   # t for USD och andel positiva
ANK_T2 = {"Raw": (0.179, 4.47, np.nan, np.nan), "Market-adjusted": (0.176, 4.05, 0.015, 0.26), "CAPM": (0.178, 4.35, 0.018, 0.38), "FF3": (0.186, 4.60, -0.048, -1.01), "FFC": (0.182, 4.44, -0.018, -0.36)}   # (ra, t, andra mattet, t), kolumn 1-5
ANK_F3 = {"EW continuous": (19.4, 3.6, 5.6, 6.5, 3.8), "EW discrete": (19.8, 3.6, 6.0, 6.5, 3.8), "VW continuous": (28.9, 5.9, 6.8, 9.6, 6.7), "VW discrete": (29.0, 5.9, 6.9, 9.8, 6.5)}
ANK_F4 = {"Morningstar": (1.16, 67.5), "Raw": (0.99, 61.7), "CAPM": (0.98, 61.5), "FF3": (0.84, 58.9), "FFC": (0.84, 59.0), "All funds": (-0.49, 35.2)}   # ur kodens utskrift "fig4_panela" och "average_all"

# ------------------------------------------------------------------ Tabell 1: beskrivande statistik
r = [r"\begin{tabular}{lrrrrrrrrrrr}", r"\toprule", r" & $N$ & Mean & CS SD & P5 & P25 & P50 & P75 & P95 & \multicolumn{3}{c}{Ben-David et al.} \\",
     r" & & & & & & & & & Mean & CS SD & P50 \\", r"\midrule"]
u = L("usa_urval").iloc[0]
r.append(rf"\multicolumn{{12}}{{l}}{{\textit{{Panel A. United States, July 1997 to December 2011 ({n0(u.fund_months)} fund-months, {n0(u.funds)} funds; Ben-David et al.: 248,463 and 3,341)}}}} \\")
for _, x in L("usa_table1").iterrows():
    a = ANK_T1[x.variable]
    r.append(f"{x.variable.replace('%', chr(92) + '%')} & {n0(x.N)} & {ff(x['mean'])} & {ff(x.cs_sd)} & {ff(x.p5)} & {ff(x.p25)} & {ff(x.p50)} & {ff(x.p75)} & {ff(x.p95)} & {ff(a[0])} & {ff(a[1])} & {ff(a[2])} \\\\")
u = L("eu_urval").iloc[0]
r += [r"\addlinespace", rf"\multicolumn{{12}}{{l}}{{\textit{{Panel B. Europe, {manadstext(u['first'])} to {manadstext(u['last'])} ({n0(u.fund_months)} fund-months, {n0(u.funds)} funds)}}}} \\"]
for _, x in L("eu_table1").iterrows():
    r.append(f"{x.variable.replace('%', chr(92) + '%')} & {n0(x.N)} & {ff(x['mean'])} & {ff(x.cs_sd)} & {ff(x.p5)} & {ff(x.p25)} & {ff(x.p50)} & {ff(x.p75)} & {ff(x.p95)} & & & \\\\")
t1c = L("eu2006_table1")
forsta06 = L("eu2006_urval")["first"].iloc[0]
r += [r"\addlinespace", rf"\multicolumn{{12}}{{l}}{{\textit{{Panel C. Europe, {manadstext(forsta06)} to December 2010 ({n0(t1c.N.max())} fund-months)}}}} \\"]
for _, x in t1c.iterrows():
    r.append(f"{x.variable.replace('%', chr(92) + '%')} & {n0(x.N)} & {ff(x['mean'])} & {ff(x.cs_sd)} & {ff(x.p5)} & {ff(x.p25)} & {ff(x.p50)} & {ff(x.p75)} & {ff(x.p95)} & & & \\\\")
u = L("byte2023_urval").iloc[0]
r += [r"\addlinespace", rf"\multicolumn{{12}}{{l}}{{\textit{{Panel D. The January 2023 switch, January 2021 to December 2024 ({n0(u.fund_months)} fund-months, {n0(u.funds)} funds; the number fell 0, 1, 2 classes for {n0(u.fall0)}, {n0(u.fall1)}, {n0(u.fall2)} funds)}}}} \\"]
for _, x in L("byte2023_table1").iterrows():
    r.append(f"{x.variable.replace('%', chr(92) + '%')} & {n0(x.N)} & {ff(x['mean'])} & {ff(x.sd)} & {ff(x.p5)} & {ff(x.p25)} & {ff(x.p50)} & {ff(x.p75)} & {ff(x.p95)} & & & \\\\")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("tabell1", r)

# ------------------------------------------------------------------ Tabell 2: stjarnan mot avkastningsmatten
us, eu = L("usa_table3").set_index("pair"), L("eu_table3").set_index("pair")
r = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{2}{c}{Ben-David et al.} & \multicolumn{2}{c}{United States, ours} & \multicolumn{2}{c}{Europe, ours} \\",
     r" & Coef. & $t$ & Coef. & $t$ & Coef. & $t$ \\", r"\midrule", r"\multicolumn{7}{l}{\textit{Panel A. Flow to top-ranked funds, pairwise (percent of assets per month)}} \\"]
for p in ["Morningstar vs Raw", "Morningstar vs CAPM", "Morningstar vs FF3", "Morningstar vs FFC", "Raw vs CAPM", "Raw vs FF3"]:
    a = ANK_T3[p]
    r.append(f"{p.replace('Morningstar', 'Star rating')} & {f(a[0], 3)} & {tp(a[1])} & {f(us.loc[p].flow_pct, 3)} & {tp(us.loc[p].t_pct)} & {f(eu.loc[p].flow_pct, 3)} & {tp(eu.loc[p].t_pct)} \\\\")
f3u, f3e = L("usa_fig3").set_index("variant").loc["EW continuous"], L("eu_fig3").set_index("variant").loc["EW continuous"]
r += [r"\addlinespace", r"\multicolumn{7}{l}{\textit{Panel B. Share of flow variation explained beyond the other block (percent, equal-weighted)}} \\",
      rf"Star rating & \multicolumn{{2}}{{c}}{{{f(ANK_F3['EW continuous'][3], 1)}}} & \multicolumn{{2}}{{c}}{{{f(100 * f3u.ratings, 1)}}} & \multicolumn{{2}}{{c}}{{{f(100 * f3e.ratings, 1)}}} \\",
      rf"Past return & \multicolumn{{2}}{{c}}{{{f(ANK_F3['EW continuous'][2], 1)}}} & \multicolumn{{2}}{{c}}{{{f(100 * f3u.returns, 1)}}} & \multicolumn{{2}}{{c}}{{{f(100 * f3e.returns, 1)}}} \\",
      rf"Fund-months & \multicolumn{{2}}{{c}}{{248,463}} & \multicolumn{{2}}{{c}}{{{n0(us.N.iloc[0])}}} & \multicolumn{{2}}{{c}}{{{n0(eu.N.iloc[0])}}} \\", r"\bottomrule", r"\end{tabular}"]
skriv("tabell2", r)

# ------------------------------------------------------------------ Tabell 3: metodbytena
a4, b4 = L("usa_t4a").iloc[0], L("usa_t4b").set_index("period")
e4, eb = L("eu2006_t4a").iloc[0], L("eu2006_t4b").set_index("period")
r = [r"\begin{tabular}{lccc}", r"\toprule", r" & Before & Event month & After \\", r"\midrule",
     r"\multicolumn{4}{l}{\textit{Panel A. United States, June 2002}} \\",
     rf"Funds with changed rating, percent per month: Ben-David et al. & 13.9 & 54.2 & 11.9 \\",
     rf"Funds with changed rating, percent per month: ours & {f(a4.before, 1)} & {f(a4.event, 1)} & {f(a4.after, 1)} \\",
     rf"Explained by month $\times$ rating: Ben-David et al. & 0.073 & & 0.074 \\", rf"Explained by month $\times$ rating: ours & {f(b4.loc['before'].rating, 3)} & & {f(b4.loc['after'].rating, 3)} \\",
     rf"Explained by month $\times$ category: Ben-David et al. & 0.043 & & 0.015 \\", rf"Explained by month $\times$ category: ours & {f(b4.loc['before'].category, 3)} & & {f(b4.loc['after'].category, 3)} \\",
     rf"Category beyond rating: Ben-David et al. & 0.022 & & 0.014 \\", rf"Category beyond rating: ours & {f(b4.loc['before'].category_beyond_rating, 3)} & & {f(b4.loc['after'].category_beyond_rating, 3)} \\",
     r"\addlinespace", r"\multicolumn{4}{l}{\textit{Panel B. Europe, October 2006}} \\",
     rf"Funds with changed rating, percent per month & {f(e4.before, 1)} & {f(e4.event, 1)} & {f(e4.after, 1)} \\",
     rf"Explained by month $\times$ rating & {f(eb.loc['before'].rating, 4)} & & {f(eb.loc['after'].rating, 4)} \\",
     rf"Fund-months & {n0(eb.loc['before'].N)} & {n0(e4.event_n)} funds & {n0(eb.loc['after'].N)} \\",
     r"\bottomrule", r"\end{tabular}"]
skriv("tabell3", r)

# ------------------------------------------------------------------ Tabell 4: risksiffran som tredje signal
s3, r3 = L("eu_signal3").set_index("spec"), L("eu_signal3_r2").set_index(["sample", "weights"])
r = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{3}{c}{Risk number} & \multicolumn{2}{c}{Star rating} & Fund-months \\", r" & Coef. & s.e. & 95\% interval & Coef. & $t$ & \\", r"\midrule",
     r"\multicolumn{7}{l}{\textit{Panel A. Percentage points of assets per year, per risk class or per star}} \\"]
for s in ["Fama-MacBeth", "Pooled, month effects"]:
    x = s3.loc[s]
    r.append(rf"{s.replace('2018-2022', '2018--2022').replace('2023-2025', '2023--2025')} & {f(x.risk_pp_year)} & {f(x.risk_se)} & [{f(x.risk_lo)}, {f(x.risk_hi)}] & {f(x.star_pp_year)} & {f(x.star_t, 1)} & {n0(x.N)} \\")
x = r3.loc[("all", "EW")]
r += [r"\addlinespace", r"\multicolumn{7}{l}{\textit{Panel B. Share of flow variation explained beyond the other two blocks (percent, equal-weighted)}} \\",
      rf"\multicolumn{{7}}{{l}}{{Past return {f(x.returns)} \quad Star rating {f(x.ratings)} \quad Risk number {f(x.risk)} \quad ({n0(x.N)} fund-months)}} \\", r"\bottomrule", r"\end{tabular}"]
skriv("tabell4", r)

# ------------------------------------------------------------------ Tabell 5: januari 2023 i ankarets Table 4-form
a, b = L("eu_t4a_risk").iloc[0], L("eu_t4b_risk").set_index("period")
r = [r"\begin{tabular}{lccc}", r"\toprule", r" & Before & January 2023 & After \\", r"\midrule",
     rf"Funds with changed risk number, percent per month & {f(a.before, 1)} & {f(a.event, 1)} & {f(a.after, 1)} \\",
     rf"Explained by month $\times$ risk number & {f(b.loc['before'].risk, 4)} & & {f(b.loc['after'].risk, 4)} \\",
     rf"Explained by month $\times$ star rating & {f(b.loc['before'].rating, 4)} & & {f(b.loc['after'].rating, 4)} \\",
     rf"Risk number beyond star rating & {f(b.loc['before'].risk_beyond_rating, 4)} & & {f(b.loc['after'].risk_beyond_rating, 4)} \\",
     rf"Fund-months & {n0(b.loc['before'].N)} & {n0(a.event_n)} funds & {n0(b.loc['after'].N)} \\", r"\bottomrule", r"\end{tabular}"]
skriv("tabell5", r)

# ------------------------------------------------------------------ Tabell 6: huvudtestet
D = L("byte2023_dos").set_index("spec")
K = [D.loc["(1) Fall x After, no volatility control"], D.loc["(2) Fall x After, volatility decile x month [main]"], D.loc["Fall x After with the star rating"]]
st = D.loc["Star rating, same regression as (2)"]
r = [r"\begin{tabular}{lccc}", r"\toprule", r" & (1) & (2) & (3) \\", r" & & Main & With star rating \\", r"\midrule",
     r"Fall $\times$ After & " + " & ".join(f(x.coef) for x in K) + r" \\", " & " + " & ".join(tp(x.se) for x in K) + r" \\",
     rf"Star rating & & & {f(st.coef)} \\", rf" & & & {tp(st.se)} \\", r"\addlinespace",
     r"95\% interval & " + " & ".join(f"[{f(x.lo)}, {f(x.hi)}]" for x in K) + r" \\",
     r"Minimum detectable effect & " + " & ".join(f(x.mde, 1) for x in K) + r" \\", r"\addlinespace",
     r"Fund effects & Yes & Yes & Yes \\", r"Category $\times$ month effects & Yes & Yes & Yes \\", r"Volatility decile $\times$ month effects & No & Yes & Yes \\",
     "Funds & " + " & ".join(n0(x.funds) for x in K) + r" \\", "Fund-months & " + " & ".join(n0(x.N) for x in K) + r" \\", r"\bottomrule", r"\end{tabular}"]
skriv("tabell6", r)

# ------------------------------------------------------------------ Bilagetabeller
r = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{2}{c}{Ben-David et al.} & \multicolumn{2}{c}{United States, ours} & \multicolumn{2}{c}{Europe, ours} \\", r" & Coef. & $t$ & Coef. & $t$ & Coef. & $t$ \\", r"\midrule"]
for titel, cu, tu, ia in [("Flow, percent of assets per month", "flow_pct", "t_pct", 0), ("Flow, USD million per month", "flow_musd", "t_musd", 2), ("Probability of a positive flow, percentage points", "pos_pp", "t_pos", 3)]:
    r.append(rf"\multicolumn{{7}}{{l}}{{\textit{{{titel}}}}} \\")
    for p in ANK_T3:
        a = ANK_T3[p]
        r.append(f"{p.replace('Morningstar', 'Star rating')} & {f(a[ia], 3 if ia == 0 else 1)} & {tp(a[1]) if ia == 0 else tp(ANK_T3_T[p][ia - 2])} & {f(us.loc[p][cu], 3 if ia == 0 else 1)} & {tp(us.loc[p][tu])} & {f(eu.loc[p][cu], 3 if ia == 0 else 1)} & {tp(eu.loc[p][tu])} \\\\")
    r.append(r"\addlinespace")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("bilaga_a1", r)

t2u, t2e = L("usa_table2").set_index("measure"), L("eu_table2").set_index("measure")
r = [r"\begin{tabular}{llcccccc}", r"\toprule", r" & & \multicolumn{2}{c}{Ben-David et al.} & \multicolumn{2}{c}{United States, ours} & \multicolumn{2}{c}{Europe, ours} \\", r"Column & Regressor & Coef. & $t$ & Coef. & $t$ & Coef. & $t$ \\", r"\midrule"]
for i, m in enumerate(ANK_T2):
    a_ = ANK_T2[m]
    r.append(f"({i + 1}) & Raw return & {f(a_[0], 3)} & {tp(a_[1])} & {f(t2u.loc[m].coef_raw, 3)} & {tp(t2u.loc[m].t_raw)} & {f(t2e.loc[m].coef_raw, 3)} & {tp(t2e.loc[m].t_raw)} \\\\")
    if i:
        r.append(f" & {m} & {f(a_[2], 3)} & {tp(a_[3])} & {f(t2u.loc[m].coef, 3)} & {tp(t2u.loc[m].t)} & {f(t2e.loc[m].coef, 3)} & {tp(t2e.loc[m].t)} \\\\")
r += [rf"Months & & \multicolumn{{2}}{{c}}{{175}} & \multicolumn{{2}}{{c}}{{{n0(t2u.months.iloc[0])}}} & \multicolumn{{2}}{{c}}{{{n0(t2e.months.iloc[0])}}} \\", r"\bottomrule", r"\end{tabular}"]
skriv("bilaga_a2", r)

f4u, f4e = L("usa_fig4").set_index("group"), L("eu_fig4").set_index("group")
r = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{2}{c}{Ben-David et al.} & \multicolumn{2}{c}{United States, ours} & \multicolumn{2}{c}{Europe, ours} \\", r"Top funds by & Flow (\%) & Positive (\%) & Flow (\%) & Positive (\%) & Flow (\%) & Positive (\%) \\", r"\midrule"]
for g in ["Morningstar", "Raw", "CAPM", "FF3", "FFC", "All funds"]:
    a = ANK_F4.get(g, (np.nan, np.nan))
    r.append(f"{g.replace('Morningstar', 'Star rating')} & {f(a[0])} & {f(a[1], 1)} & {f(f4u.loc[g].flow_pct)} & {f(f4u.loc[g].share_positive, 1)} & {f(f4e.loc[g].flow_pct)} & {f(f4e.loc[g].share_positive, 1)} \\\\")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("bilaga_a3", r)

ek, ee = L("eukid_table3").set_index("pair"), L("eu_table3_europe_factors").set_index("pair")
r = [r"\begin{tabular}{lcccc}", r"\toprule", r" & \multicolumn{2}{c}{Europe, all KID classes} & \multicolumn{2}{c}{Europe, European factors} \\", r" & Coef. & $t$ & Coef. & $t$ \\", r"\midrule"]
for p, pe in [("Morningstar vs Raw", None), ("Morningstar vs CAPM", "Morningstar vs CAPM-Europe"), ("Morningstar vs FF3", "Morningstar vs FF3-Europe"), ("Morningstar vs FFC", "Morningstar vs FFC-Europe")]:
    x = (f(ee.loc[pe].flow_pct, 3), tp(ee.loc[pe].t_pct)) if pe else ("", "")
    r.append(f"{p.replace('Morningstar', 'Star rating')} & {f(ek.loc[p].flow_pct, 3)} & {tp(ek.loc[p].t_pct)} & {x[0]} & {x[1]} \\\\")
r += [rf"Fund-months & \multicolumn{{2}}{{c}}{{{n0(ek.N.iloc[0])}}} & \multicolumn{{2}}{{c}}{{{n0(ee.N.iloc[0])}}} \\", r"\bottomrule", r"\end{tabular}"]
skriv("bilaga_a4", r)

r = [r"\begin{tabular}{lccccc}", r"\toprule", r" & Coef. & s.e. & 95\% interval & Funds & Fund-months \\", r"\midrule"]
for s_ in ["One class x After", "Two classes x After"]:
    x = D.loc[s_]
    r.append(rf"{s_.replace(' x ', ' $' + chr(92) + 'times$ ')} & {f(x.coef)} & {f(x.se)} & [{f(x.lo)}, {f(x.hi)}] & {n0(x.funds)} & {n0(x.N)} \\")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("bilaga_a5", r)

r = [r"\begin{tabular}{lccc}", r"\toprule", r" & Morningstar first, LSEG fills & LSEG first & Morningstar only \\", r"\midrule"]
P3 = ["eu2006", "eu2006_lseg_forst", "eu2006_bara_direct"]
U = [L(p + "_urval").iloc[0] for p in P3]
TA = [L(p + "_t4a").iloc[0] for p in P3]
TB = [L(p + "_t4b").set_index("period") for p in P3]
FB = [L(p + "_fig5b").set_index("variant") for p in P3]
r += ["Fund-months & " + " & ".join(n0(u.fund_months) for u in U) + r" \\", "Fund-months before the change & " + " & ".join(n0(u.before) for u in U) + r" \\", r"\addlinespace",
      "Funds with changed rating: before / October 2006 / after & " + " & ".join(f"{f(x.before, 1)} / {f(x.event, 1)} / {f(x.after, 1)}" for x in TA) + r" \\",
      r"Explained by month $\times$ rating: before / after & " + " & ".join(f"{f(x.loc['before'].rating, 4)} / {f(x.loc['after'].rating, 4)}" for x in TB) + r" \\", r"\addlinespace",
      r"\multicolumn{4}{l}{\textit{Displayed minus coming rating, 2006, with bootstrap interval and rank among years}} \\"]
for v, lab in [("a_5_vs_1", "5 against 1 star"), ("b_45_vs_12", "4--5 against 1--2 stars")]:
    r.append(lab + " & " + " & ".join(f"{f(x.loc[v].D_event)} [{f(x.loc[v].lo)}, {f(x.loc[v].hi)}], {int(x.loc[v]['rank'])}/{int(x.loc[v].of)}" for x in FB) + r" \\")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("bilaga_a6", r)

# Bilaga A4b: Table 3 i fyra former (test/tabell3_former.py)
fu, fe_ = L("usa_table3_former").set_index("pair"), L("eu_table3_former").set_index("pair")
r = [r"\begin{tabular}{lcccccccc}", r"\toprule", r" & \multicolumn{2}{c}{Code form (main)} & \multicolumn{2}{c}{Second regressor: both} & \multicolumn{2}{c}{Second regressor: sum} & \multicolumn{2}{c}{Text form} \\",
     r" & $b_1$ & $t$ & $b_1$ & $t$ & $b_1$ & $t$ & $c_A-c_B$ & $t$ \\", r"\midrule"]
for titel, x in [("United States", fu), ("Europe", fe_)]:
    r.append(rf"\multicolumn{{9}}{{l}}{{\textit{{{titel}}}}} \\")
    for p in x.index:
        y = x.loc[p]
        r.append(f"{p.replace('Morningstar', 'Star rating')} & {f(y.b_either, 3)} & {tp(y.t_either)} & {f(y.b_both, 3)} & {tp(y.t_both)} & {f(y.b_sum, 3)} & {tp(y.t_sum)} & {f(y.text_difference, 3)} & {tp(y.t_text)} \\\\")
    r.append(r"\addlinespace")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("bilaga_a4b", r)

# Figur 2 i tva perioder: flode per stjarna fore och efter reformen
uf, ef = L("usa_fore_efter").iloc[0], L("eu2006_fore_efter").set_index("period")
r = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & Before & After & Difference & $t$ & Fund-months before & Fund-months after \\", r"\midrule"]
for lab, x in [("United States, June 2002 (1997--2011)", uf), ("Europe, October 2006 (to 2016)", ef.loc["to 2016"]), ("Europe, October 2006 (to 2015)", ef.loc["to 2015"]), ("Europe, October 2006 (to 2010)", ef.loc["to 2010"])]:
    r.append(rf"{lab} & {f(x.before, 3)} ({f(x.se_before, 3)}) & {f(x.after, 3)} ({f(x.se_after, 3)}) & {f(x.difference, 3)} ({f(x.se_difference, 3)}) & {f(x.t_difference)} & {n0(x.N_before)} & {n0(x.N_after)} \\")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("figur2_tal", r)

# Talen bakom figur 3 (ekvation 2) och figur 4 (Dos x kvartal)
r = [r"\begin{tabular}{lccccc}", r"\toprule", r" & Event year & 1st percentile & 99th percentile & Position & Rank among years \\", r"\midrule"]
for lab, fil, v in [("United States 2002, 5 against 1 star", "usa_fig5b_a_5_vs_1", None), ("United States 2002, 4--5 against 1--2 stars", "usa_fig5b_b_45_vs_12", None),
                    ("Europe 2006, 5 against 1 star", "eu2006_fig5b", "a_5_vs_1"), ("Europe 2006, 4--5 against 1--2 stars", "eu2006_fig5b", "b_45_vs_12")]:
    x = L(fil); x = x.iloc[0] if v is None else x.set_index("variant").loc[v]
    r.append(rf"{lab} & {f(x.D_event)} & {f(x.lo)} & {f(x.hi)} & {x.position} & {int(x['rank'])} of {int(x.of)} \\")
r += [r"\bottomrule", r"\end{tabular}"]
skriv("figur3_tal", r)

q = L("byte2023_kvartal")
r = [r"\begin{tabular}{l" + "c" * 8 + "}", r"\toprule"]
for del_ in (q.iloc[:7], q.iloc[7:]):
    r.append("Quarter & " + " & ".join(k.replace("Q", " Q") for k in del_.quarter) + (" & " if len(del_) < 8 else "") + r" \\")
    r.append("Coef. & " + " & ".join(f(v) for v in del_.coef) + (" & " if len(del_) < 8 else "") + r" \\")
    r.append("s.e. & " + " & ".join(tp(v) for v in del_.se) + (" & " if len(del_) < 8 else "") + r" \\")
    r.append(r"\addlinespace")
r += [rf"\multicolumn{{9}}{{l}}{{Wald test that all coefficients are zero: before the switch $p$ = {f(q.p_pre.iloc[0])}; after $p$ = {f(q.p_post.iloc[0])}}} \\", r"\bottomrule", r"\end{tabular}"]
skriv("figur4_tal", r)

# ------------------------------------------------------------------ Figurer
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6, "font.family": "serif", "pdf.fonttype": 42})
SV, GR, BL = "#1a1a1a", "#8c8c8c", "#1f5fa8"


def manad(s):
    return pd.to_datetime(s + "-01")


# Figur 1: andel med andrad etikett per manad
fig, ax = plt.subplots(1, 3, figsize=(9.2, 2.7))
for a_, (namn, ev, titel) in zip(ax, [("usa_t4a_serie", "2002-06", "U.S. star ratings"), ("eu2006_t4a_serie", "2006-10", "European star ratings"), ("eu_t4a_risk_serie", "2023-01", "EU risk number")]):
    s = L(namn)
    a_.plot(manad(s.ym), s.share, color=SV, lw=0.8)
    e = s[s.ym == ev]
    a_.plot(manad(e.ym), e.share, "o", color=BL, ms=5)
    a_.annotate(f"{pd.to_datetime(ev + '-01'):%b %Y}: {e.share.iloc[0]:.1f}%", (manad(e.ym).iloc[0], e.share.iloc[0]), xytext=(6, -2), textcoords="offset points", color=BL, fontsize=8)
    a_.set_title(titel, fontsize=9); a_.set_ylim(0, 100); a_.set_ylabel("Funds with changed label (%)" if a_ is ax[0] else "")
    a_.xaxis.set_major_locator(mdates.YearLocator(3)); a_.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.tight_layout(); fig.savefig(F / "figur1.pdf"); plt.close(fig)

# Figur 2: flode per stjarna per ar
fig, ax = plt.subplots(1, 3, figsize=(9.2, 2.7), sharey=True)
for a_, (namn, titel) in zip(ax, [("usa_fig5a_coef", "United States, 1997-2011"), ("eu2006_fig5a_coef", "Europe, 2004-2016"), ("eu_fig5a_coef", "Europe, 2019-2025")]):
    s = L(namn)
    a_.axhspan(0.4, 0.6, color="#e6e6e6", lw=0)
    a_.errorbar(s.year, s.coef, yerr=1.96 * s.se, fmt="o", color=SV, ms=3.5, lw=0.8, capsize=2)
    a_.axhline(0, color=GR, lw=0.5); a_.set_title(titel, fontsize=9); a_.set_xticks(s.year[::2])
    a_.set_ylabel("Flow per star (% per month)" if a_ is ax[0] else "")
ax[0].text(ax[0].get_xlim()[0] + 0.3, 0.42, "Ben-David et al.: 0.4-0.6", fontsize=7, color="#555555")
fig.tight_layout(); fig.savefig(F / "figur2.pdf"); plt.close(fig)

# Figur 3: ekvation 2 per ar med bootstrapintervall
fig, ax = plt.subplots(1, 4, figsize=(9.6, 2.7))
for a_, (ar, sm, rad_, ev, titel) in zip(ax, [("usa_fig5b_ar_a_5_vs_1", "usa_fig5b_a_5_vs_1", None, "2002", "U.S. 2002: 5 vs 1 star"),
                                               ("usa_fig5b_ar_b_45_vs_12", "usa_fig5b_b_45_vs_12", None, "2002", "U.S. 2002: 4-5 vs 1-2 stars"),
                                               ("eu2006_fig5b_ar_a_5_vs_1", "eu2006_fig5b", "a_5_vs_1", "2006", "Europe 2006: 5 vs 1 star"),
                                               ("eu2006_fig5b_ar_b_45_vs_12", "eu2006_fig5b", "b_45_vs_12", "2006", "Europe 2006: 4-5 vs 1-2 stars")]):
    y = L(ar); y = y[y.comparison != "no"]
    s_ = L(sm); s_ = s_.iloc[0] if rad_ is None else s_.set_index("variant").loc[rad_]
    a_.bar(y.year.astype(str), y.D, color=[BL if str(v) == ev else GR for v in y.year], width=0.7)
    a_.axhline(s_.hi, color=SV, lw=0.7, ls="--"); a_.axhline(s_.lo, color=SV, lw=0.7, ls="--"); a_.axhline(0, color=SV, lw=0.5)
    a_.set_title(titel, fontsize=8.5); a_.tick_params(axis="x", rotation=90, labelsize=6.5)
    a_.set_ylabel("Displayed minus coming rating" if a_ is ax[0] else "")
fig.tight_layout(); fig.savefig(F / "figur3.pdf"); plt.close(fig)

# Figur 4: Dos x kvartal
q = L("byte2023_kvartal")
alla = sorted(list(q.quarter) + ["2022Q4"]); x = {k: i for i, k in enumerate(alla)}
fig, a_ = plt.subplots(figsize=(6.2, 2.9))
a_.errorbar([x[k] for k in q.quarter], q.coef, yerr=1.96 * q.se, fmt="o", color=SV, ms=3.5, lw=0.8, capsize=2)
a_.plot([x["2022Q4"]], [0], "o", mfc="white", color=SV, ms=4)
a_.axhline(0, color=GR, lw=0.5); a_.axvline(x["2022Q4"] + 0.5, color=BL, lw=0.8, ls="--")
a_.text(x["2022Q4"] + 0.6, a_.get_ylim()[1] * 0.9, "New risk number,\n1 January 2023", color=BL, fontsize=7.5, va="top")
a_.set_xticks(range(len(alla))); a_.set_xticklabels([k.replace("Q", " Q") for k in alla], rotation=60, fontsize=7); a_.set_ylabel("Fall x quarter (pp of assets per year)")
fig.tight_layout(); fig.savefig(F / "figur4.pdf"); plt.close(fig)

# Figur A1: medelflode per dosgrupp och manad
d = L("byte2023_flode_per_dos"); u = L("byte2023_urval").iloc[0]
fig, a_ = plt.subplots(figsize=(6.2, 2.9))
for kcol, ls, lab in [("0.0", ":", f"Number unchanged ({int(u.fall0):,} funds)"), ("1.0", "--", f"Fell one class ({int(u.fall1):,})"), ("2.0", "-", f"Fell two classes ({int(u.fall2):,})")]:
    a_.plot(manad(d.tt), d[kcol].rolling(3, min_periods=1).mean(), color=SV, lw=1.0, ls=ls, label=lab)
a_.axvline(pd.Timestamp("2023-01-01"), color=BL, lw=0.8, ls="--"); a_.axhline(0, color=GR, lw=0.5)
a_.set_ylabel("Flow (% of assets per month,\n3-month average)"); a_.legend(frameon=False, fontsize=7.5)
a_.xaxis.set_major_locator(mdates.MonthLocator([1, 7])); a_.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y")); a_.tick_params(axis="x", labelsize=7)
fig.tight_layout(); fig.savefig(F / "figur_a1.pdf"); plt.close(fig)
print("tabeller och figurer klara")
