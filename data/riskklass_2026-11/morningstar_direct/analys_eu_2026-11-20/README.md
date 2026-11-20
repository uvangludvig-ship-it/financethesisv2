# analys_eu_2026-11-20/

Kod och utdata för testen som kördes 20 nov 2026 på den europeiska basdatan (`../bas_eu_2026-11-19/`, A1–A3 och nedlagda klasser B1–B2). Körd av Claude. **Inget är omkört av en människa.** Testen är inte blinda: flera upplägg var körda innan, och det står i varje deklaration vad som var känt.

Deklarationer (sparade före körning) och resultat ligger i claude.ai-projektet "thesis", mappen `claude/`.

## Begrepp

- **Bytet 2023:** den 1 januari 2023 ersattes risksiffran SRRI (1–7, i faktabladet KIID) av SRI (1–7, i PRIIP-faktabladet). De flesta fonder fick en lägre siffra.
- **Dos:** antal steg fondens visade risksiffra föll vid bytet (0, 1 eller 2).
- **Efter:** 1 från januari 2023, annars 0.
- **"Sicksacken":** vårt arbetsnamn på regressionen flöde = b·Dos×Efter + Efter×tredjegradspolynom i fondens volatilitet + Efter×fondens medelflöde 2021–2022 + fondeffekt + kategori×månad-effekt. Namnet kommer av att Dos går upp och ned (2, 1, 2, 1 …) när volatiliteten stiger, eftersom gränserna för SRRI och SRI ligger olika.
- **Enhet:** procentenheter av förmögenheten per år, per steg i Dos.

## Test

| Skript | Vad det gör | Deklaration | Resultat |
|---|---|---|---|
| `acf_rz_form.py` | Test A: bytet 2023 i formen från Adelino, Cunha och Ferreira (2017, RFS), ekvation 1: flöde = b·Dos×Efter + fondeffekt + kategori×månad-effekt + volatilitetsdecil×månad-effekt, kluster på fond. Test B: tvärsnittet från Reuter och Zitzewitz (NBER WP 16329), avsnitt IV.F: flöde 2023 per fond på Dos, med gammal riskklass, volatilitet, flöde 2022 och kategori | `DEKLARATION_adelino_form_och_reuter_zitzewitz_reformform_2026-11-20` | `RESULTAT_adelino_form_rz_reformform_och_fama_macbeth_2026-11-20` |
| `bd_eu_fm.py` | Regressionen där visad riskklass läggs till stjärnbetyg och avkastning som förklaring av flöden, skattad med Fama-MacBeth (en regression per månad, Newey-West med sex laggar), som i ankarets tabell 6 kolumn 4 och tabell B.I | `DEKLARATION_riskklass_tredje_signal_fama_macbeth_2026-11-20` | samma resultatdokument, avsnitt 3 |
| `cci_form.py` | Bytet 2023 i formerna från Cornaggia, Cornaggia och Israelsen (2018, RFS): Dos×Efter med fond- och månadseffekter (deras tabell 4 panel B), och med Efter×gammal riskklass (deras tabell 6 panel B) | `DEKLARATION_cornaggia_form_steg_ganger_efter_2026-11-20` | `RESULTAT_cornaggia_form_steg_ganger_efter_2026-11-20` |
| `cci_diag.py` | Utforskande, inte deklarerat: varför formen i `cci_form.py` har en trend före bytet | | `NOTIS_varfor_cornaggia_formen_inte_racker_2026-11-20` |
| `es_trippel.py` | Skillnaden i flöde mellan privat och institutionell andelsklass i samma fond och månad, på Dos×Efter. Närmaste förlaga är Hartzmark och Sussman (2019, JF), tabell 7 kolumn 4, inte Evans och Sun som filnamnet och deklarationen säger | `DEKLARATION_evans_sun_privat_mot_institutionell_2026-11-20` | `RESULTAT_evans_sun_privat_mot_institutionell_2026-11-20` |
| `bd_eu_vol_tre_kolumner.py` | Flöde på fondens volatilitet, utan och med stjärnbetyg, och med visad riskklass. Förlagan är tabell VII i ankarets utkast från 2018; tabellen finns inte i den tryckta artikeln | `DEKLARATION_volatilitet_stjarnor_riskklass_tre_kolumner_2026-11-20` | `RESULTAT_volatilitet_stjarnor_riskklass_tre_kolumner_2026-11-20` |

## Huvudtal (ur `utdata/`, kontrollerade mot utskrifterna)

| Test | Skattning | SE | 95 % | Källa |
|---|---|---|---|---|
| Adelino-formen, huvud (A1) | +0,07 | 0,69 | −1,29 till +1,42 | `res_acf_rz.txt` |
| Adelino-formen utan volatilitetsdecil (A2) | +0,56 | 0,67 | −0,75 till +1,87 | `res_acf_rz.txt` |
| Adelino-formen, winsorisering 1/99 (A5) | +0,01 | 0,83 | −1,60 till +1,63 | `res_acf_rz.txt` |
| "Sicksacken", återgiven i samma skript | +0,47 | 0,52 | −0,54 till +1,49 | `res_acf_rz.txt` |
| Reuter–Zitzewitz tvärsnitt (B1) | +0,28 | 0,69 | −1,07 till +1,63 | `res_acf_rz.txt` |
| Riskklass, Fama-MacBeth (F1) | +0,61 | 0,66 | −0,67 till +1,90 | `res_bd_eu_fm.txt` |
| Riskklass, poolad, samma urval | +0,80 | 0,98 | −1,11 till +2,72 | `res_bd_eu_fm.txt` |

Adelino-formen, kontroller: gemensamt test av Dos×kvartal före bytet p 0,587; låtsasbyte januari 2021 +0,07 (SE 0,86); inplanterad effekt +3,00 återfås som +3,000. Urval: 4 818 fonder, 230 531 fondmånader, januari 2021–december 2024.

## Körordning

Bygg först mellanfilerna enligt `../analys_eu_2026-11-19/README.md` (`bas_raw.pkl`, `etiketter_eu_bas.pkl`, `panel_eu_bas.pkl`, `urval_eu_bas.pkl`, `huvudklasser_eu_bas.pkl`, `bd_eu_EU.pkl`) i en arbetsmapp utanför repot. `huvudklasser_eu_bas.pkl` ska ha 4 818 fonder; skripten avbryter annars. Kopiera sedan skripten hit till arbetsmappen och kör där:

```
python3 -I acf_rz_form.py .                       # jfr utdata/res_acf_rz.txt
python3 -I bd_eu_fm.py bd_eu_EU.pkl               # jfr utdata/res_bd_eu_fm.txt
python3 -I cci_form.py .                          # jfr utdata/res_cci_form.txt
python3 -I cci_diag.py .                          # läser cci_form.py i samma mapp; jfr utdata/res_cci_diag.txt
python3 -I es_trippel.py .                        # jfr utdata/res_es_trippel.txt
python3 -I bd_eu_vol_tre_kolumner.py bd_eu_EU.pkl res_vol3.md   # jfr utdata/res_vol3_full2.md
```

`acf_rz_form.py` tar knappt en minut.

## Utdata

`utdata/`: utskrifterna som de blev 20 nov. De innehåller bara skattningar och antal, inga fonduppgifter.

## Kända brister

- Winsoriseringen i huvudtalet är 2,5/97,5 per månad, som i "sicksacken". Ankaret använder 1/99 (rad A5).
- Låtsasbytet är inte kört för Adelino-formen utan volatilitetsdecil (A2).
- Artiklarna är lästa i utkast eller accepterade manus (`reference/litteratur/README.md`).
