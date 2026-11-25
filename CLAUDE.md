# Knihovna do pracovny

Projekt: vestavěná smrková knihovna do Přemkovy pracovny (rodinný dům, Řisuty). Navrženo v chatu s Claudem, tady pokračujeme stavbou.

Komunikace česky, stručně, akčně. Oslovení „Přemku“. Postup MVP: nejdřív nejjednodušší funkční verze, automatizovat až když je potřeba. Výstupy jako samostatné Markdown/HTML/CSV soubory bez závislostí.

## Git a publikace

Repo: https://github.com/tallyho42/truhlarna (veřejné, GitHub Pages z větve `main`, kořen).

**Po každé změně souborů automaticky commit a push** (bez ptaní). Pak Přemkovi napsat, co se commitlo, a vždy vypsat URL obou stránek:
- https://tallyho42.github.io/truhlarna/knihovna.html
- https://tallyho42.github.io/truhlarna/postup.html

Pages se po pushi obnoví do ~1 min.

**Po každé změně plánu/návrhu nezávislá kontrola** (Přemkovo pravidlo, 2026-11-24): nejdřív commit, push a Přemkovi napsat změnu a URL, **pak** spustit na pozadí nezávislého agenta, který důkladně otestuje všechno hotové (data, `prirazeni.py`, obě HTML, texty) a **přepočítá všechny délky** z míry místnosti. Agentovi nedávat svoje závěry, jen soubory a zadání. Výsledek agenta Přemkovi nahlásit a chyby opravit.

## Soubory

- `knihovna.html`: **aktuální návrh (v4)**, hloubka 250. Výkres s najetím myší na díl (rozměr, spoje), sekce Spoje s výkresem všech spojů X01–X59 (pohled zepředu + sokl shora + tabulka), kolize, kusovník. Data vkládá `drevo/prirazeni.py` mezi `/*DATA*/…/*END*/`.
- `postup.html`: pracovní postup krok za krokem (lepení K26 a K09, vrtání děr pro kolíky s výškami, drážky v policích, broušení a nátěr, sokl, spodní rám, úrovně odspodu, dokončení). Kroky a obrázky se generují z dat, která vkládá `prirazeni.py`.
- `drevo/prirazeni.py`: **zdroj pravdy pro rozměry a přiřazení** (geometrie, vzor křížení `PATTERN`, přiřazení k deskám). Po změně inventáře nebo návrhu spustit `python3 drevo/prirazeni.py`, přepíše `prirazeni.json`, `prirazeni.md` a data v HTML. Ruční prohození díl → deska (Přemek při řezání dává hezčí kusy na lepší místa) se zapisuje do `PIN` v `prirazeni.py`. Ostatní díly drží desku z minulého běhu (`PREV` z `prirazeni.json`), takže se nic už nařezaného nepřehází.
- `input/`: fotky místnosti (IMG_0506–0508) a busty (IMG_0509).
- `navrh-gemini/`: AI vizualizace z Gemini. Jen inspirace, některé mají chybně dveře v zadní stěně.
- `gemini-prompt.md`: aktuální prompt pro vizualizaci.
- `drevo/`: databáze dřeva z půdy (fáze 1).

## Místnost (změřeno)

| Rozměr | Hodnota |
|---|---|
| Šířka zadní stěny (od dřevěného obkladu k pravé stěně) | 237,0 cm |
| Výška místnosti | 259,3 cm |
| Od obkladu k hraně plně otevřeného křídla | 147,6 cm |
| Od horní hrany dveří ke stropu | 47,4 cm → horní hrana dveří 211,9 cm |
| Hloubka místnosti | cca 5 m |

- Levá stěna: smrkový obklad (sukovitý, světlý).
- Dveře: černé, bezfalcové, v **pravé boční stěně**, pant u zadní stěny. Otevírají se do místnosti a plně otevřené leží rovnoběžně se zadní stěnou, cca 12 cm od ní (odhad z fotky), přes pravých ~90 cm stěny. Klika je na volném konci křídla a v otevřené poloze míří ke zdi.
- Okno je naproti knihovně přes celou šířku, orientace východ, málo světla.
- Elektřina: prodlužka 230 V na zemi za křeslem. Pravděpodobně podlahové topení (termostat u dveří), do podlahy nevrtat.
- Zůstává: křeslo typu IKEA Strandmon (~82 × 96 × 101 cm) v levém rohu u obkladu. Mizí: stará bílá knihovna, stojací lampa, kytara.

