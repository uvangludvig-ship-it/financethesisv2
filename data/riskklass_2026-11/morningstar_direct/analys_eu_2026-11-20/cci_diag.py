"""Utforskande diagnos (inte deklarerad): varfor har Cornaggia-formen en fortrend?
python3 -I cci_diag.py ."""
import sys, numpy as np, pandas as pd
from scipy import stats
exec(open("cci_form.py").read().split("def prep(")[0].replace("M = sys.argv[1]", "M = '.'"))
B2 = B.copy()
print("SIGMA (arsvolatilitet, %) per gammal klass och dos, medel [antal]:")
t = B2.groupby(["srri22", "dos"]).sig.agg(["mean", "size"]).unstack()
print(t.round(1).to_string())
r = B2.groupby("srri22").apply(lambda g: np.corrcoef(g.dos, g.sig)[0, 1] if g.dos.nunique() > 1 and len(g) > 30 else np.nan)
print("korrelation dos-sigma inom gammal klass:", r.round(2).to_dict())
print("korrelation dos-sigma over alla fonder:", round(np.corrcoef(B2.dos, B2.sig)[0, 1], 2))

P_ = lambda s: pd.Period(s, "M")
W = A[(A.t >= P_("2021-01")) & (A.t <= P_("2024-12"))].copy(); W["tt"] = W.t.astype(str); W["tc"] = W.tt + "_" + W.cat.astype(str)
W["q"] = W.t.dt.year.astype(str) + "Q" + W.t.dt.quarter.astype(str); qs = [q for q in sorted(W.q.unique()) if q != "2022Q4"]
ks = sorted(W.srri22.dropna().unique())[1:]; s = W.sig / 10
new = {}
for q in qs:
    new["d_" + q] = (W.q == q) * W.dos
    for k in ks: new[f"k{int(k)}_" + q] = ((W.q == q) & (W.srri22 == k)).astype(float)
    for j in (1, 2, 3): new[f"p{j}_" + q] = (W.q == q) * s ** j
W = pd.concat([W, pd.DataFrame(new, index=W.index)], axis=1)
D = ["d_" + q for q in qs]; Kc = [f"k{int(k)}_" + q for q in qs for k in ks]; P1 = ["p1_" + q for q in qs]; P3 = [f"p{j}_" + q for q in qs for j in (1, 2, 3)]
pre = [i for i, q in enumerate(qs) if q < "2022Q4"]
def run(nm, X):
    b, se, V, Gn = est(W, D + X, ["fundid", "tc"]); bb = b[pre]; w = bb @ np.linalg.pinv(V[np.ix_(pre, pre)]) @ bb
    print(f"  {nm:<58} fortrend chi2 {w:6.2f}  p {stats.chi2.sf(w, len(pre)):.3f}   storsta |t| fore {np.abs(b[pre]/se[pre]).max():.2f}")
print("\nFORTREND (Dos x kvartal, sju kvartal fore, fond- och manad x kategori-effekter) med olika kontroller x kvartal:")
run("a) gammal klass (Cornaggia-formen)", Kc)
run("b) gammal klass + sigma linjart", Kc + P1)
run("c) gammal klass + polynom i sigma", Kc + P3)
run("d) bara polynom i sigma (sicksacken, utan forperiodskontroll)", P3)
run("e) ingen kontroll", [])
