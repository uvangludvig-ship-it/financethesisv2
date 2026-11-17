# build/

Kod som hämtar data till `../raw/` eller bygger `../derived/` ur den. Skripten är kopierade oförändrade från gamla repot. Alla hittar repots rot via sin egen sökväg, så de kan köras från vilken mapp som helst.

| Skript | Läser | Skriver | Kommentar |
|---|---|---|---|
| `build_ppm_panel_2018.py` | `raw/ppm/*/*/*.xlsm` från 2018 | `derived/ppm/ppm_panel_2018_2026.csv` | Kräver pandas och openpyxl. Kan köras som det är |
| `shof_monthly.py` | `raw/shof/Valuations/*.csv` och `raw/shof/Reinvestments/*.csv` | `derived/shof_monthly/` | De dagliga exporterna finns inte i repot (se `raw/shof/README.md`). Kommentaren i skriptet hänvisar till `data/MANIFEST.md`, som bara finns i gamla repot. Här är det `raw/shof/README.md` som gäller |
| `collect_ap_fi_20261031.py` | AP-fondernas webbplatser (HTTP) | `raw/ap/`, `raw/fi_short/`, `raw/ap/_collection_20261031/` | Kördes 31 okt 2026. Skriptet vägrar skriva över befintliga filer. FI:s blankningsregister fick hämtas för hand i webbläsaren eftersom direkta anrop gav 404 |

```bash
python data/build/build_ppm_panel_2018.py
```

Byggkoden för `derived/fi/` och `derived/ap/` (RIC-matchningen) finns bara i gamla repot, eftersom den hänger ihop med tidigare ämnen; se `../derived/README.md`. LSEG-datan hämtades i LSEG Workspace CodeBook med ett skript som inte är överfört.