## Tvrdá omezení

1. **Žádná kolize s dveřmi.** Nic pod horní řadou nesmí zasahovat do pásu od 147,6 cm vpravo. Ve v4 končí knihovna na 142,1 cm (rezerva 5,5 cm, Přemkovi stačí ≥ 5 cm). Pod horní řadou nad dveřmi zůstává jen stěna.
2. Horní řada nad dveřmi: spodní hrana 220,9 cm (v4), tedy 9,0 cm nad dveřmi.
3. Nad dveřmi žádné převislé rostliny.
4. Přihrádky čtvercové, uspořádání nepravidelné (některé příčky vynechané). Výjimka ve v4: sloupce 1–2 nad křeslem jsou 34,6 × 32,6 cm (ostatní 31,7 × 32,6) kvůli výklenku 73 cm.
5. Bez zadní stěny: prosvítá bílá zeď.
6. Materiál smrk 19 mm, povrch sladěný s obkladem vlevo.

## Původní návrh v3 (nahrazen v4, viz Fáze 2)

- Materiál: smrková **třívrstvá deska 19 mm** (biodeska / 3S deska, kvalita B/C kvůli sukům jako obklad). Skutečné CLT se v 19 mm nevyrábí. Pohledové hrany se třemi vrstvami, hloubka 300 mm.
- Mřížka: 7 sloupců přes celou šířku, přihrádka 31,7 × 32,7 cm (světlost), deska 1,9 cm.
  - Hlavní část: sloupce 1–4 × 7 řad, šířka 136,2 cm, od podlahy do 258,3 cm (1 cm pod strop).
  - Sokl 14 cm, zapuštěný 3 cm, čelní lišta na magnetech; skrývá zdroj a stmívač.
  - Horní řada pokračuje přes sloupce 5–7 až k pravé stěně (most nad dveřmi).
- Spojené přihrádky (sloupce zleva, řady **shora**):
  - sloupec 2, řady 1–2: **busta** (bronzový fragment tváře na tyčce a dřevěném podstavci, 40 × 20 cm), vlastní LED okruh,
  - řada 3, sloupce 3–4: dvojitá, potos + knihy,
  - řada 4, sloupce 1–2: dvojitá nad křeslem, na přední hraně spodní police (výška ~118 cm) je čtecí lampa (husí krk 24 V),
  - horní řada, sloupce 5–6: dvojitá nad dveřmi; sloupec 7 malý zamiokulkas + knihy.
- Obsah: všechny přihrádky plné, hlavně knihy (paperbacky). Rostliny jen dva druhy: potos 2× (sloupec 1 řada 1, dvojitá v řadě 3), zamiokulkas 1× (nad dveřmi). Spodní polovina jen knihy.
- LED: COB 24 V, teplá bílá, v zápustném hliníkovém profilu zafrézovaném do spodní strany police 3 cm od čela (vybrané díly viz „LED – nákupní seznam“; drážka pro profil V4 cca 15,5 × 6,5 mm). Kabely drážkou 8 × 8 mm v zadní hraně desek. Zdroj Mean Well 24 V v soklu, 4kanálový stmívač (např. Shelly Plus RGBW PM): 1 knihy, 2 rostliny (časovač), 3 busta, 4 čtecí lampa. Celkem ~50 W.
- Kotvení: skryté úhelníky každého boku a příčky do zadní zdi; pod most 2 ocelové trny do zdi; boční díl mostu přišroubovat do pravé stěny.

## Kusovník v3 (mm, hloubka 300, tl. 19; aktuální je v `drevo/prirazeni.md`)

Vodorovné desky průběžné, svislé příčky mezi nimi krátké. Průběžné jsou levý bok a pravý bok hlavní části.

