"""Fáze 2: rozložení knihovny na díly a přiřazení k deskám z půdy.

Spuštění:  python3 drevo/prirazeni.py
Čte drevo/inventar.csv, zapisuje drevo/prirazeni.json a data do knihovna.html.
Rozměry v mm. Jen standardní knihovna Pythonu.
"""
import csv, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- geometrie (mm) ----
W, H, t, TOPGAP, PLINTH, D = 2370, 2593, 19, 20, 140, 250
N, K, R = 7, 4, 7                       # sloupce celkem, sloupce hlavní části, řady
HTOP = H - TOPGAP
sw = (W - (N + 1) * t) / N              # světlost čtvercové přihrádky (jako v3)
sh = (HTOP - PLINTH - (R + 1) * t) / R
NOOK = 730                              # šířka výklenku pro křeslo (od obkladu)
# světlosti sloupců: 1–2 nad křeslem širší, 3–4 čtverce, 5–6 dvojitá nad dveřmi, 7 čtverec
CW = [(NOOK - 2 * t) / 2] * 2 + [sw, sw]
CW += [(W - 8 * t - sum(CW) - sw) / 2] * 2 + [sw]
XL = [0.0]
for c in CW: XL.append(XL[-1] + c + t)
xl = lambda j: XL[j]                    # levá hrana svislé linie j
zb = lambda k: PLINTH + k * (sh + t)    # spodní hrana vodorovné úrovně k
KERF = 4                                # prořez + začištění
WALLGAP = 5                             # vůle u stěny
SOKL_ZAP = 30                           # zapuštění soklu
SAFE = 15                               # min. rezerva v pruhu, když to jde

def exists(c, r):                       # přihrádka sloupec c, řada r (odspodu)
    if c < 1 or r < 1 or r > R: return False
    if c <= K: return not (c <= 2 and r <= 3)   # vynecháno za křeslem
    return c <= N and r == R                     # most nad dveřmi
OMIT_H = {(6, 2)}                        # úroveň k nad sloupcem c (busta)
OMIT_V = {(1, 4), (3, 5), (5, 7)}        # linie j v řadě r (dvojité přihrádky)
def Hp(k, c):
    if not exists(c, k) and not exists(c, k + 1): return False
    if c > K and k < 6: return False
    return (k, c) not in OMIT_H
def Vp(j, r):
    if not exists(j, r) and not exists(j + 1, r): return False
    return (j, r) not in OMIT_V

CR = {}
for j in range(N + 1):
    for k in range(R + 1):
        vb = k >= 1 and Vp(j, k); va = k + 1 <= R and Vp(j, k + 1)
        hl = j >= 1 and Hp(k, j); hr = j + 1 <= N and Hp(k, j + 1)
        if (vb or va) and (hl or hr): CR[(j, k)] = dict(vb=vb, va=va, hl=hl, hr=hr)

# Kdo je v křížení průběžný: H = vodorovná deska přechází přes svislou,
# V = svislá prochází a vodorovné do ní z boku dosedají na podpěrky.
# Vybráno optimalizací tak, aby žádný díl nebylo nutné kupovat.
# Pravý bok (linie 4) a příčka u výklenku (linie 2) jsou z jednoho kusu a stojí na spodní polici.
# Ostatní svislé díly jsou co nejdelší (min. počet dělení bez nákupu). Boční díl mostu (linie 7)
# se šroubuje do sádrokartonu, dno mostu i horní deska do něj dosedají z boku.
# Levý bok (linie 0) je jedna deska slepená předem z co nejméně kusů (spoj ve výšce police),
# přišroubovaná k obkladu; police vlevo do něj dosedají na podpěrky.
PATTERN = """
7 H H H H H . H V
6 V V V V V . H V
5 V V V H V . . .
4 V H V H V . . .
3 V . V V V . . .
2 . . V H V . . .
1 . . V V V . . .
0 . . H H H . . .
"""
A = {}
for line in PATTERN.strip().splitlines():
    k, *cols = line.split()
    for j, v in enumerate(cols):
        if v != '.': A[(j, int(k))] = v
