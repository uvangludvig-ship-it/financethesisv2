"""Riskklassen som tredje signal, Fama-MacBeth (ankarets tabell 6 kol. 4 och tabell B.I): tvarsnitt per manad, Newey-West 6 laggar.
Specifikation: claude/DEKLARATION_riskklass_tredje_signal_fama_macbeth_2026-11-20.md
python3 -I bd_eu_fm.py <bd_eu_EU.pkl>"""
import sys, numpy as np, pandas as pd
d = pd.read_pickle(sys.argv[1]); d = d[d.in_kod].copy()
d["star"] = d.star_c.astype(float); d["lsize"] = np.log(d["size"]); d["lage"] = np.log(d["age"].clip(lower=0.1))
X = ["star", "lab", "unad_a", "flow_l19", "lsize", "lage", "exp", "sd60"]
h = d.dropna(subset=["flow", "cat"] + X).reset_index(drop=True)
print(f"Urval: {len(h)} fondmanader, {h.FundId.nunique()} fonder, {h.ym.min()} till {h.ym.max()}")

def nw(x, lags=6):
    x = np.asarray(x, float); T = len(x); m = x.mean(); e = x - m; S = e @ e / T
    for L in range(1, lags + 1): S += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / T
    return m, np.sqrt(S / T)
def fm(g, within_cat=False, nmin=100):
    rows = []
    for ym, c in g.groupby("ym"):
        if len(c) < nmin: continue
        Z = c[["flow"] + X].astype(float)
        if within_cat: Z = Z - Z.groupby(c.cat.values).transform("mean")
        A = np.column_stack([np.ones(len(Z)), Z[X].values]); b = np.linalg.lstsq(A, Z.flow.values, rcond=None)[0]; rows.append(b[1:])
    return np.array(rows)
def pooled(g, fe):
    Z = g[["flow"] + X].astype(float); Z = Z - Z.groupby(g[fe].values).transform("mean")
    A = Z[X].values; y = Z.flow.values; Ai = np.linalg.inv(A.T @ A); b = Ai @ A.T @ y; e = y - A @ b
    def meat(cl):
        u = pd.DataFrame(A * e[:, None]).groupby(np.asarray(cl)).sum().values; G = len(u); return G / (G - 1) * u.T @ u
    V = Ai @ (meat(g.FundId.values) + meat(g.ym.values) - meat((g.FundId.astype(str) + "|" + g.ym).values)) @ Ai
    return b, np.sqrt(np.diag(V))
def rad(nm, m, s, T=None):
    print(f"  {nm:<44}{12*m:+6.2f} pp/ar  SE {12*s:4.2f}  t {m/s:+5.2f}  95 % [{12*(m-1.96*s):+6.2f}; {12*(m+1.96*s):+6.2f}]" + (f"  manader {T}" if T else ""))

print("\nF1 HUVUD, Fama-MacBeth, Newey-West 6")
B = fm(h); T = len(B)
for j, nm in [(1, "riskklass, per steg"), (0, "stjarna, per stjarna")]:
    m, s = nw(B[:, j]); rad(nm, m, s, T)
m, s = nw(B[:, 2]); print(f"  avkastning: {m:+.3f} (t {m/s:.2f}) | sd60: {nw(B[:,7])[0]:+.3f} (t {nw(B[:,7])[0]/nw(B[:,7])[1]:.2f})")
print(f"  andel manader med positiv riskklasskoefficient: {100*(B[:,1]>0).mean():.0f} %")
print("  jfr poolad, manadseffekter, kluster fond och manad, samma urval")
b, se = pooled(h, "ym"); rad("riskklass, per steg", b[1], se[1]); rad("stjarna, per stjarna", b[0], se[0])

print("\nF2 inom kategori")
B2 = fm(h, within_cat=True)
for j, nm in [(1, "riskklass, per steg"), (0, "stjarna, per stjarna")]:
    m, s = nw(B2[:, j]); rad(nm, m, s, len(B2))
h["mc"] = h.ym + "_" + h.cat.astype(str); b, se = pooled(h, "mc"); rad("jfr poolad manad x kategori: riskklass", b[1], se[1])

print("\nF3 delperioder")
for nm, g in [("2018-2022 (SRRI)", h[h.ym <= "2022-12"]), ("2023-2025 (SRI)", h[h.ym >= "2023-01"])]:
    Bs = fm(g); m, s = nw(Bs[:, 1]); rad(nm + ": riskklass", m, s, len(Bs)); m, s = nw(Bs[:, 0]); rad(nm + ": stjarna", m, s)

hv = h.copy(); hv["flow"] = hv.flow + 0.10 * hv.lab; Bv = fm(hv)
print(f"\nF4 inplanterad +0,100 per steg och manad ger {Bv[:,1].mean()-B[:,1].mean():+.4f}")
