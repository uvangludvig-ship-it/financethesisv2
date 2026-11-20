# Mått för rättning: kodblad och radskript

20 november 2026. Skriven av Claude. Underlag för rättning av uppsatstext, inte uppsatstext.

## 1. Vad måttet är

Måttet har två lager och tre kontroller.

- **Lager A, kodbladet.** 22 ja/nej-punkter om uppbyggnad och design. En läsare fyller i dem. Varje punkt har en definition och ett riktvärde: hur många av förebilderna som uppfyller den.
- **Lager B, skriptet.** `ratta.py` räknar tolv takter och femton regler på meningsnivå, jämför med riktvärden och skriver ut varje flaggad rad med radnummer.
- **Kontroller i skriptet.** Talkontroll (står talen i sammanfattning, inledning och slutsats också i resultaten, och med samma avrundning), tabellkontroll (bär tabelltexten sig själv) och termkontroll (samma sak med flera namn, blandad stavning).

Stora saker fångas av lager A. Små saker fångas av lager B och kontrollerna.

## 2. Underlag

| Grupp | Antal | Läsning |
|---|---|---|
| Sabbatuccis artiklar | 6 | Lästa i sin helhet |
| Vinnare 2019 till 2025 | 12 | Lästa i sin helhet, alla tolv |
| Toppartiklar | 2 | Lästa i sin helhet: Hartzmark och Sussman (2019), Ben-David m.fl. (arbetsversion 2019) |
| Vinnare 2011 till 2018 | 14 | Bara mätta med skriptet |
| Övriga kandidatuppsatser 2019 till 2025 | 362 | Bara mätta med skriptet |

Kodbladet är ifyllt för de 20 lästa texterna. För Sabbatuccis artiklar är en punkt bara ifylld där min läsanteckning bär den; övriga är markerade "ej kodat". Vinnarna är inte bedömda av Sabbatucci. Nio titelblad anger Adrien d'Avernas som examinator, ett Ramin Baghai (2025), två anger ingen.

## 3. Lager A: kodbladet

### 3.1 Definitioner

En punkt får 1 bara om det som står efter kolon finns i texten.

- **K01 Förlagan på första sidan:** den artikel som replikeras eller utvidgas nämns med författare och år inom inledningens första 450 ord.
- **K02 Frågan utskriven:** inledningen har en mening som slutar med frågetecken, eller en mening av typen "we ask/test/examine whether".
- **K03 Data och metod i inledningen:** inledningen säger datakälla, period och skattningsmetod.
- **K04 Tal i inledningen:** inledningen ger minst ett eget resultat som tal med enhet.
- **K05 Inget litteraturavsnitt:** ingen rubrik för litteratur, tidigare forskning eller teori. Litteraturen står i inledningen.
- **K06 Replikering i samma tabell:** minst en tabell har förlagans skattning (eller den egna replikeringen av den) i en kolumn och det nya i en annan.
- **K07 Förlagans tal bredvid det egna:** minst ett ställe i löptexten ger förlagans tal och det egna i samma stycke.
- **K08 Förutsägelse före resultat:** före huvudresultatet står vilket tecken eller vilken storlek som väntas, och varför.
- **K09 Mekanismen prövas:** minst ett test är byggt för att skilja en förklaring från en annan (delat urval, annan utfallsvariabel, interaktion, tidsfönster). En förklaring som bara berättas efteråt ger 0.
- **K10 Alternativ förklaring prövas:** minst en namngiven invändning möts med ett test eller en kontroll.
- **K11 Placebo:** minst ett test där effekten ska vara noll om tolkningen stämmer.
- **K12 Minsta påvisbara effekt:** texten räknar vilken effekt testet kunde ha upptäckt.
- **K13 Ekonomisk storlek:** huvudresultatet räknas om till en enhet läsaren kan väga (kronor, punkter, andel av medel, förlagans tal).
- **K14 Begränsningar på plats:** minst en begränsning står vid det resultat den gäller, inte bara i ett eget avsnitt eller i slutsatsen.
- **K15 Nollresultat rakt ut:** ett resultat som går emot förutsägelsen eller inte är signifikant sägs så i samma stycke.
- **K16 Inga nya resultat i slutsatsen:** slutsatsen har inga tal som inte står i resultatdelen.
- **K17 Tabelltexter som bär sig själva:** regressionstabellerna säger beroende variabel, variabeldefinitioner, standardfel, stjärnor och urval.
- **K18 Ingen innehållsförteckning.**
- **K19 Ingen läroboksförklaring:** inga stycken som förklarar OLS, effektiva marknader eller andra begrepp ur grundkursen.
- **K20 Färdplan** (beskrivande): ett stycke sist i inledningen säger vad varje avsnitt gör.
- **K21 Numrerade hypoteser** (beskrivande).
- **K22 Anspråk på att vara först** (beskrivande).

