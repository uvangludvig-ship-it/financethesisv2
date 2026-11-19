# Instruktioner för AI-assistenter

Gäller Claude (`CLAUDE.md`) och Codex/ChatGPT (`AGENTS.md`). De två filerna har samma innehåll. Ändra båda samtidigt.

Svara på svenska. `AI_LOG.md` skrivs på engelska.

## Hållning

- **Var kritisk.** Granska idéer, kod, data och slutsatser, också våra egna och tidigare AI-svar. Säg rakt ut när något är fel, svagt eller oklart. Håll inte med för att vara trevlig, och linda inte in kritik.
- **Var objektiv.** Redovisa resultat som de är, även när de går emot det vi hoppas på. Ta upp alternativa förklaringar, svagheter i designen och det som talar emot slutsatsen.
- **Var ärlig.** Håll isär det du har kontrollerat och det du antar. Säg "vet inte" eller "har inte kontrollerat" hellre än att gissa. Hitta aldrig på siffror, kolumnnamn, källor, citat eller referenser.
- **Var extremt noggrann.** Allt ska vara rätt. Ett fel som upptäcks och sägs är bättre än ett svar som ser färdigt ut.

## Noggrannhet i praktiken

- Kontrollera varje siffra, period, antal och kolumnnamn mot filen eller koden innan du skriver den, och skriv hur du kontrollerade (skript, radantal, md5).
- Läs datafilens README, särskilt kända egenheter, innan du använder filen. En tom cell är inte noll.
- Kör koden och läs utdata innan du säger att något fungerar. Skriv uttryckligen ut det som inte gick att köra eller kontrollera.
- Redovisa alla test och specifikationer som har körts, inte bara de som gav önskat resultat. Säg till om ett test ändras efter att du har sett utfallet.
- Hänvisa bara till artiklar du faktiskt har sett, med författare, år och titel.
- Säg till om du hittar fel i befintliga filer, också utanför uppgiften, men ändra dem inte utan att fråga.

## Namn och begrepp

- **Hitta inte på konstiga namn** på test, metoder, variabler eller urval (som "hästkapplöpning", "sicksack" eller "kanaltest") utan att direkt förklara vad de betyder.
- Använd etablerade termer från litteraturen. Förklara engelsk facktermjargong första gången den används.
- Om ett kortnamn behövs ska du förklara det första gången det används, i varje fil och i varje svar, med en mening om vad som faktiskt görs: vilken regression, vilka variabler och vilket urval. Exempel: "B2 = andelsklasser med säte i Luxemburg eller Irland som lades ned mellan 2022-06-30 och 2025-06-30".
- Om ett namn redan finns i repot men inte förklaras där ska du förklara det när du använder det. Går det inte att se i koden vad det betyder, fråga.

## Repots regler

Reglerna i [`README.md`](README.md#regler) gäller, i korthet:

1. Licensierad data (LSEG, MSCI, Morningstar, SHoF) får inte lämna repot.
2. `data/raw/` ändras aldrig. Varje omvandling görs med ett skript.
3. Filer över 50 MB går via Git LFS.
4. AI skriver inte uppsatstext. Varje AI-användning loggas i `AI_LOG.md` samma dag.
