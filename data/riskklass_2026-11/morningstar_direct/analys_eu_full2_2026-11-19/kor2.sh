cd /home/claude/slut/full2
M=/mnt/user-data/uploads/financethesisv2/data/riskklass_2026-11/morningstar_direct
date > tid.log
python3 -I sicksack_eu_run.py . full2 > res_sicksack_del1.txt 2>&1; echo "del1 $? $(date)" >> tid.log
python3 -I sicksack_eu_brusred.py . full2 $M > res_sicksack_del2.txt 2>&1; echo "del2 $? $(date)" >> tid.log
python3 -I ukeu_run.py full2 > res_ukeu.txt 2>&1; echo "ukeu $? $(date)" >> tid.log
python3 -I ukeu_kanal_bygg.py full2 > res_ukeu_kanal_bygg.txt 2>&1; echo "kanalbygg $? $(date)" >> tid.log
python3 -I ukeu_kanal_run.py full2 > res_ukeu_kanal.txt 2>&1; echo "kanal $? $(date)" >> tid.log
python3 -I bd_eu_analys.py bd_eu_EU_full2.pkl kod 2>&1 | grep -v Warning > res_bd_EU.txt; echo "bdEU $? $(date)" >> tid.log
python3 -I bd_eu_analys.py bd_eu_kid_full2.pkl kod 2>&1 | grep -v Warning > res_bd_kid.txt; echo "bdkid $? $(date)" >> tid.log
python3 -I bd_eu_handelse.py bd_eu_EU_full2.pkl > res_handelse_EU.txt 2>&1; echo "hEU $? $(date)" >> tid.log
python3 -I bd_eu_handelse.py bd_eu_kid_full2.pkl > res_handelse_kid.txt 2>&1; echo "hkid $? $(date)" >> tid.log
echo KLAR > klar.txt
