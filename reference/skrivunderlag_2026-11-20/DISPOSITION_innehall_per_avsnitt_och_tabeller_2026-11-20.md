# DISPOSITION, del 2: har andra ett litteraturavsnitt, och vad som ska stå i varje avsnitt (20 november 2026)

*Claude i chatten med Alexander, som frågade om andra verkligen har "Related Literature" och bad om innehållet i varje avsnitt med våra egna tabeller. Fortsättning på `DISPOSITION_uppsatsens_struktur_2026-11-20`. Förslag, inte beslut. Alla tal är körda av AI och inte omkörda av er.*

## 1. Har andra ett eget litteraturavsnitt?

| Grupp | Eget avsnitt | Var litteraturen står, och hur lång den är |
|---|---|---|
| Sabbatuccis sex artiklar | 0 av 6 | Sist i inledningen. 400 till 1 100 ord i de fyra långa (JF, RFS, RoF, WP); 0 och cirka 100 i de två korta |
| Hartzmark och Sussman (2019) | Nej | Fyra stycken sist i inledningen, cirka 640 ord. De börjar "Our paper contributes to the literature..." |
| Ankaret, arbetsversion 2019 | Nej | Invävd från första sidan, eftersom artikeln svarar på två namngivna artiklar |
| Vinnare 2019 till 2025 | 10 av 12 | Median 12 % av orden, cirka 1 000 ord. Kortast: 2023 SV "Related Works" 429 ord, 2022 PH 452, 2021 SV 510 |
| Uppsatser Sabbatucci har handlett, 2018 till 2023 | 16 av 20 har rubriken: 12 som eget avsnitt, 4 som underavsnitt (två av dem inne i inledningen: 5251 "1.2 Related Literature...", 5883 "1.1 Background and Related Literature"). 4 saknar den | Median cirka 750 ord i de elva som gick att mäta (345 till 2 400) |
| Alla finansuppsatser 2024 / 2025 / 2026 | 72 % / 67 % / 66 % har en rubrik med ordet literature, related work eller previous research | Median 660 / 850 / 510 ord där avsnittet gick att mäta |

Ingen uppsats i arkivet har Sabbatucci som examinator. Titelbladen 2024 anger d'Avernas eller Baghai, 2025 och 2026 Baghai. Hur han bedömer valet går alltså inte att se i gamla uppsatser.

**Svar:** artiklarna har det inte. Uppsatserna har det oftast, och nästan alltid längre än en sida. Kravet kommer ur två texter:

- Bild 19 (`course_intro.txt`): under rubriken om att ligga så nära en publicerad artikel som möjligt står en lista: Introduction (2 till 4 sidor), Related Literature (under 1 sida), Data and Methodology, Main Empirical Analysis, Interpretation of Empirical Findings / Discussion, Conclusion.
- Kursplanen avsnitt 8 (version 14 augusti 2026): inledningen följs av "a section with a focused presentation of the relevant literature".

Innehållet som bild 19 beskriver (närmaste artiklar, hur uppsatsen skiljer sig, bidraget) är precis det som artiklarna har i sina sista inledningsstycken. Skillnaden är bara rubriken.

**Förslag, oförändrat men nu med skälet utskrivet:** eget avsnitt 2, högst 400 ord, tre stycken. Skrivet som artiklarnas slutstycken, inte som uppsatsernas genomgångar. Det följer bådas ordalydelse och kostar en rubrik. Vill ni hellre göra som hans egna artiklar flyttas samma tre stycken till inledningens slut. Texten är densamma. En fråga till Sabbatucci avgör saken.

Förlaga för formen: vinnaren 2023 SV, "Related Works" (429 ord). Tre stycken, ett per närmaste artikel, vart och ett slutar med vad uppsatsen gör annorlunda. Motexempel: den handledda uppsatsen 5728 (2023), "Related Literature", 536 ord, som räknar upp ett fält och säger bidraget först i sista meningen.

Metod för räkningen: rubriker sökta i `reference/non_winners/text/*.txt` och `reference/old_winners/text/*.txt` med uttrycket D02 i `matt.py`, snävat till literature, related work(s), previous eller prior research. Handledda uppsatser: de 20 filer som nämner Sabbatucci på titelbladet (MediumId 3966, 4113, 4119, 4132, 4148, 5237, 5245, 5251, 5277, 5315, 5661, 5667, 5704, 5708, 5728, 5871, 5872, 5879, 5883, 5887). Ordantalen är ungefärliga (pdftotext).

