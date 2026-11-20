# reference/skrivunderlag_2026-11-20/

Underlag för hur uppsatsen ska disponeras och hur ett utkast kan rättas mot förebilder. Skrivet av Claude (claude.ai, projektet "thesis") 20 nov 2026 på Alexanders begäran. **Inget här är uppsatstext.** Filerna är kopior av dokumenten med samma namn i claude.ai-projektet, mappen `claude/` (md5 nedan).

Förebilderna är: Riccardo Sabbatuccis sex artiklar, Hartzmark och Sussman (2019), Ben-David, Li, Rossi och Song (arbetsversion 2019), de tolv prisbelönta uppsatserna 2019 till 2025 och övriga kandidatuppsatser i `../non_winners/`.

## Filer

| Fil | Vad den är |
|---|---|
| `DISPOSITION_slutlig_efter_final_result_2026-11-20.md` | **Den som gäller.** Skriven sist, efter slutpaketet `final_result/` och regeln att uppsatsen inte får innehålla egna test. Sex avsnitt, 26 sidor, inget eget litteraturkapitel (litteraturen sist i inledningen), och samma två frågor till båda etiketterna: följer flödena etiketten i tvärsnittet, och vad hände när etiketten ändrades. Vilken tabell och figur som hör till vilket avsnitt. Tre saker som måste lösas innan texten skrivs. Ersätter förslagen i de två filerna nedan där de skiljer sig |
| `DISPOSITION_uppsatsens_struktur_2026-11-20.md` | Kursens krav på strukturen (bilder, kursplan), hur förebilderna disponerar sina texter (avsnittsordning, andel av orden per avsnitt), Cochranes skrivråd i korthet, och ett förslag: sju avsnitt, cirka 30 sidor, 6 tabeller och 4 figurer |
| `DISPOSITION_innehall_per_avsnitt_och_tabeller_2026-11-20.md` | Har andra ett eget litteraturavsnitt (räknat i artiklar, vinnare, uppsatser Sabbatucci handlett och alla uppsatser 2024 till 2026). Vad som ska stå i varje avsnitt, och vilka av våra tal som hör till varje tabell och figur, med källdokument. Fem saker som inte är byggda: tabell 1 panel B till D och figur 1 till 4 |
| `MONSTER_sabbatucci_sex_artiklar_2026-11-20.md` | Femton mönster i Sabbatuccis sex artiklar, med ställe i varje artikel |
| `MONSTER_toppartiklar_finans_2026-11-20.md` | Mönster i Hartzmark och Sussman (2019) och Ben-David m.fl. (2019) |
| `MONSTER_prisvinnare_kandidat_2026-11-20.md` | Mönster i de tolv vinnarna 2019 till 2025, och var de bryter mot kursens bilder |
| `MATT_rattningsinstrument_2026-11-20.md` | Beskrivning av måttet för rättning: kodbladet (22 ja/nej-punkter om uppbyggnad, K01 till K22) och skriptet, med riktvärden ur förebilderna och vad måttet inte visar |
| `ratta.py` | Skriptet som mäter ett utkast (text eller markdown) mot riktvärdena och skriver ut flaggade rader med radnummer |
| `matt.py` | Definitionerna som `ratta.py` använder: reguljära uttryck för passiv form, garderingsord, signifikans utan storlek med mera, och reglerna R01 till R16 |
| `riktvarden.json` | Riktvärdena: samma mått räknade på förebilderna |
| `riktvarden.py` | Skriptet som räknade riktvärdena |
| `kodning_forebilder.jsonl` | Kodbladet ifyllt för de 20 lästa texterna, en rad per text |
| `struktur_forebilder.py` | Skriptet som räknade ord per avsnitt i de 20 texterna (tabellerna i den första DISPOSITION-filen) |

## Köra rättningen

```
python3 ratta.py utkast.md --forlaga "Ben-David" --ut rapport.md
python3 ratta.py utkast.md --max 0
```

`ratta.py`, `matt.py` och `riktvarden.json` ska ligga i samma mapp. Kräver bara Python 3. Kontrollerat i den här mappen 20 nov: skriptet går och skriver en rapport.

## Går inte att köra om härifrån

`riktvarden.py` och `struktur_forebilder.py` har hårdkodade sökvägar till Claudes arbetsyta och läser textversioner av Sabbatuccis sex artiklar och de två toppartiklarna. De texterna ligger inte i repot (upphovsrätt). Skripten ligger här som dokumentation av hur talen räknades. Vinnarnas och övriga uppsatsers texter finns i `../old_winners/text/` och `../non_winners/text/`.

## Förbehåll

- Måttet skiljer publicerade artiklar från uppsatser, men inte säkert vinnare från andra uppsatser (se MATT-filen, avsnitt 7).
- Vinnarna är inte bedömda av Sabbatucci. Ingen uppsats i arkivet har honom som examinator.
- Ankarets tryckta version är inte läst i det här arbetet; dess avsnitt kommer ur andra anteckningar i claude.ai-projektet.
- DISPOSITION-filerna hänvisar till resultatdokument (`RESULTAT_*`, `GRANSKNING_*`, `NOTIS_*`, `OVERSIKT_*`) som ligger i claude.ai-projektet, inte i repot.
- Alla tal i DISPOSITION-filerna är körda av AI och inte omkörda av er.
- AI-loggen är inte uppdaterad för det här arbetet.

## md5

| Fil | md5 |
|---|---|
| `DISPOSITION_innehall_per_avsnitt_och_tabeller_2026-11-20.md` | `def095ea191a1158e731462442a96e4b` |
| `DISPOSITION_uppsatsens_struktur_2026-11-20.md` | `0832c9ad2ab48557f00ae5204379d3ff` |
| `DISPOSITION_slutlig_efter_final_result_2026-11-20.md` | `8d5ba10f3783a2d741f39c882f192cf3` |
| `MATT_rattningsinstrument_2026-11-20.md` | `46138bd6c783d12636992d1211ba7a48` |
| `MONSTER_prisvinnare_kandidat_2026-11-20.md` | `2577a0b56953937e3552c75c3f31d7cc` |
| `MONSTER_sabbatucci_sex_artiklar_2026-11-20.md` | `4f54060389489604ad091a68fa0ed0cb` |
| `MONSTER_toppartiklar_finans_2026-11-20.md` | `9caf829e883b31c8ffce022d6ae3bd46` |
| `kodning_forebilder.jsonl` | `ac866c0230b918c4718e8a837944f1ad` |
| `matt.py` | `9e0b5ebc7868b6b9ca28bc7938dc300d` |
| `ratta.py` | `96e7f7c7bc0100baf7ae50d86d9fbaab` |
| `riktvarden.json` | `aef970fcf618583e6b59f91ff0b72203` |
| `riktvarden.py` | `00f3b2f5f31e095a5c1f0864ca2cf6af` |
| `struktur_forebilder.py` | `f89e9dd04a58c18ddfae28f586f00465` |