| Díl | ks | Délka | Šířka | Poznámka |
|---|---|---|---|---|
| Levý bok (u obkladu) | 1 | 2583 | 300 | od podlahy ke stropu |
| Pravý bok hlavní části | 1 | 2218 | 300 | od podlahy pod desku mostu |
| Boční díl mostu | 1 | 365 | 300 | do pravé stěny |
| Spodní police | 1 | 1324 | 300 | přes 4 sloupce |
| Police | 5 | 1324 | 300 | přes 4 sloupce |
| Police | 1 | 317 | 300 | 1 sloupec (vedle busty) |
| Police + dno mostu | 1 | 1660 | 300 | přes 5 sloupců |
| Horní deska | 1 | 2332 | 300 | přes 7 sloupců |
| Svislá příčka | 17 | 327 | 300 | |
| Svislá příčka | 2 | 674 | 300 | přes 2 řady (u busty) |
| Sokl – čelní lišta | 1 | 1324 | 130 | |
| Sokl – podpěra | 2 | 140 | 270 | |

Celkem 34 dílů, 7,5 m². Vejde se do 1 desky 5000 × 2050 (6 pruhů po 300 mm) bez rezervy, proto počítat s rezervou (+1 deska 2500 × 2050). Rozměry před řezáním ověřit na místě.

Orientační rozpočet 45–76 tis. Kč (deska 12–15 tis., truhlář 25–45 tis., LED 6,5–12,5 tis., rostliny 1–2,5 tis.).

## LED – zrušeno (2026-11-23)

Přemek se rozhodl knihovnu udělat úplně bez LED. Dřívější výběr (TopLux COB 24 V, profil V4, MiBoxer) i plán kabeláže (drážky, stoupačka, hvězda ze soklu) neplatí, žádné drážky pro kabely se nefrézují. Čtecí lampa nad křeslem je samostatná s vlastním kabelem do prodlužky.

## Stav stavby (Fáze 3)

- **2026-11-24: všechny díly nařezané**, K26 a K09 slepené (schnou). Pak broušení a nátěr, zabere několik dní.
- **ID desek z půdy (D03, A09, C04…) se dál nikde nezobrazují**, jen díly K* a S* a spoje X*. V `prirazeni.py` je `CUT_DONE = True`, přiřazení k deskám zůstává jen v datech a v `drevo/prirazeni.md` jako archiv řezání.
- **Spoje** jsou očíslované X01–X59 (`JOINTS` v `prirazeni.py`, generované z geometrie): X01–X10 sokl, pak odspodu nahoru a zleva doprava. Přemek je promýšlí, spoje jsou za něj otevřené. Nečíslované: lepené spoje v K09/K26 a úhelníky vzadu do zadní stěny.

## Nářadí

