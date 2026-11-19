# Riskmått per månadsslut ur SHoF dagskurser (returntype 1, unit_bas). VEV enligt Priip (Cornish-Fisher, T=5) och veckosigma (SRRI), fem års fönster.
import sys, numpy as np, pandas as pd
src, out = sys.argv[1], sys.argv[2]
parts=[]
for ch in pd.read_csv(src, sep=";", usecols=["performanceId","date","returntype","unit_bas"], chunksize=1_500_000, dtype={"performanceId":"category"}):
    ch=ch[ch.returntype==1]
    parts.append(ch[["performanceId","date","unit_bas"]])
d=pd.concat(parts, ignore_index=True); del parts
d["performanceId"]=d.performanceId.astype(str); d["date"]=pd.to_datetime(d.date)
d=d[d.date.dt.dayofweek<5].dropna(subset=["unit_bas"])
ends=pd.date_range("2018-12-31","2025-12-31",freq="ME")
rows=[]
for pid,g in d.groupby("performanceId", sort=False):
    s=g.drop_duplicates("date").set_index("date").unit_bas.sort_index()
    s=s[s>0]
    if len(s)<300: continue
    lr=np.log(s).diff().dropna()
    wk=np.log(s.resample("W-FRI").last().dropna()).diff().dropna()
    for e in ends:
        a=e-pd.DateOffset(years=5)
        r=lr[(lr.index>a)&(lr.index<=e)]
        if len(r)<400: continue
        n=len(r); yrs=(r.index[-1]-r.index[0]).days/365.25
        sd=r.std(ddof=1); m=r.mean(); z=(r-m)/r.std(ddof=0)
        sk=float((z**3).mean()); ku=float((z**4).mean()-3)
        N=1260.0
        var=sd*np.sqrt(N)*(-1.96+0.474*sk/np.sqrt(N)-0.0687*ku/N+0.146*sk**2/N)-0.5*sd**2*N
        vev=(np.sqrt(3.842-2*var)-1.96)/np.sqrt(5)*100
        w=wk[(wk.index>a)&(wk.index<=e)]
        sw=w.std(ddof=1)*np.sqrt(52)*100 if len(w)>=100 else np.nan
        rows.append((pid,e.strftime("%Y-%m"),n,round(yrs,3),round(vev,4),round(sd*np.sqrt(n/yrs)*100,4),round(sw,4) if sw==sw else np.nan))
pd.DataFrame(rows,columns=["pid","ym","nd","years","vev","sig_d","sig_w"]).to_csv(out,index=False)
print("klar",src.split("/")[-1],len(rows))
