import pandas as pd, numpy as np, re, glob
parts=[pd.read_excel(f,header=2).assign(chunk=f) for f in sorted(glob.glob('eu_c*.xlsx'))]
x=pd.concat(parts,ignore_index=True).drop_duplicates('SecId')
print('klasser totalt:',len(x),'fonder:',x.FundId.nunique())
EEA=set("Austria Belgium Bulgaria Croatia Cyprus Czechia Denmark Estonia Finland France Germany Greece Hungary Ireland Italy Latvia Lithuania Luxembourg Malta Netherlands Poland Portugal Romania Slovakia Slovenia Spain Sweden Iceland Norway Liechtenstein".split())
dom=x.ISIN.astype(str).str[:2].map({'LU':'Luxembourg','IE':'Ireland'})
av=x['Country Available for Sale'].fillna('').str.split(';').apply(set)
uk=av.apply(lambda s:'United Kingdom' in s)
eea_x=pd.Series([len(s&EEA-{d}) for s,d in zip(av,dom)],index=x.index)
x['side']=np.where(uk&(eea_x==0),'UK',np.where(~uk&(eea_x>0),'EU','other'))
x['Inception Date']=pd.to_datetime(x['Inception Date'],errors='coerce')
def ts(p):
    c=[k for k in x.columns if str(k).startswith(p+'_')]; m=x[c].apply(pd.to_numeric,errors='coerce'); m.columns=[pd.Period(k[-10:-3],'M') for k in c]; m.index=x.SecId; return m
flow=ts('Estimated Share Class Net Flow (Monthly)'); na=ts('Net Assets - share class (Monthly)'); sri=ts('SRI Value'); star=ts('Morningstar Rating Overall')
def hist(h,before):
    v=[(pd.Timestamp(a),int(b)) for a,b in re.findall(r"\[(\d{4}-\d\d-\d\d)\]\s*(\d)",str(h))]; v=[b for a,b in v if a<=before]; return v[-1] if v else np.nan
x['srri_dec22']=[hist(h,pd.Timestamp('2022-12-31')) for h in x['Surveyed KIID SRRI History']]
x['srri_last_date']=[(re.findall(r"\[(\d{4}-\d\d-\d\d)\]",str(h)) or [None])[-1] for h in x['Surveyed KIID SRRI History']]
x['sri_h1_23']=sri.loc[:,pd.Period('2023-01','M'):pd.Period('2023-06','M')].bfill(axis=1).iloc[:,0].values
x['n_flow']=flow.loc[:,pd.Period('2021-01','M'):pd.Period('2023-12','M')].notna().sum(axis=1).values
x['dos']=x.sri_h1_23-x.srri_dec22
x.drop(columns=[c for c in x.columns if re.search(r'_\d{4}-\d\d-\d\d$',str(c))]).to_pickle('alla_bas.pkl')
flow.to_pickle('alla_flow.pkl'); na.to_pickle('alla_na.pkl'); star.to_pickle('alla_star.pkl'); sri.to_pickle('alla_sri.pkl')
print('sidor:',x.side.value_counts().to_dict())
ok=x[(x.n_flow>=30)&(x['Inception Date']<='2021-12-31')]
print('med flöden (>=30 av 36 mån 2021-23) och start före 2022:',ok.side.value_counts().to_dict())
g=ok.groupby('FundId').side.agg(set); both=g[g.apply(lambda s:{'UK','EU'}<=s)].index
print('FONDER MED PAR:',len(both))
fd=ok[(ok.side=='EU')&ok.FundId.isin(both)].groupby('FundId').dos.median()
print('varav med dos:',fd.notna().sum(),'| dosfördelning:',fd.round().value_counts().sort_index().to_dict())
pd.Series(both).to_csv('alla_fonder_med_par.csv',index=False)