assert set(A) == set(CR), (set(A) ^ set(CR))

# ---- díly ----
P = []
for k in range(R + 1):
    c = 1
    while c <= N:
        if not Hp(k, c): c += 1; continue
        c0 = c
        while c <= N and Hp(k, c): c += 1
        js, je = c0 - 1, c - 1
        x0 = xl(js) if A.get((js, k), 'H') == 'H' else xl(js) + t
        sj = js
        for j in range(js + 1, je):
            if A.get((j, k)) == 'V':
                P.append(dict(o='H', k=k, j0=sj, j1=j, x0=x0, x1=xl(j), z0=zb(k), z1=zb(k) + t)); x0 = xl(j) + t; sj = j
        x1 = xl(je) + t if A.get((je, k), 'H') == 'H' else xl(je)
        P.append(dict(o='H', k=k, j0=sj, j1=je, x0=x0, x1=x1, z0=zb(k), z1=zb(k) + t))
for j in range(N + 1):
    r = 1
    while r <= R:
        if not Vp(j, r): r += 1; continue
        r0 = r
        while r <= R and Vp(j, r): r += 1
        kb, kt = r0 - 1, r - 1
        z0 = zb(kb) if A.get((j, kb), 'H') == 'V' else zb(kb) + t
        sk = kb
        for k in range(kb + 1, kt):
            if A.get((j, k)) == 'H':
                P.append(dict(o='V', j=j, k0=sk, k1=k, x0=xl(j), x1=xl(j) + t, z0=z0, z1=zb(k))); z0 = zb(k) + t; sk = k
        z1 = zb(kt) + t if A.get((j, kt), 'H') == 'V' else zb(kt)
        P.append(dict(o='V', j=j, k0=sk, k1=kt, x0=xl(j), x1=xl(j) + t, z0=z0, z1=z1))

for p in P:
    if p['o'] == 'H':
        walls = (p['x0'] < 1) + (p['x1'] > W - 1)
        p['L'] = round(p['x1'] - p['x0'] - WALLGAP * walls)
        p['B'] = D
        k = p['k']
        p['name'] = ('Spodní police (na soklu)' if k == 0 else 'Horní deska' if k == R else
                     'Dno mostu nad dveřmi' if p['j1'] == N else
                     'Police nad křeslem' if k == 3 and p['j0'] == 0 else 'Police')
        p['hidden'] = k in (0, R)
    else:
        p['L'] = round(p['z1'] - p['z0']); p['B'] = D
        j = p['j']
        p['name'] = ('Levý bok (u obkladu)' if j == 0 else 'Boční díl mostu (u pravé stěny)' if j == N else
                     'Pravý bok hlavní části' if j == K and p['k0'] < 6 else 'Svislá příčka')
        p['hidden'] = j in (0, N)
    p['kind'] = '3S19'

P.sort(key=lambda p: (round(p['z0']), p['o'] == 'H', p['x0']))   # = pořadí montáže
for i, p in enumerate(P): p['id'] = f"K{i + 1:02d}"

# spoje na koncích dílu
def who(pred):
    return [q['id'] for q in P if pred(q)]
