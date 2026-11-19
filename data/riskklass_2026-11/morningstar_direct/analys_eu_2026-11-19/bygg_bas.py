"""Slar ihop A1-A3 (och senare grupp B) till bas_raw.pkl och bygger ECB-manadskurser (fx_month.pkl).
python3 -I bygg_bas.py <bas_eu-mapp med A*.csv.gz [B*.csv.gz]> <eurofxref-hist.zip>"""
import sys, re, glob, zipfile, pandas as pd
mapp, fxzip = sys.argv[1:3]
out = []
for f in sorted(glob.glob(f"{mapp}/A*.csv.gz") + glob.glob(f"{mapp}/B*.csv.gz")):
    D = pd.read_csv(f, low_memory=False); D.columns = [re.sub(r"\s+", " ", c).strip() for c in D.columns]
    D = D.loc[:, ~D.columns.duplicated()]
    D = D[D.SecId.astype(str).str.match(r"^F[0-9A-Z]{9}$")].copy(); D["delfil"] = f.split("/")[-1]; out.append(D); print(f, len(D))
B = pd.concat(out, ignore_index=True); d = B.SecId.duplicated(keep="first"); print("dubbletter", int(d.sum())); B = B[~d]
B.to_pickle("bas_raw.pkl"); print("bas_raw.pkl", B.shape)
z = zipfile.ZipFile(fxzip); fx = pd.read_csv(z.open(z.namelist()[0])); fx["Date"] = pd.to_datetime(fx.Date)
fx = fx.sort_values("Date"); fx["m"] = fx.Date.dt.to_period("M"); fx.groupby("m").last().to_pickle("fx_month.pkl"); print("fx_month.pkl")
