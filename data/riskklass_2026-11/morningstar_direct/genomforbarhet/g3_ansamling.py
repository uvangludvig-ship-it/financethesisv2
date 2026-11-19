# Punkt 5: ansamling av volatilitet strax under klassgranserna? Bara riskmatt, inga floden.
import pandas as pd, numpy as np, os
H=os.path.expanduser("~/mnt")
L=pd.read_csv(f"{H}/morningstar_direct/direct_manadspanel.csv.gz",usecols=["SecId","roll","performanceid"]).drop_duplicates("SecId")
pids=set(L[L.roll=="huvudklass"].performanceid)
R=pd.read_csv(f"{H}/shof_riskklass_resultat/riskmatt/riskmatt_manad_alla.csv.gz")
print("klasser i riskmatt:",R.pid.nunique(),"| huvudklasser i Direct:",R[R.pid.isin(pids)].pid.nunique())
for urval,X in [("huvudklasser i Direct",R[R.pid.isin(pids)]),("alla klasser i riskmatt",R)]:
    print("\n#####",urval)
    for col,gr in [("sig_w",10),("sig_w",15),("vev",12),("vev",20)]:
        print(f"\n{col}, grans {gr}: antal per 0,25-fonster fran -3 till +3 (strecket = gransen); kvot = [g-0,5;g) / [g;g+0,5); kvot1 = [g-1;g)/[g;g+1)")
        for ym in ["2019-12","2021-12","2022-12","2023-12","2024-12","2025-12"]:
            v=X[X.ym==ym][col].dropna().values-gr
            h=np.histogram(v,bins=np.arange(-3,3.0001,0.25))[0]
            a=((v>=-0.5)&(v<0)).sum(); b=((v>=0)&(v<0.5)).sum(); a1=((v>=-1)&(v<0)).sum(); b1=((v>=0)&(v<1)).sum()
            print(f"  {ym}: "+" ".join(f"{x:3d}" for x in h[:12])+"  | "+" ".join(f"{x:3d}" for x in h[12:])+f"   kvot {a/max(b,1):.2f} ({a}/{b})  kvot1 {a1/max(b1,1):.2f}")
