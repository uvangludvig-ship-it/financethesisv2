# analys_eu_slutlig_2026-11-19/

Slutlig körning av alla EU-test med de nedlagda klasserna, 19 nov 2026 (Claude). Deklaration och resultat finns i claude.ai-projektet: `DEKLARATION_slutlig_korning_A_B1_B2_2026-11-19` och `RESULTAT_slutlig_korning_A_B1_B2_2026-11-19`.

- **full** = A1–A3 + B1 + B2 (huvud). B2 saknar Institutional och Index Fund; okända klasser räknas som icke-institutionella, indexfonder känns igen på namnet.
- **b1** = A1–A3 + B1 (kontroll, utan B2).
- Saknas: klasser nedlagda efter 2025-06-30.

Koden är densamma som i `../analys_eu_2026-11-19/`, med fyra ändrade filer här:
- `bygg_bas.py` läser månadsserierna som tal, för att spara minne.
- `bd_eu_bygg.py` har namnregeln för indexfonder.
- `sicksack_eu_run.py` och `sicksack_eu_brusred.py` har urvalsstorleken för taggarna `full` och `b1`.

Körordningen är densamma som i `../analys_eu_2026-11-19/README.md`, med taggen `full` eller `b1` i stället för `bas`. Lägg B-filerna i basdatamappen. `bygg_bas.py` läser `A*.csv.gz` och `B*.csv.gz`.

`utdata_full/` och `utdata_b1/` innehåller utskrifterna från varje körning.
