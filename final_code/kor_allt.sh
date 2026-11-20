#!/bin/bash
# Kor allt: radata -> paneler -> test -> tabeller och figurer -> final.pdf
#   bash kor_allt.sh                (python3)
#   PY=python bash kor_allt.sh      (i en egen miljo)
#   bash kor_allt.sh test           (hoppa over panelbygget; kraver att _arbete/ redan finns)
# Kraver: pandas, numpy, scipy, matplotlib; pdflatex for sista steget. Tar cirka en timme forsta gangen.
set -e
cd "$(dirname "$0")"; K=$(pwd); PY=${PY:-python3}
eval "$($PY -c "import config as c; print(f'MD=\"{c.MD}\"; OV=\"{c.OVRIGT}\"; A=\"{c.ARBETE}\"; UT=\"{c.UT}\"')")"
cd "$A"
if [ "$1" != "test" ]; then
echo "1/8 USA 1991-2011: fondpanel"
$PY "$K/bygg/usa_panel.py" "$MD/exporter_2026-11-18/BA37C8D419E2470DA22839DB972EB065.csv.gz" "$MD/analys_usa_2026-11-18/usa_ff3_mom_1986_2011.csv" usa_panel.pkl > logg_usa_panel.txt 2>&1
echo "2/8 Europa 2018-2025: basfil, etiketter, klasspanel, urval"
$PY "$K/bygg/eu_1_bas.py" "$MD/bas_eu_2026-11-19" "$OV/eurofxref-hist.zip" > logg_eu_1_bas.txt 2>&1
$PY "$K/bygg/eu_2_etiketter.py" bas_raw.pkl fx_month.pkl etiketter_eu_bas.pkl > logg_eu_2_etiketter.txt 2>&1
$PY "$K/bygg/eu_3_klasspanel.py" bas_raw.pkl etiketter_eu_bas.pkl bas > logg_eu_3_klasspanel.txt 2>&1
$PY "$K/bygg/eu_4_urval.py" bas > logg_eu_4_urval.txt 2>&1
echo "3/8 Europa 2018-2025: fondpaneler (EU-klasser och alla KID-klasser)"
$PY "$K/bygg/eu_5_fondpanel.py" bas EU "$MD/faktorer" bd_eu_EU.pkl > logg_eu_5_EU.txt 2>&1
$PY "$K/bygg/eu_5_fondpanel.py" bas kid "$MD/faktorer" bd_eu_kid.pkl > logg_eu_5_kid.txt 2>&1
echo "4/8 Europa 2003-2016: fondpaneler (Direct forst, LSEG forst, bara Direct)"
R="$MD/eu2006_lseg_bank_2026-11-20/radata"
$PY "$K/bygg/eu2006_1_las_export.py" "$R/direct_eu_1998_2010_075AE50B.csv.gz" > logg_eu2006_1.txt 2>&1
$PY "$K/bygg/eu2006_2_forlang.py" raw06.pkl "$R/direct_eu_2011_2016_020FAB82.csv.gz" raw16.pkl "$MD/faktorer/Developed_3_Factors.csv" "$MD/analys_usa_2026-11-18/usa_ff3_mom_1986_2011.csv" rf16.csv > logg_eu2006_2.txt 2>&1
$PY "$K/bygg/eu2006_3_lseg.py" "$R/lseg_tna_2002_2008.csv.gz" "$R/lseg_missing.csv" "$R/lseg_isin_list_2006.csv" raw16.pkl lseg_wide.pkl > logg_eu2006_3.txt 2>&1
$PY "$K/bygg/eu2006_4_fondpanel.py" raw16.pkl rf16.csv p_D.pkl D lseg_wide.pkl > logg_eu2006_4_D.txt 2>&1
$PY "$K/bygg/eu2006_4_fondpanel.py" raw16.pkl rf16.csv p_L.pkl L lseg_wide.pkl > logg_eu2006_4_L.txt 2>&1
$PY "$K/bygg/eu2006_4_fondpanel.py" raw16.pkl rf16.csv p_Direct.pkl TEST lseg_wide.pkl > logg_eu2006_4_Direct.txt 2>&1
fi
cd "$K"
echo "5/8 test: USA";               $PY test/usa.py      > "$A/logg_test_usa.txt" 2>&1
$PY test/tabell3_former.py > "$A/logg_test_tabell3_former.txt" 2>&1
echo "6/8 test: Europa 2018-2025 och bytet 2023"; $PY test/eu.py > "$A/logg_test_eu.txt" 2>&1; $PY test/byte2023.py > "$A/logg_test_byte2023.txt" 2>&1
echo "7/8 test: Europa 2006";       $PY test/eu2006.py   > "$A/logg_test_eu2006.txt" 2>&1
echo "8/8 tabeller, figurer och dokument"
$PY tabeller_figurer.py > "$A/logg_tabeller.txt" 2>&1
if command -v pdflatex > /dev/null; then (cd "$UT" && pdflatex -interaction=nonstopmode final.tex > /dev/null && pdflatex -interaction=nonstopmode final.tex > /dev/null && echo "final.pdf byggd"); else echo "pdflatex saknas: final.tex ar inte kompilerad"; fi
echo "Klart. Resultat i $UT"
