# Packar upp thesis_glober_hist-exporterna. Inga floden.
import pandas as pd, numpy as np, glob, re
keys={'Historical Corporate ESG Risk Score':'hscore','Historical Corporate ESG Risk Percent Rank in Global Category':'hrank',
 'Global Category Breakpoint Corporate ESG Risk Score 5':'bp5','Global Category Breakpoint Corporate ESG Risk Score 4':'bp4',
 'Global Category Breakpoint Corporate ESG Risk Score 3':'bp3','Global Category Breakpoint Corporate ESG Risk Score 2':'bp2'}
out=[]; gcat=[]
for f in sorted(glob.glob("hist_*.xlsx")):
    x=pd.read_excel(f,header=2); x=x[x.SecId.notna()&x.SecId.astype(str).str.startswith('F')]
    gc=[c for c in x.columns if c.startswith('Global Category') and not re.search(r'_\d{4}-\d{2}-\d{2}$',c)]
    if gc: gcat.append(x[['SecId',gc[0]]].rename(columns={gc[0]:'gcat'}))
    for k,v in keys.items():
        cols=[c for c in x.columns if c.split('<br/>')[0].split('_')[0]==k]
        if not cols: print('saknas',f,k); continue
        M=x[['SecId']+cols].melt(id_vars='SecId',var_name='c',value_name=v); M['ym']=M.c.str[-10:-3]
        M[v]=pd.to_numeric(M[v],errors='coerce'); out.append(M[['SecId','ym',v]].assign(var=v).rename(columns={v:'val'}))
L=pd.concat(out).dropna(subset=['val']).drop_duplicates(['SecId','ym','var'])
W=L.pivot_table(index=['SecId','ym'],columns='var',values='val').reset_index()
G=pd.concat(gcat).drop_duplicates('SecId') if gcat else pd.DataFrame(columns=['SecId','gcat'])
W=W.merge(G,on='SecId',how='left')
g=pd.read_csv("glober_manad.csv.gz")[['SecId','ym','glob']]
W=W.merge(g,on=['SecId','ym'],how='outer')
W.to_csv("glober_hist_manad.csv.gz",index=False)
print("rader",len(W),"klasser",W.SecId.nunique())
for v in ['hscore','hrank','bp5','bp2','gcat','glob']:
    s=W[W[v].notna()] if v in W else None
    if s is not None and len(s): print(f"{v}: klasser {s.SecId.nunique()}, forsta manad {s.ym.min()}")
# konsistens: aterskapar brytpunkterna globen?
Z=W.dropna(subset=['hscore','bp5','bp4','bp3','bp2','glob']).copy()
# lagre risk = battre: 5 glober om hscore<=bp5 ...
Z['g_hat']=np.select([Z.hscore<=Z.bp5,Z.hscore<=Z.bp4,Z.hscore<=Z.bp3,Z.hscore<=Z.bp2],[5,4,3,2],1)
print("andel dar brytpunkter+poang ger visad glob:",round((Z.g_hat==Z.glob).mean(),3),"n",len(Z))
print(pd.crosstab(Z.glob,Z.g_hat))
