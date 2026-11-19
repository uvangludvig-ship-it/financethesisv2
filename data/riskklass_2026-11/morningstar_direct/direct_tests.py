_s = open('/home/claude/scripts/fuzzy.py').read(); exec(_s[:_s.index('NEW=[(12,"vev_22",1),(20,"vev_22",1)]; OLDc')])
L = pd.read_pickle("/home/claude/direct_out/direct_long.pkl")
M = L[L.roll=="huvudklass"].copy()
M = M.sort_values(["fundid","t"])
M["sri_f"] = M.groupby("SecId").sri.transform(lambda x: x.ffill())
# if no SRI series at all, use current SRI for the post period
nos = M.groupby("SecId").sri.transform(lambda x: x.notna().sum()==0)
M.loc[nos & (M.t>=pd.Period("2023-01","M")), "sri_f"] = M.loc[nos & (M.t>=pd.Period("2023-01","M")), "sri_cur"]
# early 2023 months before first SRI obs: back-fill from first obs within 2023H1
M["sri_b"] = M.groupby("SecId").sri_f.transform(lambda x: x.bfill(limit=6))
M["act"] = np.where(M.t>=pd.Period("2023-01","M"), M.sri_b, M.srri)
lab = M[["fundid","t","act","star","cat"]].drop_duplicates(["fundid","t"])
print("funds with actual labels:", lab.dropna(subset=["act"]).fundid.nunique())
def with_act(df):
    df = df.merge(lab, on=["fundid","t"], how="left")
    df = df.dropna(subset=["act"]).copy(); df["label"]=df.act.astype(float); return df
NEW=[(12,"vev_22",1),(20,"vev_22",1)]; OLDc=[(10,"sig_w_22",-1),(15,"sig_w_22",-1)]
R2 = add_label(R.copy()); FR2 = add_label(FR.copy())
R3 = with_act(R2.drop(columns=["label"])); FR3 = with_act(FR2.drop(columns=["label"]))
print("\n=== HUVUDTEST MED RIKTIGA KLASSER (fuzzy, instrument = över gränsen x efter 2023)")
for nm, dat in [("huvudklass, privatsparare", R3), ("alla privatsparklasser per fond", FR3)]:
    print(f"-- {nm}")
    fuzzy(dat, NEW+OLDc, 3.0, "fyra gränser")
    fuzzy(dat, NEW, 3.0, "nya gränser")
    fuzzy(dat, OLDc, 3.0, "gamla gränser")
    for sp in NEW+OLDc: fuzzy(dat, [sp], 3.0, f"gräns {sp[0]} {sp[1]}")
print("\n-- jämförelse: samma urval med beräknade klasser")
FR2b = FR2[FR2.set_index(['fundid','t']).index.isin(FR3.set_index(['fundid','t']).index)]
fuzzy(FR2b, NEW+OLDc, 3.0, "fyra gränser (beräknat)")
fuzzy(FR2b, NEW, 3.0, "nya gränser (beräknat)")
FR3.to_pickle("/home/claude/direct_out/FR3.pkl")
