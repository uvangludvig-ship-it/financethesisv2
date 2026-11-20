#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""matt.py: exakta definitioner for matten i rattningsinstrumentet.

Varje regel har ett id, ett namn och en regex eller funktion. Samma kod
anvands for att rakna fram riktvarden pa forebilderna (riktvarden.py) och
for att ratta ett utkast rad for rad (ratta.py). Inget i filen ar en
bedomning; allt ar rakning.
"""
import re

# ---------------------------------------------------------------- text

def prosa(raw):
    """Behall lopande text ur ett pdftotext-utdrag och klipp referenslistan.
    Samma regel som clean.py: rader med minst 55 % bokstaver; langa rader
    maste ha minst tva ord pa fyra bokstaver."""
    lines = raw.splitlines()
    cut = None
    for i, l in enumerate(lines):
        if re.match(r'^\s*(\d+\.?\s*)?(references|bibliography|reference list|list of references|works cited)\s*$', l.strip(), re.I):
            if i > len(lines) * 0.4:
                cut = i
    if cut:
        lines = lines[:cut]
    out = []
    for l in lines:
        s = l.strip()
        if not s:
            out.append('')
            continue
        a = sum(c.isalpha() for c in s)
        if a / max(1, len(s)) < 0.55:
            continue
        if len(s) > 40 and len(re.findall(r'[A-Za-z]{4,}', s)) < 2:
            continue
        out.append(s)
    return '\n'.join(out)


ABBR = r'(?:et al|e\.g|i\.e|cf|vs|Fig|Eq|Eqs|No|pp|p|ca|approx|resp|Sec|Tab|Dr|Prof|Mr|Ms|St|Inc|Ltd|Corp|U\.S|U\.K)'


def meningar(text):
    """Dela text i meningar. Returnerar lista av (startrad, mening).
    Tom rad bryter alltid. Radnummer ar 1-baserade."""
    res = []
    lines = text.split('\n')
    buf, start = [], None

    def flush():
        nonlocal buf, start
        if not buf:
            return
        block = ' '.join(buf)
        # skydda forkortningar och decimaler
        prot = re.sub(r'\b(' + ABBR + r')\.', lambda m: m.group(1) + '<DOT>', block)
        prot = re.sub(r'(\d)\.(\d)', r'\1<DOT>\2', prot)
        parts = re.split(r'(?<=[.!?])["\')\]]*\s+(?=[A-Z(\["\'])', prot)
        # radnummer: rakna fram via teckenposition
        pos = 0
        offsets = []
        acc = 0
        for i, b in enumerate(buf):
            offsets.append((acc, start + i))
            acc += len(b) + 1
        for p in parts:
            s = p.replace('<DOT>', '.').strip()
            if s:
                ln = start
                for off, lno in offsets:
                    if off <= pos:
                        ln = lno
                res.append((ln, s))
            pos += len(p) + 1
        buf, start = [], None

    for i, l in enumerate(lines, 1):
        s = l.strip()
        if not s or s.startswith('#') or s.startswith('|'):
            flush()
            continue
        if start is None:
            start = i
        buf.append(s)
    flush()
    return res


def ord_antal(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

# ------------------------------------------------------------- regler

PASSIV = re.compile(r'\b(is|are|was|were|been|be|being)\s+(\w+ly\s+)?\w+(ed|own|ound|iven|aken|ought|uilt|eld)\b', re.I)
GARDERING = re.compile(r'\b(may|might|could|possibly|perhaps|seems?|appears?|likely|plausibl\w+|potentially|arguably|presumably|somewhat|to some extent)\b', re.I)
SIGNIF = re.compile(r'\b(statistically significant|significan(t|ce|tly)|insignifican(t|ce|tly)|p-?values?|t-?stat(istic)?s?)\b', re.I)
SIGNIVA = re.compile(r'(at|on) the\s+(1|5|10|one|five|ten)\s?(%|percent|per cent)(\s+(significance\s+)?level)?|(1|5|10)\s?(%|percent)\s+(significance\s+)?level|p\s*[<=>]\s*0?\.\d+|t\s*=\s*-?\d+\.\d+|(90|95|99)\s?(%|percent)', re.I)
TAL_ENHET = re.compile(r'(?<![\w.])-?\d[\d,]*(\.\d+)?\s?(%|percent\b|per cent\b|percentage points?\b|basis points?\b|bps?\b|pp\b|SEK\b|USD\b|EUR\b|kr\b|million\b|billion\b|bn\b|months?\b|years?\b|days?\b|standard deviations?\b)|[$€£]\s?\d', re.I)
DECIMAL = re.compile(r'(?<![\w.])-?\d+\.\d+')
NOLL = re.compile(r'\b(no|not any|does not|do not|did not|cannot|can not|fails? to|failed to|unable to)\b[^.;]{0,50}\b(effect|impact|relationship|relation|difference|evidence|influence|affect|predict|explain|association|response|react)\w*', re.I)
NOLL_OK = re.compile(r'confidence interval|power|detect|standard error|rule out|bound|as small as|as large as|smaller than|larger than', re.I)
OVERANSPRAK = re.compile(r'\b(proves?|proved|proven|proof that|confirm(s|ed)? (the|our|this) hypothes\w+|undoubtedly|without (a )?doubt|accept (the|our) null|validate[sd]? (the|our)|clearly (show|demonstrate|prove)s?|definitively|conclusively)\b', re.I)
KAUSAL = re.compile(r'\b(caus(e|es|ed|ing)|leads? to|led to|results? in|resulted in|driv(es|en by)|is driven|are driven|due to|because of|thanks to|the (effect|impact) of)\b', re.I)
TOM_FRAS = re.compile(r'\b(it is important to note|it should be noted|it is worth (noting|mentioning)|it is interesting to note|as (previously |already )?mentioned( above| earlier| before)?|as (stated|discussed|described|explained) (above|earlier|before|previously)|in order to|the fact that|needless to say|it goes without saying|at the end of the day|in today\'s world|plays? an? (important|crucial|key|vital) role|a wide range of|in terms of|with regards? to|when it comes to|it can be (seen|observed|noted) that|it is (clear|evident|obvious) that)\b', re.I)
FORSTARKNING = re.compile(r'\b(very|extremely|highly|incredibly|clearly|obviously|indeed|interestingly|strikingly|striking|remarkabl[ey]|notabl[ey]|importantly|crucial(ly)?|vast(ly)?|tremendous(ly)?|huge(ly)?|dramatic(ally)?)\b', re.I)
FORST = re.compile(r'\b(first (paper|study|thesis|to)\b|to (the best of )?our knowledge|has (not|never) been (studied|examined|investigated|tested)|unexplored|novel\b|unique(ly)?\b|fill(s|ing)? (a|the|this) gap)', re.I)
KALLA_FORST = re.compile(r'^[A-Z][A-Za-z\-\']+(,? [A-Z][A-Za-z\-\']+)*( et\.? al\.?,?| and [A-Z][A-Za-z\-\']+| & [A-Z][A-Za-z\-\']+)?\s*\((19|20)\d{2}[a-z]?\)')
TANKSTRECK = re.compile(r'—|\s–\s')
DENNA_UPPSATS = re.compile(r'\b(this|the present|the current) (thesis|paper|study|essay|report|article)\b|\bthe authors?\b', re.I)
PEDAGOGIK = re.compile(r'\b(is defined as|are defined as|can be defined as|refers to|is a (statistical |common |widely used |popular )?(method|technique|measure|model|theory|concept|tool|framework) (that|which|used|for|of)|is an? (empirical|econometric|statistical) (method|technique|tool)|(states|posits|suggests) that (markets|investors|prices|all available))\b', re.I)
TABELLPEK = re.compile(r'\b(Table|Figure|Fig\.|Graph|Tabell|Figur)\s+([IVXLC]+|\d+)[a-z]?\b')
RESULTAT = re.compile(r'\b(we find|we show|we document|we estimate|we observe|our (results?|estimates?|findings?)|the (coefficient|estimate|point estimate)|results (show|indicate|suggest))\b', re.I)
VI = re.compile(r'\b(we|our|us)\b', re.I)
KONTRAST = re.compile(r'\b(however|in contrast|conversely|whereas|by contrast|instead|nevertheless|nonetheless)\b', re.I)

UK_US = [('behaviour', 'behavior'), ('analyse', 'analyze'), ('favour', 'favor'), ('labour', 'labor'),
         ('organis', 'organiz'), ('recognis', 'recogniz'), ('emphasis', 'emphasiz'), ('modell', 'model(?=ed|ing)'),
         ('centre', 'center'), ('programme', 'program\\b'), ('summaris', 'summariz'), ('categoris', 'categoriz'),
         ('colour', 'color'), ('defence', 'defense'), ('utilis', 'utiliz'), ('characteris', 'characteriz')]


def har_storlek(s):
    """Finns ett tal som kan vara en storlek, efter att signifikansnivaer,
    p-varden och t-varden har tagits bort?"""
    t = SIGNIVA.sub(' ', s.replace('\u2212', '-'))
    t = TABELLPEK.sub(' ', t)
    return bool(TAL_ENHET.search(t) or DECIMAL.search(t))


# varje regel: id -> (namn, kort atgard, funktion mening -> bool)
REGLER = {
    'R01': ('Lång mening (över 40 ord)', 'Dela i två. En tanke per mening.',
            lambda s: ord_antal(s) > 40),
    'R02': ('Två eller fler passiva led i meningen', 'Skriv vem som gör vad: "we estimate", inte "is estimated".',
            lambda s: len(PASSIV.findall(s)) >= 2),
    'R03': ('Två eller fler garderingsord i meningen', 'Behåll högst ett. Säg i stället vad som är osäkert och varför.',
            lambda s: len(GARDERING.findall(s)) >= 2),
    'R04': ('Signifikans utan storlek', 'Ge koefficienten med enhet och sätt den i relation till något (medel, basnivå, förlagans tal).',
            lambda s: bool(SIGNIF.search(s)) and not har_storlek(s)),
    'R05': ('Nollresultat sagt som "ingen effekt"', 'Skriv vad datan kan utesluta: konfidensintervall eller minsta påvisbara effekt.',
            lambda s: bool(NOLL.search(s)) and not NOLL_OK.search(s)),
    'R06': ('Överanspråk', 'Byt "prove/confirm" mot vad testet visar: "consistent with", "we reject".',
            lambda s: bool(OVERANSPRAK.search(s))),
    'R07': ('Kausalt språk', 'Kontrollera att designen bär ordet. Annars "is associated with".',
            lambda s: bool(KAUSAL.search(s))),
    'R08': ('Tom fras', 'Stryk frasen. Meningen står kvar utan den.',
            lambda s: bool(TOM_FRAS.search(s))),
    'R09': ('Förstärkningsord', 'Stryk ordet eller byt det mot ett tal.',
            lambda s: bool(FORSTARKNING.search(s))),
    'R10': ('Anspråk på att vara först eller unik', 'Högst ett i hela uppsatsen, och bara om litteratursökningen bär det.',
            lambda s: bool(FORST.search(s))),
    'R11': ('Meningen börjar med någon annans namn', 'Börja med det egna påståendet och sätt källan sist.',
            lambda s: bool(KALLA_FORST.match(s))),
    'R12': ('Tankstreck', 'Byt mot komma, punkt eller parentes.',
            lambda s: bool(TANKSTRECK.search(s))),
    'R14': ('"This thesis/paper" eller "the authors" i stället för "we"', 'Skriv "we".',
            lambda s: bool(DENNA_UPPSATS.search(s))),
    'R15': ('Läroboksförklaring', 'Kursen: ingen pedagogisk förklaring. Stryk eller hänvisa till källan.',
            lambda s: bool(PEDAGOGIK.search(s))),
    'R16': ('Tabellhänvisning utan tal', 'Säg vad tabellen visar, med talet, i samma mening.',
            lambda s: bool(TABELLPEK.search(s)) and not har_storlek(s) and 4 <= ord_antal(s) < 30),
}

TAKT = {  # antal traffar per 1 000 ord (inte flaggor per mening)
    'passiv': PASSIV, 'gardering': GARDERING, 'signifikansord': SIGNIF, 'vi': VI,
    'kontrast': KONTRAST, 'kausal': KAUSAL, 'forstarkning': FORSTARKNING, 'tom_fras': TOM_FRAS,
}

# ------------------------------------------------- dokumentniva (ja/nej)

DOK = {
    'D01_innehallsforteckning': re.compile(r'^\s*#*\s*(table of contents|contents|innehall(sforteckning)?)\s*$', re.I | re.M),
    'D02_eget_litteraturavsnitt': re.compile(r'^\s*#*\s*(\d+(\.\d+)*\.?\s+|[IVX]+\.\s+)?(?=[^\n]{0,70}$)(?![^\n]*[.,;:]\s*$)(?:[A-Z&][\w,&\-]*\s+){0,6}(literature|previous (research|studies)|prior (research|studies)|related (works?|research)|theoretical\s+(framework|background))(\s+[\w&\-]+){0,4}\s*$', re.I | re.M),
    'D03_placebo': re.compile(r'placebo|falsification', re.I),
    'D04_styrka_mde': re.compile(r'minimum detectable|statistical power|power to detect|underpowered|low power|lack(s|ed)? (the )?(statistical )?power|limits? (our|the) power|\bMDE\b', re.I),
    'D05_ekonomisk_storlek': re.compile(r'economic(ally)? (significan|large|small|meaningful|magnitude|importan)|economic (significance|magnitude)', re.I),
    'D07_formella_hypoteser': re.compile(r'\bH\d\s*[:.)]|\bH[0aA]\b\s*:|hypothesis \d|hypothesis (one|two|i+)\b', re.I),
    'D08_avsnitt_begransningar': re.compile(r'^\s*#*\s*(\d+(\.\d+)*\.?\s+|[IVX]+\.\s+)?limitations?( of (the|this|our) (study|thesis|paper))?( and .{0,30})?\s*$', re.I | re.M),
    'D09_replikering_namnd': re.compile(r'replicat', re.I),
    'D11_fardplan': re.compile(r'(remainder|rest) of (the|this) (paper|thesis|study|essay)|remaining paper|(organi[sz]ed|structured|proceeds|outlined) as follows|Section\s+(\d+|[IVX]+)\.?\s+(presents?|describes?|places|reviews?|discuss\w*|provides?|outlines?|introduces?|details|contains|concludes)\b[^\n]{0,400}Section\s+(\d+|[IVX]+)', re.I),
    'D12_konfidensintervall': re.compile(r'confidence (interval|band)', re.I),
    'D13_klustrade_fel': re.compile(r'cluster', re.I),
    'D14_framtida_forskning_rubrik': re.compile(r'^\s*#*\s*(\d+(\.\d+)*\.?\s+|[IVX]+\.\s+)?(suggestions for |directions for |avenues for )?(future|further) research\s*$', re.I | re.M),
}


def sammanfattning(text):
    m = re.search(r'\babstract\b[:.]?', text, re.I)
    if not m or m.start() > len(text) * 0.25:
        return ''
    rest = text[m.end():m.end() + 4000]
    e = re.search(r'\bkey\s?words?\b|\bJEL\b|\n\s*(1\.?|I\.?)?\s*introduction\b|\bauthors?:|\btutors?:|\backnowledg', rest, re.I)
    ab = rest[:e.start()] if e else rest[:1800]
    return ab.strip()


def dokmatt(text):
    """Ja/nej-matt pa hela texten. Returnerar dict."""
    d = {k: int(bool(rx.search(text))) for k, rx in DOK.items()}
    ab = sammanfattning(text)
    d['D06_tal_i_sammanfattningen'] = int(bool(ab) and bool(TAL_ENHET.search(SIGNIVA.sub(' ', ab)) or DECIMAL.search(SIGNIVA.sub(' ', ab))))
    d['D15_sammanfattning_hittad'] = int(bool(ab))
    d['sammanfattning_ord'] = ord_antal(ab) if ab else None
    # D10: fraga i forsta 15 % av texten
    n15 = text[:int(len(text) * 0.15)]
    d['D10_fraga_tidigt'] = int(bool(re.search(r'[A-Za-z]{3,}\s?\?', n15)))
    return d


def takter(text):
    """Takter per 1 000 ord och flaggor per 1 000 ord for varje regel."""
    sents = meningar(text)
    n = sum(ord_antal(s) for _, s in sents) or 1
    hela = sorted(ord_antal(s) for _, s in sents if ord_antal(s) >= 5 and s[0].isupper() and s[-1] in '.?!')
    out = {'ord': n, 'meningar': len(sents),
           'ord_per_mening': (hela[len(hela) // 2] if hela else None)}
    joined = ' '.join(s for _, s in sents)
    for k, rx in TAKT.items():
        out[k] = 1000 * len(rx.findall(joined)) / n
    for rid, (_, _, f) in REGLER.items():
        out[rid] = 1000 * sum(1 for _, s in sents if f(s)) / n
    res = [s for _, s in sents if RESULTAT.search(s)]
    out['resultatmeningar_med_tal'] = (sum(1 for s in res if har_storlek(s)) / len(res)) if res else None
    sig = len(SIGNIF.findall(joined))
    out['signifikansmeningar_med_storlek'] = None
    sm = [s for _, s in sents if SIGNIF.search(s)]
    if sm:
        out['signifikansmeningar_med_storlek'] = sum(1 for s in sm if har_storlek(s)) / len(sm)
    return out
