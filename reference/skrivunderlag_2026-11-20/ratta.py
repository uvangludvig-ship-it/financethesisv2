#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ratta.py: mäter ett utkast mot förebilderna och pekar ut rader.

Användning:
    python3 ratta.py utkast.md
    python3 ratta.py utkast.md --forlaga "Ben-David" --max 40
    python3 ratta.py utkast.md --termer termer.json --ut rapport.md

Kräver matt.py och riktvarden.json i samma mapp. Utkastet ska vara ren text
eller markdown (Word: spara som .txt eller kör pandoc -t markdown).
Skriptet räknar. Det bedömer inte om frågan är bra eller om designen håller;
det gör kodbladet (KODBLAD) och en läsare.
"""
import argparse, json, os, re, sys
from decimal import Decimal, ROUND_HALF_UP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matt

HERE = os.path.dirname(os.path.abspath(__file__))
RIKT = json.load(open(os.path.join(HERE, 'riktvarden.json'), encoding='utf-8'))['matt']

TERMER_STD = [
    ['risk indicator', 'risk label', 'risk class', 'risk rating', 'risk category', 'risk score', 'risk number', 'risk figure', 'risk level'],
    ['fund flows', 'net flows', 'capital flows', 'money flows', 'inflows and outflows'],
    ['retail investors', 'individual investors', 'private investors', 'households', 'savers'],
    ['star rating', 'morningstar rating', 'stars'],
    ['treatment group', 'treated funds', 'affected funds', 'reclassified funds'],
]

LAGRE_OK = {'ord_per_mening', 'passiv', 'gardering', 'tom_fras', 'forstarkning', 'FELSUMMA', 'kontrast', 'signifikansord', 'kausal'}
HOGRE_OK = {'vi', 'resultatmeningar_med_tal', 'signifikansmeningar_med_storlek'}

RUBRIK = re.compile(r'^\s*(#{1,6}\s+.+|(\d+(\.\d+)*\.?|[IVX]+\.)\s+[A-Z][^.]{2,70}|abstract|introduction|conclusions?|concluding remarks|references|appendix.*)\s*$', re.I)


def avsnitt(lines):
    """Returnerar lista av (rubrik, startrad, slutrad) 1-baserat. Rubriker:
    markdown (#), numrerade rader eller Abstract/Introduction/Conclusion."""
    idx = []
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if s and len(s) < 90 and RUBRIK.match(s) and not s.endswith(('.', ',', ';')):
            idx.append((re.sub(r'^#+\s*', '', s), i))
    out = []
    for j, (h, a) in enumerate(idx):
        b = idx[j + 1][1] - 1 if j + 1 < len(idx) else len(lines)
        out.append((h, a, b))
    return out


def hitta(avs, monster, niva_topp=True):
    for h, a, b in avs:
        if re.search(monster, h, re.I):
            # utvidga till nästa rubrik på samma eller högre nivå
            return h, a, b
    return None


def block(avs, lines, monster):
    """Text för ett huvudavsnitt inklusive underavsnitt."""
    start = None
    for j, (h, a, b) in enumerate(avs):
        if start is None and re.search(monster, h, re.I):
            start = j
            niva = len(re.match(r'^\s*(#*)', lines[a - 1]).group(1)) or (h.split()[0].count('.') + 1 if re.match(r'\d', h) else 1)
            continue
        if start is not None:
            n2 = len(re.match(r'^\s*(#*)', lines[a - 1]).group(1)) or (h.split()[0].count('.') + 1 if re.match(r'\d', h) else 1)
            if n2 <= niva:
                return avs[start][1], a - 1
    if start is not None:
        return avs[start][1], len(lines)
    return None


def tal_i(text):
    """Tal som kan vara resultat: med enhet eller decimaler. Årtal och
    tabellnummer tas bort. Returnerar lista av (normaliserat, råform)."""
    t = matt.TABELLPEK.sub(' ', text.replace('\u2212', '-'))
    t = re.sub(r'\b(19|20)\d{2}([\u2013-]\d{2,4})?s?\b', ' ', t)
    t = re.sub(r'\b\d{1,3}-day\b', ' ', t)
    res = []
    for m in re.finditer(r'(?<![\w.])-?\d[\d,]*(\.\d+)?\s?(%|percent\b|per cent\b|percentage points?\b|basis points?\b|bps?\b|pp\b|SEK\b|USD\b|EUR\b|million\b|billion\b|bn\b)?', t):
        raw = m.group(0).strip()
        num = re.match(r'-?\d[\d,]*(\.\d+)?', raw).group(0).replace(',', '')
        unit = raw[len(re.match(r'-?\d[\d,]*(\.\d+)?', raw).group(0)):].strip().lower()
        if not unit and '.' not in num:
            continue
        unit = {'percent': '%', 'per cent': '%'}.get(unit, unit)
        res.append((num, unit, raw))
    return res


def riktrad(k, v, dec=2):
    e = RIKT.get(k, {})
    s, w, n, t = e.get('sabb'), e.get('vinn19'), e.get('ej19'), e.get('topp')
    if not (s and w):
        return None
    lo, hi = min(s['min'], w['p25']), max(s['max'], w['p75'])
    if k in LAGRE_OK:
        dom = 'ok' if v <= hi else 'över'
    elif k in HOGRE_OK:
        dom = 'ok' if v >= lo else 'under'
    else:
        dom = 'ok' if lo <= v <= hi else ('över' if v > hi else 'under')
    p = e.get('test', {}).get('p')
    stj = ' *' if (p is not None and p < 0.05) else ''
    f = lambda x: f'{x:.{dec}f}'
    return f"| {k}{stj} | {f(v)} | {f(s['min'])}–{f(s['max'])} | {f(t['median']) if t else '.'} | {f(w['p25'])}–{f(w['p75'])} | {f(n['median']) if n else '.'} | {dom} |"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fil')
    ap.add_argument('--forlaga', default=None, help='efternamn på förlagans första författare')
    ap.add_argument('--max', type=int, default=25, help='högst så många rader per regel (0 = alla)')
    ap.add_argument('--termer', default=None, help='json: lista av listor med varianter av samma term')
    ap.add_argument('--ut', default=None)
    a = ap.parse_args()
    raw = open(a.fil, encoding='utf-8', errors='ignore').read()
    lines = raw.split('\n')
    # klipp referenslistan för räkningen men behåll radnummer
    slut = len(lines)
    for i, l in enumerate(lines):
        if re.match(r'^\s*#*\s*(\d+\.?\s*)?(references|bibliography|referenser|källor)\s*$', l.strip(), re.I) and i > len(lines) * 0.4:
            slut = i
    kropp = '\n'.join(lines[:slut])
    sents = matt.meningar(kropp)
    n = sum(matt.ord_antal(s) for _, s in sents) or 1
    tk = matt.takter(kropp)
    dm = matt.dokmatt(raw)
    avs = avsnitt(lines[:slut])
    R = []
    P = R.append
    P(f'# Rättningsrapport: {os.path.basename(a.fil)}')
    P('')
    P(f'{n} ord i löptext, {len(sents)} meningar, {len(avs)} rubriker. Radnummer avser filen.')
    P('')

    # ---------------------------------------------------------- A
    P('## A. Mått mot riktvärden')
    P('')
    P('Takter är per 1 000 ord. Spannet går från det lägsta till det högsta av Sabbatuccis sex artiklar och vinnarnas mittersta hälft (p25 till p75). "ok": inom spannet, eller på rätt sida om det (färre passiva, fler tal). En stjärna: måttet skiljer vinnare 2019 till 2025 från övriga uppsatser samma år (p under 0,05, 12 mot 362). Övriga mått beskriver förebilderna men skiljer inte vinnare från andra.')
    P('')
    P('| Mått | Utkastet | Sabbatucci min–max | Toppartiklar | Vinnare p25–p75 | Övriga median | Läge |')
    P('|---|---|---|---|---|---|---|')
    for k in ['ord_per_mening', 'vi', 'passiv', 'gardering', 'signifikansord', 'kontrast', 'kausal', 'forstarkning', 'tom_fras']:
        if tk.get(k) is not None:
            r = riktrad(k, tk[k]);  r and P(r)
    for k in ['resultatmeningar_med_tal', 'signifikansmeningar_med_storlek']:
        if tk.get(k) is not None:
            r = riktrad(k, tk[k]);  r and P(r)
    fel = sum(tk[k] for k in json.load(open(os.path.join(HERE, 'riktvarden.json')))['felsumma_regler'])
    r = riktrad('FELSUMMA', fel);  r and P(r)
    P('')
    P('FELSUMMA är flaggade meningar per 1 000 ord för reglerna R02, R03, R04, R05, R06, R08, R10, R11, R14 och R15.')
    P('')

    # ---------------------------------------------------------- B
    P('## B. Kursregler och uppbyggnad')
    P('')
    def ja(x): return 'ja' if x else 'nej'
    ab = matt.sammanfattning(raw)
    intro = block(avs, lines, r'^(\d+\.?\s*|[IVX]+\.\s*)?introduction')
    conc = block(avs, lines, r'conclu')
    lit = block(avs, lines, r'literature|previous research|related work|theoretical (framework|background)')
    rows = []
    rows.append(('Innehållsförteckning', ja(dm['D01_innehallsforteckning']), 'nej', 'Kursbild 14 och 18; 0 av 6 Sabbatucci, 2 av 12 vinnare'))
    rows.append(('Sammanfattning, ord', str(matt.ord_antal(ab)) if ab else 'hittas inte', '41–101 (Sabbatucci), 135–182 (vinnare)', 'mätt'))
    rows.append(('Tal med enhet i sammanfattningen', ja(dm['D06_tal_i_sammanfattningen']), 'ja', '2 av 2 toppartiklar; vanligt hos Sabbatucci men ingen regel'))
    if intro:
        it = '\n'.join(lines[intro[0]:intro[1]])
        iw = matt.ord_antal(matt.prosa(it))
        rows.append(('Inledning, ord', str(iw), '900–1 800 (2 till 4 sidor)', 'Kursbild 19'))
        isent = matt.meningar(it)
        acc = 0; pos = None; litpos = None
        tot = sum(matt.ord_antal(s) for _, s in isent) or 1
        for _, s in isent:
            if pos is None and matt.RESULTAT.search(s):
                pos = acc / tot
            acc += matt.ord_antal(s)
        rows.append(('Första resultatmeningen, andel in i inledningen', f'{100 * pos:.0f} %' if pos is not None else 'ingen hittad', '13–81 % (Sabbatucci)', 'mätt'))
        rows.append(('Tal med enhet i inledningen', str(len([x for x in tal_i(matt.SIGNIVA.sub(" ", it)) if x[1]])), 'minst 1', '11 av 12 vinnare, 3 av 6 Sabbatucci, 2 av 2 topp'))
        if a.forlaga:
            first = ' '.join(it.split()[:450])
            rows.append((f'Förlagan ({a.forlaga}) på inledningens första sida', ja(a.forlaga.lower() in first.lower()), 'ja', '11 av 12 vinnare'))
            rows.append((f'Förlagan ({a.forlaga}) i sammanfattningen', ja(a.forlaga.lower() in ab.lower()), 'valfritt', '2 av 12 vinnare'))
        rows.append(('Färdplan i inledningen', ja(matt.DOK['D11_fardplan'].search(it)), 'ja, ett kort stycke', '5 av 6 Sabbatucci, 7 av 12 vinnare'))
    else:
        rows.append(('Inledning', 'rubriken hittas inte', '', ''))
    if lit:
        lw = matt.ord_antal(matt.prosa('\n'.join(lines[lit[0]:lit[1]])))
        rows.append(('Eget litteratur- eller teoriavsnitt, ord', str(lw), 'under 450 (en sida)', 'Kursbild 19 och kursplan avsnitt 8 föreskriver ett kort eget avsnitt; 0 av 6 Sabbatucci, 0 av 2 topp, 10 av 12 vinnare har ett'))
    else:
        rows.append(('Eget litteratur- eller teoriavsnitt', 'nej', 'ett kort, under 450 ord', 'Kursbild 19 och kursplan avsnitt 8; Sabbatucci och toppartiklarna har litteraturen i inledningen'))
    if conc:
        cw = matt.ord_antal(matt.prosa('\n'.join(lines[conc[0]:conc[1]])))
        rows.append(('Slutsats, ord', str(cw), '61–1 175 (Sabbatucci)', 'mätt'))
    rows.append(('Placebo eller falsifiering nämns', ja(dm['D03_placebo']), 'ja', '2 av 2 topp, 2 av 12 vinnare'))
    rows.append(('Styrka eller minsta påvisbara effekt nämns', ja(dm['D04_styrka_mde']), 'ja', 'Kursbild 20; ingen förebild räknar MDE'))
    rows.append(('Konfidensintervall nämns', ja(dm['D12_konfidensintervall']), 'ja', '2 av 2 topp'))
    rows.append(('Ekonomisk storlek nämns med de orden', ja(dm['D05_ekonomisk_storlek']), 'valfritt', 'storleken ska finnas, orden behövs inte'))
    rows.append(('Klustrade standardfel nämns', ja(dm['D13_klustrade_fel']), 'ja om paneldata', '2 av 2 topp'))
    rows.append(('Avsnitt som heter Limitations', ja(dm['D08_avsnitt_begransningar']), 'nej, skriv dem där de biter', '0 av 6 Sabbatucci, 1 av 12 vinnare, 29 % av övriga'))
    rows.append(('Numrerade hypoteser', ja(dm['D07_formella_hypoteser']), 'valfritt', '3 av 12 vinnare, 0 av 6 Sabbatucci'))
    P('| Punkt | Utkastet | Riktvärde | Stöd |')
    P('|---|---|---|---|')
    for r in rows:
        P('| ' + ' | '.join(r) + ' |')
    P('')

    # ---------------------------------------------------------- C
    P('## C. Rader att se över')
    P('')
    P('Varje regel: antal, takt per 1 000 ord, riktvärde, sedan raderna.')
    P('')
    UPPLYS = {'R01', 'R07', 'R09', 'R12', 'R16'}
    for rid, (namn, atgard, f) in matt.REGLER.items():
        hits = [(ln, s) for ln, s in sents if f(s)]
        e = RIKT.get(rid, {})
        s_, w_ = e.get('sabb'), e.get('vinn19')
        takt = 1000 * len(hits) / n
        rik = f"Sabbatucci {s_['min']:.2f}–{s_['max']:.2f}, vinnare {w_['p25']:.2f}–{w_['p75']:.2f}" if s_ and w_ else ''
        typ = 'upplysning' if rid in UPPLYS else 'rätta'
        P(f'### {rid} {namn} ({typ})')
        P('')
        P(f'{len(hits)} träffar, {takt:.2f} per 1 000 ord. Riktvärde: {rik}. Åtgärd: {atgard}')
        P('')
        lim = hits if a.max == 0 else hits[:a.max]
        for ln, s in lim:
            P(f'- rad {ln}: {s[:170]}{"…" if len(s) > 170 else ""}')
        if len(hits) > len(lim):
            P(f'- … och {len(hits) - len(lim)} till (kör med --max 0)')
        P('')

    # ---------------------------------------------------------- D
    P('## D. Talkontroll')
    P('')
    if not (intro or conc or ab):
        P('Hittar varken Abstract, Introduction eller Conclusion som rubrik. Talkontrollen kräver dem.')
    else:
        delar = {}
        if ab: delar['sammanfattning'] = ab
        if intro: delar['inledning'] = '\n'.join(lines[intro[0]:intro[1]])
        if conc: delar['slutsats'] = '\n'.join(lines[conc[0]:conc[1]])
        skip = set()
        for nm in ('inledning', 'slutsats'):
            blk = intro if nm == 'inledning' else conc
            if blk: skip |= set(range(blk[0], blk[1]))
        rest = '\n'.join(l for i, l in enumerate(lines) if i not in skip)
        if ab: rest = rest.replace(ab, ' ')
        body = tal_i(rest)
        bnum = {}
        for num, unit, rawf in body:
            bnum.setdefault(num, set()).add(unit)
        P('Varje tal med enhet eller decimaler i sammanfattning, inledning och slutsats, och om samma tal står i resten av texten (resultat, tabeller).')
        P('')
        P('| Del | Tal | I resten av texten |')
        P('|---|---|---|')
        allt = {}
        for nm, txt in delar.items():
            seen = set()
            for num, unit, rawf in tal_i(matt.SIGNIVA.sub(' ', txt)):
                if (num, unit) in seen: continue
                seen.add((num, unit)); allt.setdefault(nm, []).append((num, unit))
                if num in bnum:
                    st = 'ja'
                else:
                    nar = []
                    if '.' in num:
                        dec = len(num.split('.')[1])
                        q = Decimal(1).scaleb(-dec)
                        for b in bnum:
                            if '.' in b and len(b.split('.')[1]) > dec:
                                try:
                                    if Decimal(b).quantize(q, rounding=ROUND_HALF_UP) == Decimal(num): nar.append(b)
                                except Exception:
                                    pass
                        nar = sorted(set(nar))
                    st = ('avrundat från ' + ', '.join(nar[:3])) if nar else 'SAKNAS'
                P(f'| {nm} | {rawf} | {st} |')
        P('')
        # samma enhet, olika tal mellan delarna
        if len(allt) > 1:
            P('Tal som står i en av delarna men inte i de andra (kontrollera att det inte är samma storhet med olika värde):')
            P('')
            names = list(allt)
            for nm in names:
                andra = set(x for o in names if o != nm for x in allt[o])
                egna = [f'{u[0]} {u[1]}'.strip() for u in allt[nm] if u not in andra and u[1]]
                if egna:
                    P(f'- bara i {nm}: ' + ', '.join(egna[:30]))
    P('')

    # ---------------------------------------------------------- E
    P('## E. Tabeller och figurer')
    P('')
    cap = {}
    for i, l in enumerate(lines):
        m = re.match(r'^\s*[*_#>\s]*(Table|Figure|Tabell|Figur)\s+([IVXLC]+|\d+)[a-z]?\s*([:.*_]|$|[a-z]\))', l)
        if m:
            key = (m.group(1).lower()[:3], m.group(2))
            txt = []
            for l2 in lines[i:i + 14]:
                if not l2.strip() and txt: break
                if l2.strip().startswith('|'): break
                txt.append(l2.strip())
            if key not in cap: cap[key] = (i + 1, ' '.join(txt))
    ref = {}
    for ln, s in sents:
        for m in matt.TABELLPEK.finditer(s):
            ref.setdefault((m.group(1).lower()[:3], m.group(2)), []).append(ln)
    if not cap:
        P('Inga tabell- eller figurtexter hittade (en rad som börjar med "Table 1:" eller "Table 1.").')
    else:
        P('Fem delar som Sabbatuccis tabelltexter har (JF tabell II, RFS tabell 4): vad som skattas, variabeldefinitioner, standardfel, stjärnor, urval och period. Figurer: vad som visas och period.')
        P('')
        P('| Objekt | Rad | Ord | Saknas i texten | Nämns i löptext |')
        P('|---|---|---|---|---|')
        for key in sorted(cap, key=lambda k: (k[0], cap[k][0])):
            ln, txt = cap[key]
            w = matt.ord_antal(txt)
            miss = []
            if key[0] == 'tab':
                reg = bool(re.search(r'regress|coefficient|estimate|OLS|fixed effects', txt, re.I))
                if not re.search(r'\b(19|20)\d{2}\b|sample|period|observations', txt, re.I): miss.append('urval/period')
                if reg:
                    if not re.search(r'dependent variable|regress\w* of|outcome', txt, re.I): miss.append('beroende variabel')
                    if not re.search(r'standard errors?|clustered|robust|Newey|t-stat', txt, re.I): miss.append('standardfel')
                    if not re.search(r'\*|significan|10\s?%|5\s?%|1\s?%', txt, re.I): miss.append('stjärnor')
                    if not re.search(r'\bis (the|a|an|defined|equal)|denotes|equals|measured as|dummy|indicator|defined as', txt, re.I): miss.append('variabeldefinitioner')
            else:
                if not re.search(r'shows?|plots?|displays?|presents?|illustrates?|reports?', txt, re.I): miss.append('vad som visas')
                if not re.search(r'\b(19|20)\d{2}\b|sample|period', txt, re.I): miss.append('period')
            if w < 25: miss.append('kort (under 25 ord)')
            nm = ('Table ' if key[0] == 'tab' else 'Figure ') + key[1]
            P(f"| {nm} | {ln} | {w} | {', '.join(miss) if miss else 'inget'} | {'ja' if key in ref else 'NEJ'} |")
        saknar = sorted(k for k in ref if k not in cap)
        if saknar:
            P('')
            P('Nämns i löptexten men saknar tabell- eller figurtext i filen: ' + ', '.join((('Table ' if k[0] == 'tab' else 'Figure ') + k[1]) for k in saknar))
    P('')

    # ---------------------------------------------------------- F
    P('## F. Termer och stavning')
    P('')
    grupper = json.load(open(a.termer, encoding='utf-8')) if a.termer else TERMER_STD
    low = kropp.lower()
    nagot = False
    for g in grupper:
        c = {t: len(re.findall(r'\b' + re.escape(t.lower()) + r'\b', low)) for t in g}
        anv = {t: k for t, k in c.items() if k >= 2}
        if len(anv) >= 2:
            nagot = True
            P('- samma sak med flera namn? ' + ', '.join(f'"{t}" {k}' for t, k in sorted(anv.items(), key=lambda x: -x[1])))
    for uk, us in UKUS():
        cu = len(re.findall(uk, low)); ca = len(re.findall(us, low))
        if cu and ca:
            nagot = True
            P(f'- blandad stavning: {uk} {cu}, {us} {ca}')
    if not nagot:
        P('Inget att anmärka.')
    P('')
    ut = '\n'.join(R)
    if a.ut:
        open(a.ut, 'w', encoding='utf-8').write(ut)
        print('skrev', a.ut)
    else:
        print(ut)


def UKUS():
    return matt.UK_US


if __name__ == '__main__':
    main()
