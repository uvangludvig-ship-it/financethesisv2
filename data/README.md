# data/

Data som inte hör till ett visst ämne, kopierad 17 nov 2026 från `~/dev/financethesis/data/`. Varje fil i `data/` är byte-identisk med originalet (md5 kontrollerad för alla 1 237 kopierade filer i `data/` och `reference/`; därefter har bara två textfiler i `reference/course_context/` redigerats, se `AI_LOG.md`). Ingen datafil har ändrats, filtrerats eller byggts om.

| Mapp | Betyder | Vem skriver |
|---|---|---|
| `raw/` | Källfiler exakt som de kom. Ändras aldrig | ingen; filer läggs in |
| `derived/` | Det som skript tar fram ur `raw/` | bara skript |
| `build/` | Koden som hämtar eller bygger data | – |

Varje mapp under `raw/` har en egen `README.md` med filer, kolumner och kända egenheter, liksom `derived/` och `build/`. Dessa README-filer är vår dokumentation, inte källfiler.

**Licenser:** LSEG-, MSCI- (indexserierna `.dMI…`) och SHoF-data är licensierade. Repot ska vara privat. Data från FI, Pensionsmyndigheten och AP-fonderna är offentlig.

## raw/: källor

| Mapp | Innehåll | Period | Hämtad | Kommentar |
|---|---|---|---|---|
| `lseg/panel_2005_2026/` | LSEG Workspace (CodeBook): dagliga kurser, totalavkastning, volym, börsvärde, antal aktier, omsättning, bid och ask. `stocks_daily_2005.parquet`: 4 340 104 rader, 1 928 RIC. `stocks_static_2005.csv`: statiska uppgifter för 2 117 RIC. `indices_daily (1).csv`: OMXS30, OMXS30GI, OMXSPI, OMXSGI, OMXSBGI, OMXSBCAPGI. `indices_daily_extra.csv`: OMXN40, OMXSBPI, OMX Stockholm large/mid/small cap (PI och GI), STOXX, STOXXR, tre MSCI-serier. `td_universe.csv`, `td_rics_final.csv`, `td_failures (1).csv`: universum, slutlig RIC-lista och misslyckade hämtningar | aktier från 1991 för en del bolag, huvudsakligen 2005–26 okt 2026 | 26 okt 2026 | Av de 1 928 RIC är 1 526 Stockholmsnoterade (736 aktiva, 790 avnoterade; avnoterade RIC har `^` och avnoteringskod, t.ex. `3L.ST^D12`) och 402 från Oslo, Helsingfors och Köpenhamn (115 avnoterade). Enligt gamla `MANIFEST.md` byggdes beställningslistan av Stockholmsbolag plus aktier i vissa fonders innehav, så **de icke-svenska aktierna är ett urval, inte hela respektive marknad**. Filnamnen med "(1)" är som de laddades ner. `totret` är daglig avkastning i procent med extrema värden, se `raw/lseg/README.md` |
| `lseg/klassificering/` | LSEG: ICB- och TRBC-sektor, marknad och free float för 1 685 RIC (`lseg_klassificering.csv`), free float per datum (`lseg_freefloat_hist.csv`, 65 714 rader), dagliga kurser för aktier som saknas i panelen, t.ex. Nordea och Tieto (`lseg_saknade_aktier.csv`), fältlogg | 2007–2026 | 1 nov 2026 | |
| `fi/` | Finansinspektionen: svenska fonders innehav per kvartal, en zip per kvartal (`Fondinnehav_<kvartal>_<FI:s publiceringsdatum>.zip`) | 2018Q4–2026Q2, 31 kvartal | 25 okt 2026 | |
| `fi_short/` | Finansinspektionens blankningsregister: historiska positioner (31 okt och 2 nov) och aktuella positioner (2 nov), med hämtlogg och README | positioner 2010-05-10 till 2026-10-30 | 31 okt och 2 nov 2026 | Bara offentliga betydande korta nettopositioner. `<0,5` är inte noll |
| `ppm/` | Pensionsmyndighetens månadsstatistik per fond (xls/xlsm i årsmappar), fondlista 2026 (`Lista alla fonder 2026.xls`), dagliga fondkurser jan–mar 2024 (`ppm_nav_2024.xlsx`) och `FEES.txt`, som är Morningstar-avgifter från SHoF och inte från Pensionsmyndigheten | 2001-01 till 2026-08 | sep–okt 2026 | 311 filer |
| `shof/` | Swedish House of Finance: Morningstars fondregister (`fundmaster.xlsx`, samma innehåll zippat i `shof_fundmaster.zip`) och fältdefinitioner (pdf och txt) | | okt 2026 | SHoF:s dagliga exporter (`Valuations/`, `Reinvestments/`, flera GB) ligger inte i repot. Alexander har dem; de läggs på exakt de sökvägarna om de behövs |
| `ap/` | AP1–AP4:s publicerade innehavslistor (111 pdf) i `AP1/`…`AP4/`, hämtlogg och insamlingslogg (`INSAMLINGSLOGG_2026-10-31.md`, `_collection_20261031/`) | listor 2015–2026 | 31 okt 2026 | AP1 har bara två listor (2025) |