## 2. Tabeller och figurer i huvudtexten: vad som finns och vad som saknas

| Nr | Innehåll | Tal som redan finns | Källa | Saknas |
|---|---|---|---|---|
| Tabell 1 | Beskrivande statistik, fyra urval | Panel A, USA 1997 till 2011 bredvid ankarets tabell 1: 233 290 fondmånader, 2 638 fonder; flöde −0,21 (spridning 3,81) mot −0,54 (2,18) | `RESULTAT_replikering_bendavid_usa_1997_2011_2026-11-18`, "Table 1" | Panel B Europa 2018 till 2025 (130 031 fondmånader, 2 307 fonder), panel C Europa 2003 till 2010 (159 040 i huvudtestet), panel D bytet 2023 (4 818 fonder, 230 531 fondmånader): bara antalen finns |
| Figur 1 | Andel fonder med ändrad etikett per månad, tre paneler | USA juni 2002: 14,7 / 51,7 / 12,5 %. Europa oktober 2006: 18,4 / 45,8 / 15,0 %. Risksiffran januari 2023: 2,1 / 98,5 / 1,8 % | Samma; `RESULTAT_handelsetest_eu_oktober_2006_med_lseg_formogenhet_2026-11-20`; `RESULTAT_bendavids_handelsetest_januari_2023_2026-11-19` | Figuren |
| Tabell 2 | Stjärnan mot avkastningsmåtten (ankarets tabell 3 och figur 3). Kolumner: ankaret, vår USA, vår Europa | Stjärna mot rå: 0,099 (2,50) / +0,280 (4,46) / −0,076 (−0,97). Mot CAPM: 0,108 (2,72) / +0,262 (4,29) / −0,091 (−1,18). Mot FF3: 0,192 (4,85) / +0,412 (6,68) / +0,121 (1,76). Mot FFC: 0,188 (4,73) / +0,346 (5,81) / +0,120 (1,68). Rå mot CAPM: 0,032 (0,62) / −0,054 (−0,66) / −0,066 (−0,52). Rå mot FF3: 0,207 (4,74) / +0,211 (2,97) / +0,416 (4,40). Panel B, marginell förklaringsgrad betyg / avkastning: 6,5 / 5,6; 5,0 / 2,4; 0,6 / 1,2 | USA-dokumentet; `RESULTAT_omkorning_full2_ny_B2_2026-11-19`, avsnitt 2 | Inget |
| Figur 2 | Flöde per stjärna per år (ankarets figur 5A(b)) | USA 1997 till 2011: 0,61 till 0,90. Europa 2003 till 2016: 0,41 till 0,71 (2016: 0,11). Europa 2018 till 2025: 0,22 till 0,67. Ankaret: 0,4 till 0,6 | Samma tre dokument | Figuren |
| Tabell 3 | Metodbytena. Panel A, juni 2002, ankaret bredvid oss. Panel B, oktober 2006. Panel C, höll sambandet? | A: förklaringsgrad månad gånger betyg 0,073 / 0,074 mot 0,058 / 0,061; kategori 0,043 / 0,015 mot 0,029 / 0,015. B: 0,0119 till 0,0100; fonder minst fem år 0,0135 till 0,0098; tre till fem år 0,0209 till 0,0223. C: flöde per stjärna, äldre fonder +0,606 till +0,429, yngre +0,623 till +0,689; b4 −0,180 (t −1,31); Fama-MacBeth −0,319 (t −3,46) | USA-dokumentet; 2006-dokumentet, körning A och B | Inget. Inga kategorirader i panel B (`NOTIS_ankaret_last_i_sin_helhet...`, avsnitt 6) |
| Figur 3 | Ankarets figur 5B: gapet per år med jämförelseår | USA 2002: +2,61 mot [−1,04; +0,71]. Europa 2006: +0,78 mot [−2,30; +1,11], rang 1 av 14; fonder minst fem år +0,70 mot [−3,36; +0,65] | USA-dokumentet; 2006-dokumentet, test 4 | Figuren |
| Tabell 4 | Risksiffran som tredje signal | Fama-MacBeth +0,61 (SE 0,66), stjärnan +5,53 (t 11,9). Poolad +0,80 (0,98). Inom kategori −0,34 (0,93). SRRI-åren +0,59 (0,99), SRI-åren +0,65 (0,55). Marginell förklaringsgrad avkastning / betyg / risksiffra: 1,20 / 0,67 / 0,02. 66 365 fondmånader, 1 142 fonder | `RESULTAT_adelino_form_rz_reformform_och_fama_macbeth_2026-11-20`, avsnitt 3; omkörningen, avsnitt 3 | Inget |
| Tabell 5 | Januari 2023 i ankarets tabell 4-form | Förklaringsgrad månad gånger risksiffra 0,0040 till 0,0039; månad gånger betyg 0,0108 till 0,0141; risksiffra utöver betyg 0,0038 till 0,0033 | Omkörningen, avsnitt 4 | Inget. Kategoriraderna stryks (`GRANSKNING...`, steg 5) |
| Tabell 6 | Huvudtestet, dos gånger efter | (1) +0,56 (0,67). (2) huvud +0,07 (0,69), intervall −1,29 till +1,42, MDE 1,9. (3) sicksacken +0,47 (0,52). Stjärnan i samma regression +5,29 (0,56), då dos gånger efter −0,39 (0,71). Låtsasbyte januari 2021 +0,07 (0,86). 4 818 fonder, 230 531 fondmånader | Adelino-dokumentet, avsnitt 1; `GRANSKNING...`, steg 7 | Uppställningen med stjärnan och låtsasbytet som egna kolumner |
| Figur 4 | Dos gånger kvartal, 2021 kv 1 till 2024 kv 4, bas 2022 kv 4 | 15 koefficienter; före p 0,587, efter p 0,487 | Adelino-dokumentet, V1 | Figuren |

