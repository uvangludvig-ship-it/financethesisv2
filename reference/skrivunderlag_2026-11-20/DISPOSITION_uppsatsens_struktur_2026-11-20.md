# DISPOSITION: hur uppsatsens text bör struktureras (20 november 2026)

*Claude i chatten med Alexander, som bad om det bästa sättet att strukturera texten, med kursens krav kontrollerade och allt underlag läst i sin helhet. Förslag, inte beslut. Inga nya tal är körda. Talen kommer ur de resultatdokument som anges och är körda av AI, inte omkörda av er. Ankaret = Ben-David, Li, Rossi och Song (2022), RFS 35(4).*

## 1. Underlag

Läst i sin helhet för den här frågan:

- **Kursens bilder** (Sabbatucci, 27 sidor): `reference/course_context/course_intro.txt`, kontrollerad mot `source_materials/Introduction_to_research_in_finance_Fall_2026_RS.pdf` (samma 2 124 ord). Bildnummer nedan är de tryckta sidnumren.
- **Kursplanen** (`Syllabus_Fall_2026.pdf`, version 14 augusti 2026), alla avsnitt.
- **Synopsisinstruktionen** (`Synopsis_Fall_2026.pdf`, version 10 augusti 2026), **framsidesmallen** (`front_page.docx`), `requirements_checklist.md`, `CHECKLIST.md`.
- **Cochrane, "Writing Tips for Ph. D. Students"** (8 juni 2005, 13 sidor), som kursplanen avsnitt 7 rekommenderar: https://www.johnhcochrane.com/s/phd_paper_writing.pdf. Tidigare bara läst genom ett sammanfattande verktyg; nu hela texten.
- **Projektets dokument:** `OVERSIKT_alla_test_i_ordning_2026-11-19`, `INVENTERING_git_test_och_datahantering_2026-11-20`, `GRANSKNING_alla_test_mot_artiklarna_2026-11-20`, `NOTIS_ankaret_last_i_sin_helhet_reformtesten_mot_vart_2006_2026-11-20`, `NOTIS_sex_artiklar_lasta_i_sin_helhet_2026-11-20`, `NOTIS_vinnarnas_metodkallor_ett_ankare_2026-11-20`, `BESLUT_mekanism_ar_kanal_2026-11-18`, `RESULTAT_adelino_form_rz_reformform_och_fama_macbeth_2026-11-20`, `RESULTAT_handelsetest_eu_oktober_2006_med_lseg_formogenhet_2026-11-20`.
- **Förebilderna**, lästa i sin helhet tidigare i dag (`MONSTER_*_2026-11-20`): Sabbatuccis sex artiklar, Hartzmark och Sussman (2019), ankarets arbetsversion (2019) och tolv prisvinnare 2019 till 2025. Nu dessutom mätta avsnitt för avsnitt (`claude/struktur_forebilder.py`).

Inte läst av mig: ankarets tryckta version. Dess avsnitt nedan kommer ur `RATTELSE_bendavid_tryckt_version_2026-11-17` och `NOTIS_ankaret_last_i_sin_helhet...`, där en annan session läste den i sin helhet. Canvas-sidorna går inte att nå härifrån.

## 2. Kursens krav på strukturen

