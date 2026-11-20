# Kontroll av talen

Gjord av AI (Claude) 20 november 2026. Ingen av författarna har kört om något.

## 0. Regel: inget eget test

Varje test i paketet är Ben-David m.fl. (2022) eller Adelino m.fl. (2017), ur artikeln eller författarnas kod. Två anpassningar av Adelino är våra och behållna: antal steg (de har andel eller dummy) och volatilitetsdecil (de har storleksdecil). Följande ströks 20 november därför att det saknade förlaga:

| Struket | Var det stod |
|---|---|
| Betyg x Efter x Äldre för 2006, tre varianter | tabell 3, panel C |
| Samma fonder före och efter 2006 | bilaga A6 |
| Uppdelning på fondens ålder i testen av 2006 | tabell 3, figur 3, bilaga A6 |
| Krav på minst 200 fonder för jämförelseår | figur 3 (ändrade inget tal) |
| "Sicksacken": polynom i volatilitet och flöde före bytet | tabell 6, bilaga A5 |
| Låtsasbyte januari 2021 | tabell 6 |
| Fem och tjugo volatilitetsgrupper | bilaga A5 |
| Inplanterad effekt | kontroll i koden |
| Risksiffran inom kategori och per period | tabell 4 |
| Betyget mätt vid slutet av månad t-1 | bilaga A4 |
| Winsorisering 2,5/97,5 och "det större av två standardfel" | tabell 6 |
| Testen i Reuter och Zitzewitz form | tidigare bilaga |

Det som finns kvar utan förlaga står i sista avsnittet av `final.pdf` ("Kvar utan förlaga: ni avgör").

## 1. Hela kedjan från rådata

`bash kor_allt.sh` kördes i en ren kopia med repots mappstruktur: rådata till paneler, paneler till test, test till tabeller. Resultatet jämfördes med en körning på de paneler som de äldre skripten byggde 18 till 20 november.

| Jämfört | Utfall |
|---|---|
| `final_result/tal/*.csv` | 83 av 83 filer identiska, varje tal |
| `final_result/tabeller/*.tex` | 16 av 16 filer identiska |

Alla paneler utom den för tabell 6 byggdes om från rådata 21 november med femårskravet (avsnitt 5). Testen kördes sedan två gånger på samma paneler och gav identiska filer. Jämförelsen mot de äldre skriptens paneler gällde läget före ombyggnaden.

## 2. Genomgång mot författarnas kod

Varje funktion i `lib/ankartest.py` lästes mot motsvarande avsnitt i författarnas kod (`11.docx`).

| Funktion | Kodens avsnitt | Utfall |
|---|---|---|
| `table1` | tabellens not, s. 1734 (kodens avsnitt inte läst i denna körning) | Stämmer med noten |
| `table2` | "Code and Output for Table 2" | **Var fel.** Kolumn 2 till 5 har rå avkastning och ett mått till. Vår kod körde en regression per mått. Rättat. Standardfelen fick också faktorn n/(n-k) som Statas `newey` |
| `fig3`, `_diskret` | "R^2 regressions for Figure 3" | Stämmer |
| `toppfonder`, `fig4` | "Figure 4" | Stämmer |
| `table3` | "Table 3 (Flows to Top-Ranked Funds ...)" | Stämmer. Den andra regressorn (`morn5_e_unad5`) definieras inte i den kod vi har. b1 är densamma hur den än definieras (`test/tabell3_former.py`) |
| `andel_andrad` | "Table 4 ... Panel A" | Stämmer för USA. För Europa 2006 användes månadsmedel och betygsfilen. Nu som i koden: alla fondmånader, fondens föregående rad. 19,0 / 45,8 / 15,3 (var 18,4 / 45,8 / 15,0) |
| `table4b` | "Panel B of Table 4" | Stämmer (vanligt R2, skillnad mellan två regressioner). `reghdfe` tar bort observationer som är ensamma i sin grupp; det gör koden nu också. Berör bara månad x risksiffra: 0,0038 före (var 0,0040) |
| `fig5a` | "Regression for Panel A(b) of Figure 5" | Stämmer |
| `fore_efter` | samma regression, två perioder | Tillagd 20 november på Alexanders begäran. Ankaret räknar inte ut skillnaden själv. USA: -0,102 (0,064). Europa 2006: -0,170 (0,066) |
| `fig5b` | "Test For Figure 5 Panel B" | Formeln stämmer. Det kommande betyget hämtades ur betygsfilen; koden hämtar det ur urvalet i händelsemånaden. Rättat. USA 5 mot 1: 1,82 (var 1,53); 4-5 mot 1-2: 2,64 (var 2,61). Europa 2006: 3,05 (var 3,01); 0,72 (var 0,78) |

