# Mönster i Sabbatuccis texter: sex artiklar lästa i sin helhet

20 november 2026. Skriven av Claude. Underlag för rättning av uppsatstext, inte uppsatstext.

Ersätter `DD2_sabbatucci_stil_2026-11-17.md` där de två skiljer sig. Den byggde på utdrag ur arbetsversioner, lästa genom ett verktyg. Här är de tryckta versionerna lästa från första till sista stycket.

## 1. Vad som lästes

| Kort | Artikel | Fil | Sidor |
|---|---|---|---|
| JF | Pettenuzzo, Sabbatucci, Timmermann: Cash Flow News and Stock Price Dynamics, Journal of Finance 75(4), 2020 | `b07897b0-PETTENUZZO-CashFlowNews-2020.pdf` | 51 |
| RFS | Parsons, Sabbatucci, Titman: Geographic Lead-Lag Effects, Review of Financial Studies 33(10), 2020 | `a4d9847a-Parsons-GeographicLeadLagEffects-2020.pdf` | 51 |
| RoF | Johansson, Sabbatucci, Tamoni: Tradable Risk Factors for Institutional and Retail Investors, Review of Finance 29(1), 2025 | `b559b3b6-rfae034.pdf` | 37 |
| WP | Pettenuzzo, Sabbatucci, Timmermann: Firm Value and Payout Suspensions During Financial Market Distress, SSRN 3823258, 4 aug 2022 | `3abd8397-ssrn-3823258.pdf` | 64 |
| JoE | Samma tre: Dividend suspensions and cash flows during the Covid-19 pandemic, Journal of Econometrics 235, 2023 | `e0979124-...-main.pdf` | 20 |
| EL | Samma tre: Payout suspensions during the Covid-19 pandemic, Economics Letters 224, 2023 | `546a5877-...-main.pdf` | 4 |

Läst: all löptext, alla fotnoter, alla tabell- och figurtexter, bilagorna i RFS och WP. Inte läst: siffrorna i tabellcellerna och referenslistorna rad för rad. Ekvationerna i JoE avsnitt 3 blev oläsliga vid textutdraget; texten runt dem är läst.

Mätningarna i avsnitt 2 är gjorda med skript på textutdragen (`stil_features.py`, `sabb_intro.py` i arbetsytan). Meningslängd och passivmått är ungefärliga.

## 2. Mätning

| | JF | RFS | RoF | WP | JoE | EL |
|---|---|---|---|---|---|---|
| Sammanfattning, ord | 101 | 100 | 100 | 95 | 77 | 41 |
| Inledning, ord | 2 080 | 2 690 | 2 393 | 2 220 | 687 | 339 |
| Inledning, andel av filens ord | 9 % | 12 % | 13 % | 10 % | 6 % | 12 % |
| Första resultatmeningen, andel in i inledningen | 54 % | 45 % | 34 % | 13 % | 81 % | 47 % |
| Litteraturen börjar, andel in i inledningen | 81 % | 70 % | 60 % | 49 % | saknas | 70 % |
| Tal med enhet i inledningen | 0 | 7 | 10 | 11 | 0 | 0 |
| "First, Second, Third" i inledningen | 7 | 5 | 5 | 0 | 1 | 3 |
| Slutsats, ord | 578 | 1 175 | 840 | 242 | 167 | 61 |
| Tabeller i huvudtexten | 9 | 8 | 6 | 7 | 3 | 1 |
| Figurer i huvudtexten | 9 | 6 | 11 | 6 | 9 | 3 |
| "we/our" per 1 000 ord | 18,0 | 13,0 | 19,1 | 12,6 | 18,7 | 16,6 |
| Passiv form per 1 000 ord (ungefär) | 6,4 | 8,8 | 4,1 | 5,4 | 4,7 | 3,9 |
| Garderingsord per 1 000 ord | 1,6 | 3,3 | 1,9 | 4,8 | 0,5 | 3,2 |

Jämförelse: medianen bland 660 kandidatuppsatser i finans på SSE är 11,4 passiva per 1 000 ord och 4,0 garderingsord. Fem av sex artiklar ligger under uppsatsernas tionde percentil i passiv form (7,6). Källa: `MONSTER_prisvinnare_kandidat_2026-11-20.md`, avsnitt 3.

Inget av de sex har ett eget litteraturavsnitt, en innehållsförteckning eller ett avsnitt som heter "Limitations".

## 3. Femton mönster

Varje rad säger var mönstret syns. Avsnittsnummer avser de lästa filerna.

**Inledningen**

