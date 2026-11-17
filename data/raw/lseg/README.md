# raw/lseg/: LSEG Workspace

**Licensierad data** från LSEG (tidigare Refinitiv), hämtad i LSEG Workspace CodeBook. Den får inte lämna det privata repot. Indexserierna `.dMI…` kommer från MSCI och är också licensierade.

## panel_2005_2026/ (hämtad 26 okt 2026)

| Fil | Innehåll |
|---|---|
| `stocks_daily_2005.parquet` | Dagliga aktiedata: 4 340 104 rader, 1 928 RIC, 1991-11-01 till 2026-10-26 (för de flesta bolag från 2004–2005). Kolumner: `ric`, `date`, `close`, `totret`, `volume`, `mcap`, `shares`, `turnover`, `bid`, `ask`, `source` (`tr` för 4 313 966 rader, `pricing` för 26 138 rader och 15 RIC). Ligger i Git LFS |
| `stocks_static_2005.csv` | En rad per RIC (2 117): första och sista dag i panelen, antal dagar, namn (`DTSubjectName`), ISIN (`IssueISIN`), avnoteringsdatum (`RetireDate`), börskod |
| `indices_daily (1).csv` | Dagliga stängningskurser (`ric`, `date`, `close`) från juli 2004 till 23 okt 2026: `.OMXS30`, `.OMXS30GI`, `.OMXSPI`, `.OMXSGI` (från 2008), `.OMXSBGI`, `.OMXSBCAPGI` |
| `indices_daily_extra.csv` | Samma format: `.OMXN40`, `.OMXSBPI`, Stockholm large, mid och small cap (`.OMXSLC*`, `.OMXSMC*`, `.OMXSSC*`, PI och GI; large cap från 2013), `.STOXX`, `.STOXXR` och tre MSCI-serier (`.dMIEU00000NEU`, `.dMIEU00000NUS`, `.dMINO00000NEU`) |
| `td_universe.csv` | Beställningsunderlaget, 1 291 rader: RIC, namn, ISIN, börs, tillgångsslag, primär RIC, ticker, avnoteringsdatum |
| `td_rics_final.csv` | De 2 135 RIC som beställdes |
| `td_failures (1).csv` | De 18 RIC som inte gick att hämta |

Filnamnen med "(1)" är som de laddades ner.

**Innan ni använder panelen:**

- `totret` är **daglig totalavkastning i procent** (utdelningar ingår), inte ett index. Kumulerad 2010–2019 ger den t.ex. 1,46 gånger för H&M B, där priset gav 0,96. Kolumnen har extrema värden som måste rensas: 499 rader i 299 RIC ligger över 100 procent i absolutbelopp, och det högsta är cirka 352 miljoner procent.
- Avnoterade bolag har `^` och en avnoteringskod i RIC, t.ex. `3L.ST^D12`. 790 avnoterade Stockholmsbolag finns med.
- Av de 1 928 RIC med data är 1 526 Stockholmsnoterade (736 aktiva, 790 avnoterade) och 402 från Oslo, Helsingfors och Köpenhamn. **De icke-svenska aktierna är ett urval, inte hela respektive börs.** De beställdes för att de fanns i vissa fonders innehav.

```python
import pandas as pd
p = pd.read_parquet("data/raw/lseg/panel_2005_2026/stocks_daily_2005.parquet")
```

## klassificering/ (hämtad 1 nov 2026)

| Fil | Innehåll |
|---|---|
| `lseg_klassificering.csv` | 1 685 RIC: `icb` (ICB-supersektorkod, fyra siffror), `trbc` (TRBC business sector, text), `marknad` (MIC-kod; vanligast `XSTO` 390, `SSME` 315, `ONSE` 30, ofta tom), `freefloat` (procent) |
| `lseg_freefloat_hist.csv` | Free float per RIC och halvårsöversyn: `ff`, `review` (t.ex. `2007H2`), `refdag`. 65 714 rader, referensdagar 2007-05-31 till 2026-04-30 |
| `lseg_saknade_aktier.csv` | Dagliga handelsdata för två aktier som saknas i panelen: Nordea (`NDASE.ST`) och Tieto (`TIETOS.ST`), 2006-01-02 till 2026-10-30, 5 233 dagar var. Har LSEG:s fältnamn (`TRDPRC_1`, `ACVOL_UNS`, `BID`, `ASK`, `VWAP` …), inte panelens |
| `lseg_falt_logg.txt` | Vilka LSEG-fält som provades på 30 testbolag och hur många som fick värden, plus felmeddelanden för Nordea- och Tieto-RIC som inte fungerade |
