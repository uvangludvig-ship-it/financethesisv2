# Mönster i toppartiklar i finans: två artiklar lästa i sin helhet

20 november 2026, andra versionen samma dag. Skriven av Claude. Underlag för rättning av uppsatstext, inte uppsatstext.

Den första versionen byggde på sammanfattningar, förstasidor och skrivråd. Det bröt mot regeln att varje artikel som texten vilar på ska vara läst i sin helhet. Den här versionen drar bara mönster ur det som är läst så. Allt annat står i avsnitt 5 som inte läst.

## 1. Vad som lästes

| Artikel | Version | Läst | Inte läst |
|---|---|---|---|
| Hartzmark och Sussman, Do Investors Value Sustainability? A Natural Experiment Examining Ranking and Fund Flows, Journal of Finance 74(6), 2019 | ECGI Finance Working Paper 565/2018, daterad 25 mars 2019 | All löptext, alla fotnoter, alla tabell- och figurtexter | Internetbilagan, siffrorna i tabellcellerna |
| Ben-David, Li, Rossi och Song, What Do Mutual Fund Investors Really Care About? | Arbetsversion 24 september 2019 (AEA 2020) | All löptext, fotnoter, tabelltexter, bilaga A | Den tryckta versionen i Review of Financial Studies 35(4), 2022, som är längre och inte ligger öppet. Slutet av bilaga B. |

Båda ligger i uppsatsens eget område: fondflöden som svar på en enkel signal. Ben-David m.fl. är uppsatsens förlaga. Jag har läst arbetsversionen, inte den tryckta. Citera inget ur den här anteckningen som om det gällde den tryckta versionen.

Båda är kodade på samma blad som vinnarna och Sabbatuccis artiklar: 16 av 19 punkter (Hartzmark och Sussman) och 17 av 18 (Ben-David m.fl.). Se `claude/MATT_rattningsinstrument_2026-11-20.md`, avsnitt 3.3.

## 2. Hartzmark och Sussman: åtta mönster

1. **Huvudresultatet är en figur före första stycket.** Figur 1 står över inledningen: ackumulerade flöden för fonder med en, tre och fem glober, nio månader före och elva efter publiceringen.

2. **Första stycket slutar i frågan, andra börjar med svaret.** Stycke ett går igenom fyra slags investerare och slutar med frågan om investerare ser hållbarhet som bra, dåligt eller likgiltigt. Stycke två börjar med vad artikeln visar.

3. **Luckan är att frågan inte går att besvara utan en chock.** Inledningen säger varför tidigare upplägg inte räcker: fonder med hållbarhetsmandat visar bara vad deras egna köpare vill, och priser fångar risk. Sedan kommer chocken: 20 000 fonder, 8 biljoner dollar, betygsatta på en dag.

4. **Varje test inleds med invändningen det svarar på.** Avsnitt 3.4 börjar med "One still may be worried" och svarar med matchning på förperioden. Panel B i tabell 3 motiveras med att resultaten kunde bero på brus. Viktade regressioner motiveras med att små fonder kunde driva resultatet.

5. **Ett stycke räknar upp vad en alternativ förklaring måste klara.** Sist i 3.4: den måste hänga ihop med de diskreta betygen men inte med percentilerna, får inte vara en fast fondegenskap, får inte fångas av kontrollerna och måste börja verka den dag betygen publiceras.

6. **Storleken sägs i dollar och mot ett känt tal.** 12 till 15 miljarder ut ur fonder med en glob, 24 till 32 in i fonder med fem (avsnitt 3.5). Effekten ställs mot Reuter och Zitzewitz (2010): 43 till 52 punkter per stjärna.

7. **Styrkan erkänns där den är tunn, utan att räknas.** Cirka 350 observationer per percentil (3.3). Elva månaders avkastning räcker inte för säkra slutsatser (4.2). Fondnedläggningar är för sällsynta för full uppsättning kontroller (3.5).

8. **Det data inte kan skilja åt sägs, och skickas till en annan metod.** Naiva förväntningar och icke-ekonomiska motiv ger samma flöden. Författarna säger det och gör ett experiment (4.3). De skriver också vad experimentet förutsätter för att tolkningen ska hålla.

Därtill: ingen innehållsförteckning, inget litteraturavsnitt, ingen färdplan. Avsnittsrubrikerna är frågor. Varje koefficient i löptexten har sitt t-värde. Placebo finns (betyg byggda på äldre data, i internetbilagan) liksom en diskontinuitetsanalys med fyra sätt att klustra.

