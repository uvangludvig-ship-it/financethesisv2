import pandas as pd, numpy as np, re
x=pd.read_excel('direct_uk_eu_panel_2021_2025.xlsx',header=2)
EEA=set("Austria Belgium Bulgaria Croatia Cyprus Czechia Denmark Estonia Finland France Germany Greece Hungary Ireland Italy Latvia Lithuania Luxembourg Malta Netherlands Poland Portugal Romania Slovakia Slovenia Spain Sweden Iceland Norway Liechtenstein".split())
dom=x.ISIN.str[:2].map({'LU':'Luxembourg','IE':'Ireland'})
av=x['Country Available for Sale'].fillna('').str.split(';').apply(set)
uk=av.apply(lambda s:'United Kingdom' in s)
eea_x=[s&EEA-{d} for s,d in zip(av,dom)]
x['side']=np.where(uk & pd.Series([len(e)==0 for e in eea_x]),'UK',np.where(~uk & pd.Series([len(e)>0 for e in eea_x]),'EU','other'))
def ts(p):
    c=[k for k in x.columns if str(k).startswith(p+'_')]; m=x[c].apply(pd.to_numeric,errors='coerce'); m.columns=[pd.Period(k[-10:-3],'M') for k in c]; m.index=x.SecId; return m
flow=ts('Estimated Share Class Net Flow (Monthly)'); na=ts('Net Assets - share class (Monthly)'); sri=ts('SRI Value'); star=ts('Morningstar Rating Overall')
def hist(h, before):
    v=[(pd.Timestamp(a),int(b)) for a,b in re.findall(r"\[(\d{4}-\d\d-\d\d)\]\s*(\d)",str(h))]
    v=[b for a,b in v if a<=before]; return v[-1] if v else np.nan
x['srri_dec22']=[hist(h,pd.Timestamp('2022-12-31')) for h in x['Surveyed KIID SRRI History']]
x['srri_last_date']=[ (re.findall(r"\[(\d{4}-\d\d-\d\d)\]",str(h)) or [None])[-1] for h in x['Surveyed KIID SRRI History']]
x['srri_2023']=[hist(h,pd.Timestamp('2023-12-31')) for h in x['Surveyed KIID SRRI History']]
s23=sri.loc[:,pd.Period('2023-01','M'):pd.Period('2023-06','M')]
x['sri_h1_23']=s23.bfill(axis=1).iloc[:,0].values
x['n_flow_22_23']=flow.loc[:,pd.Period('2022-01','M'):pd.Period('2023-12','M')].notna().sum(axis=1).values
x['dos']=x.sri_h1_23-x.srri_dec22
x.to_pickle('par_bas.pkl'); flow.to_pickle('flow.pkl'); na.to_pickle('na.pkl'); star.to_pickle('star.pkl'); sri.to_pickle('sri.pkl')
print(x.side.value_counts().to_dict())
ok=x[x.n_flow_22_23>=20]
print('with >=20 flow months 2022-23:', ok.side.value_counts().to_dict())
f=ok.groupby('FundId').side.agg(set)
both=f[f.apply(lambda s:{'UK','EU'}<=s)].index
print('funds with UK and EU class, both with flows:',len(both))
eu=ok[(ok.side=='EU')&ok.FundId.isin(both)]
print('EU classes:',len(eu),'dose available:',eu.dos.notna().sum()); print(eu.dos.value_counts().sort_index().to_dict())
fd=eu.groupby('FundId').dos.median(); print('fund-level dose:',fd.round().value_counts().sort_index().to_dict(), 'funds with dose',fd.notna().sum())
ukc=ok[(ok.side=='UK')&ok.FundId.isin(both)]
print('UK classes:',len(ukc),'| UK SRRI entry dated 2023+:',(pd.to_datetime(ukc.srri_last_date)>='2023-03-01').sum(),'| UK with SRI value H1-2023:',ukc.sri_h1_23.notna().sum())
print('UK last SRRI date dist:',pd.to_datetime(ukc.srri_last_date).dt.year.value_counts().sort_index().to_dict())
pd.Series(both).to_csv('fonder_med_par.csv',index=False)
