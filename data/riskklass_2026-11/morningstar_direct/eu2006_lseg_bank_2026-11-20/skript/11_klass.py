"""Klassning av fondbolag: bank (B), fristaende (F), oklart/annat (O).
Regel: B = fondbolaget ingick vid referensdatum i en koncern som driver bank med
kontorsnat eller egen radgivarkar for privatkunder i Europa.
F = ingen sadan bank och inget forsakringsbolag med eget saljnat i Europa i koncernen.
O = privatbanker, forsakringsagda, administrationsplattformar, blandat eller osakert agande.
Ovriga varumarken ar oklassade och ingar inte.
Klassningen ar gjord av Claude ur allman kannedom, INTE belagd rad for rad.
Skriven innan nagot flodesutfall per grupp har raknats."""
import pandas as pd

# ---------- Agande oktober 2006 (panelen 2003-2010) ----------
B06 = ["BNP Paribas", "UBS", "Amundi", "DWS", "HSBC", "Candriam", "Mediolanum", "Union Investment",
       "SEB", "Fideuram", "Eurizon", "Robeco", "Nordea", "Deka", "Danske Invest", "Argenta", "NN IP",
       "DNB", "BCEE", "Barclays", "Fortis", "Swisscanto", "Kredietrust Luxembourg", "RBS", "ABN AMRO",
       "Handelsbanken", "KBC", "cominvest", "Lloyds Investment Fund Managers Ltd", "CR Firenze",
       "Eurobank", "Credit Suisse", "Santander"]
F06 = ["JPMorgan", "Fidelity International", "Schroders", "Goldman Sachs", "Franklin Templeton", "Invesco",
       "BlackRock", "abrdn", "Janus Henderson", "Russell Investments", "Morgan Stanley", "Jupiter", "MFS",
       "Barings", "Comgest", "Legg Mason", "First Sentier Investors", "T. Rowe Price", "Capital Group",
       "Wellington Management", "Principal", "Lazard", "Dimensional", "Putnam", "J O Hambro", "SEI", "Yuki",
       "Atlantis Investment Management", "Mercer Global Investments"]
O06 = ["GAM", "Allianz Global Investors", "Pictet", "Vontobel", "UBP", "Lombard Odier", "J. Safra Sarasin",
       "Edmond De Rothschild", "Mirabaud Asset Management", "Degroof Petercam",
       "Banque de Luxembourg Investments", "Hauck & Aufhäuser", "IPConcept", "AXXION", "LRI", "Lemanik",
       "GS&P", "Feri", "DJE Kapital", "Metzler", "AllianceBernstein", "PineBridge", "Aviva",
       "Eastspring Investments", "Manulife", "Generali", "Swiss Life", "AXA IM", "ASR", "Sanlam", "NEAM",
       "Anima", "Azimut", "Willerfunds", "BayernInvest", "Ninety One", "C WorldWide", "Belgrave", "Callander",
       "CapitalatWork", "Ofi Invest", "Finaltis", "Merrill Lynch", "iM Global Partner", "Fiera Capital",
       "Columbia Threadneedle", "BNY Mellon", "Natixis"]

# ---------- Agande december 2022 (panelen 2018-2025) ----------
B22 = ["BNP Paribas", "UBS", "Amundi", "DWS", "Eurizon", "Nordea", "Fideuram", "Mediolanum",
       "Union Investment", "Deka", "SEB", "Danske Invest", "ABN AMRO", "CA Indosuez", "Fineco", "BG",
       "Argenta", "DNB", "Swisscanto", "CPR Asset Management", "Santander", "Euromobiliare", "Eurobank",
       "BCEE", "CaixaBank", "Triodos Bank", "HSBC", "KBC", "Handelsbanken", "Credit Suisse", "Natixis"]
F22 = ["Schroders", "BlackRock", "JPMorgan", "Franklin Templeton", "Robeco", "AllianceBernstein",
       "Janus Henderson", "T. Rowe Price", "Invesco", "Morgan Stanley", "Wellington Management", "Comgest",
       "abrdn", "Capital Group", "C WorldWide", "Carmignac", "East Capital", "Lazard", "Columbia Threadneedle",
       "Fidelity International", "Allspring", "State Street", "RBC", "Russell Investments", "Eleva Capital",
       "Brandes", "MFS", "Federated Hermes", "Flossbach von Storch", "Davis  Advisers", "Ninety One",
       "Lupus alpha", "Bestinver", "Jupiter", "Dimensional", "Legg Mason", "First Sentier Investors"]
