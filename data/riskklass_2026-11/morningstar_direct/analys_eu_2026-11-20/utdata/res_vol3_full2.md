# Volatilitet, stjarnor och riskklass: tre kolumner pa samma fondmanader (bd_eu_EU.pkl)
Fondmanader 66365, fonder 1142, 2018-01 till 2025-12. Riskklass: {2: 92, 3: 953, 4: 18324, 5: 20428, 6: 25135, 7: 1433}
sd60: medel 5.22, std 1.31 (procent per manad). Flode: procent per manad.
Ankaret (arbetsversion 7 okt 2018, Table VII, USA, flode som andel, volatilitet som andel; samma enhet som har): Vol5 -0,055 (t -4,55) utan betyg; -0,0080 (t -0,63) med betyg; betyg +0,0064 per stjarna (= +0,64 procent).

## Huvud: manadseffekter, ankarets kontroller, kluster fond och manad

| Kolumn | Vol5 (sd60) | t | Betyg per stjarna | t | Riskklass per steg | t | Riskklass-dummies, p | Fondmanader |
|---|---|---|---|---|---|---|---|---|
| 1: Vol5 | -0.0194 | -0.46 | | | | | | 66365 |
| 2: Vol5 + betyg | +0.0034 | 0.09 | +0.611 | 12.39 | | | | 66365 |
| 2b: Vol5, manad x betyg | -0.0092 | -0.23 | (fasta effekter) | | | | | 66365 |
| 3: Vol5 + betyg + riskklass | -0.0319 | -0.62 | +0.611 | 12.39 | +0.109 [-0.060; +0.279] | 1.26 | 0.139 | 66365 |

Kolumn 3 med en koefficient per betyg (bas 3) och per riskklass (bas 4):

| Variabel | Koef. | t |
|---|---|---|
| sd60 | -0.076 | -1.46 |
| s_1 | -0.712 | -4.91 |
| s_2 | -0.521 | -6.22 |
| s_4 | +0.661 | 7.05 |
| s_5 | +1.534 | 9.49 |
| k_2 | -0.058 | -0.14 |
| k_3 | -0.260 | -1.07 |
| k_5 | +0.149 | 1.26 |
| k_6 | +0.169 | 0.94 |
| k_7 | +1.010 | 2.41 |

Storlek i kolumn 3, pp per ar: en standardavvikelse i Vol5 (1.31) -0.50; en stjarna +7.34; ett riskklassteg +1.31.

## Variant A: plus ra avkastning (18 manader, viktad)

| Kolumn | Vol5 (sd60) | t | Betyg per stjarna | t | Riskklass per steg | t | Riskklass-dummies, p | Fondmanader |
|---|---|---|---|---|---|---|---|---|
| 1: Vol5 | -0.0736 | -1.74 | | | | | | 66365 |
| 2: Vol5 + betyg | -0.0497 | -1.24 | +0.474 | 10.73 | | | | 66365 |
| 2b: Vol5, manad x betyg | -0.0614 | -1.54 | (fasta effekter) | | | | | 66365 |
| 3: Vol5 + betyg + riskklass | -0.0713 | -1.47 | +0.474 | 10.73 | +0.067 [-0.093; +0.227] | 0.82 | 0.198 | 66365 |

Kolumn 3 med en koefficient per betyg (bas 3) och per riskklass (bas 4):

| Variabel | Koef. | t |
|---|---|---|
| sd60 | -0.114 | -2.29 |
| s_1 | -0.431 | -3.16 |
| s_2 | -0.344 | -4.21 |
| s_4 | +0.540 | 6.07 |
| s_5 | +1.286 | 8.52 |
| k_2 | +0.116 | 0.30 |
| k_3 | -0.179 | -0.78 |
| k_5 | +0.031 | 0.27 |
| k_6 | +0.081 | 0.48 |
| k_7 | +0.837 | 2.08 |

Storlek i kolumn 3, pp per ar: en standardavvikelse i Vol5 (1.31) -1.12; en stjarna +5.68; ett riskklassteg +0.80.

## Variant B: manad x kategori

| Kolumn | Vol5 (sd60) | t | Betyg per stjarna | t | Riskklass per steg | t | Riskklass-dummies, p | Fondmanader |
|---|---|---|---|---|---|---|---|---|
| 1: Vol5 | -0.0742 | -1.27 | | | | | | 66365 |
| 2: Vol5 + betyg | +0.0503 | 0.90 | +0.654 | 13.34 | | | | 66365 |
| 3: Vol5 + betyg + riskklass | +0.0410 | 0.61 | +0.654 | 13.32 | +0.030 [-0.159; +0.218] | 0.31 | 0.895 | 66365 |

Kolumn 3 med en koefficient per betyg (bas 3) och per riskklass (bas 4):

| Variabel | Koef. | t |
|---|---|---|
| sd60 | +0.012 | 0.17 |
| s_1 | -0.877 | -5.61 |
| s_2 | -0.546 | -6.22 |
| s_4 | +0.690 | 7.31 |
| s_5 | +1.606 | 10.33 |
| k_2 | +0.447 | 0.83 |
| k_3 | +0.153 | 0.68 |
| k_5 | +0.035 | 0.25 |
| k_6 | +0.083 | 0.41 |
| k_7 | +0.350 | 0.83 |

Storlek i kolumn 3, pp per ar: en standardavvikelse i Vol5 (1.31) +0.65; en stjarna +7.84; ett riskklassteg +0.35.

## Variant C: Vol5 och Vol1 (55941 fondmanader)

| Kolumn | Vol5 | t | Vol1 | t |
|---|---|---|---|---|
| 1 | +0.0568 | 0.78 | -0.0717 | -1.28 |
| 2: + betyg | +0.0630 | 0.93 | -0.0597 | -1.11 |
| 3: + betyg + riskklass | +0.0197 | 0.28 | -0.0594 | -1.11 |

## Variant D: Vol5 inom varje betygsgrupp (ankarets Table VIII), manadseffekter

| Betyg | Vol5 | t | Riskklass per steg | t | Fondmanader |
|---|---|---|---|---|---|
| 1 | +0.0693 | 0.50 | +0.095 | 0.34 | 3650 |
| 2 | -0.0572 | -0.71 | -0.012 | -0.09 | 13854 |
| 3 | -0.0778 | -1.13 | +0.092 | 0.72 | 23284 |
| 4 | -0.1097 | -1.23 | +0.290 | 1.76 | 17094 |
| 5 | +0.1834 | 1.20 | -0.074 | -0.23 | 8483 |

Verifiering: inplanterad -0,050 per enhet Vol5 ger -0.0500 (vantat -0,0500).