- Frézka: **Makita DRT50Z**, aku kombinovaná 18 V LXT (bez stolu). Standardně kleština 6 mm (dle trhu i 1/4"), **8 mm jde s dokoupenou kleštinou** (kužel Makita 763618-5, matice z původní 6mm se použije dál; nejlevněji kamody.cz 99 Kč, 2026-11-24), 8 mm je maximum.
- Okružní pila: **Makita DHS661ZJU**, aku bezuhlíková 18 V (165 mm).
- Dál: aku vrtačka, přímočará pila, bruska, svěrky. Nemá stolní pilu.

## Otevřené body

- **Spoje K10–K09 a K24–K20:** K09 i K20 končí dole v rovině spodku police, kterou mají nést, takže kolík do boku tam nejde. Díly jsou už nařezané (rozměry se nemění), spoj se dořeší: kolíky, nebo úhelník shora (asi K24).
- **Kotvení dna mostu K24 do zadní stěny (X50):** skryté nosiče s trny nejdou dohromady s kolíky (na trny se nasouvá vodorovně, na kolíky spouští shora) a díry pro trny v 19mm hraně jsou slabé. Dořešit (drážka v levém konci K24 od zadní hrany k přednímu kolíku, úhelník, lišta pod K24…).
- K24 nemá u pravé stěny 5mm vůli jako díly ke stěně (jen 1 mm jako police) (řetěz obklad → K20 dává přesně 2370). Před montáží změřit šířku ve výšce 2,2 m.

- Ověřit horní hranu zárubně na pravé stěně (musí být pod 220 cm).
- Zarážka dveří v plně otevřené poloze.
- Povrch: Ciranova Hardwaxoil Natural White 5485 (jako zbytek domu), použije se 5 let stará plechovka bez testu. Plechovka asi 5 l (prodává se 1 l a 5 l), zbývá ~60 % = ~3 l; knihovna ~11 m² ploch (obě strany dílů) na 2 vrstvy potřebuje ~1–1,5 l, stačí. Před použitím rozmíchat ode dna a přecedit.

---

## Fáze 1: databáze dřeva z půdy

Cíl: z fotek zjistit a uložit, jaké dřevo je na půdě.

**Stav: hotovo.** Všechny relevantní kusy Přemek změřil ručně (bez fotek) a jsou v `inventar.csv`. Nezapsané zbyly jen menší spárovky (max. 400 × 800) a drobné odřezky CLT, pro knihovnu nepodstatné.

Struktura:
```
drevo/
  fotky/            # originály od Přemka, nepřejmenovávat ani neupravovat
  inventar.csv      # zdroj pravdy, jeden řádek = jeden kus nebo balík stejných kusů
  prehled.md        # generovaný souhrn (co a kolik), přepsat po každé změně
```

Sloupce `inventar.csv`:
`id, fotky, typ, druh, delka_mm, sirka_mm, tloustka_mm, ks, stav, vady, vlhkost, pouzitelnost, jistota, overeno, umisteni, poznamka`

- `umisteni`: kde kus leží na půdě, doslova jak ho Přemek napíše. A- a B-panely jsou „vpravo v šuplících“, pokud neřekne jinak.

- `id`: D01, D02… (velké desky a spárovky), A01, A02… (menší CLT panely). Ideálně štítek z malířské pásky na kusu.
- Kvalita je A/B a druh smrk, pokud Přemek v poznámce neuvede jinak.
- `delka_mm` = rozměr **po letech** (u A-panelů „výška“), `sirka_mm` = napříč letům („šířka“). Přemek zadává šířka × výška.
- `typ`: prkno / fošna / hranol / lať / palubka / spárovka / 3vrstvá deska / OSB / překližka / DTD / jiné
- `druh`: smrk / borovice / modřín / jedle / dub / buk / neurčeno…
- `stav`: suché / vlhké / neznámo; `vady`: suky, trhliny, hniloba, červotoč, zkroucení, barvené…
- `jistota`: vysoká / střední / nízká (rozpoznání z fotky)
- `overeno`: ano, když Přemek údaj potvrdil nebo změřil

Pravidla:
- Rozměry z fotky jen když je na ní metr nebo známé měřítko. Jinak odhad s `jistota=nízká` a doptat se.
- Druh dřeva z fotky je často nejistý (smrk vs. jedle vs. borovice). Napsat jistotu a co by pomohlo (fotka čela, detail letokruhů, vůně/pryskyřice).
- Nic neslučovat ani nemazat bez potvrzení. Po každé dávce fotek ukázat tabulku nových řádků a zeptat se na nejisté údaje.

Doporučení pro focení: ke každému kusu nebo balíku štítek s ID, svinovací metr položený podél, 1 celkový záběr + 1 čelo (tloušťka a vrstvy) + detail vad. U balíku vyfotit čelo, aby šly spočítat kusy.

## Fáze 2: co použít a co dokoupit

**Stav: hotovo (2026-09-27), návrh v4.** Změny oproti v3 na Přemkovo přání:
- Hloubka **250 mm** (místo 300).
- Za křeslem vynechané sloupce 1–2, řady 1–3 odspodu (6 přihrádek). **Výklenek musí mít aspoň 73 cm na šířku a 100 cm na výšku** (má 73,0 × 117,5). Vpravo od něj jsou až k zemi 2 čtvercové přihrádky.
- Proto nestejné sloupce (`CW` v `prirazeni.py`): 1–2 světlost 34,6 cm (nad křeslem), 3–4 a 7 čtverec 31,7, dvojitá nad dveřmi 59,4. Knihovna končí na 142,1 cm, k otevřeným dveřím 5,5 cm.
- Křeslo stojí šikmo (~28°), zadním rohem zajede ~14 cm do výklenku. Levý bok začíná až nad výklenkem a visí na vrutech přes obklad do zdi.
- **Sokl** jen pod sloupci 3–4, krabice S1–S4 (čelní lišta S5 na magnetech, viz níž): boky S1/S2 (3S 19, 140 × 220, oba z B10, pohledové; C02 se na půdě nenašla) stojí přesně pod K02 a K04, čelní lišta S5 mezi nimi zapuštěná 30 mm, vzadu spojka S4, uprostřed podpěra S3 pod K03 (S5, S4 i S3 z jednoho pruhu C03, S3 otočená, zbyde 1000 mm), vše zevnitř úhelníky. K01 leží na soklu (tíhu nese tlakem přes S1/S2/S3) a přišroubuje se zespodu do úhelníků na S4 (2) a vpředu na S1 a S2 (shora do S4 vrtat nejde, je 9 mm od zdi). V soklu bude prodlužka se zásuvkou pro lampičku a nabíječku: v S1 vzadu u podlahy výřez 70 × 70 mm na kabely. Čelní lišta S5 je na magnetech. Do podlahy se nevrtá, vyrovnat podložkami.
- **Čelní lišta S5 na magnetech** (rozhodnuto 2026-11-24, zkrátit z 653 na 651 kvůli vůli; stojí na filcu 3 mm, nahoře 2 mm mezera): Přemkovy feritové magnety cca Ø 15–16 × 5 (přesně změřit posuvkou). 2 páry: magnet v zadní straně S5 (20 mm od konce, 67 mm od spodní hrany, díra hloubky magnetu, z 19 zbyde 14) + magnet v dorazu (špalík z odřezku 19, 40 × 80, přilepený zevnitř na S1/S2, lišta jako distanční). Uprostřed se lišta opírá o čelo S3. Stojí na 2 filcových podložkách 3 mm, úchyt = výřez 60 × 15 ve spodní hraně, střed 160 mm od levého konce (uprostřed je za lištou S3). Přední konce S1/S2 drží malé úhelníky zevnitř nahoru do K01. Parametry `MAG` v `prirazeni.py`, spoje X04/X05 (magnet), X07/X09 (úhelník).
- **Pravý bok hlavní části** a **příčka u výklenku** jsou z jednoho kusu, **oba 2395 mm z D03** (2 pruhy, v každém zbývá 5 mm), stojí na spodní polici a jdou až pod horní desku. Dno mostu do pravého boku dosedá z boku na kolíky. Kvůli příčce je **mezera ke stropu 2 cm**, knihovna končí na 257,3 cm.
- **Svislé díly co nejdelší** (Přemek nechce přesné kolíkování): příčka vpravo dole 2 díly, příčka nad křeslem 1 kus (1016). Většina polic leží na kolících (spoj B).
- **Levý bok = jedna deska 1379 mm slepená předem** z co nejméně kusů (vyšly 2: D02 1044 + A01 335, díry A01 k obkladu), kolíky 8 mm + lepidlo, spoje ve výšce polic. Celá se přišroubuje přes obklad do dřevěné stěny, police vlevo (nad křeslem až po horní řadu) do ní dosedají na kolíky a k obkladu nesahají. V `prirazeni.py` jako `composite`, kusy `K09.1…`.
- **Boční díl mostu** se šroubuje přímo do sádrokartonu pravé stěny (bez úhelníku), horní deska do něj dosedá z boku na kolíky. Dno mostu K24 ne: K20 končí v rovině spodku dna, spoj se dořeší (viz Otevřené body).
- Díly jsou číslované odspodu nahoru a zleva doprava = pořadí montáže (Přemek to tak chce držet).
- Konstrukce z krátkých dílů: v každém křížení je jeden díl průběžný (`PATTERN` v `prirazeni.py`, vybraný optimalizací, aby se nic nekupovalo). 26 dílů + sokl, **0 ke koupi**, 29 kusů rezerva. Horní deska se slepí z C04 + C05 (Přemek souhlasí).
- **Skutečné výšky** (`ZA` v `prirazeni.py`, pole `za0` a `hole`): díly jsou nařezané na celé mm, takže výšky děr pro kolíky se počítají ze skutečných délek (police nad příčkou leží na příčce, ostatní podle zaokrouhlené díry v K02/K04, všechny police v úrovni stejně). Tabulka děr v postupu bere `hole` ze spojů. K15 vychází o 1 mm delší než místo pod K26: horní konec zabrousit.
- **Spodní rám** (K01–K04): smontovat vleže, před zvednutím 2 dočasné rozpěrky (police K14 a K18 stažené pásem), zvedat ve dvou, hned nahoře i v půlce ukotvit K02 a K04 do zdi, teprve pak pustit.
- Police na kolících z obou stran jsou o 1 mm kratší než světlost (`PINGAP`). Díry pro kolíky: na pravé straně svislého dílu 30 mm od hran, na levé 60 mm, aby se díry z obou stran nepotkaly.
- Lepidlo na magnety: Debbex Mamut Glue (MS polymer), Přemek ho má (2026-11-25). Podložky pod soklem max ~10 mm (místo pod stropem). V soklu nejdřív vyrovnat, pak lepit dorazy magnetů.
- Spoje (Přemek má aku vrtačku, okružní a přímočarou pilu, frézku, brusku, svěrky, nemá stolní pilu): A) svislý díl stojí na polici / nese ji = 2 vruty 4,5 × 50 skrz, díly srovnat k lati a předvrtat společně (žádné měření, kolíky zamítnuty jako moc přesné), B) police mezi průběžnými díly = **dřevěné kolíky Ø 6 × 20** (Přemkovy, 2026-11-24): díra ve svislém dílu 10 mm hluboká (z 19 zbyde 9), kolík 10 mm venku; police má zespodu na konci drážku 14 mm dlouhou, 4 mm hlubokou (zbyde 15), na levém konci 6 mm širokou, na pravém 8 mm (vůle), kolík pod ní kouká 2 mm, střed díry 1 mm nad spodkem police. Parametry `KOLIK` v `prirazeni.py`. Nic nesmí jít skrz. Drážky drží polici i proti posunutí, úhelník vzadu u polic není potřeba; police se zasune o pár mm výš a spustí na kolíky. Horní deska K26 (pod stropem 2 cm) se zasune zepředu o pár mm výš a spustí: leží na svislých dílech (úhelníky zespodu), vpravo na kolících v K20. Staví se na místě odspodu v pořadí čísel dílů.
- Poškozené desky (A01, A08, A18) jsou na dílech se skrytou stranou. Přiřazení drží v pruhu rezervu ≥ 15 mm, kde to jde. Výjimka: K02 a K04 z D03 a K01 z A18 (rezerva 5 mm).
- Stěny: zadní i pravá jsou sádrokarton, za zadním je dřevo. Kotvení úhelníky s dlouhým vrutem přes SDK do dřeva (K02 a K04 nahoře i v půlce, K15, K19, K25 nahoře; K09 vruty přes obklad). Kotvení dna mostu K24 do zadní stěny se dořeší (X50), skryté nosiče s trny zrušené.
- Kvalita: vše A/B z půdy (původní návrh počítal s B/C kvůli sukům jako obklad).

- Porovnat inventář s kusovníkem výše.
- Kritéria: vlhkost ≤ 10–12 % pro nábytek do vytápěné místnosti (změřit vlhkoměrem), bez hniloby a červotoče, rovné, dost dlouhé a tlusté po hoblování na 19 mm.
- Návrh počítá s třívrstvou deskou. Masivní prkna z půdy jde slepit do spárovky, ale nebudou mít vzhled tří vrstev a víc pracují. Proto zvážit, co jde použít na pohledové díly a co jen na skryté (sokl, podpěry, zkušební vzorky povrchu).
- Výstup: `drevo/prirazeni.md` (který kus → který díl, kolik odpadu) a `drevo/nakup.md` (co dokoupit, množství, orientační cena, kde).
