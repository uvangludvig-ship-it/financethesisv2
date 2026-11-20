"""Sokvagar och konstanter. Allt ar relativt repots rot, sa inget behover andras mellan datorer."""
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]                       # repots rot
MD = ROT / "data" / "riskklass_2026-11" / "morningstar_direct"  # radata (Morningstar Direct, LSEG, faktorer)
OVRIGT = ROT / "data" / "riskklass_2026-11" / "ovrigt"          # ECB:s valutakurser
ARBETE = Path(__file__).resolve().parent / "_arbete"            # byggda paneler (ligger inte i git)
UT = ROT / "final_result"
TAL = UT / "tal"                                                # ett csv per tabell eller figur
for p in (ARBETE, TAL, UT / "tabeller", UT / "figurer"):
    p.mkdir(parents=True, exist_ok=True)

# Ankarets konstanter (forfattarnas kod, "INITIAL STEP: SETUP PRIMARY DATASET")
LAMBDA = 0.20551497      # %let Lambda: avtagande vikter over 18 manader (Barber, Huang och Odean 2016, ekv. 5)
BETA_MANADER = 60        # %let n_years = 5
BETA_MINST = 36          # %let min_mm = 36
HISTORIK_MANADER = 60    # fem ars avkastningshistorik kravs i alla paneler (Barber, Huang och Odean 2016, not 8); se bygg/
MIN_TNA_MUSD = 10        # artikeln s. 1733
WINSOR = (0.01, 0.99)    # artikeln s. 1733: inom varje manad

USA_EXPORT = MD / "exporter_2026-11-18" / "BA37C8D419E2470DA22839DB972EB065.csv.gz"
USA_FAKTORER = MD / "analys_usa_2026-11-18" / "usa_ff3_mom_1986_2011.csv"
EU_BAS = MD / "bas_eu_2026-11-19"
FAKTORER = MD / "faktorer"
EU2006 = MD / "eu2006_lseg_bank_2026-11-20" / "radata"
