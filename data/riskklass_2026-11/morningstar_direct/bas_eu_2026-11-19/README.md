# bas_eu_2026-11-19/

Europeisk basdata för alla europeiska test (EU-replikering av Ben-David m.fl., hästkapplöpningen, UK–EU-testet, sicksacken på hela EU). Samma basdata hela vägen. Design: `STRUKTUR_data_usa_eu_uk_2026-11-19` i projektet.

Licensierad Morningstar Direct-data. Repot ska vara privat.

Universum: andelsklasser med domicil Luxemburg eller Irland som levde någon gång 2018–2025. Exporten delas upp på Domicile × Inception Date (30 000-radersgränsen) och dubbletter tas bort på SecId när filerna slås ihop.

| Fil | Innehåll | Klasser | md5 (gz) |
|---|---|---|---|
| `A1_aktiva_fore2015.csv.gz` | Grupp A, del 1: överlevande klasser, startade senast 2014. Avkastning och NA 2013–2025 (USD), betyg 2017–2025, SRI 2018–2025, Surveyed KIID SRRI History, Country Available for Sale | 25 683 (LU 20 318, IE 5 365) | 412007ddde2327098e18372454ee3d4e |
| `A2_aktiva_2015_2019.csv.gz` | Grupp A, del 2: överlevande klasser, startade 2015–2019. Samma kolumner som A1. Ingen överlappning med A1 | 27 614 (LU 20 786, IE 6 828) | 77c161e80d44c32ed230c18a8d4b4490 |
| `A3_aktiva_2020_2024.csv.gz` | Grupp A, del 3: överlevande klasser, startade 2020–2024. 552 kolumner (saknar NA-månader före 2016). Tre klasser finns även i A2 | 25 492 (LU 18 159, IE 7 333) | 5876bc77e591ce3d52efdbcfc55ec953 |
| `B1_nedlagda_2018_2022.csv.gz` | Grupp B, del 1: nedlagda klasser, Obsolete Date 2018-01-02 till 2022-06-30. 551 kolumner (NA från 2017-12, betyg från 2017-12) | 28 312 (LU 21 474, IE 6 838) | 33d1369a5cf1c94fdaf0ff1a49fb93e9 |
| `B2_nedlagda_2022_2025.csv.gz` | Grupp B, del 2: nedlagda klasser, Obsolete Date 2022-06-30 till 2025-06-30. 551 kolumner: samma som B1, med `Index Fund` (Yes 457) och `Institutional` (Yes 3 952, tomt 490) sist. 71 klasser finns även i B1. Ny export 19 nov; den första B2-exporten (549 kolumner, utan Institutional och Index Fund, gz-md5 ffa0c869f126a01550a73031183b377e) ligger inte i git | 29 196 (LU 22 618, IE 6 578) | bf3e89994c8699cbbf3f1673968b7b79 |

Gzippade oförändrade Direct-exporter (originalnamn A1 `0E048842A0C54E46B4DCBF9851DF3638_in_.csv`, A2 `3C07371D56394F3187AE60D5C0411360_in_.csv`, md5 okomprimerad f7b907c47501822089fc53c51be556cb; A3 `2D9337D8B09D4A0DA6A68D5C6BBA473B_in_.csv`, md5 okomprimerad aa887c62c562eeb3a163a7d575fabca6; B1 `59F09AE5F19149B898CEC051006D72E0_in_.csv`, okomprimerad 982a140cee7bcb849c9742b759f976f5; B2 `226F9EC4243A44408972432B3BA329CB(in).csv`, okomprimerad 73bc15d48c4d138deb4251287702e278; den första B2-exporten hette `135DF1D55832449B9CA0BEE70CF35985_in_.csv`, okomprimerad 14beafc6cf45c616209cfbee18a2332a). `pd.read_csv` läser .gz direkt.

## Kända egenheter

- Antalet klasser med SRI faller från 14 352 (dec 2022) till 10 341 (jan 2023). Utrett: Direct har glesa månadsvärden för SRI, med toppar i juni och december. Första värdet under första halvåret 2023 ger SRI för de flesta.
- Sida ur Country Available for Sale: UK 806, EU 8 465, båda 14 158, ingen 2 254.

Grupp A (överlevande) är komplett med A1–A3. Grupp B (nedlagda) täcker Obsolete Date 2018-01-02 till 2025-06-30 (B1–B2). Saknas: klasser nedlagda efter 2025-06-30.
