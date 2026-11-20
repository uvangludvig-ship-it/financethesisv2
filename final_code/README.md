# final_code

All kod som ger talen i `final_result/`. Skriven av AI (Claude) 20 november 2026. Ingen av författarna har kört den ännu.

**Regel: inget eget test.** Varje test är Ben-David m.fl. (2022) eller Adelino m.fl. (2017), ur artikeln eller författarnas kod. Egna test och varianter ströks 20 november; listan står i `KONTROLL.md`.

## Köra

```
cd final_code
source ~/lseg_env/bin/activate        # eller en annan miljö med pandas, numpy, scipy, matplotlib
PY=python bash kor_allt.sh            # rådata -> paneler -> test -> tabeller, figurer, final.pdf
PY=python bash kor_allt.sh test       # hoppar över panelbygget (kräver att _arbete/ finns)
```

Första körningen tog ungefär 20 minuter här. Minnesåtgången är inte mätt; den största mellanfilen är 0,8 GB. Sista steget kräver `pdflatex`; saknas det byggs allt utom `final.pdf`.

## Vad som behövs i repot

| Sökväg under `data/riskklass_2026-11/` | Innehåll |
|---|---|
| `morningstar_direct/exporter_2026-11-18/BA37C8D419E2470DA22839DB972EB065.csv.gz` | USA, Morningstar Direct |
| `morningstar_direct/bas_eu_2026-11-19/` (A1, A2, A3, B1, B2) | Europa 2013 till 2025 |
| `morningstar_direct/eu2006_lseg_bank_2026-11-20/radata/` | Europa 1998 till 2016 och LSEG |
| `morningstar_direct/faktorer/` | Fama-Frenchs Developed- och Europe-faktorer |
| `morningstar_direct/analys_usa_2026-11-18/usa_ff3_mom_1986_2011.csv` | Amerikanska faktorer |
| `ovrigt/eurofxref-hist.zip` | ECB:s valutakurser |

Datan är licensierad. Repot ska vara privat.

## Mappar

| Mapp | Innehåll |
|---|---|
| `config.py` | Sökvägar och ankarets konstanter (lambda, 60 månader, minst 36, 10 MUSD, winsorisering 1/99) |
| `bygg/` | Rådata till fondpaneler. De ursprungliga skripten, oförändrade i sak |
| `lib/stat.py` | OLS med fasta effekter, kluster på fond och månad, Fama-MacBeth, Newey-West, förklaringsgrad |
| `lib/ankartest.py` | Ankarets test som funktioner: `table1`, `table2`, `fig3`, `fig4`, `table3`, `fig5a`, `fore_efter`, `andel_andrad`, `table4b`, `fig5b` |
| `test/usa.py` | USA 1997 till 2011: ankarets avsnitt 3.1 till 3.3 |
| `test/eu.py` | Europa 2018 till 2025: samma test, risksiffran som tredje signal, januari 2023 i ankarets tabell 4-form |
| `test/eu2006.py` | Europa, oktober 2006: ankarets tabell 4 och figur 5, med tre sätt att slå ihop Morningstar och LSEG |
| `test/byte2023.py` | Bytet 1 januari 2023 i Adelino, Cunha och Ferreiras form |
| `test/tabell3_former.py` | Ankarets tabell 3 i kodens och textens form |
| `KONTROLL.md` | Hur talen är avstämda och vad som rättades 20 november |
| `tabeller_figurer.py` | `final_result/tal/*.csv` till `tabeller/*.tex` och `figurer/*.pdf` |
| `kor_allt.sh` | Kör allt i ordning |
| `_arbete/` | Byggda paneler och loggar. Ligger inte i git |

## Vilken funktion ger vilken tabell

| I `final.pdf` | Funktion | Förlaga |
|---|---|---|
| Tabell 1 | `ankartest.table1` | Ben-David m.fl. (2022) tabell 1, s. 1734 |
| Tabell 2 A, bilaga A1 | `ankartest.table3` | tabell 3, s. 1744; kodens avsnitt "Table 3 (Flows to Top-Ranked Funds ...)" |
| Tabell 2 B | `ankartest.fig3` | figur 3, s. 1741 |
| Figur 2 | `ankartest.fig5a` | figur 5 A(b), s. 1747 |
| Tabellen under figur 2 | `ankartest.fore_efter` | samma regression i två perioder; skillnaden räknar ankaret inte ut |
| Figur 1, tabell 3 A och B, tabell 5 | `ankartest.andel_andrad`, `table4b` | tabell 4, s. 1746 |
| Figur 3 | `ankartest.fig5b` | ekvation 2, s. 1749; figur 5 B, s. 1747 |
| Tabell 4 | `test/eu.py:tredje_signal` | figur 5 A(b) med risksiffran tillagd; Fama-MacBeth enligt bilaga B.3, s. 1767 |
| Tabell 6, figur 4, bilaga A5 | `test/byte2023.py` | Adelino m.fl. (2017) ekvation 1, s. 3236; figur 4, s. 3243; uppdelning per steg enligt deras tabell IA.5 (nämnd s. 3242) |
| Bilaga A2 | `ankartest.table2` | tabell 2, s. 1736 till 1737 |
| Bilaga A3 | `ankartest.fig4` | figur 4, s. 1743 |
| Bilaga A4 | `test/eu.py`, `test/tabell3_former.py` | ankarets tabell 3 på andra data och i textens form |
| Bilaga A6 | `test/eu2006.py` | ankarets test med andra datakällor |

Slumptalsfrön: USA 20261118, Europa 2006 20261120. Med dem återges bootstrapintervallen exakt.

## Inte med

- UK mot EU (bilaga A8). Skripten ligger i `data/riskklass_2026-11/morningstar_direct/analys_eu_full2_2026-11-19/`.
- Banktestet. Skripten ligger i `eu2006_lseg_bank_2026-11-20/skript/`.
- Egna test (strukna 20 november, se `KONTROLL.md`).

Se `KONTROLL.md` för hur talen är avstämda.