### 3.2 Riktvärden

| Nr | Punkt | Sabbatucci | Toppartiklar | Vinnare 2019 till 2025 |
|---|---|---|---|---|
| K01 | Förlagan nämns på inledningens första sida | ej kodat | 1 av 2 | 11 av 12 |
| K02 | Frågan står utskriven, som fråga eller som "we ask/test whether" | ej kodat | 2 av 2 | 9 av 12 |
| K03 | Inledningen säger data och metod | 6 av 6 | 2 av 2 | 12 av 12 |
| K04 | Inledningen ger minst ett eget resultat som tal med enhet | 3 av 6 | 2 av 2 | 11 av 12 |
| K05 | Inget eget litteratur- eller teoriavsnitt | 6 av 6 | 2 av 2 | 2 av 12 |
| K06 | Förlagans resultat återskapas i samma tabell som det nya | 2 av 3 | 1 av 2 | 4 av 12 |
| K07 | Förlagans tal står bredvid det egna i texten | 3 av 3 | 2 av 2 | 8 av 12 |
| K08 | Förutsägelsen sägs före resultatet | 3 av 3 | 2 av 2 | 11 av 12 |
| K09 | Mekanismen prövas med ett eget test | 3 av 3 | 2 av 2 | 9 av 12 |
| K10 | Minst en alternativ förklaring prövas | 1 av 1 | 2 av 2 | 3 av 12 |
| K11 | Placebo eller falsifieringstest | 0 av 6 | 2 av 2 | 2 av 12 |
| K12 | Minsta påvisbara effekt räknas | 0 av 6 | 0 av 2 | 0 av 12 |
| K13 | Storleken sägs i ekonomiska enheter | 4 av 4 | 2 av 2 | 11 av 12 |
| K14 | Begränsningar står där de biter | 2 av 2 | 2 av 2 | 7 av 12 |
| K15 | Nollresultat och motsägande resultat sägs rakt ut | 2 av 2 | 1 av 1 | 10 av 10 |
| K16 | Slutsatsen har inga nya resultat | ej kodat | 2 av 2 | 11 av 12 |
| K17 | Tabelltexterna bär sig själva | 2 av 2 | 2 av 2 | 8 av 12 |
| K18 | Ingen innehållsförteckning | 6 av 6 | 2 av 2 | 10 av 12 |
| K19 | Ingen läroboksförklaring | ej kodat | 2 av 2 | 2 av 12 |
| K20 | Färdplan sist i inledningen | 5 av 6 | 1 av 2 | 7 av 12 |
| K21 | Numrerade hypoteser | 0 av 6 | 0 av 2 | 3 av 12 |
| K22 | Anspråk på att vara först | 4 av 6 | 1 av 2 | 3 av 12 |

### 3.3 Varje text för sig

Kolumnerna är K01 till K19. En punkt betyder ej kodat.