Fem saker måste alltså byggas: tabell 1 panel B till D, och figur 1 till 4. Allt annat finns som tal.

Ur ankaret replikerar ni avsnitt 3 (3.1 till 3.3). Avsnitt 4 (teckentestet och avkastningsuppdelningen, tabell 5 och 6) replikeras inte. Det ska stå i texten.

## 3. Avsnitt för avsnitt

### Sammanfattning (högst 100 ord)

Fyra meningar: frågan; vad ni gör (replikering, Europa, bytet 2023); de två fynden med ett tal var (stjärnan +5,3 procentenheter per år och stjärna; risksiffran +0,07 per steg, högst en tredjedel av en stjärna); vad det betyder. Ingen litteratur.

### 1. Introduction (3 sidor, 1 500 ord, inga tabeller)

1. **Fallet.** Varje fond som säljs till privatsparare i EU bär två etiketter: Morningstars stjärnor och den lagstadgade risksiffran 1 till 7. Den 1 januari 2023 fick 98,5 % av fonderna ny siffra utan att portföljen ändrades.
2. **Frågan och vad ni gör.** Vilken etikett flyttar pengarna? "In this paper, we..." här. Ankaret nämnt med författare och år.
3. **Metod och data.** Ankarets avsnitt 3 replikerat på amerikanska fonder 1997 till 2011 ur Morningstar Direct. Samma test på 2 307 europeiska aktiefonder 2018 till 2025. Morningstars europeiska metodbyte oktober 2006. Bytet av risksiffra 2023 på 4 818 fonder, i Adelino, Cunha och Ferreiras form.
4. **Resultaten, numrerade.** (i) USA: femstjärniga fonder drar 0,28 % mer per månad än fonder med lika bra avkastning (ankaret 0,10), och juni 2002 återges. (ii) Europa: en stjärna är värd 0,2 till 0,7 % i månadsflöde varje år, men stjärnan slår inte rå avkastning (−0,08, t −0,97), och efter oktober 2006 föll flödet per stjärna från 0,61 till 0,43 för de fonder vars formel ändrades. (iii) Risksiffran: inget samband utöver stjärnan (+0,6 procentenheter per år, SE 0,7, mot stjärnans +5,5), och fonder vars siffra föll mer fick inte mer pengar (+0,07 per steg, intervall −1,3 till +1,4).
5. **Tolkningen.** Risk når flödena genom stjärnan, inte genom den lagstadgade siffran. Vad det inte visar: varför.
6. **Färdplan,** två eller tre meningar, om ni vill.

