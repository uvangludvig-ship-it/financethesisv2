# Barber, Huang och Odean (2016) läst: urval och metod mot vårt bygge

21 november 2026. Claude i chatten med Alexander, som laddade upp artikeln och bad om en kontroll av om vi gjort något fel. Ingen av författarna har kört om något.

## Vad som är läst

Barber, B. M., X. Huang och T. Odean. "Which Factors Matter to Investors? Evidence from Mutual Fund Flows." SSRN-versionen daterad 18 maj 2016 (ssrn.com/abstract=2408231), 77 sidor med tabeller och nätbilaga. Hela brödtexten, tabell 1, alla tabellnoter och nätbilagans metoddelar är lästa. **Den tryckta versionen (Review of Financial Studies 29(10), 2600–2642) är inte läst.** Sidnummer skiljer sig; hänvisningarna nedan gäller avsnitt och noter i SSRN-versionen.

## Varför den spelar roll

Ankarets kod säger att analysen görs på samma fondmånader som Barber, Huang och Odean. Det bekräftas av talen: deras tabell 5 har 257 053 observationer, och 248 463 i kolumnen med stjärnbetyg. 248 463 är exakt ankarets antal fondmånader. Ankarets urval är alltså deras urval, begränsat till fondmånader med betyg.

## Deras urval och metod (avsnitt 2)

| Del | Vad de gör | Var |
|---|---|---|
| Källa | CRSP:s fonddatabas, månadsdata från 1991 | 2.1 |
| Fonder | Diversifierade, aktivt förvaltade amerikanska aktiefonder; indexfonder enligt CRSP tas bort | 2.1, 2.2 |
| Flöde | TNA(t)/TNA(t-1) minus (1 + avkastning). Flöden läggs ihop över andelsklasser, avkastningen vägs med förmögenhet | 2.1, ekvation 1 |
| Storlek | Minst 10 miljoner dollar i slutet av månaden före | 2.1 |
| Flödesfilter | Månadsflöde över -90 % och under 1 000 % | 2.1 |
| Sammanslagningar | När två fonder slås ihop sätts ingående förmögenhet till de två fondernas summa | not 6 |
| Morningstar | Kopplas på stilruta via CUSIP; bara lyckade kopplingar behålls | 2.1 |
| **Historik** | **Fem års avkastningshistorik krävs för att en fond ska ingå** | not 8, 2.6 |
| Betor | Rullande regression på 60 månader, t-60 till t-1 | 2.2, ekvation 2 |
| Alfa | Månadens avkastning minus beta gånger faktoravkastning | ekvation 3 |
| Signal | Vägt medel över 18 månader med avtagande vikter; 18 valt med AIC | 2.3, ekvation 4 till 6 |
| Kontroller | Flöde från t-19, avgift, dummy för fonder utan köp- och säljavgift, avkastningens spridning över tolv månader, log storlek, log ålder, månadseffekter | 2.3 |
| Standardfel | Klustrade på fond och månad | 3.2.1 |
| Stjärnor | Förmögenhetsvägt totalbetyg över klasser, fem grupper med gränser vid 1,5, 2,5, 3,5 och 4,5 | 3.2.2 |
| Winsorisering | Flödet bara vid -90 % och 1 000 %; övriga variabler vid 1 och 99 % | not till tabell 1 |
| Avvikande värden | Observationer med Cooks D över 4/n tas bort i regressionerna | not 16 |

Deras tabell 1 (maj 1997 till november 2011, 257 053 fondmånader): flöde medel -0,53 %, standardavvikelse 2,25 %, kvartiler -1,62 / -0,61 / 0,45; storlek median 397 MUSD; ålder median 154 månader. De skriver själva att urvalet lutar mot större och äldre fonder på grund av femårskravet.

Värdet på lambda (0,2055) står inte i den lästa versionens text. Ankaret anger det (s. 1765).

## Vad vi gör rätt

Flödesformeln, summeringen över andelsklasser, gränsen 10 MUSD, att indexfonder tas bort, 60-månadersfönstret, alfats definition, 18 månader med avtagande vikter, stjärnbetyget (förmögenhetsvägt, avrundat vid halva), månadseffekter och kluster på fond och månad. Kontrollerna följer ankaret, som använder 60 månaders spridning i stället för tolv och ingen avgiftsdummy.