| Text | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | Uppfyllda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2019 PH Tobin's Q and Filing Lag | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 8 av 19 |
| 2019 SV Swedish Value Premium | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 9 av 19 |
| 2020 PH Chasing Your Own Tail | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 13 av 19 |
| 2020 SV Bank Stock Returns | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 16 av 19 |
| 2021 PH In the Eye of a Pandemic | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 10 av 19 |
| 2021 SV Microstructure Invariance | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 13 av 19 |
| 2022 PH Crypto Liquidity | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 11 av 19 |
| 2022 SV Owning the Wave | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | · | 1 | 0 | 1 | 0 | 10 av 18 |
| 2023 PH FOMC Cycle | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 15 av 19 |
| 2023 SV Wealth Inequality | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | · | 1 | 1 | 1 | 0 | 11 av 18 |
| 2024 PH The Smooth Transition | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 12 av 19 |
| 2025 Leading the Wallet (pris 2026 enligt katalogen) | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 13 av 19 |
| Ben-David m.fl. 2019 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | · | 1 | 1 | 1 | 1 | 17 av 18 |
| Hartzmark och Sussman 2019 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 16 av 19 |
| Sabbatucci EL 2023 | · | · | 1 | 0 | 1 | · | · | · | · | · | 0 | 0 | · | · | · | · | · | 1 | · | 3 av 6 |
| Sabbatucci JF 2020 | · | · | 1 | 0 | 1 | 1 | 1 | · | · | · | 0 | 0 | 1 | · | 1 | · | 1 | 1 | · | 8 av 11 |
| Sabbatucci JoE 2023 | · | · | 1 | 0 | 1 | · | · | · | · | · | 0 | 0 | · | · | · | · | · | 1 | · | 3 av 6 |
| Sabbatucci RFS 2020 | · | · | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | · | 1 | 1 | · | 13 av 15 |
| Sabbatucci RoF 2025 | · | · | 1 | 1 | 1 | · | · | 1 | 1 | · | 0 | 0 | 1 | · | · | · | · | 1 | · | 7 av 9 |
| Sabbatucci WP 2022 | · | · | 1 | 1 | 1 | 0 | 1 | 1 | 1 | · | 0 | 0 | 1 | 1 | · | · | · | 1 | · | 9 av 12 |

Vinnarna uppfyller 8 till 16 av 19 punkter, median 11,5. De två toppartiklarna uppfyller 16 och 17. Sabbatuccis RFS-artikel uppfyller 13 av de 15 punkter jag kunde koda.

### 3.4 Läsning

- **Alla förebilder gör det:** K03, K08, K13, K15. Saknas en av dem i utkastet är det ett fel.
- **Sabbatucci och toppartiklarna gör det, vinnarna oftast inte:** K05, K10, K11 (toppartiklarna), K14, K17, K19. Här skiljer sig en artikel från en uppsats. Kursens bilder kräver K17 (bild 14), K18 (bild 14 och 18) och K19 (bild 18). K05 kräver de inte: bild 19 och kursplanen avsnitt 8 föreskriver ett eget avsnitt "Related Literature" under en sida. För uppsatsen läses K05 därför som "litteraturavsnittet är högst en sida och inget teoriavsnitt finns" (rättat 20 november, se `DISPOSITION_uppsatsens_struktur_2026-11-20`).
- **Ingen förebild gör det:** K12. Punkten vilar bara på kursens bild 20. Sabbatucci räknar inte minsta påvisbara effekt i något av de sex. Hartzmark och Sussman säger var styrkan är tunn utan att räkna.
- **Inte en regel:** K04 (tre av Sabbatuccis sex ger inga tal i inledningen), K20, K21, K22.

## 4. Lager B: skriptet

Definitionerna är reguljära uttryck i `matt.py`. Samma kod räknar riktvärdena och rättar utkastet. Takter är träffar per 1 000 ord. Regler är flaggade meningar per 1 000 ord. p-värdet jämför vinnare 2019 till 2025 (12) med övriga uppsatser samma år (362), Mann-Whitney.

### 4.1 Takter

