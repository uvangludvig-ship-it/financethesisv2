# Packar upp Direct-exporterna (dataset thesis_glober_2016) till en manadspanel. Inga floden.
import pandas as pd, numpy as np, glob
m={'Low':1,'Below Average':2,'Average':3,'Above Average':4,'High':5}
out=[]
for f in sorted(glob.glob("glober_*.xlsx")):
    x=pd.read_excel(f,header=2); x=x[x.SecId.notna()&x.SecId.astype(str).str.startswith('F')]
    r=[c for c in x.columns if c.startswith('Portfolio ESG Risk Rating_')]
    s=[c for c in x.columns if c.startswith('Portfolio Corporate ESG Risk Score')]
    R=x[['SecId']+r].melt(id_vars='SecId',var_name='c',value_name='glob'); R['ym']=R.c.str[-10:-3]
    S=x[['SecId']+s].melt(id_vars='SecId',var_name='c',value_name='score'); S['ym']=S.c.str[-10:-3]
    R['glob']=R.glob.map(m); S['score']=pd.to_numeric(S.score,errors='coerce')
    P=R[['SecId','ym','glob']].merge(S[['SecId','ym','score']],on=['SecId','ym'],how='outer'); P['lista']=f[7:-5]; out.append(P)
P=pd.concat(out).drop_duplicates(['SecId','ym'])
P=P[P.glob.notna()|P.score.notna()]
P.to_csv("glober_manad.csv.gz",index=False)
print("klasser med nagot varde:",P.SecId.nunique(),"| med glob nagon gang:",P[P.glob.notna()].SecId.nunique())
print("glob-serien borjar:",P[P.glob.notna()].ym.min(),"| poang borjar:",P[P.score.notna()].ym.min())
c=P[P.glob.notna()].groupby('ym').SecId.nunique()
print("klasser med glob per manad (urval):",{k:int(c.get(k,0)) for k in ['2018-08','2019-08','2019-09','2019-10','2022-12','2023-01','2026-10']})
Q=P[P.glob.notna()].pivot(index='SecId',columns='ym',values='glob')
cols=list(Q.columns); ch=[]
for a,b in zip(cols[:-1],cols[1:]):
    both=Q[a].notna()&Q[b].notna()
    ch.append((b,int(both.sum()),float((Q.loc[both,a]!=Q.loc[both,b]).mean())))
ch=pd.DataFrame(ch,columns=['ym','n','andel_byte'])
print("\nManader dar over 20 % bytte glob:"); print(ch[ch.andel_byte>0.2].to_string(index=False))
print("\nMedian andel byte per manad:",round(ch.andel_byte.median(),3))
print("\nFordelning av glober 2019-08 och 2019-09:")
print(pd.crosstab(Q['2019-08'],Q['2019-09']))
