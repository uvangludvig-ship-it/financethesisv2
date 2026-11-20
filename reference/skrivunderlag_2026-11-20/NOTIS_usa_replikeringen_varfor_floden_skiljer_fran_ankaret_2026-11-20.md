# USA-replikeringen: varför våra flöden skiljer sig från ankarets

20 november 2026. Claude i chatten med Alexander, som frågade hur talen kan vara så olika. Diagnos, inga test för uppsatsen. Ingen av författarna har kört om något.

## Skillnaden

| | Ankaret | Vi |
|---|---|---|
| Fonder / fondmånader | 3 341 / 248 463 | 2 638 / 233 290 |
| Flöde, spridning mellan fonder | 2,18 | 3,81 |
| Flöde, 5:e och 95:e percentilen | -4,10 / 3,40 | -4,91 / 5,60 |
| Fondstorlek, median (MUSD) | 411 | 307 |
| Ålder, 5:e percentilen och median (år) | 6,7 / 12,8 | 5,0 / 11,2 |
| Flöde till femstjärniga fonder, % per månad | 1,16 | 2,47 |
| Tabell 3, stjärnan mot rå avkastning | 0,099 | 0,280 |
| Händelsetestet, 5 mot 1 stjärna | 2,84, över gränsen (cirka 1,3, avläst ur figuren) | 1,82, under gränsen 2,22 |
| Händelsetestet, 4-5 mot 1-2 stjärnor | 1,81, över gränsen (cirka 0,4, avläst ur figuren) | 2,64, över gränsen 0,72 |

Riktningen är densamma i varje test. Storlekarna skiljer sig med en faktor två till tre.

## Fynd 1: ankarets urval är Barber, Huang och Odeans

Kodens huvud: "the main analysis is carried out the same panel of fund-month observations used in BHO(RFS 2016)" och "The sample starts from the BHO(2016) sample". Urvalet är alltså inte byggt av ankaret. Filtren står i Barber, Huang och Odean (2016), som inte är läst.

Belägg för att ett filter saknas hos oss: med kravet minst 6,5 års ålder får vi ålder P5 7,0 och median 12,8, mot ankarets 6,7 och 12,8. Det stämmer med ett fullt fönster på 60 månader plus 18 månader för signalen, som texten säger (s. 1733). Vi följde kodens `min_mm = 36`. Den raden tillämpas inom ett urval som redan är filtrerat.

Med 6,5-årskravet (192 054 fondmånader, 2 227 fonder) rör sig talen mot ankaret men inte ända fram: tabell 3 stjärnan mot rå avkastning 0,213 (t 3,09); mot FF3 0,327 (4,94); tabell 4 panel A 14,0 / 53,2 / 12,1 (ankaret 13,9 / 54,2 / 11,9); betygets förklaringsgrad 0,059 / 0,058; flöde till femstjärniga fonder 2,15; flödets spridning 3,53; händelsetestet 5 mot 1 2,19 [-1,73; 3,48], inom; 4-5 mot 1-2 2,70 [-0,71; 0,61], över.

## Fynd 2: exporten saknar förmögenhet för många andelsklasser

Export `BA37C8D4...` (16 577 klasser, 5 039 fonder). Andel klassmånader med avkastning men utan förmögenhet: 38 % år 1997, 29 % år 2002, 22 % år 2006, 14 % år 2011. I ungefär hälften av alla fondmånader saknar minst en klass förmögenhet; i vårt urval är bara 40 % av fondmånaderna kompletta. Värden som står stilla från månaden före är sällsynta (högst 2 %).

Följd: fondens storlek blir för liten, gränsen 10 MUSD och betygets vikter räknas på en del av fonden, och fonder helt utan förmögenhet faller bort.

Det förklarar inte flödenas spridning: kompletta fondmånader har spridning 4,02 och fonder med en enda klass 4,07 (de är mindre, median 138 till 194 MUSD).

## Fynd 3: flödena har fetare svansar i alla grupper

Vår 1:a och 99:e percentil ligger kring -12 % och +14 % varje år. Fonder över 1 000 MUSD har spridning 2,71, fortfarande över ankarets 2,18 för alla. Orsaken är inte funnen. Möjligt: annan källa för förmögenheten (Morningstar mot CRSP), eller filter på flöden hos Barber, Huang och Odean. Båda använder månadsdata, så frekvensen är inte förklaringen.

## Beslut

Alexander valde 20 november att inte bygga om panelen. Paketet står kvar med 36 månader.

## Vad som skulle behövas för att komma närmare

1. Barber, Huang och Odean (2016), urvalsavsnittet, läst i sin helhet.
2. 60 månader (texten och ankarets åldersfördelning) i stället för minst 36 (koden). Gäller även Europapanelen. Bytet ska i så fall redovisas öppet, med talen för 36 månader i bilagan.
3. Om Morningstar Direct har fondens totala förmögenhet per månad för USA: ny export, så att flödena kan räknas på hela fonden.
4. Samma kontroll av saknad förmögenhet i Europaexporterna. Inte gjord.

## Vad uppsatsen ska säga

USA-delen återskapar ankarets resultat i riktning, på andra data och ett urval som inte är identiskt. Talen är inte jämförbara i storlek. Händelsetestet 2002 är säkerställt för 4-5 mot 1-2 stjärnor, men inte för 5 mot 1.
