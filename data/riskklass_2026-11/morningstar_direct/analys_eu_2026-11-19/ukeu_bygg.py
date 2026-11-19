"""UK mot EU: sidserier per fond och niva. Skriver urval (antal manader) men inga flodesvarden efter dec 2022.
python3 -I ukeu_bygg.py <tag>  -> ukeu_sidor_<tag>.pkl, ukeu_dos_<tag>.pkl"""
import sys, numpy as np, pandas as pd
T = sys.argv[1]; P_ = lambda s: pd.Period(s, "M")
L = pd.read_pickle(f"panel_eu_{T}.pkl"); E = pd.read_pickle(f"urval_eu_{T}.pkl")
E["uk"] = E["Country Available for Sale"].fillna("").str.contains("United Kingdom")
ni = ~E.inst
EU = set(E.index[ni & (E.sida == "EU")])
UK = {1: set(E.index[ni & (E.sida == "UK")]), 2: set(E.index[ni & E.uk & (E.cur == "GBP")]), 3: set(E.index[ni & E.uk])}
Ls = L[L.stor & (L.t >= P_("2019-01")) & (L.t <= P_("2025-12"))].copy(); Ls["usd"] = Ls.f * Ls.na_lag

def side(sec, nm):
    X = Ls[Ls.SecId.isin(sec)]
    G = X.groupby(["fundid", "t"]).agg(usd=("usd", "sum"), na=("na_lag", "sum"), nk=("SecId", "nunique")).reset_index()
    G["r"] = G.usd / G.na; G["sida"] = nm; return G

out = []
for lev in (1, 2, 3):
    S = pd.concat([side(EU, "EU"), side(UK[lev], "UK")], ignore_index=True)
    y = S.t.dt.year
    def okset(y0, y1):
        n1 = S[y.isin(y0)].groupby(["fundid", "sida"]).size().unstack(); n2 = S[y.isin(y1)].groupby(["fundid", "sida"]).size().unstack()
        n1 = n1.reindex(columns=["EU", "UK"]).fillna(0); n2 = n2.reindex(index=n1.index, columns=["EU", "UK"]).fillna(0)
        return set(n1.index[(n1.EU >= 18) & (n1.UK >= 18) & (n2.EU >= 18) & (n2.UK >= 18)])
    f_main = okset([2021, 2022], [2023, 2024]); f_pl = okset([2019, 2020], [2021, 2022])
    S["niva"] = lev; S["ok_main"] = S.fundid.isin(f_main); S["ok_pl"] = S.fundid.isin(f_pl)
    out.append(S[S.ok_main | S.ok_pl])
    nk = S[S.ok_main & (S.t == P_("2022-12"))].groupby("sida").nk.mean()
    print(f"Niva {lev}: fonder med bada sidor 18+18 man 2021-24: {len(f_main)} | latsasfonster 2019-22: {len(f_pl)} | klasser per sida dec 2022: EU {nk.get('EU', np.nan):.1f}, UK {nk.get('UK', np.nan):.1f}")
A = pd.concat(out, ignore_index=True)
# winsorisering 2,5/97,5 inom manad, over alla fond-sid-observationer inom niva
for lo, hi, nm in [(.025, .975, "f"), (.01, .99, "f1")]:
    q = A.groupby(["niva", "t"]).r.quantile([lo, hi]).unstack()
    k = pd.MultiIndex.from_arrays([A.niva, A.t])
    A[nm] = A.r.clip(q[lo].reindex(k).values, q[hi].reindex(k).values) * 100
# kategori och dos fran fondens storsta EU-klass (dec 2022)
Ce = E[E.index.isin(EU)].sort_values("na_dec22", ascending=False).groupby("FundId").head(1).set_index("FundId")
A = A.join(Ce[["Morningstar Category", "dos", "sig", "srri22"]].rename(columns={"Morningstar Category": "cat"}), on="fundid")
A.to_pickle(f"ukeu_sidor_{T}.pkl")
for lev in (1, 2, 3):
    f = A[(A.niva == lev) & A.ok_main].drop_duplicates("fundid")
    d = f[f.dos.isin([0, 1, 2]) & f.sig.notna()]
    print(f"Niva {lev}: med dos {len(d)} (0: {(d.dos==0).sum()}, 1: {(d.dos==1).sum()}, 2: {(d.dos==2).sum()}) | aktie {f.cat.astype(str).str.contains('Equity').sum()} | kategorier {f.cat.nunique()}")
# UK-sidans SRRI: behaller UK-klasserna SRRI? (andel med SRRI-post efter 2022)
import re
raw = None
