# derived/

Tabeller byggda ur `../raw/`. Ändra dem inte för hand; bygg om dem från `raw/` med skript i `../build/`.

## fi/

`fi_holdings_long.csv.gz` (Git LFS) innehåller alla FI-innehav i [`../raw/fi/`](../raw/fi/README.md), en rad per fond, instrument och kvartal. Filen har 3 064 860 rader, 31 kvartal (2018Q4–2026Q2) och 886 fonder.

Kolumnerna har FI:s namn:

- **Instrumentet:** `Tillgångsslag_enligt_LVF_5_kap`, `Instrumentnamn`, `ISIN-kod_instrument`, `Landkod_Emittent`, `Valuta`, `Antal`, `Kurs_som_använts_vid_värdering_av_instrumentet`, `Marknadsvärde_instrument` och `Andel_av_fondförmögenhet_instrument`
- **Fonden och kvartalet:** `Kvartalsslut`, `Fondbolag_namn`, `Fond_institutnummer`, `Fond_namn`, `Fond_ISIN-kod`, `Fondförmögenhet` och `Jämförelseindex`
- **Källan:** `zip`, källfilen

Den byggdes i en notebook i gamla repot. Där finns inget fristående byggskript, så tabellen kan inte byggas om härifrån ännu.

## ppm/

`ppm_panel_2018_2026.csv` innehåller Pensionsmyndighetens statistik per fond och månad från januari 2018, med 53 062 rader. Den byggs från [`../raw/ppm/`](../raw/ppm/README.md) med `../build/build_ppm_panel_2018.py`.

Kolumnerna:

| Kolumner | Innehåll |
|---|---|
| `fondnr`, `fondnamn`, `isin`, `date` | Fonden och månaden |
| `val_*` | Antal fondval för kvinnor (`_k`), män (`_m`) och totalt (`_tot`), från fliken "Fondval & marknadsvärde" |
| `mv_*` | Marknadsvärden, uppdelade på samma sätt |
| `handel_netto` | Nettohandel |
| `kategori`, `fondtyp`, `forvaltare`, `svensk`, `forvaltning`, `upphandlad` | Fondens kategori och förvaltning |
| `ret_ytd`, `ret_1m`, `ret_12m`, `ret_36m` | Avkastning |
| `fee_net`, `fee_gross` | Avgifter |
| `valuta`, `startdatum` | Övrig information |

Vilka källkolumner de motsvarar står i skriptet. Bara `val_tot`, `mv_tot`, `handel_netto`, avkastningarna och avgifterna är omvandlade till tal; övriga kolumner är text.

## shof_monthly/

Månadsaggregat av SHoF:s dagliga exporter (`Valuations/`, `Reinvestments/`), som inte finns i repot, se [`../raw/shof/`](../raw/shof/README.md). Byggd med `../build/shof_monthly.py`; `monthly.log` är körloggen.

| Fil | Innehåll |
|---|---|
| `shof_valuations_monthly.csv` | 457 842 rader och 4 984 andelsklasser. En rad per andelsklass (`performanceId`) och månad (`ym`). Innehåller `secid`, valutor för klass och fond, månadens sista dag med data, `tnaclass` och `tnafund` (sista värdet i månaden), `nf_class` och `nf_fund` (summan av dagliga nettoflöden), `ndays` och `nf_class_n` (antal dagar med flödesdata) |
| `shof_rips_monthly.csv` | 442 507 rader. Återinvesterad kurs i SEK vid månadens sista dag (`tri_sek`) per andelsklass, `returntype` och månad. `returntype` 1 är totalavkastning (402 059 rader) och 18 skattejusterad (40 448 rader) |

## ap/

Tabellerna är tolkade ur AP-fondernas pdf:er i [`../raw/ap/`](../raw/ap/README.md). De har AP1–AP4:s innehav på den svenska aktiemarknaden, med rapportdatum 2015-06-30 till 2026-06-30. Datumet 2013 i ett filnamn är startåret som efterfrågades. Inga listor från 2013 eller 2014 hittades.

| Fil | Innehåll |
|---|---|
| `ap_svenska_aktier_2013_2026.csv` | 10 444 rader: AP4 3 633, AP3 3 329, AP2 3 289 och AP1 193. Kolumner: `fond`, `datum`, `bolagsnamn`, `ISIN`, `antal aktier`, `marknadsvärde` (SEK, omräknat från källans enhet). Antalen är inte splitjusterade |
| `ap_svenska_aktier_med_ric.csv` | Samma rader med källhänvisning (fil, sida, rad, URL), urvalsgrund, kvalitetsflaggor och RIC |
| `matchningar_att_granska.csv` | Rader med osäker eller saknad RIC, med förslag |
| `excluded_rows.csv` | 3 105 bortvalda rader: främst innehav som inte identifierats som svenska (2 892), men också bolagssummor, kreditfonder och instrument som inte är aktier |
| `parse_rejections.csv`, `source_checks.csv` | Rader som inte gick att tolka (inga) och summakontroller mot källorna |

**Om RIC-kolumnen:** bara 4 412 av 10 444 rader har RIC. Matchningen gjordes mot en lista över indexhändelser från ett tidigare ämne, så bolag som någon gång funnits i den listan har mycket oftare fått RIC. Matchningsskripten är inte överförda. För att få RIC för alla rader, matcha `ISIN` mot `IssueISIN` i `../raw/lseg/panel_2005_2026/stocks_static_2005.csv`.
