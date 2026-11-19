# raw/morningstar/: Morningstar-export

**Licensierad data** från Morningstar. Den får inte lämna det privata repot.

## `226F9EC4243A44408972432B3BA329CB(in).csv` (nedladdad 19 nov 2026)

Filnamnet är som filen laddades ner. 72 MB, UTF-8 med BOM, komma som avgränsare. Ligger i Git LFS.

**Urval:** 29 196 andelsklasser (unika `SecId`) i 7 139 fonder (`FundId`). Alla är öppna fonder (`Investment Type` = Open-End Fund) med säte i Luxemburg (22 618) eller Irland (6 578), och **alla är avvecklade**: `Obsolete Date` är ifyllt för varje andelsklass, 2022 (3 603), 2023 (7 121), 2024 (14 647) och 2025 (3 825). 15 040 andelsklasser har Sverige bland länderna i `Country Registered for Sale`. Exakt vilket filter som gav urvalet framgår inte av filen.

**Kolumner (551):**

| Grupp | Innehåll |
|---|---|
| Statiska, kolumn 0–101 | Namn, valuta, ISIN, Morningstar-kategori (broad group, group, category, global category), säte, juridisk form, stilruta, förvaltarbolag och varumärke, startdatum, förvaltare (namn, kön, historik, längsta och genomsnittlig tid), jämförelseindex, fondförmögenhet, utdelning och avkastning, dagliga totalavkastningar, avgifter (net expense ratio, ongoing charge), omsättningshastighet, `SecId`, `PerformanceId`, `FundId`, avvecklingsdatum, länder där fonden är registrerad och får säljas, SRRI-historik |
| `Monthly Return <ÅÅÅÅ-MM> USD` | Månadsavkastning i USD, 156 kolumner 2013-01 till 2025-12 |
| `Net Assets - share class (Monthly) <ÅÅÅÅ-MM> USD` | Andelsklassens förmögenhet per månad i USD, 97 kolumner 2017-12 till 2025-12 |
| `Morningstar Rating Overall <ÅÅÅÅ-MM>` | Morningstar-betyg (stjärnor) per månad, 97 kolumner 2017-12 till 2025-12 |
| `SRI Value <ÅÅÅÅ-MM>` | Riskindikatorn SRI per månad, 97 kolumner 2017-12 till 2025-12 |

**Innan ni använder filen:**

- Kolumnnamnen innehåller radbrytningar (t.ex. `"Base \nCurrency"`). Ersätt `\n` med mellanslag när filen läses in.
- Sex kolumnnamn förekommer två gånger: `SecId`, `FundId`, `Inception Date`, `Morningstar Category`, `Morningstar Category Group` och `Annual Report Ongoing Charge`. pandas döper om dubbletterna till `.1`.
- De sista 13 raderna är inte fonder utan Morningstars sammanfattning (en tom rad, `Summary Statistics`, antal, percentiler, summa, medel, max, min, median, standardavvikelse). Filtrera på `Investment Type == "Open-End Fund"`.
- Datum har formatet `M/D/ÅÅÅÅ` (t.ex. `9/26/2022`).
- Eftersom fonderna är avvecklade glesnar månadsserierna mot slutet: `Monthly Return` har som mest 16 135 ifyllda andelsklasser (2021–2022) och efter 2025-05 nästan inga. En tom cell betyder att andelsklassen inte fanns eller redan var avvecklad, inte noll.
- `Inception Date` ligger efter 2026 för 5 andelsklasser (som mest 2079), vilket måste vara fel i källan.
- Många statiska fält är nästan tomma, t.ex. `Ticker` (8), `CUSIP` (1) och `Morningstar Rating Overall` utan datum (1).

```python
import pandas as pd
m = pd.read_csv("data/raw/morningstar/226F9EC4243A44408972432B3BA329CB(in).csv", encoding="utf-8-sig", low_memory=False)
m.columns = [c.replace("\n", " ") for c in m.columns]
m = m[m["Investment Type"] == "Open-End Fund"]
```
