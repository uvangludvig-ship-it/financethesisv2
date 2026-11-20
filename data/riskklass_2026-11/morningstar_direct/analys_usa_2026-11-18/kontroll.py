# Oberoende kontroll: explicita dummies i stället för avmedling
import sys, numpy as np, pandas as pd
d=pd.read_pickle(sys.argv[1])
M=pd.get_dummies(d.ym).astype(float).values
S=pd.get_dummies(d.star.astype(int),drop_first=True).astype(float).values
y=d.flow.values
def R2(X,w=None):
    w=np.ones(len(y)) if w is None else w; sw=np.sqrt(w)
    b,*_=np.linalg.lstsq(X*sw[:,None],y*sw,rcond=None); e=y-X@b
    yb=np.average(y,weights=w); return 1-np.sum(w*e**2)/np.sum(w*(y-yb)**2)
a=R2(M); b=R2(np.c_[M,d.signal.values]); c=R2(np.c_[M,S]); dd=R2(np.c_[M,d.signal.values,S])
print('EW kont: totalt %.1f tid %.1f avk %.1f betyg %.1f gem %.1f'%(100*dd,100*a,100*(dd-c),100*(dd-b),100*(dd-a-(dd-c)-(dd-b))))
w=(d.tna_l/d.groupby('ym').tna_l.transform('sum')).values
a=R2(M,w); b=R2(np.c_[M,d.signal.values],w); c=R2(np.c_[M,S],w); dd=R2(np.c_[M,d.signal.values,S],w)
print('VW kont: totalt %.1f tid %.1f avk %.1f betyg %.1f'%(100*dd,100*a,100*(dd-c),100*(dd-b)))
# Table 3 punktskattning
top=(d.star==5).astype(float); n5=d.assign(t=top).groupby('ym').t.transform('sum')
tr=(d.groupby('ym').signal.rank(ascending=False,method='first')<=n5).astype(float)
bb,*_=np.linalg.lstsq(np.c_[M,top,tr],y,rcond=None); print('Table 3 %%-skillnad: %.3f'%(bb[-2]-bb[-1]))
# Figure 5 A(b) poolat
bb,*_=np.linalg.lstsq(np.c_[M,d.star.values,d.signal.values],y,rcond=None); print('Stjärna poolat: %.3f'%bb[-2])
# Andel betyg 5: rå andel per månad i urvalet
print('andel 5 stjärnor', round((d.star==5).mean()*100,1), 'andel 1 stjärna', round((d.star==1).mean()*100,1))