O22 = ["Goldman Sachs", "Pictet", "Azimut", "Candriam", "Allianz Global Investors", "Vontobel", "Generali",
       "Belgrave", "Edmond De Rothschild", "DJE Kapital", "AXXION", "Feri", "Anima", "NEAM", "Metzler",
       "IPConcept", "VPBank", "GAM", "Claresco", "Ofi Invest", "UBP", "Notz Stucki", "PMG", "Swiss Life",
       "Sparinvest", "BZ Bank", "ASR", "BayernInvest", "Sycomore Asset Management", "Eastspring Investments",
       "RAM", "Kredietrust Luxembourg", "Kairos", "Mandarine Gestion", "De Pury Pictet", "Aviva", "LOYS",
       "Cornèr Banca", "OkoWorld", "Finaltis", "Weiler&Eberhardt", "Lemanik", "Ersel", "Groupama", "Abante",
       "CapSolutions GmbH", "ETHENEA", "TARENO", "ODDO BHF", "CapitalatWork", "Controlfida Management",
       "La Financière de l'Echiquier", "Pure Capital", "Mapfre", "Swiss Rock", "M&G", "Cholet Dupont",
       "Hauck & Aufhäuser", "Kempen", "FPM Frankfurt", "Banca Popolare di Sondrio (SUISSE)",
       "Credit Andorra", "Fullerton", "Banca March", "PKB", "Sauren Finanzdienstleistungen", "Lingohr", "CB",
       "Feri Trust", "WWK Investment"]
USBANK = ["JPMorgan", "Goldman Sachs", "Morgan Stanley"]


def klassa(fb, vintage):
    """fb: DataFrame index FundId med brand, firm, Name. Returnerar Series grp (B/F/O/NaN) och usbank."""
    B, F, O = (B06, F06, O06) if vintage == 2006 else (B22, F22, O22)
    m = {**{b: "B" for b in B}, **{b: "F" for b in F}, **{b: "O" for b in O}}
    g = fb.brand.map(m)
    if vintage == 2006:
        # Undantag: dagens varumarke doljer en annan agare 2006
        ing = (fb.brand == "Goldman Sachs") & (fb.firm == "Goldman Sachs Asset Management B.V.")  # f.d. ING IM / NN IP
        cs = (fb.brand == "abrdn") & fb.Name.astype(str).str.startswith("CS EF")  # f.d. Credit Suisse Equity Fund
        g[ing | cs] = "B"
    us = fb.brand.isin(USBANK) & (g == "F")
    return g, us


if __name__ == "__main__":
    r = pd.read_pickle("/home/claude/eu2006/lang/raw16.pkl")["st"]
    nm = r.dropna(subset=["FundId"]).groupby("FundId").Name.first()
    fb = pd.read_pickle("/home/claude/bank/fb.pkl").join(nm)
    g, us = klassa(fb, 2006)
    p = pd.read_pickle("/home/claude/lseg/an/p_D.pkl")
    p = p[(p.ym >= "2003-01") & (p.ym <= "2010-12")]
    p["grp"] = p.FundId.map(g).fillna("oklassad")
    p["us"] = p.FundId.map(us).fillna(False)
    t = p.groupby("grp").agg(fondmanader=("FundId", "size"), fonder=("FundId", "nunique"))
    t["andel"] = (t.fondmanader / t.fondmanader.sum()).round(3)
    print("2003-2010\n", t, "\nvarav USA-banker i F:", int(p.us.sum()), p[p.us].FundId.nunique())
    q0 = p[p.ym == "2006-10"]
    print("okt 2006 fonder per grupp:", q0.groupby("grp").FundId.nunique().to_dict(),
          "| andel formogenhet:", (q0.groupby("grp").tna_l.sum() / q0.tna_l.sum()).round(3).to_dict())
    print("minsta antal fonder en manad:", p[p.grp.isin(["B", "F"])].groupby(["ym", "grp"]).size().unstack().min().to_dict())
    fb2 = pd.read_pickle("/home/claude/bank/fb_1825.pkl")
    g2, us2 = klassa(fb2, 2022)
    q = pd.read_pickle("/home/claude/slut/full2/bd_eu_EU_full2.pkl")
    q["grp"] = q.FundId.map(g2).fillna("oklassad")
    q["us"] = q.FundId.map(us2).fillna(False)
    t = q.groupby("grp").agg(fondmanader=("FundId", "size"), fonder=("FundId", "nunique"))
    t["andel"] = (t.fondmanader / t.fondmanader.sum()).round(3)
    print("2018-2025\n", t, "\nvarav USA-banker i F:", int(q.us.sum()), q[q.us].FundId.nunique())
    print("minsta antal fonder en manad:", q[q.grp.isin(["B", "F"])].groupby(["ym", "grp"]).size().unstack().min().to_dict())
    # lista for deklarationen
    rows = []
    for v, (B, F, O) in {"okt 2006": (B06, F06, O06), "dec 2022": (B22, F22, O22)}.items():
        for k, L in (("B", B), ("F", F), ("O", O)):
            rows += [(v, k, b) for b in L]
    pd.DataFrame(rows, columns=["agande_per", "grupp", "varumarke"]).to_csv("/home/claude/bank/klassning_fondbolag.csv", index=False)
