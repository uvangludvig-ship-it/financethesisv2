# raw/shof/: Swedish House of Finance (Morningstar)

**Licensierad data** från Morningstar via SHoF. Den får inte lämna det privata repot. Levererad i oktober 2026.

| Fil | Innehåll |
|---|---|
| `fundmaster.xlsx` | Morningstars fondregister: 80 258 andelsklasser och 57 kolumner. Bland annat id (`performanceid`, `secid`, `fundid`), fondbolag, namn, ISIN, domicil, valuta, juridisk form, UCITS, startdatum, status och nedläggningsdatum, fondtyp, indexförvaltning, AUM och avkastning över 1 månad till 5 år |
| `shof_fundmaster.zip` | Samma fil zippad, så som den levererades |
| `shof_field_definitions.pdf`, `.txt` | SHoF:s definitioner av fälten i alla exporter, också de dagliga. Exempel: `returntype` 1 är totalavkastning, 6 marknadsavkastning och 18 skattejusterad avkastning |

**Dagliga exporter finns inte i repot.** `Valuations/` har TNA, antal andelar och nettoflöde per andelsklass och dag. `Reinvestments/` har återinvesterade kurser. Tillsammans är de flera GB.

- Alexander har dem.
- Lägg dem på exakt `data/raw/shof/Valuations/` och `data/raw/shof/Reinvestments/`, där git ignorerar dem.
- De är redan aggregerade till månad i [`../../derived/shof_monthly/`](../../derived/README.md#shof_monthly).

`../ppm/FEES.txt` innehåller avgifter med samma id och kommer också från SHoF.