| Mått | Sabbatucci median (min till max) | Toppartiklar | Vinnare median (p25 till p75) | Övriga median | p |
|---|---|---|---|---|---|
| Ord per mening (median, hela meningar) | 24 (17 till 24) | 20 | 22 (21 till 22) | 22 | 0,808 |
| "we/our/us" | 18,21 (11,25 till 19,81) | 12,93 | 19,00 (15,92 till 20,00) | 14,07 | 0,031 |
| Passiva led | 4,79 (3,62 till 9,28) | 9,59 | 9,50 (8,47 till 11,69) | 11,10 | 0,380 |
| Garderingsord | 2,57 (0,58 till 4,36) | 3,26 | 2,56 (1,71 till 3,53) | 4,15 | 0,003 |
| Signifikansord | 3,19 (0,80 till 3,94) | 3,61 | 3,88 (1,46 till 5,54) | 4,63 | 0,204 |
| Kontrastord (however m.fl.) | 1,87 (1,21 till 2,94) | 0,78 | 1,93 (1,26 till 2,22) | 2,53 | 0,008 |
| Kausala uttryck | 1,25 (0,79 till 2,10) | 2,58 | 3,21 (1,94 till 3,46) | 2,60 | 0,430 |
| Förstärkningsord | 2,65 (1,79 till 3,80) | 0,64 | 0,72 (0,47 till 1,01) | 0,87 | 0,337 |
| Tomma fraser | 0,24 (0,00 till 1,17) | 0,43 | 0,95 (0,58 till 1,35) | 0,89 | 0,783 |
| Andel resultatmeningar med tal | 0,21 (0,00 till 0,75) | 0,18 | 0,10 (0,06 till 0,20) | 0,09 | 0,658 |
| Andel signifikansmeningar med storlek | 0,21 (0,00 till 0,33) | 0,34 | 0,12 (0,06 till 0,24) | 0,18 | 0,255 |
| FELSUMMA (tio regler) | 4,22 (3,62 till 6,86) | 5,35 | 8,20 (6,95 till 9,77) | 9,36 | 0,234 |

### 4.2 Regler på meningsnivå

| Regel | Vad som flaggas | Typ | Sabbatucci median (min till max) | Vinnare median (p25 till p75) | Övriga median | p |
|---|---|---|---|---|---|---|
| R01 | Lång mening (över 40 ord) | upplysning | 4,14 (3,52 till 5,13) | 2,46 (1,76 till 3,91) | 2,03 | 0,115 |
| R02 | Två eller fler passiva led i meningen | rätta | 0,54 (0,35 till 0,87) | 0,77 (0,61 till 0,87) | 1,00 | 0,133 |
| R03 | Två eller fler garderingsord i meningen | rätta | 0,25 (0,00 till 0,63) | 0,17 (0,06 till 0,42) | 0,36 | 0,034 |
| R04 | Signifikans utan storlek | rätta | 1,70 (0,80 till 2,60) | 3,06 (0,99 till 4,06) | 3,22 | 0,402 |
| R05 | Nollresultat sagt som "ingen effekt" | rätta | 0,32 (0,00 till 0,63) | 0,31 (0,21 till 0,39) | 0,56 | 0,064 |
| R06 | Överanspråk | rätta | 0,03 (0,00 till 0,23) | 0,11 (0,00 till 0,33) | 0,11 | 0,567 |
| R07 | Kausalt språk | upplysning | 1,22 (0,79 till 2,10) | 3,09 (1,83 till 3,28) | 2,49 | 0,471 |
| R08 | Tom fras | rätta | 0,24 (0,00 till 1,04) | 0,95 (0,58 till 1,30) | 0,85 | 0,795 |
| R09 | Förstärkningsord | upplysning | 2,37 (1,79 till 3,50) | 0,70 (0,47 till 1,01) | 0,84 | 0,363 |
| R10 | Anspråk på att vara först eller unik | rätta | 0,41 (0,11 till 0,80) | 0,33 (0,09 till 0,58) | 0,17 | 0,138 |
| R11 | Meningen börjar med någon annans namn | rätta | 0,32 (0,00 till 0,84) | 1,08 (0,76 till 1,29) | 0,73 | 0,123 |
| R12 | Tankstreck | upplysning | 0,28 (0,00 till 1,61) | 0,00 (0,00 till 0,51) | 0,08 | 0,705 |
| R14 | "This thesis/paper" eller "the authors" i stället för "we" | rätta | 0,34 (0,05 till 1,21) | 0,74 (0,49 till 1,13) | 0,98 | 0,149 |
| R15 | Läroboksförklaring | rätta | 0,09 (0,00 till 0,42) | 0,11 (0,00 till 0,26) | 0,20 | 0,253 |
| R16 | Tabellhänvisning utan tal | upplysning | 1,40 (0,69 till 2,41) | 1,16 (0,67 till 1,41) | 1,47 | 0,210 |