### 2. Related Literature (0,8 sida, 400 ord, inga tabeller)

1. **Stjärnor och flöden.** Ankaret; Del Guercio och Tkac (2008) och Reuter och Zitzewitz (2021) för att betyget har en egen effekt. Skillnaden: ni replikerar på andra data, flyttar testen till Europa och prövar ett europeiskt metodbyte som ger ett svagare svar än ankarets.
2. **Hur risk kommer in i flöden.** Barber, Huang och Odean (2016), Berk och van Binsbergen (2016), Evans och Sun (2021). Skillnaden: ni prövar en etikett som säger risken rakt ut.
3. **Etiketter som experiment.** Hartzmark och Sussman (2019): hållbarhetsgloberna flyttade pengar. Skillnaden: en lagstadgad etikett som ändrades för nästan alla och inte flyttade pengar.

Adelino, Cunha och Ferreira nämns i metoddelen, inte här. Inte lästa av någon i projektet: Del Guercio och Tkac (2008), Barber, Huang och Odean (2016), Berk och van Binsbergen (2016). Lästa bara i utkast: Reuter och Zitzewitz, Evans och Sun, Hartzmark och Sussman (`NOTIS_sex_artiklar_lasta_i_sin_helhet_2026-11-20`). Läs trycket innan stycket skrivs.

### 3. Data and Methodology (5,5 sidor, 1 900 ord; tabell 1, figur 1)

**A. De två etiketterna (0,75 sida).** Stjärnan: 1 till 5, riskjusterad avkastning rangordnad inom kategori. De två metodbytena: USA juni 2002 (jämförelsegrupp), Europa oktober 2006 (från tre års historik till tre, fem och tio år; fonder under fem år behöll treårsbetyget). Risksiffran: SRRI till 2022, SRI från 1 januari 2023, med gränserna före och efter. Figur 1.

**B. Data (2,5 sidor).** Källor: Morningstar Direct, LSEG för förmögenhet 2002 till 2008, Kenneth Frenchs faktorer. Andelsklasser summerade till fond. Flödet som ekvation 1. Urvalsregler: minst 10 MUSD, winsorisering 1/99 inom månad, indexfonder utanför. De fyra urvalen, tabell 1. Avvikelserna från ankaret, alla fem (`GRANSKNING...`, steg 3). Kritik av källorna: flödena sprider 1,7 gånger mer än ankarets; avgift och kategori är dagens; klasser nedlagda efter juni 2025 saknas; regressionen med tre signaler bygger på 1 142 av 2 307 fonder.

**C. Tre regressioner (1,5 sidor).** Ekvation 2: ankarets flödesregression (flöde på betyg, avkastningssignal, kontrollerna i ankarets ekvation 5, månadseffekt). Ekvation 3: ankarets reformtest (gapet sorterat på visat betyg minus gapet sorterat på det nya betyget, övriga år som jämförelse). Ekvation 4: dos gånger efter med fondeffekt, kategori gånger månad och volatilitetsdecil gånger månad. Dos = antal steg siffran föll (0 / 1 / 2: 418 / 2 574 / 1 826 fonder). Varför volatiliteten kontrolleras. Hur minsta påvisbara effekt räknas. Kluster. Varje variabel definierad.

### 4. Do Flows Follow the Star? (8 sidor, 2 500 ord; tabell 2 och 3, figur 2 och 3)

**A. Stjärnan mot avkastningen, USA och Europa.** Förutsägelse: om spararna följer etiketten slår stjärnan varje avkastningsmått. Tabell 2, figur 2. USA: återges, med större skillnader i procent och lägre förklaringsgrad; säg att flödena sprider mer. Europa: stjärnan positiv varje år men slår inte rå avkastning eller CAPM; rå avkastning slår FF3 (+0,42, t 4,40). Säg rakt ut att det skiljer Europa från USA.

