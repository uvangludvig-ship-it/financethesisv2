import sys, numpy as np, pandas as pd
from math import erfc, sqrt
src = open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "08_korn_bc.py")).read().split("# ---------------- Korning B ----------------")[0]
sys.argv = ["x", sys.argv[1]]; exec(src)
for c in ("star", "unad_a"):
    d[c + "_E"] = d[c] * d.efter; d[c + "_A"] = d[c] * d.aldre; d[c + "_EA"] = d[c] * d.efter * d.aldre
d["EA"] = d.efter * d.aldre
XS = ["star", "star_E", "star_A", "star_EA", "unad_a", "unad_a_E", "unad_a_A", "unad_a_EA", "aldre", "EA"]
g = d[(d.ym >= "2003-01") & (d.ym <= "2010-12") & (d.age >= 3)]
b, se, n, nf = ols(g, "flow", XS)
print(f"n {n}, fonder {nf}")
for k in XS:
    t = b[k] / se[k]; print(f"{k:12s} {b[k]:+.4f}  SE {se[k]:.4f}  t {t:+.2f}  p {erfc(abs(t)/sqrt(2)):.3f}")