"Rätta" är regler där Sabbatucci ligger lågt eller kursen säger ifrån. "Upplysning" är regler där förebilderna själva ligger högt eller där en läsare måste avgöra: Sabbatucci har fler långa meningar och fler förstärkningsord än uppsatserna, och kausalt språk är rätt när designen bär det.

FELSUMMA är summan av R02, R03, R04, R05, R06, R08, R10, R11, R14 och R15.

### 4.3 Mått på hela texten

| Mått | Sabbatucci (6) | Toppartiklar (2) | Vinnare (12) | Övriga (362) | p |
|---|---|---|---|---|---|
| Innehållsförteckning | 0 av 6 | 0 av 2 | 2 av 12 | 16 % | 1,00 |
| Rubrik för litteratur eller teori | 0 av 6 | 0 av 2 | 9 av 12 | 83 % | 0,44 |
| Ordet placebo eller falsification | 0 av 6 | 2 av 2 | 1 av 12 | 11 % | 1,00 |
| Styrka eller minsta påvisbara effekt nämns | 1 av 6 | 1 av 2 | 1 av 12 | 17 % | 0,70 |
| "Economically significant" eller liknande | 3 av 6 | 1 av 2 | 2 av 12 | 22 % | 1,00 |
| Tal med enhet i sammanfattningen | 2 av 6 | 1 av 2 | 2 av 12 | 17 % | 1,00 |
| Numrerade hypoteser | 1 av 6 | 0 av 2 | 2 av 12 | 33 % | 0,35 |
| Rubriken Limitations | 0 av 6 | 0 av 2 | 1 av 12 | 29 % | 0,19 |
| Ordet replicate | 3 av 6 | 1 av 2 | 6 av 12 | 49 % | 1,00 |
| Frågetecken i textens första 15 procent | 1 av 6 | 2 av 2 | 9 av 12 | 65 % | 0,55 |
| Färdplansfras | 6 av 6 | 1 av 2 | 6 av 12 | 35 % | 0,36 |
| Konfidensintervall nämns | 0 av 6 | 2 av 2 | 3 av 12 | 17 % | 0,44 |
| Klustrade standardfel nämns | 3 av 6 | 2 av 2 | 5 av 12 | 45 % | 1,00 |
| Rubriken Future research | 0 av 6 | 0 av 2 | 2 av 12 | 17 % | 1,00 |

Sammanfattningen hittades bara i tre av Sabbatuccis sex filer, så den raden vilar på tre artiklar.

## 5. Kontrollerna

- **Talkontroll.** Skriptet tar varje tal med enhet eller decimaler i sammanfattning, inledning och slutsats och söker samma tal i resten av texten. Utfall: "ja", "avrundat från" (med kandidaterna) eller "SAKNAS". Sabbatuccis egna tryckta artiklar har två sådana fel (RoF: 2 till 4 procent i sammanfattningen, 2 till 5 i slutsatsen; WP: 38 procent i inledningen, 39 i avsnitt 4).
- **Tabellkontroll.** För varje tabelltext: ord, och vilka av fem delar som saknas (urval och period, beroende variabel, standardfel, stjärnor, variabeldefinitioner). Förlaga: JF tabell II och RFS tabell 4. Skriptet listar också tabeller som nämns men saknar text, och tabeller som aldrig nämns.
- **Termkontroll.** Grupper av ord för samma sak, till exempel "risk indicator", "risk label", "risk class". Två varianter med minst två träffar var flaggas. Egna grupper ges med `--termer`.

## 6. Körning