## Vad vi gör fel eller annorlunda

1. **Femårskravet saknas.** Vi tar med fonder från 36 månaders historik. De kräver fem år. Ankarets kodrad `min_mm = 36` gäller antalet observationer i fönstret, inom ett urval som redan har femårskravet. Med kravet minst 6,5 års ålder (60 plus 18 månader) blir vår medianålder 154 månader, exakt deras. Det tar bort ungefär 41 000 av våra 233 290 fondmånader. **Det här är ett fel i vårt bygge.**
2. **Sammanslagningar justeras inte.** De justerar (not 6). Hos oss blir en sammanslagning ett stort falskt inflöde i den övertagande fonden. Exporten visar inte vilka fonder som slagits ihop.
3. **Flödena har extrema värden som deras saknar.** Med samma filter (-90 % till 1 000 %) och femårskravet är vår standardavvikelse 8,4 % mot deras 2,25 %. Mitten stämmer: våra kvartiler är -1,56 / -0,55 / 0,54 mot deras -1,62 / -0,61 / 0,45. Skillnaden sitter i den yttersta procenten: 1,1 % av våra fondmånader har ett flöde över 20 % i absolut tal. Det tyder på fel i förmögenhetsdatan (saknade andelsklasser, sammanslagningar, omflyttningar mellan klasser), inte på verkliga flöden.
4. **Flödesfiltret -90 % till 1 000 % används inte.** Utan betydelse efter winsoriseringen vid 1 och 99 %.
5. **Dagens kategori i stället för den historiska stilrutan.** Känd avvikelse.

## Följd

Punkt 1 går att rätta och har stöd i källan. Punkt 2 och 3 är datafel som kräver bättre förmögenhetsdata (CRSP, eller fondens hela förmögenhet ur Morningstar Direct). Winsoriseringen vid 1 och 99 % dämpar punkt 3 men tar inte bort den: efter winsorisering är vår spridning 3,6 mot ankarets 2,18.

## Gjort 21 november: femårskravet infört för USA

På Alexanders begäran. `final_code/bygg/usa_panel.py` kräver nu en avkastning 60 månader eller mer före varje beta, och minst 36 observationer i fönstret (ankarets kod). Panelen är byggd om från rådata och alla USA-test körda om.

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
| Rå mot FF3 | 0,207 (4,74) | 0,211 (2,97) | 0,185 (2,65) |
| Flöde till femstjärniga fonder, % per månad | 1,16 | 2,47 | 2,11 |
| Marginell förklaringsgrad, betyg / avkastning (%) | 6,5 / 5,6 | 5,0 / 2,4 | 5,1 / 2,5 |
| Ändrat betyg före / juni 2002 / efter | 13,9 / 54,2 / 11,9 | 14,7 / 51,7 / 12,5 | 14,0 / 53,0 / 12,1 |
| Betygets förklaringsgrad före / efter | 0,073 / 0,074 | 0,058 / 0,061 | 0,064 / 0,061 |
| Kategori före / efter | 0,043 / 0,015 | 0,029 / 0,015 | 0,037 / 0,017 |
| Kategori utöver betyg före / efter | 0,022 / 0,014 | 0,017 / 0,011 | 0,023 / 0,013 |
| Händelsetestet, 5 mot 1 | 2,84, över | 1,82, inom | 2,47 [-1,64; 3,11], inom |
| Händelsetestet, 4-5 mot 1-2 | 1,81, över | 2,64, över | 2,96 [-0,67; 0,62], över |
| Flöde per stjärna före / efter, skillnad | | -0,102 (t -1,58) | -0,128 (t -1,96) |
| Ankarets tabell 2, kolumn 1 | 0,179 (4,47) | 0,156 (2,44) | 0,130 (2,41) |
| Flöde per stjärna per år | 0,4 till 0,6 | 0,61 till 0,90 | 0,58 till 0,80 |