def end_text(p, side):
    if p['o'] == 'H':
        j = p['j0'] if side == 0 else p['j1']; k = p['k']
        if (p['x0'] < 1 and side == 0) or (p['x1'] > W - 1 and side == 1):
            wall = 'k obkladu' if side == 0 else 'k pravé stěně'
        else: wall = None
        a = A.get((j, k))
        x = xl(j) + t / 2
        vert = who(lambda q: q['o'] == 'V' and q['j'] == j and q['z0'] - 1 <= zb(k) + t / 2 <= q['z1'] + 1)
        if a == 'V':
            s = f"dosedá na 2 podpěrky 5 mm v boku dílu {vert[0]}" if vert else "na podpěrkách"
        else:
            below = who(lambda q: q['o'] == 'V' and q['j'] == j and abs(q['z1'] - zb(k)) < 1)
            above = who(lambda q: q['o'] == 'V' and q['j'] == j and abs(q['z0'] - (zb(k) + t)) < 1)
            parts = []
            if below: parts.append(f"leží na {below[0]}")
            if above: parts.append(f"nese {above[0]}")
            s = ', '.join(parts) + (' (spoj A: vruty skrz)' if k < R else ' (úhelník zespodu)') if parts else ''
        return (wall + ', ' if wall else '') + s
    else:
        j = p['j']; k = p['k0'] if side == 0 else p['k1']
        a = A.get((j, k))
        if a == 'V':
            sh_ = who(lambda q: q['o'] == 'H' and q['k'] == k and (abs(q['x1'] - xl(j)) < 1 or abs(q['x0'] - (xl(j) + t)) < 1))
            base = ('stojí na soklu' if k == 0 and side == 0 else
                    'visí na vrutech do stěny' if side == 0 else 'končí v rovině desky')
            return base + (f"; do boku dosedá {', '.join(sh_)} (podpěrky)" if sh_ else '')
        hz = who(lambda q: q['o'] == 'H' and q['k'] == k and q['x0'] - 1 <= xl(j) + t / 2 <= q['x1'] + 1)
        if side == 0:
            if not hz: return ''
            under = any(q['o'] == 'V' and q['j'] == j and abs(q['z1'] - zb(k)) < 1 for q in P)
            return f"stojí na {hz[0]} " + ("(pod ní je další příčka: úhelník vzadu v přihrádce)" if under else "(spoj A: 2 vruty zespodu skrz polici)")
        return (f"pod {hz[0]}" + (' (úhelník vzadu)' if k == R else ' (spoj A: 2 vruty shora skrz polici)')) if hz else ''
for p in P:
    p['ends'] = [end_text(p, 0), end_text(p, 1)]
    p['note'] = ''
    if p['o'] == 'H' and p['k'] == 0: p['note'] = 'Leží celou plochou na soklu.'
    if p['name'].startswith('Dno mostu'): p['note'] = 'Nese most nad dveřmi. Leží na pravém boku hlavní části, pravým koncem dosedá na podpěrky v bočním dílu mostu. Navíc 2 skryté nosiče polic přišroubované přes sádrokarton do dřeva za ním (v zadní hraně dna 2 díry, nasune se na ně).'
    if p['name'].startswith('Police nad křeslem'): p['note'] = 'Na přední hraně je čtecí lampa (husí krk 24 V).'
    if p['o'] == 'V' and p['j'] in (0, N): p['note'] = ('Přišroubovat přes obklad do levé stěny (2–3 vruty s hmoždinkou).' if p['j'] == 0 else 'Přišroubovat přímo do pravé stěny (sádrokarton: kovové hmoždinky do SDK, ideálně do profilu), bez úhelníku. Dno mostu a horní deska do něj dosedají z boku na podpěrky.')
    if p['o'] == 'H' and p['k'] == R: p['note'] = 'Zasouvá se zepředu jako poslední, pod stropem jsou jen 2 cm.'
    p['grain'] = 'léta vodorovně (podél délky)' if p['o'] == 'H' else 'léta svisle (podél výšky)'

