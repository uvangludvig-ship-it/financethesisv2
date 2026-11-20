"""Fondbolag per fond (Branding Name, Firm Name) ur exporterna. Skriver fb.pkl (2006-panelen) och fb_1825.pkl (2018-2025).
python3 10_bygg_fb.py <direct_eu_1998_2010.csv(.gz)> <mapp med A1-A3, B1, B2 .csv.gz>
Rekonstruerad 20 nov 2026 ur de kommandon som kordes direkt i terminalen; samma logik."""
import sys, re, glob
import numpy as np, pandas as pd
norm = lambda c: re.sub(r"\s+", " ", c).strip()
md = lambda s: s.mode().iat[0] if s.notna().any() else np.nan
# 2006-panelen
f = sys.argv[1]
h = pd.read_csv(f, nrows=0, encoding="utf-8-sig").columns
want = [c for c in h if norm(c) in ("SecId", "FundId", "Firm Name", "Branding Name")]
d = pd.read_csv(f, usecols=want, encoding="utf-8-sig", low_memory=False); d.columns = [norm(c) for c in d.columns]
d = d[d.SecId.astype(str).str.startswith("F")]
fb = d.dropna(subset=["FundId"]).groupby("FundId").agg(brand=("Branding Name", md), firm=("Firm Name", md), nb=("Branding Name", "nunique"))
fb.to_pickle("fb.pkl")
# 2018-2025
out = []
for g in sorted(glob.glob(sys.argv[2].rstrip("/") + "/*.csv.gz")):
    h = pd.read_csv(g, nrows=0).columns
    want = [c for c in h if norm(c) in ("SecId", "FundId", "Firm Name", "Branding Name", "Name")]
    x = pd.read_csv(g, usecols=want, low_memory=False); x.columns = [norm(c) for c in x.columns]; out.append(x)
d = pd.concat(out).drop_duplicates("SecId")
fb2 = d.dropna(subset=["FundId"]).groupby("FundId").agg(brand=("Branding Name", md), firm=("Firm Name", md), Name=("Name", "first"))
fb2.to_pickle("fb_1825.pkl")
print(len(fb), len(fb2))