Talen ligger närmare ankarets och alla slutsatser står kvar. Koefficienterna är fortfarande ungefär dubbelt så stora som ankarets; t-värdena för stjärnan mot CAPM, FF3 och FFC ligger nu nära ankarets.

## Gjort 21 november: femårskravet infört också för Europa

På Alexanders begäran, efter en förhandsvisning. `bygg/eu_5_fondpanel.py` och `bygg/eu2006_4_fondpanel.py` har samma regel. Tabell 6 (bytet 2023) berörs inte; den bygger på ett annat urval.

| | Med 36 månader | Med fem år |
|---|---|---|
| **Europa 2018 till 2025:** första månad | januari 2018 | juni 2019 |
| Fondmånader / fonder | 130 031 / 2 307 | 94 203 / 1 837 |
| Stjärnan mot rå avkastning | -0,076 (-0,97) | -0,081 (-0,88) |
| Stjärnan mot CAPM | -0,091 (-1,18) | -0,100 (-1,12) |
| Stjärnan mot FF3 | 0,121 (1,76) | 0,042 (0,52) |
| Stjärnan mot FFC | 0,120 (1,68) | 0,075 (0,91) |
| Rå avkastning mot FF3 | 0,416 (4,40) | 0,258 (2,33) |
| Risksiffran, tredje signalen (Fama-MacBeth) | 0,61 (0,66) [-0,67; 1,90] | 1,08 (0,66) [-0,22; 2,37] |
| Risksiffran, poolat | 0,80 (0,98) | 1,02 (1,01) |
| Stjärnan i samma regression | 5,53 (t 11,9) | 5,10 (t 11,0) |
| Marginell förklaringsgrad: avkastning / betyg / risksiffra | 1,20 / 0,67 / 0,02 | 1,20 / 0,57 / 0,02 |
| Bytte risksiffra januari 2023 | 98,5 % (1 040 fonder) | 98,5 % (923 fonder) |
| Månad x risksiffra före / efter | 0,0038 / 0,0039 | 0,0040 / 0,0044 |
| Flöde per stjärna per år | 0,22 till 0,67 | 0,19 till 0,63 |
| **Europa 2006:** första månad | januari 2003 | juni 2004 |
| Fondmånader / före bytet | 296 337 / 57 043 | 217 614 / 24 924 |
| Ändrat betyg före / oktober 2006 / efter | 19,0 / 45,8 / 15,3 | 20,3 / 48,0 / 14,6 |
| Betygets förklaringsgrad före / efter | 0,0119 / 0,0100 | 0,0138 / 0,0097 |
| Händelsetestet, 5 mot 1 | 3,05 [-2,54; 2,99], över | 4,91 [-4,45; 4,08], över |
| Händelsetestet, 4-5 mot 1-2 | 0,72 [-2,31; 1,11], inom | 0,89 [-1,97; 0,52], över |
| Flöde per stjärna före / efter, skillnad (till 2016) | -0,170 (t -2,57) | -0,190 (t -2,04) |
| Samma, till 2015 / till 2010 | -0,139 (-2,10) / -0,146 (-2,05) | -0,156 (-1,67) / -0,201 (-2,03) |

Ingen slutsats ändras. Händelsetestet 2006 ligger nu över gränsen i båda måtten. Fallet i flöde per stjärna efter 2006 är lika stort men mindre säkert.

Perioderna kortas därför att avkastningen i exporterna börjar 2013 respektive 1998. Med månadsavkastning från juli 2011 för listorna i `bas_eu_2026-11-19` och från augusti 1996 för listorna i `eu2006_lseg_bank_2026-11-20/radata` kan regeln gälla utan förlust.

## Inte gjort

- Sammanslagningar och de extrema flödena är inte åtgärdade. Ingen regel ur ankaret eller Barber, Huang och Odean löser dem: filtret -90 % till 1 000 % binder inte, och winsoriseringen vid 1 och 99 % används redan. Morningstar Direct kan ha egna flödesfält och fondens hela förmögenhet; det är inte prövat.
- Den tryckta versionen är inte jämförd med SSRN-versionen.
- Samma kontroll av flödenas svansar är inte gjord på Europapanelerna.