| Krav | Källa |
|---|---|
| Sex delar i denna ordning: Introduction, Related Literature, Data and Methodology, Main Empirical Analysis, Interpretation of Empirical Findings / Discussion, Conclusion | Bild 19; kursplanen avsnitt 8 |
| Inledningen 2 till 4 sidor, med styckena bakgrund, fråga, metod, resultat, tolkning. Den ska gå att läsa som en sammanfattning av hela uppsatsen | Bild 19 |
| Litteraturen under en sida: de närmaste artiklarna, hur uppsatsen skiljer sig, bidraget. Ingen översikt | Bild 19; kursplanen avsnitt 7 och 8 |
| Högst 40 sidor, enkelt radavstånd, 12 punkter, tabeller inräknade, bilaga utanför. Huvudtexten 25 till 40 sidor från inledning till slutsats. Längre är inte bättre | Bild 19; kursplanen avsnitt 3, 7 och 8 |
| Så nära en artikel i Journal of Finance som möjligt. Ingen innehållsförteckning | Bild 14 och 18; kursplanen avsnitt 7 |
| Ingen fullständig litteraturgenomgång, inga utvikningar, ingen förklaring av standardmetoder (OLS), ingen bakgrund för nybörjare. Varje avsnitt, stycke och mening har ett syfte | Bild 18 |
| Tabell- och figurtexter som bär sig själva: variabler definierade, typ av teststatistika. Numrerade och med titel | Bild 14; kursplanen avsnitt 8 |
| Data beskrivs och källorna granskas kritiskt. Urvalsskevhet och minsta påvisbara effekt tas upp | Kursplanen avsnitt 8; bild 20 |
| Resultaten jämförs med litteraturen och får en ekonomisk tolkning. Förklara "varför", jaga inte signifikans | Kursplanen avsnitt 8; bild 5 |
| Huvudövningen i en nyckelartikel replikeras, sedan en utvidgning som är mer än ett nytt land | Bild 10 och 17 |
| Slutsatsen kort, utan upprepning, och knuten till frågan | Kursplanen avsnitt 8 |
| Ekvationer på egen centrerad rad; bara de som åberopas numreras. Härledningar i bilaga | Kursplanen avsnitt 8 |
| Referenser: författare och år; alla författare första gången, "et al." sedan vid tre eller fler. Listan börjar på ny sida, heter "References", alfabetisk, JF-stil | Kursplanen avsnitt 8 |
| Alla källor anges, även uppsatser, tabellformat och kod | Bild 25 |
| Framsida enligt mallen: titel, sammanfattning, nyckelord, författare, handledare, examinator | Kursplanen avsnitt 7; `front_page.docx` |
| AI-bilaga obligatorisk | Kursplanen avsnitt 11 |
| En zip med data, kod och README på engelska, senast 7 december 10.00 | Kursplanen avsnitt 9 |

Om referenslistan räknas in i de 40 sidorna står inte. Planera så att den ryms ändå.

## 3. Vad förebilderna gör

Mätt på huvudtexten från inledning till slutsats. Ordantalen för artiklarna innehåller tabelltext och fotnoter (pdftotext), så andelarna är ungefärliga. Vinnarnas texter är rensad löptext.

**Ordning och antal avsnitt** (I inledning, L litteratur, teori eller bakgrund, H hypoteser, D data, M metod, R resultat, B robusthet, X diskussion, C slutsats):

| Text | Ordning |
|---|---|
| Sabbatucci, JF 2020 | I D M R R R C |
| Sabbatucci, RFS 2020 | I D L R B C |
| Sabbatucci, RoF 2025 | I D M R R C |
| Sabbatucci, WP 2022 | I D R R R C |
| Sabbatucci, JoE 2023 | I D M R C |
| Sabbatucci, EL 2023 | I D R R C |
| Hartzmark och Sussman 2019 | I L D R R C (L är "Sustainability Ratings", institutionell bakgrund) |
| Ankaret, arbetsversion 2019 | I H D R R C |
| Ankaret, tryckt 2022 (ur projektets noter) | Inledning, data (2), vad som driver flöden (3.1 till 3.3), tidigare test (4), slutsats, bilaga A och B |
| Vinnare 2019 PH, 2019 SV | I L DM R C |
| Vinnare 2020 PH | I L D R R R R C |
| Vinnare 2020 SV | I L M D R X C |
| Vinnare 2021 PH | I L H D M R X C |
| Vinnare 2021 SV, 2022 PH | I L L L H D R C |
| Vinnare 2022 SV | I L D R B C |
| Vinnare 2023 PH | I L DM R X C |
| Vinnare 2023 SV | I L M DM R B C |
| Vinnare 2024 PH | I DM R X C |
| 2025 (inofficiell) | I L D R B C |

**Andel av orden, median per grupp:**

| Del | Sabbatucci (6) | Toppartiklar (2) | Vinnare (12) |
|---|---|---|---|
| Inledning | 15 % | 20 % | 13 % |
| Eget litteratur- eller teoriavsnitt | 0 % (1 av 6 har bakgrund) | 2 % | 12 % (10 av 12 har ett enligt handkodningen; 11 om "Conceptual Framework" räknas) |
| Data och metod | 23 % | 8 % | 26 % |
| Resultat och robusthet | 52 % | 62 % | 27 % |
| Eget diskussionsavsnitt | 0 av 6 | 0 av 2 | 4 av 12 (20 till 30 % av orden) |
| Slutsats | 5 % | 4 % | 4 % |
| Ord i huvudtexten, median | 12 700 | 11 400 | 9 000 (5 700 till 16 800) |
| Tabeller / figurer i huvudtexten, median | 6,5 / 7,5 | H&S 9 / 6; ankaret tryckt 6 / 8 (ur `RATTELSE_bendavid_tryckt_version_2026-11-17`) | 5 / 3 |