# sokl: pevná krabice pod sloupci 3–4. Boky soklu stojí přesně pod K02 a K04,
# čelní lišta mezi nimi zapuštěná 30 mm, vzadu spojka u zdi, uprostřed podpěra pod K03.
xa, xb = xl(2), xl(K)                    # levá hrana levého a pravého boku soklu
SOKL_H = PLINTH
SOKL = [
    dict(id='S1', o='S', name='Sokl: levý bok (pod K02)', L=SOKL_H, B=D - SOKL_ZAP, kind='3S19',
         x0=xa, x1=xa + t, z0=0, z1=SOKL_H, hidden=False, grain='léta svisle',
         ends=['stojí na podlaze (nevrtat, vyrovnat podložkami)', 'nese K01, nad ním stojí K02'],
         note='Pohledový: je vidět z výklenku pro křeslo. Vpředu končí 30 mm za čelem K01. Vzadu u podlahy výřez 70 × 70 mm (u zdi) pro kabel prodlužky, lampičky a nabíječky.'),
    dict(id='S2', o='S', name='Sokl: pravý bok (pod K04)', L=SOKL_H, B=D - SOKL_ZAP, kind='3S19',
         x0=xb, x1=xb + t, z0=0, z1=SOKL_H, hidden=False, grain='léta svisle',
         ends=['stojí na podlaze (nevrtat, vyrovnat podložkami)', 'nese K01, nad ním stojí K04'],
         note='Pohledový: je vidět ze strany od dveří. Vpředu končí 30 mm za čelem K01.'),
    dict(id='S3', o='S', name='Sokl: střední podpěra (pod K03)', L=SOKL_H, B=D - SOKL_ZAP - t, kind='3S19',
         x0=xl(3), x1=xl(3) + t, z0=0, z1=SOKL_H, hidden=True, grain='libovolně (skrytý díl, z C03 léta vodorovně)',
         cutL=D - SOKL_ZAP - t, cutB=SOKL_H,
         ends=['stojí na podlaze', 'nese K01 pod příčkou K03'], note='Skrytá za čelní lištou. Z C03 se řeže otočená (201 po letech × 140), u skrytého dílu na směru let nezáleží.'),
    dict(id='S4', o='S', name='Sokl: zadní spojka', L=round(xb - xa - t), B=100, kind='3S19',
         x0=xa + t, x1=xb, z0=SOKL_H - 100, z1=SOKL_H, hidden=True, grain='léta vodorovně',
         ends=['mezi boky soklu u zdi, nahoře', 'do boků zevnitř úhelníky'], note='Drží boky soklu pohromadě vzadu. K01 se do ní shora přišroubuje 2 vruty, jinak je K01 se soklem nespojená. Skrytá.'),
    dict(id='S5', o='S', name='Sokl: čelní lišta', L=round(xb - xa - t), B=SOKL_H - 5, kind='3S19',
         x0=xa + t, x1=xb, z0=5, z1=SOKL_H, hidden=False, grain='léta vodorovně',
         ends=['mezi boky soklu, zapuštěná 30 mm za čelem K01, 5 mm nad podlahou', 'pevně úhelníky zevnitř, nebo na magnetech (Přemek rozhodne)'],
         note='Pevná varianta: úhelníky zevnitř dřív, než se na sokl položí K01. Odnímatelná: magnety, pak jde k prodlužce v soklu.'),
]

# ---- sklad ----
STOCK = []
for r in csv.DictReader(open(os.path.join(ROOT, 'drevo', 'inventar.csv'), encoding='utf-8')):
    if r['pouzitelnost'] == 'nenalezeno': continue   # na půdě se nenašlo
    kind = '3S19' if (r['typ'] == '3vrstvá deska' and r['tloustka_mm'] == '19') else \
           'SP18' if (r['typ'] == 'spárovka' and r['tloustka_mm'] == '18') else None
    for i in range(int(r['ks'])):
        sid = r['id'] if int(r['ks']) == 1 else f"{r['id']}-{i + 1}"
        STOCK.append(dict(id=sid, src=r['id'], typ=r['typ'], th=int(r['tloustka_mm']), L=int(r['delka_mm']),
                          Wd=int(r['sirka_mm']), holes=bool(r['vady']), vady=r['vady'], loc=r['umisteni'], kind=kind, note=''))
