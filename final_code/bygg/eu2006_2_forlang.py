"""Slar ihop exporten 1998-2010 med forlangningen 2011-2016. python3 -I sla_ihop.py ../full/raw06.pkl <forlangning.csv> raw16.pkl <Developed_3_Factors.csv> <usa.csv> rf16.csv"""
import sys, re, numpy as np, pandas as pd
x = pd.read_pickle(sys.argv[1])
d = pd.read_csv(sys.argv[2], low_memory=False, encoding="utf-8-sig"); d.columns = [re.sub(r"\s+", " ", c).strip() for c in d.columns]
d = d[d.SecId.astype(str).str.match(r"^F[0-9A-Z]{9}$")].copy()
def ser(prefix):
    cols = [c for c in d.columns if c.startswith(prefix) and re.search(r"\d{4}-\d{2}", c)]
    m = {c: re.search(r"\d{4}-\d{2}", c).group(0) for c in cols}; z = d.set_index("SecId")[cols].rename(columns=m); z = z[sorted(z.columns)]
    return z.apply(lambda s: pd.to_numeric(s.astype(str).str.replace(",", ""), errors="coerce"))
R2, NA2, RET2, FS = ser("Morningstar Rating Overall "), ser("Net Assets - share class (Monthly)"), ser("Monthly Return"), ser("Fund Size - comprehensive")
print("klasser gammal fil", len(x["R"]), "| ny fil", len(d), "| gemensamma", len(set(x["R"].index) & set(d.SecId)))
# overlapp 2010-12: ska vara lika
for nm, a, b in [("betyg", x["R"], R2), ("NA", x["NA"], NA2)]:
    j = a[["2010-12"]].join(b[["2010-12"]], lsuffix="_g", rsuffix="_n").dropna(); print(f"overlapp 2010-12 {nm}: n {len(j)}, lika {(np.isclose(j.iloc[:,0], j.iloc[:,1], rtol=1e-6)).mean():.4f}")
def cat(a, b):
    b = b[[c for c in b.columns if c not in a.columns]]; return a.join(b, how="left")
out = {"R": cat(x["R"], R2), "NA": cat(x["NA"], NA2), "RET": cat(x["RET"], RET2), "FS": FS.reindex(x["R"].index), "st": x["st"]}
for k in ("R", "NA", "RET", "FS"): print(k, out[k].shape, out[k].columns.min(), out[k].columns.max())
pd.to_pickle(out, sys.argv[3])
# riskfri ranta
def rd(fn):
    rows = []
    for ln in open(fn, encoding="latin-1"):
        p = [t.strip() for t in ln.split(",")]
        if re.fullmatch(r"\d{6}", p[0]) and len(p) >= 5: rows.append((p[0], float(p[4])))
        elif rows and not re.fullmatch(r"\d{6}", p[0]): break
    return pd.Series(dict(rows))
dev = rd(sys.argv[4]); usa = pd.read_csv(sys.argv[5]).assign(k=lambda z: z.yyyymm.astype(str)).set_index("k").RF
j = pd.concat([dev.rename("dev"), usa.rename("usa")], axis=1).dropna(); j = j[(j.index >= "199801")]
print("RF Developed mot USA, 1998-01..2011-12: n", len(j), "max avvikelse", float((j.dev - j.usa).abs().max()))
dev[(dev.index >= "199801") & (dev.index <= "201612")].rename("RF").rename_axis("yyyymm").reset_index().to_csv(sys.argv[6], index=False); print("RF-manader sparade:", int(((dev.index >= "199801") & (dev.index <= "201612")).sum()))
