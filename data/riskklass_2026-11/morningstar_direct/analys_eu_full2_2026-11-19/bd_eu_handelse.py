"""Ben-Davids handelsetest (Table 4, Figure 5B) pa bytet av risksiffra januari 2023.
Specifikation: claude/DEKLARATION_bendavids_handelsetest_januari_2023_2026-11-19.md
python3 -I bd_eu_handelse.py <panel.pkl>   (kraver <panel>_etikett.pkl fran bd_eu_bygg.py)"""
import sys, numpy as np, pandas as pd
P = sys.argv[1]
d = pd.read_pickle(P); d = d[d.in_kod].copy().reset_index(drop=True); d["star"] = d.star_c.astype(int)
LA = pd.read_pickle(P.replace(".pkl", "_etikett.pkl"))[["FundId", "ym", "lab"]]
rng = np.random.default_rng(20261119)
print(f"# Handelsetest januari 2023, {P}: {len(d)} fondmanader, {d.FundId.nunique()} fonder")

def fe_demean(X, groups, maxit=500, tol=1e-10):
    X = X.astype(float).copy()
    for _ in range(maxit):
        prev = X.copy()
        for g in groups: X = X - X.groupby(g.values).transform("mean")
        if len(groups) == 1 or np.abs((X - prev).values).max() < tol: break
    return X
def r2(y, X, groups):
    sst = np.sum((y - y.mean()) ** 2); Z = fe_demean(pd.concat([y.rename("y"), X], axis=1), groups)
    e = Z["y"].values; A = Z.drop(columns="y").values; b, *_ = np.linalg.lstsq(A, e, rcond=None); e = e - A @ b
    return 1 - np.sum(e ** 2) / sst

# ---------- Test 1: andel med andrad siffra (Table 4A) ----------
q = d.dropna(subset=["lab"]).sort_values(["FundId", "ym"]).copy(); q["prev"] = q.groupby("FundId").lab.shift(1); q = q.dropna(subset=["prev"])
q["ch"] = (q.lab != q.prev).astype(float); grp = np.where(q.ym < "2023-01", "fore", np.where(q.ym == "2023-01", "jan", "efter")); ms = q.assign(g=grp).groupby(["g", "ym"]).ch.mean()
print("\n## Test 1 (Table 4A): andel fonder med andrad visad siffra per manad")
print(f"  fore jan 2023: {100*q[grp=='fore'].ch.mean():.1f} % (std over manader {100*ms['fore'].std():.1f}) | januari 2023: {100*q[grp=='jan'].ch.mean():.1f} % (n {int((grp=='jan').sum())}) | efter: {100*q[grp=='efter'].ch.mean():.1f} % ({100*ms['efter'].std():.1f})")
print("  ankaret (betyg, juni 2002): 13,9 % (3,5) / 54,2 % / 11,9 % (2,8)")
qs = d.sort_values(["FundId", "ym"]).copy(); qs["ps"] = qs.groupby("FundId").star.shift(1); qs = qs.dropna(subset=["ps"])
print(f"  som jamforelse, andrat stjarnbetyg per manad i samma urval: {100*(qs.star != qs.ps).mean():.1f} %")

# ---------- Test 2: marginellt R2 (Table 4B) ----------
h = d.dropna(subset=["lab"]).copy(); h["lab"] = h.lab.astype(int)
h["m_star"] = h.ym + "_" + h.star.astype(str); h["m_lab"] = h.ym + "_" + h.lab.astype(str); h["m_cat"] = h.ym + "_" + h.cat
print("\n## Test 2 (Table 4B): marginellt R2 utover manadseffekter och ra overavkastning\n| | Fore (2018-2022) | Efter (2023-2025) |\n|---|---|---|")
res = {}
for nm, g in [("fore", h[h.ym <= "2022-12"]), ("efter", h[h.ym >= "2023-01"])]:
    g = g.reset_index(drop=True); y = g.flow; X = g[["unad_a"]]
    b0 = r2(y, X, [g.ym]); rs = r2(y, X, [g.m_star]); rl = r2(y, X, [g.m_lab]); rc = r2(y, X, [g.m_cat]); rsl = r2(y, X, [g.m_star, g.m_lab])
    res[nm] = (rs - b0, rl - b0, rc - b0, rsl - rs, len(g))
for i, lab in enumerate(["Manad x betyg", "Manad x risksiffra", "Manad x kategori", "Risksiffra utover betyg"]):
    print(f"| {lab} | {res['fore'][i]:.4f} | {res['efter'][i]:.4f} |")
print(f"Fondmanader fore {res['fore'][4]}, efter {res['efter'][4]}. Ankaret (USA): manad x betyg 0,073 / 0,074; manad x kategori 0,043 / 0,015.")