```
python3 ratta.py utkast.md --forlaga "Ben-David" --ut rapport.md
python3 ratta.py utkast.md --max 0            # alla rader, inte bara de 25 första per regel
python3 ratta.py utkast.md --termer termer.json
```

Filerna `ratta.py`, `matt.py` och `riktvarden.json` ska ligga i samma mapp. Utkastet ska vara text eller markdown med rubrikerna Abstract, Introduction och Conclusion. Riktvärdena räknas om med `riktvarden.py`.

## 7. Vad måttet visar och inte visar

1. **Det skiljer artiklar från uppsatser.** FELSUMMA är 4,2 i median för Sabbatucci, 5,4 för toppartiklarna, 8,2 för vinnarna och 9,4 för övriga uppsatser. Artiklar mot uppsatser: p under 0,001 (8 mot 374).
2. **Det skiljer inte säkert vinnare från andra uppsatser.** FELSUMMA: p 0,23. Av 45 mått har fyra p under 0,05: garderingsord, kontrastord, "we" och R03. Två väntas av slumpen.
3. **Kodbladet är inte prövat mot uppsatser som inte vann.** De är inte lästa. Riktvärdena säger vad förebilderna gör, inte vad som ger pris.
4. **Automatiken mot handkodningen, 14 texter:** innehållsförteckning 14 av 14 rätt, litteraturrubrik 13, färdplan 13, placebo 13, numrerade hypoteser 11. "Styrka nämns" är inte samma sak som K12: två texter nämner styrka utan att räkna.
5. **Passiv form och meningslängd är ungefärliga.** Uttrycket för passiv fångar inte oregelbundna verb fullt ut. Meningslängden är medianen bland hela meningar.
6. **Frågan och designen bedöms inte.** Om frågan är intressant oavsett utfall (kursbild 24) kan inget av lagren säga.

## 8. Prov på egen text

Körd på ett utdrag ur `THESIS_DRAFT_V8_2026-11-12` (den äldre designen): sammanfattning, inledning, delar av 4.3 och slutsats, 1 938 ord. Det aktuella utkastet har jag inte haft.

| | Utdraget | Riktvärde |
|---|---|---|
| FELSUMMA | 2,6 | Sabbatucci 3,6 till 6,9 |
| Passiva led | 5,7 | Sabbatucci 3,6 till 9,3 |
| Sammanfattning, ord | 110 | Sabbatucci 41 till 101 |
| Inledning, ord | 1 314 | 900 till 1 800 |
| Första resultatmeningen | 45 % in | Sabbatucci 13 till 81 % |
| Färdplan i inledningen | ja | 5 av 6 Sabbatucci, 7 av 12 vinnare |

Flaggade rader: tre meningar med två passiva led (rad 25, 27, 49), en mening som säger att ingen effekt kan fastställas utan att ge vad som kan uteslutas (rad 19), en mening som börjar med Greenwood och Sammon (rad 9). Talkontrollen: alla tio tal i sammanfattningen utom 2,6 och 0,37 finns i resten, avrundade från två decimaler till en; 2,2 har två kandidater (2,15 och 2,22), och bara den ena är rätt storhet. Tabell 14 saknar urval och period i texten.

Provet visar att skriptet går på er markdown och vad det ger. Det är inte en rättning av uppsatsen.

## 9. Källor

- Sabbatuccis sex artiklar: `claude/MONSTER_sabbatucci_sex_artiklar_2026-11-20.md`.
- Vinnarna: `reference/old_winners/` och `reference/non_winners/text/6338.txt` i repot `financethesisv2`; `claude/MONSTER_prisvinnare_kandidat_2026-11-20.md`.
- Toppartiklarna: `claude/MONSTER_toppartiklar_finans_2026-11-20.md`.
- Kursens bilder: `reference/course_context/course_intro.txt` (bild 5, 14, 16, 18, 19, 20, 24).
- Kod och data i projektet: `claude/ratta.py`, `claude/matt.py`, `claude/riktvarden.py`, `claude/riktvarden.json`, `claude/kodning_forebilder.jsonl`.
