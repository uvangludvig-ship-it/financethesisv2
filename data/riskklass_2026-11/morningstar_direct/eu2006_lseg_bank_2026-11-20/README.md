# eu2006_lseg_bank_2026-11-20/

Data, skript och utskrifter för två test som kördes 20 november 2026 av Claude i chatten med Alexander:

1. Ankarets händelsetest (Ben-David m.fl. 2022, avsnitt 3.3) på Morningstars metodbyte i Europa oktober 2006.
2. Bankägda mot fristående fondbolag (flöde per stjärna, 2003–2010 och 2018–2025).

**Ingen av författarna har kört om något här.** Skript 01–09 tar sina filer som argument och körs med `kor_2006.sh`. Skript 10–12 (banktestet) har fortfarande hårdkodade sökvägar till Claudes arbetsyta.

Licensierad data (Morningstar Direct, LSEG). Repot ska vara privat.

## radata/

| Fil | Innehåll | Källa | md5 |
|---|---|---|---|
| `direct_eu_1998_2010_075AE50B.csv.gz` | Direct-export, andelsklasser med domicil Luxemburg eller Irland. 18 423 rader, 16 233 klasser efter att 2 190 rader med SecId som börjar "0P" tagits bort (LU 13 035, IE 3 198). Monthly Return 1998-01 till 2010-12 (USD), Net Assets - share class och Morningstar Rating Overall 2000-01 till 2010-12, statiska fält inklusive Firm Name och Branding Name. Originalnamn `075AE50B9EE44D6490361581D37F9629_in_.csv` | Morningstar Direct (KTH), Alexander, 20 nov | gz 33ba41c2b314a428b02c4e6758b6c27e, okomprimerad af913b241fbd9f19cab3b9339929b89f |
| `direct_eu_2011_2016_020FAB82.csv.gz` | Förlängning för samma klasser: avkastning 2011-01 till 2016-12, NA och betyg 2010-12 till 2016-12, Fund Size - comprehensive 2002-12 till 2005-12. Originalnamn `020FAB82B8334F4496D96073CF8199C4_in_.csv` | Morningstar Direct, Alexander, 20 nov | gz 6d1a50553795ea90863649ba666f55a2, okomprimerad cdf0c7c20bb95c3be033bb28044c0c20 |
| `lseg_isin_list_2006.csv` | Beställningslistan till LSEG: 9 637 ISIN med SecId, FundId, namn, prioritet 1–3 | byggd ur exporten ovan | 4f29aa51a498b3b95fe77b69f10946f4 |
| `lseg_tna_2002_2008.csv.gz` | Fondförmögenhet per andelsklass och månad i USD ur LSEG (fältet `TR.FundTotalNetAssets`, 2002-12-31 till 2008-12-31, månadsvis). 383 502 rader, 7 723 ISIN med data. Kolumner ISIN, date, tna_usd | LSEG Data Library, hämtad av Alexander med `skript/03_lseg_hamta.py`, 20 nov | gz 58c689820b9120d3bb53da4775a8ccc8, okomprimerad 1f9567d9000343fb9ffef034d48b9920 |
| `lseg_missing.csv` | 1 914 ISIN som LSEG inte gav data för | samma körning | a1bede64c62c869c6ef1e83951fbec5c |

En första export (`A220A1490B144CDBAB32701240FB5720_in_.csv`) var kapad vid 30 000 rader och innehöll bara nedlagda fonder. Den används inte och ligger inte här.

## Kör om allt för 2006 med ett kommando

```
cd skript
bash kor_2006.sh
```

Kräver Python med pandas och numpy (i en egen miljö: `PY=python bash kor_2006.sh`). Tar 10–20 minuter. Skriptet går från de gzippade exporterna till alla utskrifter, lägger mellanfilerna i `arbete/` (ligger inte i git) och jämför varje utskrift med den sparade i `utdata/`. Kontrollerat 20 nov i en ren kopia av mapparna: alla fem utskrifter återges exakt. Indata utanför mappen: `../faktorer/Developed_3_Factors.csv` och `../analys_usa_2026-11-18/usa_ff3_mom_1986_2011.csv`.

## skript/ i körordning