Tre saker syns:

1. **Artiklarna lägger hälften av texten på resultat. Vinnarna lägger en fjärdedel där** och lika mycket på litteratur, teori och hypoteser. Bild 18 beskriver just det som en studentuppsats.
2. **Resultatavsnitten i artiklarna heter efter frågan eller fyndet,** inte "Results". Hartzmark och Sussman: "Do Investors Value Sustainability?" och "Why do investors value sustainability?". Ankaret: "How Do Investors Utilize Morningstar Ratings?". Sabbatucci, WP: "Determinants of Payout Suspension Decisions".
3. **Ingen artikel har ett avsnitt som heter Discussion, Limitations eller Hypotheses** (utom ankarets "The Null Hypothesis" i arbetsversionen). Tolkningen står vid varje resultat.

## 4. Cochrane i korthet (det som rör strukturen)

- Bestäm det enda centrala bidraget och skriv det i ett stycke innan något annat.
- Tidningsstil: det viktigaste först. Inledningen börjar med vad uppsatsen gör och ger faktumet bakom resultatet, inte bara slutsatsen. Högst tre sidor.
- Litteraturen kommer efter bidraget, kort, i eget avsnitt eller avskild. Två eller tre närmaste artiklar.
- Före huvudresultatet ska inget stå som läsaren inte behöver för att förstå det. Inga uppvärmningsövningar, ingen lång databeskrivning, ingen replikering av andras arbete före.
- Efter huvudresultatet: figurer och tabeller som ger intuition, sedan begränsade robusthetstest. Det mesta i bilaga.
- Slutsatsen kort. Ett eller två stycken om gränser och följder går bra.
- Varje tabell har en text som bär sig själv. Regressionstabeller anger ekvationen och vänsterledet. Inget tal i en tabell som inte nämns i texten. Två till tre signifikanta siffror.
- Hänvisningar framåt och bakåt ("as we will see", "recall") tyder på fel ordning.

## 5. Där källorna säger olika, och vad jag föreslår

| Fråga | Kursen | Sabbatuccis egna och toppartiklarna | Cochrane | Förslag |
|---|---|---|---|---|
| Eget litteraturavsnitt | Ja, under en sida (bild 19, kursplan 8) | Nej, litteraturen står sist i inledningen | Efter bidraget, eget avsnitt eller avskilt | **Eget avsnitt 2, högst en sida.** Kursens regel gäller, och den är förenlig med de andra två |
| Eget diskussionsavsnitt | Ja (bild 19, kursplan 8) | Nej, 0 av 8 | Nej | **Eget avsnitt, kort (2 till 3 sidor).** Tolkningen står också vid varje resultat, så avsnittet väger förklaringar mot varandra i stället för att upprepa |
| Replikeringen före huvudresultatet | Replikera nyckelartikelns huvudövning (bild 17) | Det kända resultatet återskapas i samma tabell som det nya (RFS tabell 4, JF tabell II) | Inte före huvudresultatet om läsaren inte behöver det | **Före, men i samma tabeller som det nya.** Läsaren behöver stjärnan: den är måttstocken ("en tredjedel av en stjärna per steg") och den positiva kontrollen för nollresultatet |
| Metodavsnitt | "Data and Methodology" | 3 av 6 har metod- eller modellavsnitt; toppartiklarna inget | Beskriv vad du gör där du gör det | **En kort del C i dataavsnittet** med de tre regressionerna. Detaljerna står vid varje test |
| Färdplan sist i inledningen | Inget krav | 5 av 6 | Behövs inte | Två eller tre meningar, eller ingen. Fritt val |
| Hypotesavsnitt, "Limitations" | Inget krav | Inget | Inget | Inget. Förutsägelsen sägs före varje test, gränsen vid det resultat den gäller |

