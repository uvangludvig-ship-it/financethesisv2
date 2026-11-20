# Utforskande: varför skiljer sig talen från ankaret? Inte deklarerat.
import sys, numpy as np, pandas as pd, re
d=pd.read_pickle('panel.pkl'); alla=pd.read_pickle('panel_alla.pkl')
def R2(y,X,M,w=None):
    w=np.ones(len(y)) if w is None else w; sw=np.sqrt(w); Z=np.c_[M,X] if X is not None else M
    b,*_=np.linalg.lstsq(Z*sw[:,None],y*sw,rcond=None); e=y-Z@b; yb=np.average(y,weights=w)
    return 1-np.sum(w*e**2)/np.sum(w*(y-yb)**2)
def summary(g,lab):
    M=pd.get_dummies(g.ym).astype(float).values; S=pd.get_dummies(g.star.astype(int),drop_first=True).astype(float).values
    y=g.flow.values; s=g.signal.values[:,None]
    a=R2(y,None,M); b=R2(y,s,M); c=R2(y,S,M); dd=R2(y,np.c_[s,S],M)
    bb,*_=np.linalg.lstsq(np.c_[M,g.star.values,g.signal.values],y,rcond=None)
    print(f"{lab:38s} n={len(g):6d} fonder={g.FundId.nunique():5d} flöde medel {g.flow.mean():+.2f} CS std {g.groupby('ym').flow.std().mean():.2f} | R2 tot {100*dd:.1f} avk {100*(dd-c):.1f} betyg {100*(dd-b):.1f} | stjärna {bb[-2]:.2f} | 5★ {100*(g.star==5).mean():.1f}% 1★ {100*(g.star==1).mean():.1f}%")
summary(d,'Huvudurval')
summary(d[d.age>=6.5],'Ålder >= 6,5 år (78 mån)')
summary(d[d.age>=12.8],'Ålder >= 12,8 år (ankarets median)')
summary(d[d.ym>='2002-07'],'Bara efter juni 2002')
summary(d[d.ym<='2002-06'],'Bara före juni 2002')
# stjärnfördelning: andelsklassnivå (rå) mot fondnivå
raw=pd.read_csv(sys.argv[1],encoding='latin-1',low_memory=False,dtype=str)
raw.columns=[re.sub(r'\s+',' ',c.replace('\n',' ')).strip() for c in raw.columns]
raw=raw[raw['Morningstar Category Group'].eq('Equity')]
sc=[c for c in raw.columns if c.startswith('Morningstar Rating Overall') and re.search(r'\d{4}-\d{2}',c)]
v=pd.to_numeric(raw[sc].stack(),errors='coerce').dropna()
print('Andelsklasser, alla betygsmånader: fördelning %', (v.value_counts(normalize=True).sort_index()*100).round(1).to_dict())
fa=alla.dropna(subset=['star_d']); fa=fa[fa.ym>='1999-01']
print('Fondnivå, alla fonder med betyg: %', (fa.star_d.value_counts(normalize=True).sort_index()*100).round(1).to_dict())
print('Fondnivå, urvalet: %', (d.star.value_counts(normalize=True).sort_index()*100).round(1).to_dict())
big=fa[fa.ym.isin(d.ym.unique())].merge(d[['FundId','ym']].assign(inn=1),how='left',on=['FundId','ym'])
print('Fondnivå, med betyg men utanför urvalet: %', (big[big.inn.isna()].star_d.value_counts(normalize=True).sort_index()*100).round(1).to_dict())
# hur mycket av flödesspridningen kommer från extrema månader
q=d.flow; print('Andel |flöde|>10 %/mån:', round((q.abs()>10).mean()*100,1),'%; CS std om flöde kapas vid ±10:', round(d.assign(f=q.clip(-10,10)).groupby('ym').f.std().mean(),2))