Bootstrapintervallet följer artikelns not 24 (s. 1749). Antalet dragningar (10 000) anger ankaret inte.

## 3. Tabell 6 mot Adelino m.fl.

| Del | Adelino m.fl. (s. 3236) | Vi |
|---|---|---|
| Ekvation | Recalibrated x Post, enhetseffekter, delstat x år, storleksdecil x år "in some specifications" | Fall x After, fondeffekter, kategori x månad, volatilitetsdecil x månad i kolumn 2 och 3 |
| Standardfel | klustrade på county | klustrade på fond |
| Händelsefigur | koefficient per händelseår (figur 4, s. 3243) | koefficient per kvartal |
| Per steg | tabell IA.5 (nämnd s. 3242, inte läst) | bilaga A5 |

Winsoriseringen (1/99 inom månad) är ankarets, s. 1733. Huvudtalet blev +0,01 (0,82); med 2,5/97,5 och det större av två standardfel var det +0,07 (0,69).

## 4. Ankarets egna tal

Inskrivna för hand i `tabeller_figurer.py`. Kontrollerade mot den tryckta artikeln och kodens utskrifter i denna körning:

| Tal | Källa | Kontrollerat |
|---|---|---|
| Tabell 1 (27 tal) | tryckt, s. 1734 | Ja |
| Tabell 2, kolumn 1 till 5 | kodens utskrift | Ja |
| Figur 3 (20 tal) | kodens utskrift | Ja |
| Figur 4 | kodens utskrift (`fig4_panela`, `average_all`) | Ja |
| Tabell 3 (60 tal) | tryckt, s. 1744 | Ja |
| Tabell 4 (8 tal) | tryckt, s. 1746, och kodens utskrift | Ja |
| 0,4 till 0,6 procent per stjärna | tryckt, s. 1748 | Ja |

En av er bör ändå läsa dem mot artikeln en gång.

## 5. USA-urvalet mot ankarets

Ankaret byggde inte sitt urval. Analysen görs på Barber, Huang och Odeans (2016) fondmånader: deras tabell 5 har 248 463 observationer i kolumnen med stjärnbetyg, exakt ankarets antal. Artikeln är läst 21 november i SSRN-versionen (18 maj 2016); se `reference/skrivunderlag_2026-11-20/NOTIS_barber_huang_odean_last_urval_och_metod_2026-11-21.md`.

**Rättat 21 november: femårskravet.** De kräver fem års avkastningshistorik för att en fond ska ingå (not 8, avsnitt 2.6). Vi krävde 36 månader. `bygg/usa_panel.py` kräver nu en avkastning 60 månader eller mer före varje beta, och minst 36 observationer i fönstret (ankarets kod).

| | Ankaret | Vi före | Vi nu |
|---|---|---|---|
| Fondmånader / fonder | 248 463 / 3 341 | 233 290 / 2 638 | 193 059 / 2 244 |
| Ålder, 5:e percentil / median (år) | 6,7 / 12,8 | 5,0 / 11,2 | 6,9 / 12,8 |
| Fondstorlek, median (MUSD) | 411 | 307 | 365 |
| Flöde, spridning mellan fonder | 2,18 | 3,81 | 3,41 |
| Stjärnan mot rå avkastning | 0,099 (2,50) | 0,280 (4,46) | 0,217 (3,26) |
| Stjärnan mot CAPM | 0,108 (2,72) | 0,262 (4,29) | 0,181 (2,80) |
| Stjärnan mot FF3 | 0,192 (4,85) | 0,412 (6,68) | 0,327 (5,09) |
| Stjärnan mot FFC | 0,188 (4,73) | 0,346 (5,81) | 0,303 (4,85) |
| Flöde till femstjärniga fonder, % per månad | 1,16 | 2,47 | 2,11 |
| Ändrat betyg före / juni 2002 / efter | 13,9 / 54,2 / 11,9 | 14,7 / 51,7 / 12,5 | 14,0 / 53,0 / 12,1 |
| Betygets förklaringsgrad före / efter | 0,073 / 0,074 | 0,058 / 0,061 | 0,064 / 0,061 |
| Kategori utöver betyg före / efter | 0,022 / 0,014 | 0,017 / 0,011 | 0,023 / 0,013 |
| Händelsetestet, 5 mot 1 | 2,84, över | 1,82, inom | 2,47 [-1,64; 3,11], inom |
| Händelsetestet, 4-5 mot 1-2 | 1,81, över | 2,64, över | 2,96 [-0,67; 0,62], över |
| Flöde per stjärna före / efter, skillnad | | -0,102 (t -1,58) | -0,128 (t -1,96) |