# C04 + C05 (2500 × 160) slepit podélně na 2500 × 320 -> pruh 250 na horní desku
GLUE = ('C04', 'C05')
g = [s for s in STOCK if s['id'] in GLUE]
STOCK = [s for s in STOCK if s['id'] not in GLUE]
STOCK.append(dict(id='C04+C05', src='C04', typ='3vrstvá deska', th=19, L=min(x['L'] for x in g), Wd=sum(x['Wd'] for x in g),
                  holes=False, vady='', loc=g[0]['loc'], kind='3S19',
                  note='slepit C04 a C05 podélně (lepidlo D3 + kolíky 8 mm po ~300 mm, svěrky), pak oříznout na 250'))

def strips_of(s, width):
    n = (s['Wd'] + KERF) // (width + KERF)
    return [dict(stock=s['id'], idx=i, y=i * (width + KERF), w=width, L=s['L'], free=s['L'], items=[]) for i in range(n)]

# Stabilita: díl zůstane na desce z minulého běhu, pokud se tam pořád vejde (Přemek už řeže).
_prev_path = os.path.join(ROOT, 'drevo', 'prirazeni.json')
PREV = {q['id']: q.get('src') for q in json.load(open(_prev_path, encoding='utf-8'))['parts']} if os.path.exists(_prev_path) else {}

def place(pieces, stocks, width, prefer=None, strips=None):
    strips = strips if strips is not None else [x for s in stocks for x in strips_of(s, width)]
    left, rest = [], []
    for p in sorted(pieces, key=lambda p: -p.get('cutL', p['L'])):
        need = p.get('cutL', p['L']) + KERF
        st = next((x for x in strips if x['stock'] == PREV.get(p['id']) and x['free'] >= need), None)
        if not st: rest.append(p); continue
        p['src'] = st['stock']; p['strip'] = st['idx']; p['off'] = st['L'] - st['free']
        st['items'].append(p['id']); st['free'] -= need
    for p in rest:
        need = p.get('cutL', p['L']) + KERF
        cand = [s for s in strips if s['free'] >= need]
        if prefer: cand = [s for s in cand if prefer(p, s)] or cand
        cand = [s for s in cand if s['free'] - need >= SAFE] or cand   # rezerva na nepřesný řez
        if not cand: left.append(p); continue
        best = min(cand, key=lambda s: (s['free'] - need, 0 if s['items'] else 1))
        p['src'] = best['stock']; p['strip'] = best['idx']; p['off'] = best['L'] - best['free']
        best['items'].append(p['id']); best['free'] -= need
    return strips, left

by = {s['id']: s for s in STOCK}
holes = [s for s in STOCK if s['kind'] == '3S19' and s['holes']]
clean = [s for s in STOCK if s['kind'] == '3S19' and not s['holes']]
# 1) poškozené desky jen na díly se skrytou stranou
clean = [s for s in clean if s['id'] != 'C04+C05']
# 0) horní deska ze slepených C04 + C05 (spára je shora u stropu, zespodu skoro není vidět)
st0, _ = place([p for p in P if p['name'] == 'Horní deska'], [by['C04+C05']], D)
for p in P: p['composite'] = p['o'] == 'V' and p['j'] == 0
import copy, itertools
HOLE_IDS = {h['id'] for h in holes}
# Ruční přiřazení díl -> deska (Přemek prohazuje podle vad při řezání). Tyto díly se umístí první,
# zbytek dopočítá optimalizace.
PIN = {
    'K10': 'D08-3', 'K14': 'B01',   # 2026-11-24 prohozeno
}
def pin(strips):
    for pid, sid in PIN.items():
        q = next(x for x in P if x['id'] == pid)
        need = q.get('cutL', q['L']) + KERF
        st = next((x for x in strips if x['stock'] == sid and x['free'] >= need), None)
        assert st, f"{pid} ({q['L']} mm) se nevejde na {sid}"
        q['src'] = sid; q['strip'] = st['idx']; q['off'] = st['L'] - st['free']
        st['items'].append(pid); st['free'] -= need
