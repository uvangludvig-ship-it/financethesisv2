# raw/fi/: Finansinspektionens fondinnehav

Offentlig data. Svenska fonders innehav vid varje kvartalsslut, som fondbolagen rapporterar till FI. Hämtad från FI:s webbplats 25 okt 2026.

- En zip per kvartal, 2018Q4–2026Q2 (31 st). Filnamn: `Fondinnehav_<kvartal>_<tidpunkt då FI skapade filen>.zip`.
- Varje zip har en mapp per fondbolag och en XML-fil per fond (`<fond>_<institutnummer>_VPFO_<kvartal>_<tid>.xml`): 626 fonder för 2018Q4 och 726 för 2026Q2.
- I zipparna från 2023Q4 och framåt skiljs mappar med bakåtsnedstreck (`\`) i stället för `/`. Kod som läser filnamnen måste klara båda.
- Alla kvartal i långt format, en rad per fond, instrument och kvartal: [`../../derived/fi/fi_holdings_long.csv.gz`](../../derived/README.md#fi).