**B. Etiketten eller det den mäter.** Tabell 3, figur 3. USA 2002: 51,7 % bytte betyg, förklaringsgraden oförändrad, gapet +2,61 utanför bandet. Säg att jämförelsen fem mot en stjärna ligger inom bandet. Europa 2006: 45,8 % bytte. Före bytet följde flödena det visade betyget (2006 högst av fjorton år). Efter bytet föll flödet per stjärna för de berörda fonderna och inte för de yngre; huvudtestet är inte signifikant (t −1,31), Fama-MacBeth är det (t −3,46). Slutsats: ankarets "etiketten oavsett innehåll" återges inte fullt i Europa; stjärnan har ändå ett positivt samband i varje cell.

### 5. Do Flows Follow the Risk Label? (9,5 sidor, 3 000 ord; tabell 4 till 6, figur 4)

**A. Risksiffran bredvid stjärnan.** Tabell 4. Förutsägelse och tecken. Resultat: +0,61 (SE 0,66); förklaringsgrad 0,02 mot stjärnans 0,67. Samband, inte orsak.

**B. Bytet i januari 2023.** Tabell 5, figur 1 igen. 98,5 % fick ny siffra; förklaringsgraden 0,0040 före och 0,0039 efter.

**C. Huvudtestet.** Tabell 6, figur 4. Upplägg: fonder med samma gamla siffra fick olika nya beroende på var volatiliteten låg mot de nya gränserna. Förutsägelse: bär siffran risk in i flödena får fonder vars siffra föll mer pengar. Skattning +0,07 (SE 0,69). Intervall, MDE 1,9. Stjärnan i samma regression +5,29. Ingen trend före (p 0,59). Låtsasbyte 2021 +0,07 (SE 0,86).

**D. Robusthet.** Ett stycke: sicksacken +0,47, tvärsnittsformen +0,28, winsorisering 1/99 +0,01 (SE 0,83), bara aktiefonder, utan Sverige. Tabellerna i bilaga A.

### 6. Interpretation of Empirical Findings (2,5 sidor, 1 200 ord, inga tabeller)

**A. Storleken.** Övre gränsen 1,42 mot stjärnans 5,29: högst en dryg fjärdedel av en stjärna per steg i huvudformen, en tredjedel enligt läsregeln. Räkna om till pengar för en medianfond (inte räknat än).

**B. Tre läsningar av nollan.** Testet är för svagt: MDE och den inplanterade effekten talar emot. Siffran är överflödig när stjärnan finns: stjärnan innehåller redan en riskjustering (Evans och Sun). Siffran når inte spararna: här hör banktestet hemma om det tas med (b2 −0,221, t −2,46, och −0,281, t −3,65), med förbehållen i `RESULTAT_bankagda_mot_fristaende_fondbolag_2026-11-20`. Kanal, inte psykologi.

**C. Europa mot USA.** Stjärnan slår inte avkastningen i Europa, och 2006 försvagar ankarets slutsats där.

**D. Mot Hartzmark och Sussman.** En frivillig etikett på Morningstars sida flyttade pengar; en lagstadgad i faktabladet gjorde det inte. Vad det betyder för en lagstadgad etikett, sagt försiktigt.

### 7. Conclusion (0,6 sida, 300 ord)

Svaret på frågan i stycke 2 i inledningen. Inga nya tal. Ett stycke om gränser: Europa 2006 ger ett svagare svar än USA 2002; nollan gäller flöden i fonder som redan har en stjärna.

### Bilagor

- **A. Övriga resultat.** A1 alla tio par i ankarets tabell 3, USA och Europa. A2 ankarets tabell 2 (samlade flöden): 0,179 (4,47) / 0,156 (2,45) / 0,257 (2,72). A3 ankarets figur 4 (flöde till toppfonder). A4 varianter av replikeringen (betyg per t−1, Europe-faktorer, alla KID-klasser). A5 robusthet för tabell 6 (rad A3 till A5, sicksackens C1 till C6, tvärsnittsformen B1 till B4). A6 varianter av 2006 (LSEG först, bara Direct, samma fonder före och efter). A7 flöde per dosgrupp och månad kring bytet. A8 UK mot EU.
- **B. Variabler och databygge,** med avvikelserna från ankaret i en tabell.
- **C. AI disclosure.**