1. **Luckan sägs som något som inte gick att mäta eller skilja åt.** RFS, inledningen: antalet analytiker och antalet gemensamma analytiker följs åt inom en bransch, så ingen kan säga vilket som gör kurserna effektiva. JF: kvartalsdata döljer dynamiken, och fyra numrerade hinder räknas upp. RoF: handelbara riktmärken för faktorerna finns inte. WP: tidigare test tar finansieringsunderskottet för givet och ser därför aldrig interna källor. Ingen av de sex säger "ingen har gjort detta i land X".

2. **Ett läge eller ett mått som löser problemet, visat med ett fall läsaren kan se.** RFS: Costco och Amazon 2013, tolv och sjutton analytiker, ingen gemensam; Amazon och Google delar nio. Figur 1 är en fyrfältare. WP: Carnivals kedja av beslut 2020, med datum och belopp (figur 1). JoE avsnitt 4.2: två bolag, A och B, med tio miljoner dollar var.

3. **"In this paper, we" kommer tidigt.** 3 % in i RFS, 8 % i WP, 16 % i RoF. JF tar tre stycken på sig (27 %).

4. **Resultaten står i inledningen, uppräknade.** RoF: "two key findings", sedan First och Second. EL: tre resultat, numrerade. RFS, RoF och WP ger tal med enhet: 24 punkter per procent (RFS), 2 till 4 procent om året och 58 procent förklarat (RoF), 2,5 procent högre värde per procent sparad kassa (WP). JF, JoE och EL ger riktning och styrka i ord. Tal i inledningen är alltså vanligt men inte en regel hos honom.

5. **Litteraturen står sist i inledningen och är ordnad efter vad pappret tillför.** Varje stycke slutar med skillnaden mot de nämnda artiklarna. RFS: två litteraturer, och efter varje en mening om det egna bidraget. RoF: närmast besläktade papper nämns vid namn, och skillnaden sägs i nästa mening. WP: tre tidigare test av pecking order, sedan vad de inte fångar.

6. **Färdplanen är ett kort stycke sist.** JF, RoF, WP, JoE, EL. RFS väver in avsnittshänvisningarna i resultatsammanfattningen i stället.

**Analysen**

7. **Varje test motiveras av en fråga eller en förutsägelse som sägs före resultatet.** WP avsnitt 4: tre möjliga tecken på en koefficient och vad vart och ett skulle betyda, sedan tabellen. RFS avsnitt 2.1: en proposition och två empiriska följder, sedan testen. RoF 5.3 och WP avsnitt 2 ställer frågan rakt ut och svarar i nästa mening.

8. **Det kända resultatet återskapas först, i samma tabell som det nya.** RFS tabell 4: bransch 24 punkter (t 11,71) bredvid stad 6 punkter (t 5,11), med hänvisning till Moskowitz och Grinblatt (1999). JF tabell II panel B: de två tidigare måtten ger t 2,16 och 6,41; det egna ger 4,04 och 7,23 i samma panel. WP: Faulkender och Wangs 0,94 dollar per dollar ställs mot det egna talet.

9. **Mekanismen prövas med en kontrast, och testet är skillnaden.** RFS tabell 6: branscheffekten faller från 0,28 till 0,098 med analytikertäckning och likheten förkastas på enprocentsnivån; stadseffekten ligger still (0,067 mot 0,060, p 0,877). WP: utdelningsstopp mot obligationer mot nyemission, och finanskrisen mot pandemin. RoF: privat mot institutionell, långt ben mot kort ben, och gapet delat i två kostnader plus en rest.

10. **Storleken sägs i enheter som går att känna.** JF: halveringstid 350 handelsdagar; ett hopp var sextionde dag; 2,32 procent högre säkerhetsekvivalent avkastning. WP: från tionde till nittionde percentilen sänker sannolikheten för utdelningsstopp med 13,4 procent, och basnivån (19,3 procent) står i nästa mening. RFS: en dollar blir cirka 70 i marknaden och knappt 20 i lägsta kvintilen.

11. **Avsnitt börjar med syftet och slutar med vad läsaren ska ta med sig.** Slutmeningarna börjar med fraser som "We conclude from", "These results show", "To summarize", "The key takeaway is", "Taken together". Det finns i alla sex.

12. **Nollresultat och svaga resultat sägs rakt, med skälet.** RFS avsnitt 3.3: interaktionen väntas ge noll och ger noll. JF: en koefficient med p 0,12 kallas inte signifikant, i samma mening som den tolkas. RFS 4.2: skillnaden är inte signifikant "at conventional levels", och det står där.

