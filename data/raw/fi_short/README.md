# raw/fi_short/: FI:s blankningsregister

Offentlig data från [FI:s blankningsregister](https://www.fi.se/sv/vara-register/blankningsregistret/). Hämtad 31 okt och 2 nov 2026.

| Fil | Innehåll |
|---|---|
| `HistoriskaPositioner_2026-10-31.ods` | Historiska positioner: 39 061 rader, positionsdatum 2010-05-10 till 2026-10-30 |
| `HistoriskaPositioner_2026-11-02.ods` | Samma register hämtat igen 2 nov |
| `AktuellaPositioner_2026-11-02.ods` | Aktuella positioner 2 nov |
| `download_log_2026-10-31.csv` | Varje hämtningsförsök 31 okt med URL, tid i UTC, sökväg, storlek, SHA-256 och eventuellt fel |
| `README_2026-10-31.md` | Anteckningar från hämtningen 31 okt |

- Registret visar bara **offentliga betydande korta nettopositioner**, inte alla positioner ned till anmälningsgränsen.
- `<0,5` betyder under 0,5 procent, inte noll.
- I äldre rader är datumen datumceller och i nyare ofta text.
- Läs med `pd.read_excel(f, engine="odf")` (kräver `odfpy`).

Mer om hämtningen står i [`../ap/INSAMLINGSLOGG_2026-10-31.md`](../ap/INSAMLINGSLOGG_2026-10-31.md#fi).
