# raw/ap/: AP-fondernas innehavslistor

Offentliga pdf:er. AP1–AP4 publicerar sina aktieinnehav, oftast per halvår. Hämtade 31 okt 2026 med `../../build/collect_ap_fi_20261031.py`.

| Mapp eller fil | Innehåll |
|---|---|
| `AP1/` | 2 pdf: 2025-06-30 och 2025-12-31. AP1 lades ned 31 dec 2025, och äldre listor gick inte att hitta |
| `AP2/` | 47 pdf, 2015–2026 (svenska och utländska aktier i separata filer) |
| `AP3/` | 38 pdf, 2017–2026 |
| `AP4/` | 24 pdf, 2015–2026 |
| `INSAMLINGSLOGG_2026-10-31.md` | **Läs den först.** Vilka halvår som fanns och vilka som saknas, hur "svenska aktier" definierades, kända egenheter per fond och kontroller |
| `download_log_2026-10-31.csv` | Varje hämtningsförsök med URL, tid i UTC, sökväg, storlek, SHA-256 och eventuellt fel |
| `_collection_20261031/` | Sidorna och länklistorna som skriptet läste (html, json), täckning per fond och halvår (`coverage.csv`, `missing_lists.csv`) och kontroller |

Viktigt från insamlingsloggen:

- 66 av 112 efterfrågade kombinationer av fond och halvår har data.
- En saknad lista betyder inte att fonden saknade innehav.
- AP2:s antal är på många listor **netto efter utlånade aktier**.
- AP4 slår ibland ihop aktieslag.

Tolkade tabeller: [`../../derived/ap/`](../../derived/README.md#ap).
