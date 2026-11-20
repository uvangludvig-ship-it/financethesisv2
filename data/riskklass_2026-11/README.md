# data/riskklass_2026-11/

Data till riskklassuppsatsen (Evans & Sun, Ben-David, UK–EU), kopierad från Alexanders Hämtade filer 19 nov 2026. Allt här hör till det ämnet; resten av `data/` är ämnesoberoende.

| Mapp | Innehåll |
|---|---|
| `morningstar_direct/` | Direct-exporter (thesis, kostnad, SFDR, glober, UK–EU), faktorer, Riksbank, byggda paneler (.pkl) och körskript per test |
| `morningstar_direct/exporter_2026-11-18/` | Direct-exporterna från 18–19 nov (USA 1991–2011 och Europa), gzippade. `pd.read_csv` läser .gz direkt |
| `morningstar_direct/bas_eu_2026-11-19/` | Europeisk basdata: alla LU- och IE-klasser, överlevande (A1–A3); nedlagda (grupp B) läggs till. Gzippade oförändrade Direct-exporter |
| `morningstar_direct/analys_eu_2026-11-19/` | Skript och utdata för sicksacken, UK mot EU, kanaltesten och Ben-David på EU med hästkapplöpningen (19 nov 2026). Se mappens README för körordning |
| `morningstar_direct/analys_usa_2026-11-18/` | Replikering av Ben-David m.fl. (2022) på amerikanska aktiefonder 1997–2011 (Table 2–4, Figure 3–5), körd 18–19 nov 2026. Skript och utskrifter; indata i `exporter_2026-11-18/` och `faktorer/` |
| `morningstar_direct/analys_eu_slutlig_2026-11-19/` | EU-testen (sicksacken, UK mot EU, kanaltesten, Ben-David på EU) med nedlagda klasser: A1–A3 + B1 + första B2 (`utdata_full/`) och A1–A3 + B1 (`utdata_b1/`). Ersatt av `analys_eu_full2_2026-11-19/` |
| `morningstar_direct/analys_eu_full2_2026-11-19/` | Slutlig körning av EU-testen 2018–2025 med A1–A3, B1 och den nya B2 (med Institutional och Index Fund), inklusive händelsetestet januari 2023. Se mappens README för körordning |
| `morningstar_direct/eu2006_lseg_bank_2026-11-20/` | Händelsetestet på Morningstars metodbyte i Europa oktober 2006 och bankägda mot fristående fondbolag. Rådata: Direct-exporter LU/IE 1998–2016 (gz) och LSEG-fondförmögenhet 2002–2008, md5 i mappens README |
| `shof/riskklass_resultat/` | SHoF-data bearbetad: bas, sek, riskmått, privatklasser (val_monthly), rips_stats |
| `shof/bestallning_privatklasser/` | Beställningslistan till SHoF |
| `ovrigt/` | F-F momentum, ECB växelkurser, Master-Weblist, norska personkunder, fyra små Direct-exporter |

## Inte med

- **SHoF-rådatan** `FUNDS_RIPS_*.csv` (10 filer) och `FUNDS_VALUATIONS_*.csv` (16 filer): 18 GB okomprimerat, 4,8 GB gzippat. Repots `.gitignore` håller SHoF:s dagliga exporter utanför git (licens och storlek); de delas för hand. Gzippad kopia: `~/dev/shof_radata_gz/` på Alexanders dator. Allt som byggts av den finns i `shof/riskklass_resultat/`.
- `shof/riskklass_resultat/test3/panel_test3.pkl` (116 MB). Byggs om med `test3/bygg.py`.
- `ler.xlsx` och `Search Results_*.xlsx`: misslyckade exporter ("User is not entitled to export this data").
