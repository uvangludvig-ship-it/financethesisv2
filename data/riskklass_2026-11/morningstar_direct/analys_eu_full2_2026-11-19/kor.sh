cd /home/claude/slut/full
python3 -I sicksack_eu_run.py . full > res_sicksack_del1.txt 2>&1
python3 -I sicksack_eu_brusred.py . full /mnt/user-data/uploads/financethesisv2/data/riskklass_2026-11/morningstar_direct > res_sicksack_del2.txt 2>&1
python3 -I ukeu_run.py full > res_ukeu.txt 2>&1
python3 -I ukeu_kanal_bygg.py full > res_ukeu_kanal_bygg.txt 2>&1 && python3 -I ukeu_kanal_run.py full > res_ukeu_kanal.txt 2>&1
python3 -I bd_eu_analys.py bd_eu_EU_full.pkl kod 2>&1 | grep -v Warning > res_bd_EU.txt
python3 -I bd_eu_analys.py bd_eu_kid_full.pkl kod 2>&1 | grep -v Warning > res_bd_kid.txt
echo KLAR > klar.txt