Rättelse av `MATT_rattningsinstrument_2026-11-20`, avsnitt 3.4: där stod att kursens bilder kräver K05 (inget eget litteraturavsnitt). Det är fel. Bild 19 och kursplanen avsnitt 8 föreskriver ett eget kort avsnitt. Rättat i dokumentet och i `ratta.py`.

## 6. Förslaget

Ett bidrag, i en mening: *spararna i Europa följer Morningstars stjärna men inte EU:s lagstadgade risksiffra, och när siffran byttes för nästan alla fonder i januari 2023 flyttade pengarna högst en tredjedel av vad en stjärna flyttar.* Allt i texten ska tjäna den meningen.

Ordningen är den Alexander valde 19 november: USA-replikering, Europa, risksiffran, bilaga. Oktober 2006 läggs där ankaret har sin reform.

| Nr | Avsnitt (arbetsrubrik) | Sidor | Ord | Vad det ska göra | Tabeller och figurer |
|---|---|---|---|---|---|
| | Framsida enligt mallen. Sammanfattning högst 100 ord (Sabbatucci 41 till 101; Cochrane 100 till 150): säg vad ni finner, ingen litteratur | | | | |
| 1 | Introduction | 3 | 1 500 | Se avsnitt 7 nedan | |
| 2 | Related Literature | 0,8 | 400 | Tre stycken, vart och ett slutar med skillnaden mot er: (a) stjärnor och flöden: ankaret, Reuter och Zitzewitz (2021), Del Guercio och Tkac (2008); (b) hur risk kommer in i flöden: Evans och Sun (2021), Barber, Huang och Odean (2016); (c) andra etiketter som naturliga experiment: Hartzmark och Sussman (2019) | |
| 3 | Data and Methodology | 5,5 | 1 900 | A. De två etiketterna och de tre metodbytena (USA juni 2002, Europa oktober 2006, EU januari 2023): bara det läsaren behöver för testen. B. Data: källor, urval, flödesmåttet, de fyra urvalen i en tabell, avvikelser från ankaret, kritisk granskning av källorna, urvalsskevhet. C. Tre regressioner: ankarets flödesregression, ankarets reformtest, dos gånger efter enligt Adelino, Cunha och Ferreira ekvation 1. Alla variabler definierade | Tabell 1: beskrivande statistik, fyra urval. Figur 1: andel fonder med ändrad etikett per månad kring de tre bytena |
| 4 | Do Flows Follow the Star? | 8 | 2 500 | A. Stjärnan mot avkastningsmåtten, USA 1997 till 2011 och Europa 2018 till 2025 (steg 1 och 3). B. Etiketten eller det den mäter: juni 2002 i USA och oktober 2006 i Europa (steg 2 och 2006-testet). Säg rakt ut att ankarets slutsats inte återges fullt för Europa 2006 | Tabell 2: ankarets tabell 3 med kolumnerna ankaret, vår USA, vår Europa. Figur 2: flöde per stjärna per år. Tabell 3: reformtesten, 2002 och 2006 bredvid varandra. Figur 3: ankarets figur 5B för 2002 och 2006 med jämförelseår |
| 5 | Do Flows Follow the Risk Label? | 9,5 | 3 000 | A. Risksiffran som tredje signal (steg 4, samband, poolat och Fama-MacBeth). B. Bytet i januari 2023: 98,5 % fick ny siffra (steg 5). C. Huvudtestet: fick fonder vars siffra föll mer pengar? Förutsägelse, skattning, minsta påvisbara effekt, förtrend, låtsasbyte, stjärnan i samma regression. D. Robusthet: ett stycke som pekar till bilagan | Tabell 4: tre signaler. Tabell 5: ankarets tabell 4 på januari 2023. Tabell 6: huvudtestet i tre kolumner (enligt `GRANSKNING...`: +0,56, +0,07, +0,47), med stjärnan och MDE. Figur 4: dos gånger kvartal |
| 6 | Interpretation of Empirical Findings | 2,5 | 1 200 | A. Storleken: ett steg mot en stjärna, och i pengar för en medianfond. B. Tre läsningar av nollan och vad varje test säger om dem: siffran når inte spararna; siffran är överflödig när stjärnan finns; testet är för svagt (MDE avgör). Kanal, inte psykologi (`BESLUT_mekanism_ar_kanal`). C. Vad 2006 gör med ankarets slutsats i Europa. D. Mot Hartzmark och Sussman, och vad det betyder för en lagstadgad etikett | |
| 7 | Conclusion | 0,6 | 300 | Svaret på frågan i inledningen. Inga nya tal. Ett stycke om gränser och följder | |
| | **Summa** | **30** | **10 800** | Resultat 51 % av orden, inledning 14 %, litteratur 4 %, data och metod 18 %, tolkning 11 %, slutsats 3 % | 6 tabeller, 4 figurer |
| | References (ny sida) | 2 | | | |
| | Appendix A: övriga resultat. Appendix B: variabler och databygge. Appendix C: AI disclosure | | | | |