## 3. Ben-David m.fl.: sex mönster

1. **Förlagan replikeras först, och det egna talet ställs bredvid förlagans.** Avsnitt 4.1.1: den egna koefficienten för marknadsdelen är 72 procent lägre än den för alfa, mot förlagans 71. Först därefter kommer invändningen.

2. **Nollhypotesen har ett eget avsnitt och motiveras med tidigare belägg.** Avsnitt 2 säger vad investerare gör enligt tjugo års litteratur och kräver att ett nytt test ska kunna förkasta det.

3. **Testet prövas på data där svaret är känt.** Flöden simuleras så att de per konstruktion inte skiljer på avkastningens delar. Förlagans test ger samma koefficienter ändå (tabell 2, kolumn 2 till 5). Det är ett test av testet.

4. **Mekanismen namnges och prövas.** Varför ger testet fel svar? Flödenas känslighet varierar över tid och är lägst när marknadsavkastningen sprider mest (4.1.3 och bilaga A.3).

5. **Placebo med andra år.** Händelsestudien kring Morningstars metodbyte i juni 2002 görs om för alla andra år, och de åren ger konfidensintervallet (figur 3, panel B och C).

6. **Förlagans metod förklaras på några rader, inget annat.** Två avsnitt heter "Explanation of ... Methodology". Inget stycke förklarar vad en regression är.

Därtill: inget stycke handlar om det egna bidraget. Ordet "contribution" står en gång, i en fotnot om de två artiklar som granskas. Bidraget är meningen om vad tidigare test inte kan förkasta. Slutsatsen är tre stycken utan nya tal. Varje tabelltext säger vad som skattas, kontrollerna, standardfelen och stjärnorna.

## 4. Vad de två har gemensamt med Sabbatuccis sex

| Mönster | Hartzmark och Sussman | Ben-David m.fl. | Sabbatucci |
|---|---|---|---|
| Inget eget litteraturavsnitt | ja | ja | 6 av 6 |
| Förutsägelse eller fråga före varje test | ja | ja | 3 av 3 kodade |
| Mekanismen prövas med en kontrast | ja | ja | 3 av 3 kodade |
| Storlek i enheter som går att väga | ja | ja | 4 av 4 kodade |
| Tabelltexter som bär sig själva | ja | ja | 2 av 2 kodade |
| Placebo | ja | ja | 0 av 6 |
| Minsta påvisbara effekt räknas | nej | nej | 0 av 6 |

Placebo är det som skiljer. De två artiklarna i uppsatsens eget område har det, Sabbatuccis egna har det inte.

## 5. Inte läst i sin helhet

Det här fanns i första versionen. Inget mönster ovan vilar på det.

- **AFA:s lista över de 25 mest citerade artiklarna i Journal of Finance** (https://www.afajof.org/page/Top25Cited). Bara titlar och sammanfattningar.
- **Jegadeesh och Titman (1993)** och **Sirri och Tufano (1998).** Bara sammanfattningar.
- **Cochrane, Writing Tips for Ph.D. Students** (https://bfi.uchicago.edu/wp-content/uploads/2022/06/Cochrane-John-phd_paper_writing_slides.pdf) och **Heads formel för inledningar** (https://blogs.ubc.ca/khead/research/research-advice/formula). Lästa genom ett hämtverktyg som sammanfattar. Använd dem som läsning, inte som belägg.
- **Sex artiklar i förlagans område** är lästa i sin helhet i en annan körning, för innehållet och inte för stilen: `claude/NOTIS_sex_artiklar_lasta_i_sin_helhet_2026-11-20.md`.

Vill ni ha fler toppartiklar lästa så här, säg vilka. Två räcker inte för att säga vad "toppartiklar" gör i allmänhet. De räcker för att säga vad de två närmaste gör.

## 6. Källor

- Hartzmark och Sussman: https://www.ecgi.global/sites/default/files/2026-10/fin-565-2018_do_investors_value_sustainability_a_natural_experiment_exami.pdf. Tryckt: Journal of Finance 74(6), 2789 till 2837, https://doi.org/10.1111/jofi.12841.
- Ben-David, Li, Rossi och Song: https://www.aeaweb.org/conference/2020/preliminary/paper/Att8B6GH. Tryckt: Review of Financial Studies 35(4), 1723 till 1774.
- Kodning: `claude/kodning_forebilder.jsonl`.