def run(segs):
    """Rozmístí díly na čerstvé pruhy; kusy slepeného boku přednostně na poškozené desky (skrytá strana)."""
    for q in P + segs:
        if q.get('name') != 'Horní deska':
            for k in ('src', 'strip', 'off'): q.pop(k, None)
    hs = [x for s in holes for x in strips_of(s, D)]
    cs = [x for s in clean for x in strips_of(s, D)]
    pin(hs + cs)
    _, b0 = place(segs, None, D, strips=hs + cs, prefer=lambda p, st: st['stock'] in HOLE_IDS)
    place([q for q in P if q['hidden'] and 'src' not in q and not q['composite'] and q['name'] != 'Horní deska'], None, D, strips=hs)
    _, b1 = place([q for q in P if 'src' not in q and not q['composite']], None, D, strips=cs)
    _, b2 = place(b1, None, D, strips=hs)
    return hs + cs, b0 + b2
# levý bok: slepit z co nejméně kusů, spoje ve výšce polic (zakryje je konec police)
SEGS, best = [], None
comp = [q for q in P if q['composite']]
for p in comp:
    cuts = [zb(k) + t / 2 - p['z0'] for k in range(R + 1) if p['z0'] < zb(k) + t / 2 < p['z1'] and (0, k) in A]
    for n in range(0, len(cuts) + 1):
        for cc in itertools.combinations(cuts, n):
            bnd = [0] + list(cc) + [p['L']]
            segs = [dict(id=f"{p['id']}.{i + 1}", L=round(bnd[i + 1] - bnd[i]) - (KERF if 0 < i or i < len(bnd) - 2 else 0) * 0)
                    for i in range(len(bnd) - 1)]
            pool, bb = run(segs)
            waste = sum(x['free'] for x in pool if x['items'])
            sc = (len(bb), n, waste)
            if best is None or sc < best[0]: best = (sc, segs)
        if best and best[0][0] == 0: break
    segs = best[1]
    for i, sg in enumerate(segs):
        sg.update(o='G', name=f"{p['name']}, kus {i + 1}/{len(segs)}", B=D, kind='3S19', parent=p['id'], hidden=True,
                  grain='léta svisle (podél výšky)', ends=['slepit s ostatními kusy do jedné desky', 'kolíky 8 × 35 + lepidlo, spoj ve výšce police'], note='')
    SEGS += segs
pool, buy = run(SEGS)
for p in comp:
    segs = [sg for sg in SEGS if sg['parent'] == p['id']]
    p['segments'] = [sg['id'] for sg in segs]
    p['src'] = None if any('src' not in sg for sg in segs) else ' + '.join(sg['src'] for sg in segs)
    p['note'] = (f"Jedna deska slepená předem z {len(segs)} kusů ({' + '.join(str(sg['L']) for sg in segs)} mm) na tupo: 3 kolíky 8 × 35 + lepidlo na spoj. Spoj je ve výšce police, zakryje ho její konec. Celou desku přišroubovat přes obklad do dřevěné stěny, police do ní dosedají na podpěrky." if len(segs) > 1
                 else "Přišroubovat přes obklad do dřevěné stěny, police do něj dosedají na podpěrky.")
st2 = [x for x in pool if x['stock'] not in HOLE_IDS]
st1 = [x for x in pool if x['stock'] in HOLE_IDS]
# sokl: lišta z úzkého pruhu 3S, podpěry ze spárovky 18
used_ids = {x['stock'] for x in pool if x['items']} | {'C04+C05', 'C03'}
spare3s = [s_ for s_ in clean if s_['id'] not in used_ids and s_['id'][0] in 'AB']   # boky soklu z menších panelů A/B
# oba pohledové boky z jedné desky (stejná kresba), nejmenší deska, do které se vejdou
_sides = [q for q in SOKL if q['id'] in ('S1', 'S2')]
_need = sum(q['L'] for q in _sides) + KERF * len(_sides)
_one = sorted([s_ for s_ in spare3s if strips_of(s_, D - SOKL_ZAP) and s_['L'] >= _need], key=lambda s_: s_['L'] * s_['Wd'])
st3, buy3 = place(_sides, _one[:1] or spare3s, D - SOKL_ZAP)
# S5, S4 a S3 (otočená) za sebou z jednoho pruhu C03 přes celou šířku
st3b, buy3b = place([q for q in SOKL if q['id'] in ('S5', 'S4', 'S3')], [by['C03']], by['C03']['Wd'])
st4, buy4, st4b, buy4b = [], [], [], []
st3 += st3b; st4 += st4b
buy += buy3 + buy3b + buy4 + buy4b
st1 = st0 + st1
# sloučit pruhy podle desky
strips = {}
for s in st1 + st2 + st3 + st4:
    if s['items']: strips.setdefault(s['stock'], []).append(s)
