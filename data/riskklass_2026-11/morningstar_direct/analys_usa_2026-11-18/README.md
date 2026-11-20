# analys_usa_2026-11-18/

Skript och utskrifter för replikeringen av Ben-David, Li, Rossi och Song (2022) på amerikanska aktiefonder, körd 18–19 november 2026 av Claude i chatten med Alexander. **Ingen av författarna har kört om något.** Skripten har sökvägar till Claudes arbetsyta som måste ändras.

Indata: `../exporter_2026-11-18/` (Direct-exporterna för USA 1991–2011) och `../faktorer/` (Fama-French).

| Skript | Gör |
|---|---|
| `bygg_panel_full.py` | Fondmånadspanel 1997–2011 (huvudkörningen) |
| `analys_full.py` | Table 2, 3, 4, Figure 3, 4, 5A, 5B |
| `analys_kod.py`, `table3_kod.py` | Samma test i den form författarnas kod har (Table 3: halva skillnaden, ingen månadseffekt) |
| `kontroll_full.py` | Kontroller av panelen |
| `vassare.py` | Varianter närmare ankaret (se `NOTIS_usa_replikering_narmare_ankaret_2026-11-19` i Claude-projektet) |
| `bygg_panel.py`, `analys.py`, `kontroll.py`, `diagnos.py` | Första körningen 1999–2005, ersatt av 1997–2011 |

Utskrifter i `utdata/`. Deklaration och resultat i Claude-projektet: `DEKLARATION_replikering_bendavid_usa_1997_2011_2026-11-18`, `RESULTAT_replikering_bendavid_usa_1997_2011_2026-11-18`, `JAMFORELSE_bendavid_kod_mot_var_replikering_2026-11-18`.