Kvar och inte rättbart med nuvarande data:

1. **Exporten saknar förmögenhet för många andelsklasser:** 38 % av klassmånaderna 1997, 29 % 2002, 22 % 2006, 14 % 2011.
2. **Fondsammanslagningar justeras inte.** De justerar (not 6).
3. **Våra flöden har extrema värden som deras saknar.** Med deras filter (-90 % till 1 000 %) är vår standardavvikelse ungefär 8 % mot deras 2,25 %. Kvartilerna stämmer; skillnaden sitter i den yttersta procenten.

**Europapanelerna fick samma regel 21 november** (`bygg/eu_5_fondpanel.py`, `bygg/eu2006_4_fondpanel.py`).

| | Med 36 månader | Med fem år |
|---|---|---|
| **Europa 2018 till 2025:** första månad | januari 2018 | juni 2019 |
| Fondmånader / fonder | 130 031 / 2 307 | 94 203 / 1 837 |
| Stjärnan mot rå avkastning | -0,076 (-0,97) | -0,081 (-0,88) |
| Stjärnan mot FF3 | 0,121 (1,76) | 0,042 (0,52) |
| Rå avkastning mot FF3 | 0,416 (4,40) | 0,258 (2,33) |
| Risksiffran, tredje signalen (Fama-MacBeth) | 0,61 [-0,67; 1,90] | 1,08 [-0,22; 2,37] |
| Stjärnan i samma regression | 5,53 (t 11,9) | 5,10 (t 11,0) |
| Marginell förklaringsgrad: avkastning / betyg / risksiffra | 1,20 / 0,67 / 0,02 | 1,20 / 0,57 / 0,02 |
| Månad x risksiffra före / efter | 0,0038 / 0,0039 | 0,0040 / 0,0044 |
| **Europa 2006:** första månad | januari 2003 | juni 2004 |
| Fondmånader före bytet | 57 043 | 24 924 |
| Ändrat betyg före / oktober 2006 / efter | 19,0 / 45,8 / 15,3 | 20,3 / 48,0 / 14,6 |
| Betygets förklaringsgrad före / efter | 0,0119 / 0,0100 | 0,0138 / 0,0097 |
| Händelsetestet, 5 mot 1 | 3,05 [-2,54; 2,99], över | 4,91 [-4,45; 4,08], över |
| Händelsetestet, 4-5 mot 1-2 | 0,72 [-2,31; 1,11], inom | 0,89 [-1,97; 0,52], över |
| Flöde per stjärna före / efter, skillnad | -0,170 (t -2,57) | -0,190 (t -2,04) |

Ingen slutsats ändras. Förlusten av perioder beror på att avkastningen i exporterna börjar 2013 respektive 1998. Med månadsavkastning från juli 2011 (2018 till 2025) och från augusti 1996 (2006) kan regeln gälla utan att perioderna kortas. Tabell 6 berörs inte; den bygger på ett annat urval.

## 6. Källan för oktober 2006

Morningstar (2023), "The Morningstar Rating for Funds", bilaga 2, s. 19: den 31 oktober 2006 infördes fem- och tioårsbetyg i Europa, totalbetyget blev ett vägt medel av tre-, fem- och tioårsbetygen, och uppskjutna avgifter och inlösenavgifter började räknas in. Två saker ändrades alltså samma dag. Morningstar ändrade metoden igen 31 oktober 2016. Se `reference/skrivunderlag_2026-11-20/NOTIS_kalla_for_morningstars_metodbyte_i_europa_oktober_2006_2026-11-20.md`.

## 7. Inte kontrollerat

- Panelbyggarna i `bygg/` är inte lästa mot författarnas kod rad för rad i denna körning. De granskades 18 till 20 november (`GRANSKNING_alla_test_mot_artiklarna_2026-11-20`).
- Adelino m.fl.:s kod har vi inte. Artikeln är läst i trycket på s. 3236 till 3237 och 3242 till 3245.
- Barber, Huang och Odean (2016) är läst i SSRN-versionen, inte i trycket. Fama och MacBeth (1973), Cameron, Gelbach och Miller (2011) och Statas manual är inte lästa.