for sid in strips: strips[sid].sort(key=lambda s: s['idx'])

ALL = P + SOKL + SEGS
# těsné pruhy: upozornit v poznámce dílu
_by_id = {q['id']: q for q in ALL}
for sid, lst in strips.items():
    for st in lst:
        slack = st['L'] - sum(_by_id[i].get('cutL', _by_id[i]['L']) + KERF for i in st['items']) + KERF
        if slack < SAFE:
            for i in st['items']:
                q = _by_id[i]
                q['note'] = (q.get('note', '') + f" Těsný řez: z desky {sid} zbývá jen {slack} mm, řezat přesně"
                             + (", u stěny se dá díl zkrátit o pár mm navíc." if q.get('L') and (q.get('x1', 0) > W - 1 or q.get('x0', 1) < 1) else ".")).strip()
for p in ALL:
    if p.get('src') and p['src'] in by:
        s = by[p['src']]
        p['srcinfo'] = dict(id=s['id'], loc=s['loc'], typ=s['typ'], th=s['th'], L=s['L'], Wd=s['Wd'], vady=s['vady'])
    elif not p.get('segments'):
        p['src'] = None

# kontrola: díly se do pruhu vejdou
for sid, lst in strips.items():
    for s in lst:
        tot = sum(next(q.get('cutL', q['L']) for q in ALL if q['id'] == i) + KERF for i in s['items'])
        assert tot <= s['L'], (sid, s['idx'], tot, s['L'])

# počty spojovacího materiálu
dowel_joints = sum(1 for p in P if p['o'] == 'V' for e in p['ends'] if 'skrz' in e)
pin_ends = sum(1 for p in P if p['o'] == 'H' for e in p['ends'] if 'podpěrky' in e)
angle_top = sum(1 for p in P if p['o'] == 'V' and 'úhelník' in p['ends'][1])
verts = [p for p in P if p['o'] == 'V']
used = sorted(strips)
unused = [s for s in STOCK if s['id'] not in strips]

