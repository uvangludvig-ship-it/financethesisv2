# bas_eu_2026-11-19/

Europeisk basdata för alla europeiska test (EU-replikering av Ben-David m.fl., hästkapplöpningen, UK–EU-testet, sicksacken på hela EU). Samma basdata hela vägen. Design: `STRUKTUR_data_usa_eu_uk_2026-11-19` i projektet.

Licensierad Morningstar Direct-data. Repot ska vara privat.

Universum: andelsklasser med domicil Luxemburg eller Irland som levde någon gång 2018–2025. Exporten delas upp på Domicile × Inception Date (30 000-radersgränsen) och dubbletter tas bort på SecId när filerna slås ihop.

| Fil | Innehåll | Klasser | md5 (gz) |
|---|---|---|---|
| `A1_aktiva_fore2015.csv.gz` | Grupp A, del 1: överlevande klasser, startade senast 2014. Avkastning och NA 2013–2025 (USD), betyg 2017–2025, SRI 2018–2025, Surveyed KIID SRRI History, Country Available for Sale | 25 683 (LU 20 318, IE 5 365) | 412007ddde2327098e18372454ee3d4e |
| `A2_aktiva_2015_2019.csv.gz` | Grupp A, del 2: överlevande klasser, startade 2015–2019. Samma kolumner som A1. Ingen överlappning med A1 | 27 614 (LU 20 786, IE 6 828) | 77c161e80d44c32ed230c18a8d4b4490 |
| `A3_aktiva_2020_2024.csv.gz` | Grupp A, del 3: överlevande klasser, startade 2020–2024. 552 kolumner (saknar NA-månader före 2016). Tre klasser finns även i A2 | 25 492 (LU 18 159, IE 7 333) | 5876bc77e591ce3d52efdbcfc55ec953 |

Gzippade oförändrade Direct-exporter (originalnamn A1 `0E048842A0C54E46B4DCBF9851DF3638_in_.csv`, A2 `3C07371D56394F3187AE60D5C0411360_in_.csv`, md5 okomprimerad f7b907c47501822089fc53c51be556cb; A3 `2D9337D8B09D4A0DA6A68D5C6BBA473B_in_.csv`, md5 okomprimerad aa887c62c562eeb3a163a7d575fabca6). `pd.read_csv` läser .gz direkt.

## Kända egenheter

- Antalet klasser med SRI faller från 14 352 (dec 2022) till 10 341 (jan 2023). Utrett: Direct har glesa månadsvärden för SRI, med toppar i juni och december. Första värdet under första halvåret 2023 ger SRI för de flesta.
- Sida ur Country Available for Sale: UK 806, EU 8 465, båda 14 158, ingen 2 254.

Grupp A (överlevande) är komplett med A1–A3. Grupp B (klasser nedlagda från 2018) saknas och läggs till här när den kommer.
