# Kontroll av talen

Gjord av AI (Claude) 20 november 2026. Ingen av författarna har kört om något.

## 0. Regel: inget eget test

Varje test i paketet är Ben-David m.fl. (2022) eller Adelino m.fl. (2017), ur artikeln eller författarnas kod. Följande ströks 20 november därför att det saknade förlaga:

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

Panelbyggarna i `bygg/` ger alltså samma paneler som förut.

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

## 5. Inte kontrollerat

- Panelbyggarna i `bygg/` är inte lästa mot författarnas kod rad för rad i denna körning. De granskades 18 till 20 november (`GRANSKNING_alla_test_mot_artiklarna_2026-11-20`).
- Adelino m.fl.:s kod har vi inte. Artikeln är läst i trycket på s. 3236 till 3237 och 3242 till 3245.
- Barber, Huang och Odean (2016), Fama och MacBeth (1973), Cameron, Gelbach och Miller (2011) och Statas manual är inte lästa.
- Morningstars ändring i Europa oktober 2006 saknar primärkälla.
