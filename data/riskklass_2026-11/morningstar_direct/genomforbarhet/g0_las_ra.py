# Laser raa SRI-serier och SRRI-historik ur Direct-exporten (ingen framatfyllning). Inga floden.
import pandas as pd, numpy as np, glob, re, os
H=os.path.expanduser("~/mnt/morningstar_direct")
fr=[]
for f in sorted(glob.glob(f"{H}/direct_thesis_*.xlsx")):
    d=pd.read_excel(f,header=2); d=d[d.SecId.notna()]; fr.append(d); print(os.path.basename(f),d.shape)
d=pd.concat(fr,ignore_index=True).drop_duplicates("SecId")
cols=[c for c in d.columns if str(c).startswith("SRI Value_")]
sri=d[cols].apply(pd.to_numeric,errors="coerce"); sri.columns=[pd.Period(str(c).split("_")[-1][:7],"M") for c in cols]; sri.index=d.SecId.values
sri.to_pickle("ra_sri.pkl")
rows=[]
for sid,h in zip(d.SecId,d["Surveyed KIID SRRI History"]):
    for a,b in re.findall(r"\[(\d{4}-\d\d-\d\d)\]\s*(\d)",str(h)): rows.append((sid,pd.Timestamp(a),int(b)))
Hh=pd.DataFrame(rows,columns=["SecId","date","srri"]); Hh.to_pickle("ra_srri_hist.pkl")
print("klasser",len(d),"| med nagon SRI-obs",int(sri.notna().any(axis=1).sum()),"| SRRI-historikposter",len(Hh),"klasser med historik",Hh.SecId.nunique())
print("andra kolumner:",[c for c in d.columns if "_" not in str(c)])
print("SRI obs per manad (urval):",sri.notna().sum().iloc[[0,12,24,36,48,58,59,60,61,62,66,72,84,96,105]].to_dict())
print("SRRI-historik, poster per ar:",Hh.date.dt.year.value_counts().sort_index().to_dict())
