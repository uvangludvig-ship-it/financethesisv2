"""Kanaltesten K2 (historisk avkastning) och K3 (kostnader) enligt
DEKLARATION_uk_mot_eu_kanaltest_avkastning_kostnad_2026-11-19. python3 -I ukeu_kanal_run.py <tag>"""
import sys, numpy as np, pandas as pd
T = sys.argv[1]
src = open("ukeu_run.py").read().split("for lev in (2, 1, 3):")[0].replace("T = sys.argv[1]", f"T = {T!r}")
exec(src)  # dm, clus, est, line, rule, prepN, P_, STAR, A0
K = pd.read_pickle(f"ukeu_kanal_{T}.pkl"); C = pd.read_pickle(f"ukeu_kost_{T}.pkl"); L = pd.read_pickle(f"panel_eu_{T}.pkl")
K = K.merge(L[["SecId", "t", "star_lag"]], on=["SecId", "t"], how="left")
repsec = K.drop_duplicates("fundid").set_index("fundid")[["SecId", "cat"]]
to = C.to.where((C.to >= 0) & (C.to <= 1000))
eu = C[(C.sida == "EU") & ~C.inst & C.oc.notna() & (C.na_dec22 > 0)]
ER = eu.groupby("FundId").apply(lambda g: np.average(g.oc, weights=g.na_dec22))

def addK(W):
    W = W.merge(K[["fundid", "t", "P12", "P36", "star_lag"]], on=["fundid", "t"], how="left"); return W
def show(nm, W, X, keys=("fs", "fm"), k=0):
    b, se, V, G = est(W, "y", X, list(keys)); line(nm, b[k], se[k], G, len(W)); return b, se

for lev in (2, 1, 3):
    A = A0[A0.niva == lev]
    print(f"\n================ NIVA {lev}{' (HUVUDNIVA)' if lev == 2 else ''} ================")
    W = addK(prepN(A)).dropna(subset=["P12"])
    W["euP"] = W.eu * W.P12; W["eeP"] = W.ee * W.P12
    print("  K2 HISTORISK AVKASTNING (P = rang 0-1 av 12 man avkastning inom kategori; pp/ar fran samst till bast)")
    b, se = show("b2: Efter x EU x P (huvudtal)", W, ["eeP", "euP", "ee", "efpre"])
    print(f"    b1 (EU-sidans extra kanslighet fore): {b[1]:+.2f} (SE {se[1]:.2f})")
    # beskrivande: kanslighet per sida och period
    D = W.copy(); D["sm"] = D.sida + "|" + D.tt; cols = []
    for s_ in ("EU", "UK"):
        for p_, v in (("fore", 0.0), ("efter", 1.0)):
            c = f"P_{s_}_{p_}"; D[c] = D.P12 * (D.sida == s_) * (D.efter == v); cols.append(c)
    bd, sd, V, G = est(D, "y", cols, ["fs", "sm"])
    print("    Beskrivande kanslighet (fond x sida, sida x manad): " + " | ".join(f"{c[2:]} {bd[i]:+.2f} ({sd[i]:.2f})" for i, c in enumerate(cols)))
    show("K2a utan ANCOVA", W, ["eeP", "euP", "ee"])
    W36 = W.dropna(subset=["P36"]).copy(); W36["euP"] = W36.eu * W36.P36; W36["eeP"] = W36.ee * W36.P36
    show("K2b P over 36 manader", W36, ["eeP", "euP", "ee", "efpre"])
    W3 = addK(prepN(A, "2019-01", "2022-12", "2021-01", okcol="ok_pl")).dropna(subset=["P12"]); W3["euP"] = W3.eu * W3.P12; W3["eeP"] = W3.ee * W3.P12
    show("K2c latsasbyte jan 2021", W3, ["eeP", "euP", "ee", "efpre"])
    Ws = addK(prepN(A)).dropna(subset=["star_lag"]); Ws["euS"] = Ws.eu * Ws.star_lag; Ws["eeS"] = Ws.ee * Ws.star_lag
    show("K2d Efter x EU x stjarna (per stjarna)", Ws, ["eeS", "euS", "ee", "efpre"])
    We = W.copy(); yrs = [2021, 2023, 2024]; cy = []
    for y_ in yrs: We[f"euPy{y_}"] = We.euP * (We.t.dt.year == y_); cy.append(f"euPy{y_}")
    b, se, V, G = est(We, "y", cy + ["euP", "ee", "efpre"], ["fs", "fm"])
    print("    K2e EU x P per ar (bas 2022): " + " | ".join(f"{y_} {b[i]:+.2f} ({se[i]:.2f})" for i, y_ in enumerate(yrs)))

    print("  K3 KOSTNADER")
    f = W.drop_duplicates("fundid")[["fundid"]].copy()
    f["to"] = f.fundid.map(repsec.SecId).map(to); f["cat"] = f.fundid.map(repsec.cat); f["ER"] = f.fundid.map(ER)
    f["TO"] = f.groupby("cat").to.rank(pct=True)
    WK = prepN(A).merge(f[["fundid", "TO", "ER"]], on="fundid", how="left")
    WK2 = WK.dropna(subset=["TO", "ER"]).copy(); WK2["eeTO"] = WK2.ee * WK2.TO; WK2["eeER"] = WK2.ee * WK2.ER
    b, se = show("d: Efter x EU x omsattning (rang 0-1)", WK2, ["eeTO", "eeER", "ee", "efpre"])
    print(f"    e: Efter x EU x kostnadskvot (per procentenhet): {b[1]:+.2f} (SE {se[1]:.2f}, t {b[1]/se[1]:+.2f}) | fonder {WK2.fundid.nunique()}")
    a = WK.dropna(subset=["TO"]).copy(); a["eeTO"] = a.ee * a.TO; show("K3a bara omsattning", a, ["eeTO", "ee", "efpre"])
    a = WK.dropna(subset=["ER"]).copy(); a["eeER"] = a.ee * a.ER; show("K3a bara kostnadskvot", a, ["eeER", "ee", "efpre"])
    P3 = prepN(A, "2019-01", "2022-12", "2021-01", okcol="ok_pl").merge(f[["fundid", "TO", "ER"]], on="fundid").dropna(subset=["TO", "ER"])
    P3["eeTO"] = P3.ee * P3.TO; P3["eeER"] = P3.ee * P3.ER
    b, se = show("K3b latsas jan 2021: omsattning", P3, ["eeTO", "eeER", "ee", "efpre"]); print(f"    K3b latsas: kostnadskvot {b[1]:+.2f} (SE {se[1]:.2f})")
    b, se = show("K3c utan ANCOVA: omsattning", WK2, ["eeTO", "eeER", "ee"]); print(f"    K3c utan ANCOVA: kostnadskvot {b[1]:+.2f} (SE {se[1]:.2f})")
    # verifiering K2
    Wv = W.copy(); Wv["y"] = Wv.y + (-4.0 / 12) * Wv.eeP; b, se, V, G = est(Wv, "y", ["eeP", "euP", "ee", "efpre"], ["fs", "fm"])
    b0, _, _, _ = est(W, "y", ["eeP", "euP", "ee", "efpre"], ["fs", "fm"])
    print(f"  VERIFIERING K2: inplanterad -4,00 ger {b[0]:+.3f} (vantat {b0[0] - 4:+.3f})")
