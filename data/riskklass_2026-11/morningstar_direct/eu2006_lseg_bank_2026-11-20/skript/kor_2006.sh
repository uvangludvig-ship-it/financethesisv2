#!/bin/bash
# Kor hela 2006-kedjan fran radata till utskrifter. Tar cirka 10-20 minuter.
#   bash kor_2006.sh            (anvander python3)
#   PY=python bash kor_2006.sh  (om du star i en egen miljo, t.ex. lseg_env)
# Kraver pandas och numpy. Mellanfiler och utskrifter hamnar i ../arbete/ (ligger inte i git).
set -e
cd "$(dirname "$0")"; S=$(pwd); R=$S/../radata; F=$S/../../faktorer; U=$S/../../analys_usa_2026-11-18
A=$S/../arbete; mkdir -p "$A"; cd "$A"; PY=${PY:-python3}
echo "1/8 laser exporten 1998-2010";      $PY "$S/01_tack.py" "$R/direct_eu_1998_2010_075AE50B.csv.gz" > logg_01_tack.txt 2>&1
echo "2/8 lagger till 2011-2016";         $PY "$S/02_sla_ihop.py" raw06.pkl "$R/direct_eu_2011_2016_020FAB82.csv.gz" raw16.pkl "$F/Developed_3_Factors.csv" "$U/usa_ff3_mom_1986_2011.csv" rf16.csv > logg_02_sla_ihop.txt 2>&1
echo "3/8 LSEG: bred tabell och tackning"; $PY "$S/04_koll_lseg.py" "$R/lseg_tna_2002_2008.csv.gz" "$R/lseg_missing.csv" "$R/lseg_isin_list_2006.csv" raw16.pkl lseg_wide.pkl > logg_04_koll_lseg.txt 2>&1
echo "4/8 LSEG mot Direct";               $PY "$S/05_koll2.py" raw16.pkl lseg_wide.pkl > logg_05_koll2.txt 2>&1
echo "5/8 paneler";                       $PY "$S/06_bygg_komb.py" raw16.pkl rf16.csv p_D.pkl D lseg_wide.pkl > logg_06_p_D.txt 2>&1
                                          $PY "$S/06_bygg_komb.py" raw16.pkl rf16.csv p_L.pkl L lseg_wide.pkl > logg_06_p_L.txt 2>&1
                                          $PY "$S/06_bygg_komb.py" raw16.pkl rf16.csv p_Direct.pkl TEST lseg_wide.pkl > logg_06_p_Direct.txt 2>&1
echo "6/8 ankarets fyra test";            for p in p_D p_L p_Direct; do $PY "$S/07_analys16.py" $p.pkl > logg_07_$p.txt 2>&1; done
echo "7/8 test B och C";                  for p in p_D p_L p_Direct; do $PY "$S/08_korn_bc.py" $p.pkl > logg_08_$p.txt 2>&1; done
echo "8/8 jamfor med sparade utskrifter"
T=$S/../utdata; ok=1
for par in "p_D_res.md:res_2006_test1_4_direct_forst.md" "p_L_res.md:res_2006_test1_4_lseg_forst.md" "p_D_res_bc.md:res_2006_test_B_C_direct_forst.md" "p_L_res_bc.md:res_2006_test_B_C_lseg_forst.md" "p_Direct_res_bc.md:res_2006_test_B_C_bara_direct.md"; do
  n=${par%%:*}; g=${par##*:}
  if diff -q "$n" "$T/$g" > /dev/null; then echo "  LIKA      $n"; else echo "  SKILJER   $n  (se: diff $A/$n $T/$g)"; ok=0; fi
done
[ $ok = 1 ] && echo "Allt aterges exakt." || echo "Nagot skiljer sig. Skicka raderna ovan till Claude."