30 sidor lämnar tio sidor luft under taket. Använd inte luften. Vinnarnas median är 9 000 ord.

Numrering: JF har inledningen utan rubrik och avsnitten I, II, III med delarna A, B, C (så i Sabbatuccis JF-artikel). Välj den eller arabiska siffror och håll den.

## 7. Inledningens stycken

Bild 19 ger ordningen. Cochrane och Sabbatuccis egna inledningar ger tyngden.

1. **Ett fall läsaren kan se** (högst 120 ord). En fond som den 1 januari 2023 gick från risksiffra 6 till 4 utan att portföljen ändrades, bredvid sin stjärna. Sabbatucci gör så: Costco och Amazon i RFS, Carnival i WP.
2. **Frågan och vad ni gör.** "In this paper, we" inom första halvsidan (hos honom 3 till 27 % in). Ankaret nämnt med författare och år.
3. **Metod och data.** Replikeringen, de fyra urvalen i en mening var, bytet 2023 som test.
4. **Resultaten, numrerade, med tal och enhet.** Stjärnan i USA och Europa. Risksiffran som samband. Huvudtestet med intervall och "högst en tredjedel av en stjärna". Säg nollan rakt ut.
5. **Tolkningen.** Vilken signal bär risken in i flödena. Vad resultatet inte betyder.
6. **Färdplan,** två eller tre meningar, om ni vill ha en.

Litteraturen står inte här utan i avsnitt 2.

## 8. Vad som går till bilagan

Enligt `OVERSIKT_alla_test_i_ordning_2026-11-19` och `INVENTERING...`, avsnitt 2:

- Appendix A: sicksacken och Reuter och Zitzewitz reformform som alternativa former (om de inte står som kolumner i tabell 6), stödtesten till huvudtestet, varianter av replikeringen, tre grupper kring bytet (steg 6, utforskande), UK mot EU, kanaltesten, privat mot institutionell.
- Appendix B: variabeldefinitioner, databygget, avstämning mot SHoF, avvikelserna från ankaret i en tabell (Morningstar Direct i stället för CRSP, tabell 3 i kodens form, dagens avgift och kategori, betor på minst 36 av 60 månader, USD och Developed-faktorer).
- Struket: Cornaggia-formerna, tre kolumner med volatilitet, hopp vid gränserna, instrumentet från 17 november, ankarets figur 5B på januari 2023.

Varje bilagetabell ska nämnas i huvudtexten, annars ska den bort.

## 9. Öppet

1. **Bankägda mot fristående fondbolag.** Inte beslutat. Hör i så fall hemma i avsnitt 6 B som ett kanaltest (når siffran spararen genom rådgivaren?), med en tabell till. Då blir det 7 tabeller.
2. **Huvudform för sista testet.** `GRANSKNING...` föreslår Adelino-formen, vald på härkomst. Inte bekräftat av er.
3. **Artiklar som inte är lästa i tryck** och som avsnitt 2 lutar sig mot: Reuter och Zitzewitz (2021), Del Guercio och Tkac (2008), Adelino m.fl. (`INVENTERING...`, avsnitt 3). Läs innan de citeras.
4. **Talen är inte omkörda av er.** Frys tabellerna ur er egen körning innan resultattexten skrivs.
5. **Titeln.**

## 10. Skrivordning

1. Bidraget i ett stycke (Cochrane, avsnitt 1). Det styr vad som stryks.
2. De tio tabellerna och figurerna, frysta, med fullständiga tabelltexter.
3. Avsnitt 4 och 5 runt dem. Sedan 3, sedan 6.
4. Inledningen, sedan avsnitt 2, slutsatsen och sammanfattningen sist.
5. Rätta varje avsnitt med `ratta.py` och kodbladet.