13. **Mätfel erkänns på plats, med riktning och storlek.** RFS 4.1: huvudkontoren är felklassade för flyttade bolag. Författarna räknar fram en felandel på cirka 10 procent, säger att felet drar mot noll och kastar sedan om 1 till 50 procent av orterna slumpvis (tabell A4). WP: "With this important caveat in mind" före ett tal som vilar på ett antagande.

14. **Robusthet är varianter av urval, vikter och skattningsmetod, och det mesta ligger i bilaga.** Huvudtexten ger en mening och en hänvisning. RFS avsnitt 4 är undantaget, med nio bilagetabeller och ett test som en granskare föreslog (fotnot 25).

15. **Tabelltexten bär sig själv.** Ekvationen skrivs ut igen, varje variabel definieras, standardfelen anges (Newey-West med antal laggar), stjärnorna förklaras, urvalsperioden står sist. Se JF tabell II och RFS tabell 4.

## 4. Rättelser av den äldre anteckningen

| Påstående 17 november | Efter läsning av tryckt version |
|---|---|
| RoF tabell 5 jämför fondnamn med innehav, och fotnot 5 säger att flöden följer namn | Stämmer inte för den tryckta versionen. Tabell 5 gäller transaktionskostnader. Namn mot innehav ligger i Supplementary Appendix A.4. Huvudtexten (avsnitt 2.1) säger bara att klassning efter namn inte är optimal. Hänvisa inte till fotnoten. |
| Ingen placebo i något papper | Håller i huvudsak. RFS tabell A4 (slumpade huvudkontor) är närmast. WP bilaga B är en skillnad-i-skillnad kring 9 april 2020. |
| Litteraturen står sist i inledningen | Håller i alla fyra långa artiklar. JoE har inget litteraturblock alls. |
| Talen står i inledningen i fyra av fem | Tre av sex här (RFS, RoF, WP). |

## 5. Vad som inte ska kopieras

- **Meningslängden.** Snittet är 26 till 35 ord per mening, över uppsatsernas median (26). Era egna stilregler säger kortare.
- **Anspråk på att vara först.** Finns i RFS, RoF, EL och JF. Cochrane avråder (se `MONSTER_toppartiklar_finans_2026-11-20.md`). Använd det högst en gång och bara om litteratursökningen bär det.
- **Inledningens längd.** Hans egna är 2 100 till 2 700 ord. Kursens bild 19 säger 2 till 4 sidor, och litteraturen under en sida. Bilden gäller.
- **Tal som inte stämmer med varandra.** RoF anger 2 till 4 procent i sammanfattningen och 2 till 5 i slutsatsen. WP anger 38 procent i inledningen och 39 i avsnitt 4. Sådant händer även i tryck. Kontrollera varje tal på alla ställen där det står.

## 6. Tillägg samma dag: kodblad och riktvärden

De sex artiklarna är nu kodade på samma blad som vinnarna och två toppartiklar, och mätta med samma skript. Se `claude/MATT_rattningsinstrument_2026-11-20.md`.

- **Kodbladet.** En punkt är bara ifylld där avsnitt 3 ovan bär den. Alla sex: data och metod i inledningen, inget litteraturavsnitt, ingen innehållsförteckning, ingen placebo, ingen räknad minsta påvisbara effekt. Där det är kodat: förutsägelse före resultat (3 av 3), mekanismen prövad med en kontrast (3 av 3), storlek i ekonomiska enheter (4 av 4), förlagans tal bredvid det egna (3 av 3).
- **Nya mätvärden per 1 000 ord, median och spann över de sex:** passiva led 4,8 (3,6 till 9,3), garderingsord 2,6 (0,6 till 4,4), "we" 18,2 (11,3 till 19,8), förstärkningsord 2,7 (1,8 till 3,8), flaggade meningar på tio regler 4,2 (3,6 till 6,9). Uppsatsernas median på det sista måttet är 9,4.
- **Två saker han gör mer än uppsatserna:** långa meningar (4,1 över 40 ord per 1 000 ord mot 2,0) och förstärkningsord (2,7 mot 0,9). Det är alltså inte fel i hans ögon, men era egna stilregler säger kortare och utan.
- Tabellen i avsnitt 2 är mätt med ett äldre skript. Talen där och här skiljer sig något eftersom definitionerna gör det. Riktvärdena i måttfilen gäller.

## 7. Källor

De sex PDF-filerna ovan, uppladdade 20 november 2026. Kursens bilder: `reference/course_context/course_intro.txt` i `financethesisv2` (bild 14, 18, 19).
