"""SHoF + Direct: overlapp, flodeskorrelation och precision pa latsasbytet jan 2021. Inga floden efter dec 2022 anvands.
python3 -I pool_latsas.py <ss_eu-katalog> <morningstar_direct-katalog>"""
import sys, numpy as np, pandas as pd
D_, M = sys.argv[1:3]; P_ = lambda s: pd.Period(s, "M")
sys.path.insert(0, D_); from sicksack_funk import dm, clus, est, wins, evaluate
L = pd.read_pickle(f"{D_}/panel_eu_a1.pkl"); E = pd.read_pickle(f"{D_}/urval_eu_a1.pkl"); B = pd.read_pickle(f"{D_}/huvudklasser_eu_a1.pkl")
L = L[(L.t >= P_("2019-01")) & (L.t <= P_("2022-12"))]
K = pd.read_pickle(f"{M}/tvillingar/tv_klasser.pkl"); ES = pd.read_pickle(f"{M}/byte2023/etiketter.pkl")
K = K[(K.t >= P_("2019-01")) & (K.t <= P_("2022-12"))]; assert K.t.max() <= P_("2022-12") and L.t.max() <= P_("2022-12")

# svenska urvalet, som i sicksack_run.py (urvalet bygger pa antal manader 2021-24, inte pa varden)
K0 = pd.read_pickle(f"{M}/tvillingar/tv_klasser.pkl"); K0["y"] = K0.t.dt.year
ES["sri_ny"] = ES.sri23.fillna(ES.sri_h2_22); ES["dos_bred"] = ES.srri22 - ES.sri_ny
pm = K0[(K0.roll == "huvudklass") & (K0.institutionalonly != 1)]
n = pm.groupby(["SecId", "y"]).size().unstack(fill_value=0)
keep = set(n.index[((n[2021] + n[2022]) >= 18) & ((n[2023] + n[2024]) >= 18)])
Es = ES[ES.SecId.isin(keep) & ES.srri22.notna() & ES.sri_ny.notna() & ES.dos_bred.isin([0, 1, 2]) & ES.sig_w.notna()]
has_cat = set(pm[pm.SecId.isin(Es.SecId) & (pm.t <= P_("2022-12"))].dropna(subset=["cat_lag"]).SecId)
Es = Es[Es.SecId.isin(has_cat)].set_index("SecId"); assert len(Es) == 1421
sw_f = set(Es.fundid); eu_f = set(B.FundId)
print(f"OVERLAPP: svenska urvalet {len(sw_f)} fonder, EU A1 {len(eu_f)} fonder, bada {len(sw_f & eu_f)}, union {len(sw_f | eu_f)}")
print(f"  svenska fonder utanfor EU A1: {len(sw_f - eu_f)} | EU-fonder utanfor svenska urvalet: {len(eu_f - sw_f)}")

# flodeskorrelation, samma klass, 2019-2022
k = K[K.SecId.isin(Es.index)][["SecId", "t", "f"]].rename(columns={"f": "f_shof"})
d = L[["SecId", "t", "f", "stor"]].assign(f_dir=lambda x: x.f * 100)
J = k.merge(d, on=["SecId", "t"]); J = J[J.stor]
lo, hi = J.f_shof.quantile([.01, .99]); J2 = J[J.f_shof.between(lo, hi) & J.f_dir.between(*J.f_dir.quantile([.01, .99]))]
print(f"\nFLODEN, samma klass, 2019-2022: {J.SecId.nunique()} klasser, {len(J)} manader | korrelation {J2.f_shof.corr(J2.f_dir):.3f} (utan 1 % svansar)")
print(f"  sd SHoF {J2.f_shof.std():.2f}, sd Direct {J2.f_dir.std():.2f} | median |skillnad| {(J2.f_shof - J2.f_dir).abs().median():.2f} pp per manad")
gj = J2.assign(y=J2.t.dt.year).groupby(["SecId", "y"])[["f_shof", "f_dir"]].mean()
print(f"  arsmedel per klass: korrelation {gj.f_shof.corr(gj.f_dir):.3f}")

# radbyggare
mb = B.reset_index().set_index("FundId")[["SecId", "dos", "sig", "Morningstar Category"]].rename(columns={"Morningstar Category": "cat"})
def direct_fund(funds, w=(.025, .975)):
    X = L[L.SecId.isin(E.index[~E.inst & (E.sida != "UK")]) & L.fundid.isin(funds) & L.stor].copy(); X["usd"] = X.f * X.na_lag
    G = X.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum")).reset_index(); G["f"] = wins(G.usd / G.na, G.t, *w) * 100
    G = G.join(mb, on="fundid").merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left"); G["kalla"] = 0.0; return G
def shof(w=(.025, .975)):
    S = K[K.SecId.isin(Es.index)][["SecId", "fundid", "t", "f", "star_lag", "cat_lag"]].rename(columns={"cat_lag": "cat"})
    S["f"] = wins(S.f, S.t, *w)
    S = S.join(Es[["dos_bred", "sig_w"]].rename(columns={"dos_bred": "dos", "sig_w": "sig"}), on="SecId"); S["kalla"] = 1.0; return S
def anc(A):
    pm_ = A[A.efter == 0].groupby("SecId").f.mean(); A["efpre"] = A.efter * A.SecId.map(pm_).fillna(0); return ["efpre"]
def anc_src(A):
    A["ek"] = A.efter * A.kalla; return anc(A) + ["ek"]

print("\nPRECISION, latsasbyte jan 2021 (kombinationen: fondniva for Direct, wins 2,5/97,5, ANCOVA)")
rows = []
def rep(nm, r): print(f"  {nm:<58} fonder {r[0]:5d} | SE {r[1]:5.2f} | stjarna {r[2]:+5.2f} | MDE i stjarnor {2.8*r[1]/r[2]:5.2f}")
rep("a. Sverige, SHoF, deklarerat (wins 1/99, ingen ANCOVA)", evaluate(shof((.0, 1.)), ""))
rep("b. Sverige, SHoF, kombinationen", evaluate(shof(), "", anc))
rep("c. EU utan svenska urvalet, Direct, kombinationen", evaluate(direct_fund(eu_f - sw_f), "", anc))
rep("d. EU A1 alla, Direct, kombinationen", evaluate(direct_fund(eu_f), "", anc))
P = pd.concat([shof(), direct_fund(eu_f - sw_f)], ignore_index=True)
rep("e. SHoF dar det finns, annars Direct (union)", evaluate(P, "", anc_src))
