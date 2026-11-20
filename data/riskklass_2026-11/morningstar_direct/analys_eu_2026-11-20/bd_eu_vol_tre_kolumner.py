"""Ben-David m.fl., arbetsversion 7 okt 2018, Table VII (flode pa volatilitet med och utan betyg),
overford till EU-panelen, med EU:s riskklass som tredje kolumn.
Specifikation: claude/DEKLARATION_volatilitet_stjarnor_riskklass_tre_kolumner_2026-11-20.md
Indata: panelen fran claude/bd_eu_bygg.py (samma som Ben-David pa EU och hastkapplopningen).
Anvandning: python3 -I bd_eu_vol_tre_kolumner.py <panel.pkl> <ut.md>
"""
import sys
import numpy as np
import pandas as pd
from scipy import stats

PANEL, UT = sys.argv[1], sys.argv[2]
allp = pd.read_pickle(PANEL)
d = allp[allp["in_kod"]].copy().reset_index(drop=True)
out = []
def say(s=""):
    print(s); out.append(s)

def fe_demean(X, groups, maxit=500, tol=1e-10):
    X = X.astype(float).copy()
    for _ in range(maxit):
        prev = X.copy()
        for g in groups:
            X = X - X.groupby(np.asarray(g)).transform("mean")
        if len(groups) == 1 or np.abs((X - prev).values).max() < tol:
            break
    return X

def ols(y, X, fe, fund, month):
    Z = pd.concat([y.rename("y"), X], axis=1)
    Z = fe_demean(Z, [fe])
    yt = Z["y"].values; A = Z.drop(columns="y").values
    Ai = np.linalg.inv(A.T @ A); b = Ai @ A.T @ yt; e = yt - A @ b
    def meat(cl):
        u = pd.DataFrame(A * e[:, None]).groupby(np.asarray(cl)).sum().values; G = len(u)
        return G / (G - 1) * u.T @ u
    inter = (pd.Series(fund).astype(str) + "|" + pd.Series(month).astype(str)).values
    V = Ai @ (meat(fund) + meat(month) - meat(inter)) @ Ai
    return pd.Series(b, index=X.columns), pd.DataFrame(V, index=X.columns, columns=X.columns)

def wald(b, V, cols):
    bb = b[cols].values; VV = V.loc[cols, cols].values
    w = float(bb @ np.linalg.pinv(VV) @ bb); return w, stats.chi2.sf(w, len(cols))

# ---- variabler ----
d["lsize"] = np.log(d["size"]); d["lage"] = np.log(d["age"].clip(lower=0.1))
d["star"] = d["star_c"].astype(float)
# Vol1: standardavvikelse av manadsavkastningen de 12 foregaende manaderna (minst 10), ur panelens ret
d = d.sort_values(["FundId", "ym"]).reset_index(drop=True)
P = d.pivot(index="ym", columns="FundId", values="ret").sort_index()
P = P.reindex(pd.period_range(d.ym.min(), d.ym.max(), freq="M").astype(str))
sd12 = P.shift(1).rolling(12, min_periods=10).std().stack().rename("sd12")
d = d.merge(sd12.reset_index().rename(columns={"level_0": "ym"}), on=["ym", "FundId"], how="left")
d["m_cat"] = d["ym"] + "_" + d["cat"].astype(str)
d["m_star"] = d["ym"] + "_" + d["star_c"].astype(str)

C = ["exp", "lsize", "lage", "flow_l19"]          # ankarets kontroller som finns i panelen
need = ["flow", "sd60", "star", "lab", "cat", "unad_a"] + C
h = d.dropna(subset=need).reset_index(drop=True)
h["lab"] = h["lab"].astype(int)
say(f"# Volatilitet, stjarnor och riskklass: tre kolumner pa samma fondmanader ({PANEL})")
say(f"Fondmanader {len(h)}, fonder {h.FundId.nunique()}, {h.ym.min()} till {h.ym.max()}. "
    f"Riskklass: {h.lab.value_counts().sort_index().to_dict()}")
say(f"sd60: medel {h.sd60.mean():.2f}, std {h.sd60.std():.2f} (procent per manad). Flode: procent per manad.")
say("Ankaret (arbetsversion 7 okt 2018, Table VII, USA, flode som andel, volatilitet som andel; samma enhet som har):"
    " Vol5 -0,055 (t -4,55) utan betyg; -0,0080 (t -0,63) med betyg; betyg +0,0064 per stjarna (= +0,64 procent).")

S = pd.get_dummies(h["star"].astype(int), prefix="s").astype(float).drop(columns="s_3")
L = pd.get_dummies(h["lab"], prefix="k").astype(float)
L = L.drop(columns="k_4") if "k_4" in L else L.iloc[:, 1:]
fund, month = h.FundId.values, h.ym.values