out = dict(
    geo=dict(W=W, H=H, t=t, TOPGAP=TOPGAP, PLINTH=PLINTH, D=D, N=N, K=K, R=R, sw=sw, sh=sh, KERF=KERF, XL=XL, CW=CW, NOOK=NOOK),
    pattern={f"{j},{k}": v for (j, k), v in A.items()},
    parts=[{k: p[k] for k in ('id', 'o', 'name', 'L', 'B', 'kind', 'x0', 'x1', 'z0', 'z1', 'src', 'ends', 'grain', 'hidden', 'note')
            if k in p} | {'strip': p.get('strip'), 'off': p.get('off'), 'srcinfo': p.get('srcinfo'), 'cutL': p.get('cutL'), 'cutB': p.get('cutB'), 'segments': p.get('segments'), 'parent': p.get('parent')} for p in ALL],
    stock={sid: dict(**{k: by[sid][k] for k in ('id', 'typ', 'th', 'L', 'Wd', 'vady', 'loc', 'note')},
                     strips=[dict(idx=s['idx'], y=s['y'], w=s['w'], items=s['items']) for s in lst])
           for sid, lst in strips.items()},
    unused=[{k: s[k] for k in ('id', 'typ', 'th', 'L', 'Wd', 'loc', 'vady')} for s in unused],
    buy=[p['id'] for p in buy],
    counts=dict(dowels=dowel_joints * 2, dowel_joints=dowel_joints, pins=pin_ends * 2, pin_ends=pin_ends,
                angle_top=angle_top, verts=len(verts), parts=len(P), sokl=len(SOKL)),
)
json.dump(out, open(os.path.join(ROOT, 'drevo', 'prirazeni.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# vložit data do HTML
for html_path in (os.path.join(ROOT, 'knihovna.html'), os.path.join(ROOT, 'postup.html')):
  if os.path.exists(html_path):
    h = open(html_path, encoding='utf-8').read()
    h = re.sub(r'/\*DATA\*/.*?/\*END\*/', lambda m: '/*DATA*/' + json.dumps(out, ensure_ascii=False) + '/*END*/', h, flags=re.S)
    open(html_path, 'w', encoding='utf-8').write(h)

if __name__ == '__main__':
    print(f"díly {len(P)} + sokl {len(SOKL)}, ke koupi {len(buy)}: {[p['id'] for p in buy]}")
    for p in ALL:
        print(p['id'], p['name'][:28].ljust(28), p['L'], '×', p['B'], p['src'], p.get('strip'), p.get('off'), '|', ' / '.join(p['ends']))
    print('použito', used)
    print('nepoužito', [s['id'] for s in unused])
    print(out['counts'])

# ---- prirazeni.md ----
LOC_ORDER = ['vlevo pod střechou', 'vlevo dole pod střechou', 'vlevo vzadu pod střechou', 'vpravo dole pod střechou', 'vpravo v šuplících']
PBY = {p['id']: p for p in ALL}
md = ['# Přiřazení dílů k deskám z půdy', '',
      'Generováno skriptem `drevo/prirazeni.py` z `inventar.csv`. Návrh: `knihovna.html`.',
      f'Hloubka 250 mm, tl. 19 mm, prořez {KERF} mm, u stěny vůle {WALLGAP} mm. Délka dílu je vždy po letech.', '',
      f"**Ke koupi: {len(out['buy'])} dílů.** Použito {len(strips)} desek z půdy, {len(unused)} kusů zůstává jako rezerva.", '',
      '## Co snést z půdy a jak nařezat', '']
for loc in LOC_ORDER:
    sids = sorted([sid for sid in strips if by[sid]['loc'] == loc], key=lambda x: (len(x), x))
    if not sids: continue
    md += [f'### {loc[0].upper() + loc[1:]}', '', '| Deska | Rozměr | Pruh | Díly (délka) | Odpad v pruhu |', '|---|---|---|---|---|']
    for sid in sids:
        s = by[sid]
        for st in strips[sid]:
            items = ', '.join(f"{i} ({PBY[i].get('cutL') or PBY[i]['L']})" for i in st['items'])
            md.append(f"| {sid} | {s['L']} × {s['Wd']}{' · ' + s['vady'] if s['vady'] else ''} | {st['idx'] + 1}: {st['w']} mm | {items} | {st['free']} mm |")
    md.append('')
md += ['## Díly', '', '| Díl | Název | Délka × šířka | Z desky | Spoje |', '|---|---|---|---|---|']
for p in ALL:
    md.append(f"| {p['id']} | {p['name']} | {p['L']} × {p['B']} | {p['src'] or 'koupit'} | {' / '.join(p['ends'])} |")
md += ['', '## Rezerva (nepoužito)', '', ', '.join(f"{s['id']} ({s['L']} × {s['Wd']}{', ' + s['typ'] + ' ' + str(s['th']) if s['typ'] != '3vrstvá deska' else ''})" for s in unused), '']
open(os.path.join(ROOT, 'drevo', 'prirazeni.md'), 'w', encoding='utf-8').write('\n'.join(md))
