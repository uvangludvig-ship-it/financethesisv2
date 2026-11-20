# analys_eu_full2_2026-11-19/

Skript och utskrifter för den slutliga körningen på europeiska fonder 2018–2025 ("full2"): basdata A1–A3, B1 och den nya B2 (med Institutional och Index Fund). Ersätter `analys_eu_slutlig_2026-11-19/` (som använde den första B2-exporten). Kört 19 november 2026 av Claude i chatten med Alexander. **Ingen av författarna har kört om något.**

Indata: `../bas_eu_2026-11-19/` (A1, A2, A3, B1, B2), `../faktorer/`, `../uk_eu/`. Skripten har hårdkodade sökvägar till Claudes arbetsyta som måste ändras.

Körordning: `bygg_bas.py`, `bygg_panel_eu.py`, `bygg_etiketter_eu.py`, `urval_eu.py`, `bd_eu_bygg.py`, sedan `kor2.sh` (sicksacken, UK mot EU, kanaltestet, Ben-David på EU med hästkapplöpningen, händelsetestet januari 2023). `kor.sh` är samma körning på den gamla B2-filen.

Utskrifter i `utdata/`. Deklaration och resultat i Claude-projektet: `DEKLARATION_omkorning_full2_ny_B2_2026-11-19`, `RESULTAT_omkorning_full2_ny_B2_2026-11-19`.

Test som kördes senare på samma panel av andra chattar (skripten ligger i Claude-projektet, inte här): `bd_eu_fm.py`, `acf_rz_form.py`, `es_trippel.py`, `cci_form.py`, `bd_eu_vol_tre_kolumner.py`.