def kolumner(extra, fe_col, rubrik):
    say(f"\n## {rubrik}\n")
    say("| Kolumn | Vol5 (sd60) | t | Betyg per stjarna | t | Riskklass per steg | t | Riskklass-dummies, p | Fondmanader |")
    say("|---|---|---|---|---|---|---|---|---|")
    X1 = h[["sd60"] + extra + C]
    b, V = ols(h["flow"], X1, h[fe_col], fund, month); se = np.sqrt(np.diag(V)); se = pd.Series(se, index=X1.columns)
    say(f"| 1: Vol5 | {b.sd60:+.4f} | {b.sd60/se.sd60:.2f} | | | | | | {len(h)} |")
    X2 = h[["sd60", "star"] + extra + C]
    b, V = ols(h["flow"], X2, h[fe_col], fund, month); se = pd.Series(np.sqrt(np.diag(V)), index=X2.columns)
    say(f"| 2: Vol5 + betyg | {b.sd60:+.4f} | {b.sd60/se.sd60:.2f} | {b.star:+.3f} | {b.star/se.star:.2f} | | | | {len(h)} |")
    if fe_col == "ym":
        X2b = h[["sd60"] + extra + C]
        b, V = ols(h["flow"], X2b, h["m_star"], fund, month); se = pd.Series(np.sqrt(np.diag(V)), index=X2b.columns)
        say(f"| 2b: Vol5, manad x betyg | {b.sd60:+.4f} | {b.sd60/se.sd60:.2f} | (fasta effekter) | | | | | {len(h)} |")
    X3 = h[["sd60", "star", "lab"] + extra + C].astype(float)
    b, V = ols(h["flow"], X3, h[fe_col], fund, month); se = pd.Series(np.sqrt(np.diag(V)), index=X3.columns)
    lo, hi = b.lab - 1.96 * se.lab, b.lab + 1.96 * se.lab
    X3d = pd.concat([h[["sd60"]], S, L, h[extra + C]], axis=1)
    bd, Vd = ols(h["flow"], X3d, h[fe_col], fund, month); w, p = wald(bd, Vd, list(L.columns))
    say(f"| 3: Vol5 + betyg + riskklass | {b.sd60:+.4f} | {b.sd60/se.sd60:.2f} | {b.star:+.3f} | {b.star/se.star:.2f} | "
        f"{b.lab:+.3f} [{lo:+.3f}; {hi:+.3f}] | {b.lab/se.lab:.2f} | {p:.3f} | {len(h)} |")
    sed = pd.Series(np.sqrt(np.diag(Vd)), index=X3d.columns)
    say("\nKolumn 3 med en koefficient per betyg (bas 3) och per riskklass (bas 4):\n")
    say("| Variabel | Koef. | t |\n|---|---|---|")
    for c in ["sd60"] + list(S.columns) + list(L.columns):
        say(f"| {c} | {bd[c]:+.3f} | {bd[c]/sed[c]:.2f} |")
    sdv = h.sd60.std()
    say(f"\nStorlek i kolumn 3, pp per ar: en standardavvikelse i Vol5 ({sdv:.2f}) {12*b.sd60*sdv:+.2f}; "
        f"en stjarna {12*b.star:+.2f}; ett riskklassteg {12*b.lab:+.2f}.")

kolumner([], "ym", "Huvud: manadseffekter, ankarets kontroller, kluster fond och manad")
kolumner(["unad_a"], "ym", "Variant A: plus ra avkastning (18 manader, viktad)")
kolumner([], "m_cat", "Variant B: manad x kategori")

# Variant C: Vol5 och Vol1
hc = h.dropna(subset=["sd12"]).reset_index(drop=True)
say(f"\n## Variant C: Vol5 och Vol1 ({len(hc)} fondmanader)\n\n| Kolumn | Vol5 | t | Vol1 | t |\n|---|---|---|---|---|")
for nm, X in [("1", ["sd60", "sd12"]), ("2: + betyg", ["sd60", "sd12", "star"]), ("3: + betyg + riskklass", ["sd60", "sd12", "star", "lab"])]:
    XX = hc[X + C].astype(float); b, V = ols(hc["flow"], XX, hc["ym"], hc.FundId.values, hc.ym.values)
    se = pd.Series(np.sqrt(np.diag(V)), index=XX.columns)
    say(f"| {nm} | {b.sd60:+.4f} | {b.sd60/se.sd60:.2f} | {b.sd12:+.4f} | {b.sd12/se.sd12:.2f} |")

# Variant D: inom varje betygsgrupp (ankarets Table VIII)
say("\n## Variant D: Vol5 inom varje betygsgrupp (ankarets Table VIII), manadseffekter\n\n| Betyg | Vol5 | t | Riskklass per steg | t | Fondmanader |\n|---|---|---|---|---|---|")
for s_, g in h.groupby("star"):
    g = g.reset_index(drop=True)
    if len(g) < 500: continue
    XX = g[["sd60", "lab"] + C].astype(float); b, V = ols(g["flow"], XX, g["ym"], g.FundId.values, g.ym.values)
    se = pd.Series(np.sqrt(np.diag(V)), index=XX.columns)
    say(f"| {int(s_)} | {b.sd60:+.4f} | {b.sd60/se.sd60:.2f} | {b.lab:+.3f} | {b.lab/se.lab:.2f} | {len(g)} |")

# Verifiering: inplanterad effekt
hv = h.copy(); hv["flow"] = hv["flow"] - 0.05 * hv["sd60"]
X1 = h[["sd60"] + C]; b0, _ = ols(h["flow"], X1, h["ym"], fund, month); bv, _ = ols(hv["flow"], hv[["sd60"] + C], hv["ym"], fund, month)
say(f"\nVerifiering: inplanterad -0,050 per enhet Vol5 ger {bv.sd60 - b0.sd60:+.4f} (vantat -0,0500).")
open(UT, "w").write("\n".join(out))