| Nr | Skript | Gör | In | Ut |
|---|---|---|---|---|
| 01 | `01_tack.py` | Läser exporten 1998–2010, tar bort "0P"-rader, gör breda tabeller | `direct_eu_1998_2010…csv` | `raw06.pkl` |
| 02 | `02_sla_ihop.py` | Lägger till 2011–2016 och bygger riskfri ränta | `raw06.pkl`, exporten 2011–2016, `faktorer/Developed_3_Factors.csv`, USA-faktorerna | `raw16.pkl`, `rf16.csv` |
| 03 | `03_lseg_hamta.py` | Hämtar förmögenhet ur LSEG (körs på dator med LSEG Workspace) | `lseg_isin_list_2006.csv` | `lseg_tna_2002_2008.csv`, `lseg_missing.csv` |
| 04 | `04_koll_lseg.py` | Bred LSEG-tabell och täckning | LSEG-filerna | `lseg_wide.pkl` |
| 05 | `05_koll2.py` | Avstämning LSEG mot Direct där båda finns | | utskrift |
| 06 | `06_bygg_komb.py` | Fondmånadspanel. Argument: `raw16.pkl rf16.csv ut.pkl D|L|TEST lseg_wide.pkl`. D = Direct först, LSEG fyller. L = LSEG först. TEST = bara Direct | | `p_D.pkl`, `p_L.pkl`, `p_Direct.pkl` |
| 07 | `07_analys16.py` | Ankarets fyra test (andel betygsbyten, förklaringsgrad, flöde per stjärna per år, ekvation 2 med bootstrap och rang) | panel | `*_res.md` |
| 08 | `08_korn_bc.py` | Test B (Betyg×Efter×Äldre, Fama-MacBeth) och C (samma fonder före och efter) | panel | `*_res_bc.md` |
| 09 | `09_b_full.py` | Test B på bara Direct | | |
| 10 | `10_bygg_fb.py` | Fondbolag per fond ur Branding Name och Firm Name. **Rekonstruerad** ur kommandon som kördes direkt i terminalen | exporterna | `fb.pkl`, `fb_1825.pkl` |
| 11 | `11_klass.py` | Klassning bank, fristående, oklart | | `klassning_fondbolag.csv` |
| 12 | `12_kor_bank.py` | Banktestet på båda panelerna | `p_D.pkl`, `bd_eu_EU_full2.pkl` (byggs i `analys_eu_full2_2026-11-19/`) | `res_bank.md` |
| 13 | `13_lseg_hamta_mer.py` | Hämtar mer ur LSEG: förmögenhet 1999-12 till 2002-12 och fondbolag per ISIN. Skriven 20 nov. Bara `prov` är körd mot LSEG (Alexander, 20 nov): de tio testfonderna har ingen förmögenhet före 2003, `TR.FundCompany` ger samma namn med datum oktober 2006 som i dag, `TR.FundPromoter` och `TR.FundAdvisor` finns men licensen nekar, `TR.FundTER` fungerar. Slutsats: `tna` och `bolag` är inte värda att köra | `lseg_isin_list_2006.csv` | `lseg_tna_2000_2002.csv`, `lseg_missing_2000_2002.csv`, `lseg_fondbolag.csv` |

## Hur datan har hanterats (det som måste kontrolleras)

- **Urval:** bara SecId som börjar med F. Indexfonder bort. Fonden måste ha minst 10 MUSD månaden före.
- **Flöde per klass:** NA(t) − NA(t−1) × (1 + avkastning(t)). Bara när båda månaderna kommer från samma källa.
- **Flöde per fond:** summan över klasserna delad med summan av NA(t−1), i procent. Winsoriserat vid 1 och 99 procent inom varje månad.
- **Betyg per fond:** NA-vägt medel över klasserna, avrundat till heltal.
- **Signal:** 18 månaders exponentiellt vägd överavkastning, λ = 0,20551497 (ankarets kod).
- **LSEG mot Direct:** 223 960 klassmånader finns i båda. Medianen av kvoten är 1,0000. 87,0 % ligger inom 1 % och 92,9 % inom 5 %. Korrelationen mellan flödena är 0,933.
- **Fondbolag:** Branding Name och Firm Name är dagens namn. Klassningen i `11_klass.py` är Claudes, ur minnet, och är inte belagd rad för rad.

## utdata/

Utskrifterna från körningarna. `res_2006_test1_4_direct_forst.md` och `res_2006_test_B_C_direct_forst.md` är huvudkörningen. Deklarationer och tolkning ligger i Claude-projektet "thesis":

- `DEKLARATION_handelsetest_eu_oktober_2006_med_lseg_formogenhet_2026-11-20`, `RESULTAT_…`
- `NOTIS_ankaret_last_i_sin_helhet_reformtesten_mot_vart_2006_2026-11-20`
- `DEKLARATION_bankagda_mot_fristaende_fondbolag_2026-11-20`, `RESULTAT_…`
