# raw/ppm/: Pensionsmyndighetens fondstatistik

Statistik om premiepensionen per fond och månad, offentlig från Pensionsmyndigheten. Hämtad i september och oktober 2026. Mappen har 311 filer.

| Mapp eller fil | Innehåll |
|---|---|
| `2001-2008/` (95), `2009-2014/` (72), `2015-2020/` (73), `2021-2026/` (68) | Månadsstatistik per fond, en fil per månadsslut i årsmappar, januari 2001 till augusti 2026. Format och namn byts över tid: `PPM 010131.xls`, `PM 140131.xlsm`, `Statistik Premiepension 2018-01-31.xlsm`, `Statistik-Premiepension-2021-01-31.xlsm` |
| `Lista alla fonder 2026.xls` | Pensionsmyndighetens fondlista 2026 |
| `ppm_nav_2024.xlsx` | Dagliga fondkurser för 451 fonder, **bara 2024-01-02 till 2024-03-28** (63 dagar): fondbolag, fondnummer, fondnamn, datum, köp- och säljkurs, valutakurs och kurs i SEK |
| `FEES.txt` | **Kommer inte från Pensionsmyndigheten.** Avgifter i Morningstars format från SHoF (`performanceid`, `secid`, prospektdatum, avgiftstyp, belopp, brytpunkter): 347 401 rader, prospektdatum 2002-04-01 till 2026-01-14. 99,99 procent av `performanceid` finns i SHoF:s fondregister. Licensierad som SHoF-datan |

Panel per fond och månad för 2018 och framåt: `../../derived/ppm/ppm_panel_2018_2026.csv`, byggd med `../../build/build_ppm_panel_2018.py`.
