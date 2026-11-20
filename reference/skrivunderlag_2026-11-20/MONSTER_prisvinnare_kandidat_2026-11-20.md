# Mönster i SSE:s prisvinnande kandidatuppsatser i finans

20 november 2026, andra versionen samma dag. Skriven av Claude. Underlag för rättning av uppsatstext, inte uppsatstext.

Den första versionen byggde på två uppsatser lästa i sin helhet och inledningarna i resten. Den här bygger på alla tolv vinnare 2019 till 2025, lästa från första till sista stycket och kodade på samma blad. Där versionerna skiljer sig gäller den här.

## 1. Vad som lästes

| År | Pris | Titel (kort) | Förlaga | Examinator enligt titelbladet |
|---|---|---|---|---|
| 2019 | Per Hiller | Tobin's Q and Filing Lag | ingen enskild (Lindenberg och Ross 1981, Spence 1973) | Adrien d'Avernas |
| 2019 | Staffan Viotti | The Swedish Value Premium and Disasters | Petkova och Zhang (2005), Bai m.fl. (2019) | anges inte |
| 2020 | Per Hiller | Chasing Your Own Tail | Tuzun (2014), Kyle och Obizhaeva (2012) | Adrien d'Avernas |
| 2020 | Staffan Viotti | Bank Stock Returns and Monetary Policy Surprises | English m.fl. (2018) | anges inte (handledare d'Avernas och Romei) |
| 2021 | Per Hiller | In the Eye of a Pandemic | Busse och Green (2002) | Adrien d'Avernas |
| 2021 | Staffan Viotti | Market Microstructure Invariance | Kyle och Obizhaeva (2017, 2019) | Adrien d'Avernas |
| 2022 | Per Hiller | Predicting Liquidity in the Cryptocurrency Market | Kyle och Obizhaeva (2016, 2017) | Adrien d'Avernas |
| 2022 | Staffan Viotti | Owning the Wave | Baek, Kang och Park (2004) | Adrien d'Avernas |
| 2023 | Per Hiller | Changing Patterns over the FOMC Cycle | Cieslak, Morse och Vissing-Jorgensen (2019) | Adrien d'Avernas |
| 2023 | Staffan Viotti | The Drivers of Wealth Inequality | Gabaix, Lasry, Lions och Moll (2016) | Adrien d'Avernas |
| 2024 | Per Hiller | The Smooth Transition | Ahern och Dittmar (2012) | Adrien d'Avernas |
| 2025 | pris 2026 enligt katalogen | Leading the Wallet | Guiso och Zaccaria (2023) | Ramin Baghai |

Källor: `reference/old_winners/text/` och `reference/non_winners/text/6338.txt` i repot `financethesisv2`. Vinnaren 2025 är markerad i repots `INDEX.md` som belönad 2026 enligt katalogen; den är inte bekräftad på annat sätt.

Läst: all löptext, alla tabell- och figurtexter. Inte läst: siffrorna i tabellcellerna, referenslistorna, bilagorna i 2021 PH och 2025. Vinnarna 2011 till 2018 är mätta med skriptet men inte lästa.

**Förbehåll om examinator.** Ingen av de tolv är bedömd av Riccardo Sabbatucci. Nio titelblad anger Adrien d'Avernas, ett Ramin Baghai, två anger ingen. I höst sätter Sabbatucci betyget (kursens bild 16). Vinnarna visar vad som belönades under andra examinatorer. Där vinnarna och kursens bilder går isär gäller bilderna.

## 2. Kodbladet

Varje uppsats är kodad på 19 ja/nej-punkter. Definitionerna står i `claude/MATT_rattningsinstrument_2026-11-20.md`, avsnitt 3. Varje rad i `claude/kodning_forebilder.jsonl` har en anteckning om vad koden vilar på.

| Punkt | Vinnare som uppfyller den |
|---|---|
| K03 Inledningen säger data och metod | 12 av 12 |
| K01 Förlagan nämns på inledningens första sida | 11 av 12 |
| K04 Minst ett eget resultat som tal i inledningen | 11 av 12 |
| K08 Förutsägelsen sägs före resultatet | 11 av 12 |
| K13 Storleken sägs i ekonomiska enheter | 11 av 12 |
| K16 Slutsatsen har inga nya resultat | 11 av 12 |
| K15 Motsägande resultat sägs rakt ut | 10 av 10 kodade |
| K18 Ingen innehållsförteckning | 10 av 12 |
| K02 Frågan står utskriven | 9 av 12 |
| K09 Mekanismen prövas med ett eget test | 9 av 12 |
| K07 Förlagans tal bredvid det egna | 8 av 12 |
| K17 Tabelltexterna bär sig själva | 8 av 12 |
| K14 Begränsningar står där de biter | 7 av 12 |
| K06 Replikering i samma tabell som det nya | 4 av 12 |
| K10 Alternativ förklaring prövas | 3 av 12 |
| K05 Inget eget litteratur- eller teoriavsnitt | 2 av 12 |
| K11 Placebo | 2 av 12 |
| K19 Ingen läroboksförklaring | 2 av 12 |
| K12 Minsta påvisbara effekt räknas | 0 av 12 |

Per uppsats: 8 till 16 uppfyllda av 19, median 11,5. Högst ligger 2020 SV (16) och 2023 PH (15). Lägst ligger de två från 2019 (8 och 9).

## 3. Elva mönster, med var de syns

1. **Förlagan sägs rakt ut och tidigt.** 2020 SV skriver i inledningens fjärde stycke att uppsatsen replikerar English m.fl. (2018) med ändringar och förlänger den med 2012 till 2019. 2021 PH nämner Busse och Green (2002) i första stycket. 2025 kallar sin modell en utvidgning av Guiso och Zaccaria (2023). 2024 nämner Ahern och Dittmar (2012) i sammanfattningens andra mening. 2023 PH skriver att de följer Cieslak m.fl. (2019) i metod och datakällor så nära som möjligt.

2. **Utvidgningen är ett läge där en namngiven sak skiljer sig, så att förlagans förklaring kan prövas.** 2024: Frankrike gav sex år och mild sanktion, Norge två år och upplösning, och då går det att fråga om det var kvoten eller brådskan som sänkte värdet. 2023 PH: tre numrerade skäl till att perioden efter 2016 skiljer sig, alla hämtade ur förlagans egen förklaring. 2020 SV: räntan vid nollgränsen efter 2008. Där marknaden är ny får det ett skäl: 2021 SV skriver att teorin ska gälla på alla marknader och prövar det, 2020 PH att en enda utgivare gör mätningen renare än i USA.

3. **Avvikelsen från förlagan sägs tillsammans med vad den kostar.** 2020 SV har dagsdata där förlagan har intradagsdata, och skriver att en fjärdedel av förklaringsgraden blir kvar (resultatdelen, efter tabell I a). 2021 PH går i dataavsnittet igenom varje skillnad mot förlagans data och säger hur idealdata hade sett ut. 2021 SV har ett eget underavsnitt om databegränsningar (5.1.1).

4. **Förlagans tal ställs bredvid det egna.** 2020 PH: 89 miljoner kronor i ombalansering per procent indexrörelse mot Tuzuns 1,04 miljarder dollar. 2020 SV: egen förklaringsgrad mot förlagans 0,099 till 0,103. 2021 SV: den egna lutningen mot Kyle och Obizhaevas för ryska aktier. 2023 PH tabell I: 1994 till 2016 återskapat i kolumn 1 (14 och 11 punkter), 2017 till 2022 i kolumn 2 (−17 och −5). 2024: egen skillnad 0,83 procent mot förlagans 3,56.

5. **Varje koefficient räknas om till en storlek, och räkningen visas.** 2020 PH: 1,499 gånger 1 procent gånger 2,7 procent ger 4,0 punkter (avsnitt 5.1), och samma räkning görs för varje test. 2020 SV: en överraskning på 25 punkter ger 1 till 1,2 procents kursfall före krisen och 3 till 3,5 procents uppgång efter.

6. **Förutsägelsen kommer före resultatet.** 2021 PH har sex numrerade hypoteser, var och en följd av de artiklar den vilar på (avsnitt 3). 2021 SV gör förutsägelsen till ett tal: lutningen ska vara 1, och testet är om konfidensintervallet 0,971 till 1,005 innehåller det.

7. **Resultat som går emot sägs rakt ut, och ett nollresultat får bära uppsatsen.** 2021 PH skriver "This goes against our hypothesis" om branschtestet. 2020 SV pekar själv ut att en koefficient byter tecken mellan två tabeller och kallar slutsatserna därifrån "highly tentative". 2021 SV redovisar att årsvisa regressioner förkastar hypotesen som helheten inte förkastar. 2025 skriver att utbildningens tecken går emot den egna modellen. 2024 års titel och slutsats vilar på tre koefficienter som inte skiljer sig från noll. 2023 PH visar att ett känt mönster har försvunnit.

8. **Förklaringar skiljs åt med ett eget test, ofta ur den institutionella miljön.** 2020 PH: en enda utgivare och ett känt handelsfönster gör att direkt effekt kan skiljas från handel i förväg. 2021 PH: samma klockslag 2019 är kontrafaktum. 2020 SV: en dummy för besked om kvantitativa lättnader samma dag. 2024: amerikanska bolag som kontroll i händelsestudien och som placebo i instrumentregressionen (tabell 7), och styrelsens kompetens som eget utfall. 2023 PH: styrelsemöte gånger räntehöjningsår (tabell II) och VIX över cykeln för att ställa läckor mot riskpremie.

9. **Egen datainsamling.** 2021 PH såg alla 36 presskonferenser och klockade delarna. 2020 PH fick fonddata från utgivaren och byggde om indexet minut för minut. 2021 SV bearbetade 375 miljoner rader. 2020 SV fick förlagans banklista av författarna.

10. **Bidraget räknas upp.** Nio av tolv räknar upp två till fyra bidrag i inledningen eller i ett eget stycke.

11. **Slutsatsen upprepar, den lägger inte till.** Elva av tolv har inga nya tal i slutsatsen. Undantaget är 2019 SV.

## 4. Där vinnarna bryter mot kursens bilder

Det här ska inte kopieras.

- **Eget litteratur- eller teoriavsnitt:** tio av tolv. 2021 SV har omkring sex sidor teori som härleder förlagan på nytt. 2021 PH har omkring tre sidor litteratur. Bild 19: litteraturen under en sida.
- **Läroboksförklaringar:** tio av tolv. 2021 SV förklarar vad en regression och en spread är. 2023 PH och 2024 förklarar FOMC, VIX och ROE. Bild 18: ingen pedagogisk förklaring.
- **Ingen räknar minsta påvisbara effekt.** 2020 PH skyller två nollresultat på kort urval utan att räkna vad testet kunde ha sett. 2021 SV tolkar att hypotesen inte förkastas som att den bekräftas. 2024 drar en nollslutsats på 89 till 93 bolag utan styrkeberäkning. Bild 20.
- **Signifikans utan storlek.** 2021 PH redovisar resultaten nästan bara som signifikansnivåer. Bild 5.
- **Tunna tabelltexter:** fyra av tolv (2024 PH, 2022 SV, 2021 PH, 2019 PH). 2024 års regressionstabeller 6 till 14 har bara en stjärnförklaring som not. Bild 14: tabelltexten ska räcka för att förstå tabellen.
- **Längd:** 2025 är 72 sidor. Bild 19: högst 40.
- **Förklaringar som berättas men inte prövas.** 2021 PH lägger beteendeteorier på resultaten i efterhand. 2020 SV har ett långt tolkningsavsnitt med "could".
- **Många test utan justering.** 2025 har tjugo tabeller i huvudtexten och läser små signifikanta koefficienter en och en. Ett resultat vilar på 5 000 hushåll i tre länder.
- **Enstaka fel.** 2019 SV kallar t = −1,47 signifikant. 2022 SV skriver 203 punkter och 0,203 procent om samma tal. Två uppsatser har innehållsförteckning (båda 2019; bild 14 och 18).

## 5. Mätning

Riktvärdena för takter och regler står i `claude/MATT_rattningsinstrument_2026-11-20.md`, avsnitt 4. Tre saker därifrån:

- Vinnarna har färre garderingsord (2,6 mot 4,2 per 1 000 ord, p 0,003), färre kontrastord (1,9 mot 2,5, p 0,008) och fler "we" (19,0 mot 14,1, p 0,031) än övriga uppsatser 2019 till 2025. De har också färre meningar med två garderingsord (regel R03, p 0,034).
- På 41 andra mått syns ingen säker skillnad. Ytstilen skiljer inte vinnare från andra.
- Mot Sabbatuccis artiklar ligger vinnarna dubbelt så högt i flaggade meningar (8,2 mot 4,2 per 1 000 ord).

Siffrorna i den första versionens tabell kom från ett äldre skript med andra definitioner. De gäller inte längre som riktvärden.

## 6. Källor

Repot `financethesisv2`: `reference/old_winners/text/*.txt`, `reference/non_winners/text/6338.txt`, `reference/non_winners/INDEX.md`, `reference/course_context/course_intro.txt` (bild 5, 14, 16, 18, 19, 20). Original: https://arc.hhs.se/download.aspx?MediumId=6053 (2024), https://arc.hhs.se/download.aspx?MediumId=5734 (2023 Per Hiller), https://arc.hhs.se/download.aspx?MediumId=6338 (2025). Kodning: `claude/kodning_forebilder.jsonl`.