## derived/: byggt ur raw

| Fil | Innehåll | Byggd av |
|---|---|---|
| `fi/fi_holdings_long.csv.gz` | Alla FI-innehav i långt format: 3 064 860 rader, 31 kvartal, 886 fonder, 17 kolumner (tillgångsslag, instrumentnamn, ISIN, emittentland, valuta, antal, kurs, marknadsvärde …). Git LFS | En notebook i gamla repot (cell 16–17), inte överförd eftersom den i övrigt hör till ett gammalt ämne. Ett fristående byggskript saknas än |
| `ppm/ppm_panel_2018_2026.csv` | PPM-panel per fond och månad: 53 062 rader, 25 kolumner (fondnr, fondnamn, värden, marknadsvärden, nettohandel, kategori, fondtyp, förvaltare …) | `build/build_ppm_panel_2018.py` från `raw/ppm/` |
| `shof_monthly/shof_valuations_monthly.csv` | SHoF-värderingar per andelsklass och månad: TNA och nettoflöde för andelsklass och fond, 457 842 rader, 4 984 andelsklasser | `build/shof_monthly.py` från SHoF:s dagliga exporter i `raw/shof/Valuations/` och `Reinvestments/` (finns inte i repot) |
| `shof_monthly/shof_rips_monthly.csv` | Återinvesterade kurser (totalavkastningsindex i SEK) per andelsklass och månad, 442 507 rader | samma |
| `ap/` | AP1–AP4:s innehav av svenska aktier, rapportdatum 2015-06-30 till 2026-06-30, tolkade ur `raw/ap/`: `ap_svenska_aktier_2013_2026.csv` (10 444 rader: AP4 3 633, AP3 3 329, AP2 3 289, AP1 193), samma rader med RIC i `ap_svenska_aktier_med_ric.csv`, samt uteslutna rader, matchningar att granska, tolkningsfel och källkontroller | `parse_ap_20261031.py` och `finalize_ap_fi_20261031.py` i gamla repot. Inte överförda: RIC-matchningen läser en händelselista från ett gammalt ämne och går inte att köra här |

## build/

| Skript | Gör |
|---|---|
| `build_ppm_panel_2018.py` | Bygger `derived/ppm/ppm_panel_2018_2026.csv`. Hittar repots rot med `../..` och går att köra som det är |
| `collect_ap_fi_20261031.py` | Hämtade AP-fondernas innehavslistor och FI:s blankningsregister till `raw/ap/` och `raw/fi_short/` |
| `shof_monthly.py` | Aggregerar SHoF:s dagliga exporter till månad. Kräver `raw/shof/Valuations/` och `Reinvestments/` |

LSEG-panelerna hämtades med `data/build/lseg/lseg_pull_v4.py` i gamla repot (körs i LSEG Workspace CodeBook). Skriptet är inte överfört eftersom beställningslistan byggdes för ett gammalt ämne.

## Kvar i gamla repot

Följande finns i `~/dev/financethesis/data/` men är inte överfört, eftersom urvalet eller innehållet styrs av ett gammalt ämne eller för att filen är en dubblett:

- `raw/ftn/`, `derived/ftn/`: Fondtorgsnämndens upphandlingsrapporter och bud
- `input/omxsb/`: OMXSB- och OMXS30-ändringar 2005–2026, RIC-koppling, strykningsorsaker, trackerfonders förmögenhet
- `input/swing/`, `input/holdings_external/`, `input/lseg/`, `input/shof_bestallning_riskklass/`, `derived/exit_days/`, `derived/measurements/`, `derived/facts/`
- `raw/lseg/panel_2005_2026/fund_nav_tna_daily.csv` och `td_funds_resolved.csv`: daglig NAV för 205 utvalda fonder
- `raw/lseg/panel_2005_2026/stocks_daily_2005.csv.gz`: trasig som mottagen (gzip CRC-fel); parquet-filen har samma rader
- `raw/lseg/panel_eu/`: 670 europeiska aktier ur vissa fonders innehav, plus dagliga SEK-kurser (`fx_sek_daily.csv`)
- `raw/lseg/panel_2012_2026/`, `raw/lseg/datastream/`: äldre hämtningar, ersatta av `panel_2005_2026`
- `raw/lseg/twins/`: kurser för fyra A-aktier
- `raw/fi/earlier_download_2026-10/`: fyra kvartal hämtade tidigare under andra namn
- `raw/shof/Valuations/`, `Reinvestments/`: pilotexporter från 3–4 nov
- `raw/omxsb_extension_20261031/`, `raw/anchor_*`, `raw/deep_dd_*`, `derived/anchor_*`, `derived/deep_dd_*`, `derived/ccc13_*`: underlag för gamla alternativ

Den fullständiga beskrivningen av varje fil, med hashar, finns i `~/dev/financethesis/data/MANIFEST.md`.