# ---------- Test 3: Figure 5B, ekvation (2) ----------
def hog(lab, ym): return np.where(pd.isna(lab), np.nan, (lab >= np.where(ym <= "2022-12", 6, 5)).astype(float))
d["yr"] = d.ym.str[:4].astype(int); d["mo"] = d.ym.str[5:].astype(int); d["h_vis"] = hog(d.lab, d.ym)
LA["h"] = hog(LA.lab, LA.ym); LA["yr"] = LA.ym.str[:4].astype(int); LA["mo"] = LA.ym.str[5:].astype(int)
jan = LA[LA.mo == 1].assign(yr=lambda x: x.yr - 1)[["FundId", "yr", "h"]].rename(columns={"h": "h_foc"})   # fokal for okt-dec ar y = januari y+1
dec = LA[LA.mo == 12].assign(yr=lambda x: x.yr + 1)[["FundId", "yr", "h"]].rename(columns={"h": "h_foc"})  # fokal for jan-mar ar Y = december Y-1
def spread(g, col, fc): return g.loc[g[col] == 1, fc].mean() - g.loc[g[col] == 0, fc].mean()
def fig5b(dd, months, foc, event, fc, title):
    e = dd[dd.mo.isin(months)].merge(foc, on=["FundId", "yr"], how="inner").dropna(subset=["h_vis", "h_foc"])
    pm = e.groupby("ym").apply(lambda g: pd.Series({"S_vis": spread(g, "h_vis", fc), "S_foc": spread(g, "h_foc", fc), "n": len(g)}), include_groups=False)
    pm["D"] = pm.S_vis - pm.S_foc; pm["yr"] = pm.index.str[:4].astype(int)
    yy = pm.groupby("yr").agg(S_vis=("S_vis", "sum"), S_foc=("S_foc", "sum"), D=("D", "sum"), n=("n", "mean"))
    print(f"\n### {title}\n| Ar | Fonder | Spread, visad siffra | Spread, andra sorteringen | Skillnad D |\n|---|---|---|---|---|")
    for y_, r_ in yy.iterrows():
        s = "**" if y_ == event else ""; print(f"| {s}{y_}{s} | {r_.n:.0f} | {r_.S_vis:+.2f} | {r_.S_foc:+.2f} | {s}{r_.D:+.2f}{s} |")
    plac = pm[pm.yr != event]; ys = sorted(plac.yr.unique())
    boot = [rng.choice(plac.D[plac.yr == rng.choice(ys)].values, 3, replace=True).sum() for _ in range(10000)]
    lo, hi = np.quantile(boot, [0.01, 0.99]); ev = yy.loc[event]
    ps = yy.drop(event)
    print(f"Handelsear {event}: D = {ev.D:+.2f}. Jamforelsear: D medel {ps.D.mean():+.2f}, min {ps.D.min():+.2f}, max {ps.D.max():+.2f}; bootstrap 1-99 % [{lo:+.2f}; {hi:+.2f}]; utanfor: {'ja' if (ev.D < lo or ev.D > hi) else 'nej'}.")
    print(f"Spread pa visad siffra: handelsear {ev.S_vis:+.2f}; jamforelsear medel {ps.S_vis.mean():+.2f}, min {ps.S_vis.min():+.2f}, max {ps.S_vis.max():+.2f}.")
    return e
d["flow_dm"] = d.flow - d.groupby(["ym", "cat"]).flow.transform("mean")
print("\n## Test 3 (Figure 5B, ekv. 2). Spread = medelflode hog risk minus lag risk, % per manad, summerat over tre manader")
e1 = fig5b(d, [10, 11, 12], jan, 2022, "flow", "Fore bytet (ankarets test): okt-dec ar y; andra sorteringen = siffran i januari y+1")
e2 = fig5b(d, [1, 2, 3], dec, 2023, "flow", "Efter bytet (spegling, tillagg): jan-mar ar Y; andra sorteringen = siffran i december Y-1")
print("\n## Variant V1: flodet rensat fran manad x kategori-medel")
fig5b(d, [10, 11, 12], jan, 2022, "flow_dm", "V1 fore bytet"); fig5b(d, [1, 2, 3], dec, 2023, "flow_dm", "V1 efter bytet")

# ---------- Utforskande, ej deklarerat: tre grupper runt bytet ----------
print("\n## UTFORSKANDE (ej deklarerat): medelflode % per manad for tre grupper, efter siffra dec 2022 (SRRI) och jan 2023 (SRI)")
a = LA[LA.ym == "2022-12"].set_index("FundId").lab; b = LA[LA.ym == "2023-01"].set_index("FundId").lab
G = pd.concat([a.rename("srri"), b.rename("sri")], axis=1).dropna()
G["grp"] = np.where((G.srri >= 6) & (G.sri >= 5), "3. hog -> hog (SRRI 6-7, SRI 5+)", np.where((G.srri >= 6) & (G.sri <= 4), "2. hog -> lag (SRRI 6-7, SRI 4-)", np.where((G.srri <= 5) & (G.sri <= 4), "1. lag -> lag (SRRI 5-, SRI 4-)", "ovrigt")))
x = d.merge(G[["grp"]], left_on="FundId", right_index=True)
for fc in ("flow", "flow_dm"):
    per = {"2021": x[x.yr == 2021], "2022 jan-sep": x[(x.yr == 2022) & (x.mo <= 9)], "2022 okt-dec": x[(x.yr == 2022) & (x.mo >= 10)], "2023 jan-mar": x[(x.yr == 2023) & (x.mo <= 3)], "2023 apr-dec": x[(x.yr == 2023) & (x.mo >= 4)], "2024": x[x.yr == 2024]}
    t = pd.DataFrame({k: v.groupby("grp")[fc].mean() for k, v in per.items()}); t["fonder"] = x.groupby("grp").FundId.nunique()
    print(f"\n{'Ratt flode' if fc == 'flow' else 'Rensat fran manad x kategori'}:"); print(t.round(2).to_string())
