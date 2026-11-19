# analys_eu_2026-11-19/

Kod och utdata för testen på den europeiska basdatan (`../bas_eu_2026-11-19/`, A1–A3, överlevande LU- och IE-klasser). Körd av Claude 19 nov 2026. **Preliminärt:** grupp B (nedlagda klasser) saknas. Inget är omkört av en människa än.

Deklarationer och resultat ligger i claude.ai-projektet "thesis" (mappen `claude/`). Varje test deklarerades innan det kördes:

| Test | Deklaration | Resultat |
|---|---|---|
| Sicksacken, A1 | `DEKLARATION_sicksack_eu_preliminar_2026-11-19` | `RESULTAT_sicksack_eu_preliminar_2026-11-19` |
| Sicksacken, A1–A3, deklarerad och brusreducerad | `DEKLARATION_sicksack_eu_A1_A3_och_brusreducerad_2026-11-19` | `RESULTAT_sicksack_eu_A1_A3_och_brusreducerad_2026-11-19` |
| UK mot EU, nivåskift och dos | `DEKLARATION_uk_mot_eu_A1_A3_2026-11-19` | `RESULTAT_uk_mot_eu_A1_A3_2026-11-19` |
| UK mot EU, kanaltest (avkastning, kostnad) | `DEKLARATION_uk_mot_eu_kanaltest_avkastning_kostnad_2026-11-19` | `RESULTAT_uk_mot_eu_kanaltest_avkastning_kostnad_2026-11-19` |
| Ben-David på EU och hästkapplöpningen | `DEKLARATION_bendavid_eu_och_hastkapplopning_A1_A3_2026-11-19` | `RESULTAT_bendavid_eu_och_hastkapplopning_A1_A3_2026-11-19` |
| Brusval (låtsasår, inga utfall) | | `NOTIS_brus_sicksack_eu_latsas_2026-11-19`, `NOTIS_shof_plus_direct_sicksack_2026-11-19` |

## Körordning

Kopiera mappen till en arbetsmapp utanför repot och kör där, så hamnar de stora .pkl-filerna inte i git. Skripten läser varandra och mellanfilerna ur arbetsmappen. Alla körs med `python3 -I`. `MD` = sökvägen till repots `data/riskklass_2026-11/morningstar_direct`.

```
python3 -I bygg_bas.py $MD/bas_eu_2026-11-19 $MD/../ovrigt/eurofxref-hist.zip   # -> bas_raw.pkl, fx_month.pkl
python3 -I bygg_etiketter_eu.py bas_raw.pkl fx_month.pkl etiketter_eu_bas.pkl
python3 -I bygg_panel_eu.py bas_raw.pkl etiketter_eu_bas.pkl bas                                  # -> panel_eu_bas.pkl, urval_eu_bas.pkl
python3 -I urval_eu.py bas                                                                         # -> huvudklasser_eu_bas.pkl
# sicksacken
python3 -I sicksack_eu_run.py . bas                                                                # del I (deklarerad)
python3 -I sicksack_eu_brusred.py . bas $MD                                                        # del II (brusreducerad; C3 läser SHoF-panelen i $MD)
# UK mot EU
python3 -I ukeu_bygg.py bas && python3 -I ukeu_run.py bas
python3 -I ukeu_kanal_bygg.py bas && python3 -I ukeu_kanal_run.py bas
# Ben-David och hästkapplöpningen
python3 -I bd_eu_bygg.py bas EU $MD/faktorer bd_eu_EU.pkl && python3 -I bd_eu_analys.py bd_eu_EU.pkl kod
python3 -I bd_eu_bygg.py bas kid $MD/faktorer bd_eu_kid.pkl && python3 -I bd_eu_analys.py bd_eu_kid.pkl kod
```

Brusvalet på låtsasår, som bara använder flöden till och med december 2022: `brus_latsas.py`, `pool_latsas.py` (med `sicksack_funk.py`), `diag_se.py`. Dessa kördes på A1 (tag `a1`). Skripten läser `*_a1.pkl`.

## Utdata (som de blev 19 nov)

`utdata/`: utskrifterna från varje körning (`resultat_*.txt`), Ben-David-tabellerna (`bd_eu_*_resultat_kod.md`) och händelsestudierna (`sicksack_eu_handelsstudie_*.csv`).

## När grupp B kommer

Lägg filerna som `B*.csv.gz` i `bas_eu_2026-11-19/` och kör allt ovan igen. Skripten innehåller kontroller av urvalets storlek (`assert len(B) == ...`) som då måste uppdateras.
