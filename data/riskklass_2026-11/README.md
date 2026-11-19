# data/riskklass_2026-11/

Data till riskklassuppsatsen (Evans & Sun, Ben-David, UK–EU), kopierad från Alexanders Hämtade filer 19 nov 2026. Allt här hör till det ämnet; resten av `data/` är ämnesoberoende.

| Mapp | Innehåll |
|---|---|
| `morningstar_direct/` | Direct-exporter (thesis, kostnad, SFDR, glober, UK–EU), faktorer, Riksbank, byggda paneler (.pkl) och körskript per test |
| `morningstar_direct/exporter_2026-11-18/` | Direct-exporterna från 18–19 nov (USA 1991–2011 och Europa), gzippade. `pd.read_csv` läser .gz direkt |
| `shof/riskklass_resultat/` | SHoF-data bearbetad: bas, sek, riskmått, privatklasser (val_monthly), rips_stats |
| `shof/bestallning_privatklasser/` | Beställningslistan till SHoF |
| `ovrigt/` | F-F momentum, ECB växelkurser, Master-Weblist, norska personkunder, fyra små Direct-exporter |

## Inte med

- **SHoF-rådatan** `FUNDS_RIPS_*.csv` (10 filer) och `FUNDS_VALUATIONS_*.csv` (16 filer): 18 GB okomprimerat, 4,8 GB gzippat. Repots `.gitignore` håller SHoF:s dagliga exporter utanför git (licens och storlek); de delas för hand. Gzippad kopia: `~/dev/shof_radata_gz/` på Alexanders dator. Allt som byggts av den finns i `shof/riskklass_resultat/`.
- `shof/riskklass_resultat/test3/panel_test3.pkl` (116 MB). Byggs om med `test3/bygg.py`.
- `ler.xlsx` och `Search Results_*.xlsx`: misslyckade exporter ("User is not entitled to export this data").
