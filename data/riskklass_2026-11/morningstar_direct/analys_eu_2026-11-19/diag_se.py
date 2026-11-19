"""Varfor SE inte foll: kollapsad dekomposition SE ~ sd(e) / (sqrt(N) * sd(dos_resid)). Anvander inget nytt utfall utover redan korda."""
import numpy as np, pandas as pd
P_ = lambda s: pd.Period(s, "M")
def decomp(C, nm):
    catc = pd.factorize(C.cat)[0]
    w = lambda v: v - (np.bincount(catc, v) / np.bincount(catc))[catc]
    s = C.sig.values / 10; Pm = np.column_stack([w(s), w(s**2), w(s**3)])
    def res(v):
        v = w(v); b = np.linalg.lstsq(Pm, v, rcond=None)[0]; return v - Pm @ b
    dr = res(C.dos.values.astype(float)); yr = res(C.dd.values)
    b = (dr @ yr) / (dr @ dr); e = yr - b * dr
    print(f"{nm:<28} N {len(C):5d} | sd flode-andring {C.dd.std():6.1f} | sd resid {e.std():6.1f} | sd dos (rå) {C.dos.std():.2f} | sd dos resid {dr.std():.2f} | SE approx {e.std()/np.sqrt(len(C))/dr.std():.2f}")
    return e
# EU
L = pd.read_pickle("panel_eu_a1.pkl"); B = pd.read_pickle("huvudklasser_eu_a1.pkl")
A = L[L.SecId.isin(B.index) & (L.t >= P_("2021-01")) & (L.t <= P_("2024-12"))].dropna(subset=["fw"])
A = A.assign(f=A.fw * 100, efter=(A.t >= P_("2023-01")))
g = A.groupby(["SecId", "efter"]).f.mean().unstack(); dd = (g[True] - g[False]) * 12
C = pd.DataFrame({"dd": dd}).join(B[["dos", "sig", "Morningstar Category"]].rename(columns={"Morningstar Category": "cat"})).dropna()
eEU = decomp(C, "EU A1 (Direct-floden)")
# andel manader med exakt noll flode, och storsta klasser
print("  EU: andel klassmanader med |flode| < 0,01 %:", round((A.f.abs() < 0.01).mean(), 3), "| sd manadsflode", round(A.f.std(), 2))
# Sverige
M = "/mnt/user-data/uploads/financethesisv2/data/riskklass_2026-11/morningstar_direct"
E = pd.read_pickle(f"{M}/byte2023/etiketter.pkl"); K = pd.read_pickle(f"{M}/tvillingar/tv_klasser.pkl"); K["y"] = K.t.dt.year
E["sri_ny"] = E.sri23.fillna(E.sri_h2_22); E["dos_bred"] = E.srri22 - E.sri_ny
pm = K[(K.roll == "huvudklass") & (K.institutionalonly != 1)]
n = pm.groupby(["SecId", "y"]).size().unstack(fill_value=0)
keep = set(n.index[((n[2021] + n[2022]) >= 18) & ((n[2023] + n[2024]) >= 18)])
Es = E[E.SecId.isin(keep) & E.srri22.notna() & E.sri_ny.notna() & E.dos_bred.isin([0, 1, 2]) & E.sig_w.notna()]
has_cat = set(pm[pm.SecId.isin(Es.SecId) & (pm.t <= P_("2022-12"))].dropna(subset=["cat_lag"]).SecId)
Es = Es[Es.SecId.isin(has_cat)].set_index("SecId"); print("Sverige urval", len(Es))
S = pm[pm.SecId.isin(Es.index) & (pm.t >= P_("2021-01")) & (pm.t <= P_("2024-12"))].dropna(subset=["cat_lag", "f"])
S = S.assign(efter=(S.t >= P_("2023-01")))
g = S.groupby(["SecId", "efter"]).f.mean().unstack(); dd = (g[True] - g[False]) * 12
cat22 = S[S.t <= P_("2022-12")].sort_values("t").groupby("SecId").cat_lag.last()
C2 = pd.DataFrame({"dd": dd, "cat": cat22}).join(Es[["dos_bred", "sig_w"]].rename(columns={"dos_bred": "dos", "sig_w": "sig"})).dropna()
decomp(C2, "Sverige (SHoF-floden)")
print("  SE: andel klassmanader med |flode| < 0,01 %:", round((S.f.abs() < 0.01).mean(), 3), "| sd manadsflode", round(S.f.std(), 2))
# svansar: hur mycket av residualvariansen kommer fran de 5 % storsta |resid| i EU
q = np.quantile(np.abs(eEU), .95); print("  EU: andel av residualvariansen fran de 5 % storsta:", round((eEU[np.abs(eEU) >= q]**2).sum() / (eEU**2).sum(), 2))
