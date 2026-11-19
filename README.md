# Finance thesis BE451, hösten 2026 (v2): Alexander Fox och Ludvig Pauli Uväng

Ny start 17 november 2026. Hit har bara det gemensamma flyttats från det gamla repot (`financethesis`): kursens regler och material, vinnar- och icke-vinnaruppsatserna och data som inte hör till ett visst ämne. Gamla ämnesidéer, beslutsunderlag och våra egna analyser följde inte med. De ligger orörda kvar i det gamla repot (se [Vad som inte följde med](#vad-som-inte-följde-med)).

## Kursen i korthet

| | |
|---|---|
| Kurs | BE451 Degree Project in Finance, 15 ECTS, Handelshögskolan i Stockholm |
| Handledare | Michael Klug (asset pricing, index investment, machine learning, demand curves, market microstructure) |
| Examinator och kursansvarig | Riccardo Sabbatucci. Sätter betyget; frågor som inte gäller forskningen går till honom |
| TA för kod och ekonometri | Morteza Aghajanzadeh |
| Kursadministratör | Anneli Sandbladh (tar emot replikationspaketet) |

**Datum som återstår**

| Datum | Vad |
|---|---|
| **Måndag 7 december kl. 10.00** | Uppsatsen i Canvas (det är den versionen som betygsätts) och replikationspaketet, en zip per grupp, med e-post till anneli.sandbladh@hhs.se |
| Före 12 december | Presentation av egen uppsats och opposition på en annan grupps, på plats |
| 18 december kl. 18.00 | Slutversion i Publish Thesis. Bara mindre korrigeringar efter seminariet |

**Form:** engelska, högst 40 sidor utan appendix, 12 punkter och enkelt radavstånd, ingen innehållsförteckning, officiell framsida (`reference/course_context/source_materials/front_page.docx`). Upplägget ska likna en artikel i JF, JFE eller RFS: Introduction (2–4 sidor, självbärande), Related Literature (under en sida, bara de närmaste artiklarna), Data and Methodology, Main Empirical Analysis, Discussion, Conclusion, References, Appendix. Tabeller och figurer ska ha självbärande texter.

**Vad kursen vill ha:** standardupplägget är replikation och meningsfull utvidgning av en nyare artikel i en topptidskrift. Listan över godkända tidskrifter finns i [`course_context/README.md`](reference/course_context/README.md#litteraturregler). Att bara flytta frågan till Norden räcker inte utan ett ekonomiskt skäl. Bedömningskriterier (bild 4): Useful, Correct, Relevant, Contribution, Independence. Betyget vägs också av presentation, opposition, självständighet och uppträdande.

**AI:** syllabus tillåter AI med ett obligatoriskt appendix som redovisar användningen. Språkgranskning kan vara tillåten, men AI får inte skriva någon del av uppsatsen direkt. Allt loggas samma dag i [`AI_LOG.md`](AI_LOG.md). Kursmaterialet formulerar detta olika på olika ställen, se [`course_context/README.md`](reference/course_context/README.md#ai-motstridiga-formuleringar--följ-den-försiktiga-linjen).

Fullständiga krav med källhänvisning: [`reference/course_context/requirements_checklist.md`](reference/course_context/requirements_checklist.md). Svensk sammanställning av Canvas: [`reference/course_context/README.md`](reference/course_context/README.md).

## Struktur

```
reference/          läsmaterial; översikt i reference/README.md
  course_context/   kursens material: syllabus, synopsisinstruktion, handledare och ämnen,
                    introduktionsföreläsningen, ekonometrikursen med kod, framsidesmall,
                    kravlista, mall för replikationspaketets README
  old_winners/      de 25 prisbelönta SSE-uppsatserna i finans 2011–2024 (pdf och text) med index
  non_winners/      de 635 övriga kandidatuppsatserna i finans 2009–2026 som text, med index
data/               data som inte hör till ett visst ämne; översikt i data/README.md
  raw/              källfilerna, en mapp per källa med egen README.md
                    (lseg, fi, fi_short, ppm, shof, ap, morningstar)
  derived/          tabeller byggda ur raw/ (README.md beskriver kolumnerna)
  build/            skripten som hämtar och bygger (README.md)
AI_LOG.md           kursens krav: varje AI-användning loggas samma dag
```

## Vinnaruppsatserna och de andra

- [`reference/old_winners/INDEX.md`](reference/old_winners/INDEX.md): 25 uppsatser som fått Per Hiller- eller Staffan Viotti-priset 2011–2024, kontrollerade mot SSE:s samling 3 september. Pdf i mappen, text i `text/`.
- [`reference/non_winners/INDEX.md`](reference/non_winners/INDEX.md): alla 635 uppsatser i SSE:s katalog märkta "Bachelor Thesis in Finance" som inte ingår i prissamlingen, läst 1 oktober. Text i `text/<MediumId>.txt`, metadata och sammanfattningar i `catalogue_index.json`, länk till varje original. Pdf:erna (cirka 1 GB) ligger inte i repot. `thesis_metrics.py` räknar enkla strukturmått på texterna.
- 6338, *Leading The Wallet* (2025), har en prisnotering för 2026 i katalogen men fanns inte i den officiella prissamlingen 1 oktober. Den ligger bland icke-vinnarna och är märkt i indexet.

Kursens regel: bygg inte idén på tidigare uppsatser, utgå från forskningsartiklar. När frågan är bestämd ska relevanta uppsatser läsas och citeras om ni använder deras idéer, text, tabellupplägg eller kod. Plagiatkontroll görs.

## Vad som inte följde med

Allt nedan finns kvar i `~/dev/financethesis` (GitHub: `financethesis`, privat). Inget har raderats eller ändrats där.

| Inte överfört | Var det ligger i gamla repot | Varför |
|---|---|---|
| Alla tidigare uppsatsalternativ (00–17) med kod, resultat, testkort och utkast | `pagaende/`, `under_utredning/`, `arkiv/` | Gamla ämnesidéer |
| Synopsisen från 9 september och dess källfiler | `reference/synopsis/`, `arkiv/00_amnesval_sep2026/` | Gamla ämnesidéer |
| Ankarsökningar, djupgranskningar och beslutsunderlag 13–16 november | `reference/anchor_*`, `deep_dd_*`, `followup_*`, `ccc13_*` | Gamla ämnesidéer och slutsatser |
| Våra egna analyser av vinnarna: vinnare mot icke-vinnare, slutsatsjämförelse, vinnargranskning, strukturkodning, PCA | `reference/winners_analysis/` | Skrivna för att välja mellan gamla ämnen; innehåller tolkningar som kan styra valet |
| Våra genomförbarhetsnoteringar per handledarämne | `reference/course_context/TUTORS_AND_TOPICS.md` | Egna bedömningar. Kursens egen text finns kvar i v2 |
| Gamla AI-loggen | `AI_LOG.md` | Hör till de gamla alternativen. Behövs när AI-appendixet skrivs |
| Data byggd för gamla ämnen: Fondtorgsnämnden, OMXSB-händelselistor, swing pricing, tranchdagar, NAV för 205 utvalda fonder, europeiska aktier ur vissa fonders innehav, ankardata m.m. | `data/` (se `data/README.md` där) | Urvalet styrs av ett gammalt ämne. En förteckning finns i [`data/README.md`](data/README.md#kvar-i-gamla-repot) |

Utanför båda repona finns M&A-databasen från Capital IQ i `~/dev/capiq-transactions/` (affärer med målbolag i DACH och Norden, annonserade 2015–2026, och europeiska PE-, VC- och family office-firmor). Den är ett eget projekt och är inte kopierad hit.

## Regler

1. **Repot ska vara privat.** Det innehåller licensierad data från LSEG, MSCI och SHoF. `financethesisv2` var privat på GitHub 17 nov 2026.
2. **`data/raw/` ändras aldrig.** Varje omvandling är ett skript i `data/build/`. En ny datafil får en rad i `data/README.md` samma dag.
3. **Filer över 50 MB går via Git LFS** (`.gitattributes`). Kör `git lfs install` en gång per dator.
4. **AI skriver inte uppsatstext.** AI-skrivet material är underlag som författarna skriver om, och varje användning loggas i `AI_LOG.md`.
