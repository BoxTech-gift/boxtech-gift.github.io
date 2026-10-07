#!/usr/bin/env python3
"""Export both transcribed gift catalogues to models.json / models.csv and the static /catalog-2026/ assets.

Catalogue 1 (data.py, 111 pages): every model number is published with the prefix "O" (O19030-411).
Catalogue 2 (data2.py, original 223 pages; the first and last page are removed -> 221 pages):
  printed model numbers get the prefix "N" (NF-191, NP207); products without a printed model number get a
  reference code N-P<page>-<k>[-<colour #>] that is used in the request list / WhatsApp text instead.
Every product crop and every page image carries the BoxTech gifts watermark (wm.py), always applied to clean
source pixels rendered from the PDFs (never to an already watermarked file).

Sources:  catalogue 1 page renders pg-000..110.jpg (+ pdfc/qpdf.pdf) next to this file;
          catalogue 2: $CAT2_SRC/catalog2.pdf (rendered to $CAT2_SRC/src/s-NNN.jpg at 200 dpi if missing).
Run:      FORCE=1 python3 export.py
"""
import os, re, json, csv, shutil, subprocess
from collections import Counter
from PIL import Image
import wm
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get('SITE_OUT', os.path.join(HERE, 'site'))
CAT2_SRC = os.environ.get('CAT2_SRC', '/workspace/gift_catalog2')
FORCE = os.environ.get('FORCE') == '1'
def load(fn, var):
    ns = {}; exec(open(os.path.join(HERE, fn), encoding='utf8').read(), ns); return ns[var]
D1, D2 = load('data.py', 'D'), load('data2.py', 'D2')

CATS = [  # key, ar, en (display order)
 ('kits','أطقم وبوكسات ترحيب','Welcome kits & gift sets'),
 ('caps','كابات','Caps'), ('drinkware','زمزميات وأكواب','Drinkware'), ('mugs','مجات','Mugs'), ('pens','أقلام','Pens'),
 ('keychains','ميداليات','Keychains'), ('notebooks','دفاتر ونوت بوك','Notebooks'), ('electronics','إلكترونيات وشواحن','Electronics & chargers'),
 ('cardholders','محافظ وحوامل بطاقات','Wallets & card holders'), ('giftboxes','علب هدايا','Gift boxes'),
 ('bags','أكياس وشنط','Bags'), ('promo','هدايا دعائية','Promo items'), ('mousepads','ماوس باد','Mouse pads'),
 ('badges','بروشات وبطاقات وعلاقات','Badges, lanyards & ID'), ('islamic','مسابح وسجادات صلاة','Prayer beads & prayer rugs'),
 ('fragrance','معطرات وفواحات','Fragrance & diffusers'),
 ('apparel','ملابس وشماغ','Apparel'), ('certificates','أغلفة شهادات','Certificate covers'), ('accessories','إكسسوارات','Accessories'),
 ('printing','مستلزمات طباعة','Printing supplies'), ('frames','براويز','Frames'), ('flags','أعلام وساريات','Flags & poles'),
 ('stands','ستاندات عرض','Display stands'), ('stationery','أدوات مكتبية وحوامل إعلانات','Stationery & sign holders')]
CAT = {k: (a, e) for k, a, e in CATS}
COL = {  # key: ar, en, hex
 'green':('أخضر','Green','#1f7a3a'),'white':('أبيض','White','#ffffff'),'black':('أسود','Black','#1a1a1a'),'pink':('وردي','Pink','#f2a7c3'),
 'sky':('سماوي','Sky blue','#7cc8f0'),'purple':('بنفسجي','Purple','#6a3fa0'),'red':('أحمر','Red','#c8202f'),'navy':('كحلي','Navy','#1d2a5a'),
 'yellow':('أصفر','Yellow','#f5c400'),'orange':('برتقالي','Orange','#f07f1d'),'beige':('بيج','Beige','#d9c6a3'),'brown':('بني','Brown','#6b4429'),
 'blue':('أزرق','Blue','#1f5fbf'),'silver':('فضي','Silver','#c0c4c8'),'gray':('رمادي','Gray','#8a8d91'),'lilac':('ليلكي','Lilac','#b9a2d8'),
 'lightblue':('أزرق فاتح','Light blue','#9cc3e6'),'maroon':('عنابي','Maroon','#7a1f2b'),'lightgreen':('أخضر فاتح','Light green','#8fd18a'),
 'gunmetal':('رصاصي','Gunmetal','#53565a'),'cork':('فلين','Cork','#b98b5e'),'metallicblue':('أزرق معدني','Metallic blue','#2f5d8c'),
 'kraft':('كرافت','Kraft','#b88a5a'),'multi':('متعدد الألوان','Multicolour','conic-gradient(#c8202f,#f5c400,#1f7a3a,#1f5fbf,#6a3fa0,#c8202f)'),
 'teal':('تركوازي','Teal','#178f8f'),'cream':('كريمي','Cream','#f3ead6'),'gold':('ذهبي','Gold','#c9a03d'),'rosegold':('روز جولد','Rose gold','#d4a19a'),
 'mustard':('خردلي','Mustard','#d1a12a'),'petrol':('بترولي','Petrol','#1e5a6b'),'tan':('جملي','Tan','#c19a6b'),'pepsiblue':('أزرق بيبسي','Pepsi blue','#004b93'),
 'magenta':('فوشي','Magenta','#d0217c'),'natural':('خشبي طبيعي','Natural wood','#d8b98a'),'clear':('شفاف','Clear','#eef3f6'),
 'peach':('خوخي','Peach','#f6b59a'),'lightmagenta':('فوشي فاتح','Light magenta','#ec8fc4'),'cyan':('سيان','Cyan','#00a9d6'),
 'lightcyan':('سيان فاتح','Light cyan','#8fdcee'),'bronze':('برونزي','Bronze','#9c6b3a'),
 'olive':('زيتي','Olive','#6f6b2e'),'darkolive':('زيتي غامق','Dark olive','#46431f'),'greenmarble':('أخضر رخامي','Green marble','#4f7d5c'),
 'charcoal':('فحمي','Charcoal','#3b3d40'),'bluegray':('أزرق رمادي','Blue gray','#6c7a89'),'sage':('أخضر رمادي','Sage','#a3b5a6'),
}
def color(key):
    if key in COL: a, e, h = COL[key]; return dict(key=key, ar=a, en=e, hex=[h])
    cs = [COL[p] for p in key.split('/')]
    return dict(key=key, ar=' / '.join(c[0] for c in cs), en=' / '.join(c[1] for c in cs), hex=[c[2] for c in cs])

def save_webp(im, path, q):
    if os.path.exists(path) and not FORCE: return
    im.save(path, 'WEBP', quality=q, method=6)
OUTC = f'{SITE}/catalog-2026'
for d in ('img', 'pages', 'pages2'): os.makedirs(f'{OUTC}/{d}', exist_ok=True)
os.makedirs(f'{SITE}/catalog-data', exist_ok=True)

# ---------- catalogue 2 sources: page renders + trimmed PDF ----------
C2_FIRST, C2_LAST, C2_TOTAL = 2, 222, 223
src2 = os.path.join(CAT2_SRC, 'src')
if not os.path.exists(os.path.join(src2, 's-%03d.jpg' % C2_LAST)):
    os.makedirs(src2, exist_ok=True)
    subprocess.check_call(['pdftoppm', '-f', str(C2_FIRST), '-l', str(C2_LAST), '-r', '200', '-jpeg', '-jpegopt', 'quality=95',
                           os.path.join(CAT2_SRC, 'catalog2.pdf'), os.path.join(src2, 's')])
pdf2 = os.path.join(CAT2_SRC, 'catalog2-trimmed.pdf')
if not os.path.exists(pdf2) or FORCE:  # drop page 1 (cover) and page 223 (back cover / contact page), lossless repack
    subprocess.check_call(['qpdf', os.path.join(CAT2_SRC, 'catalog2.pdf'), '--pages', '.', f'{C2_FIRST}-{C2_LAST}', '--',
                           '--object-streams=generate', '--compress-streams=y', '--recompress-flate', '--compression-level=9', pdf2])
pdf1 = os.path.join(HERE, 'pdfc', 'qpdf.pdf'); pdf1 = pdf1 if os.path.exists(pdf1) else os.path.join(HERE, 'catalog.pdf')

CATALOGS = {
 '1': dict(key='1', ar='الكتالوج ١', en='Catalogue 1', prefix='O', first=1, last=111, pages_dir='pages',
           pdf='BoxTech-gifts-catalog-2026.pdf', pdf_src=pdf1, src=lambda n: os.path.join(HERE, 'pg-%03d.jpg' % (n - 1))),
 '2': dict(key='2', ar='الكتالوج ٢', en='Catalogue 2', prefix='N', first=C2_FIRST, last=C2_LAST, pages_dir='pages2',
           pdf='BoxTech-gifts-catalog-2-2026.pdf', pdf_src=pdf2, src=lambda n: os.path.join(src2, 's-%03d.jpg' % n)),
}
srcs = {}
def page_img(cat, n):
    k = (cat, n)
    if k not in srcs: srcs.clear(); srcs[k] = Image.open(CATALOGS[cat]['src'](n)).convert('RGB')
    return srcs[k]
C2_BOX = (0.09, 0.985, 0.012, 0.988)  # default crop for catalogue 2: whole page below the running header

products, rows, uncertain, noprint = [], [], [], []
for catk, D in (('1', D1), ('2', D2)):
    C = CATALOGS[catk]; cnt = {}
    for p in D:
        n = p['page'] + 1 if catk == '1' else p['page']           # catalogue-1 data uses 0-based page index
        cnt[n] = cnt.get(n, 0) + 1
        pid = ('p%03d-%d' if catk == '1' else 'n%03d-%d') % (n, cnt[n])
        t, b, l, r = p['box'] or C2_BOX; im = page_img(catk, n); W, H = im.size
        crop = im.crop((round(l * W), round(t * H), round(r * W), round(b * H)))
        if catk == '2' and crop.width > 1000: crop = crop.resize((1000, round(crop.height * 1000 / crop.width)), Image.LANCZOS)
        save_webp(wm.apply(crop), f'{OUTC}/img/{pid}.webp', 82)
        vs = []; ref0 = 'N-P%03d-%d' % (n, cnt[n])
        for j, v in enumerate(p['variants']):
            m, ck = v[0], v[1]; lab = v[2] if len(v) > 2 else ''
            c = color(ck)
            if catk == '1':
                pm = C['prefix'] + m if re.match(r'^\d', m) else m
                vid = pm if '?' not in m else 'O?-%s-%d' % (pid, j + 1); ref = vid; kind = '?' if '?' in m else 'm'
                if '?' in m: uncertain.append(dict(catalog=catk, page=n, name_ar=p['ar'], model=m, color=c['ar'], label=lab, note=p['note']))
            else:
                ref = ref0 if len(p['variants']) == 1 else '%s-%d' % (ref0, j + 1)
                if m:
                    pm = C['prefix'] + m; kind = 'm'
                    vid = pm if sum(1 for x in p['variants'] if x[0] == m) == 1 else '%s-%s' % (pm, ck.replace('/', '-'))
                else:
                    pm = ''; kind = 'r'; vid = ref
            vs.append(dict(id=vid, model=pm, model_raw=m, ref=ref, kind=kind, color=c, label=lab))
            spec = ' | '.join(x for x in (p['specs'], lab) if x)
            note = p['note'] if catk == '1' or m else ' | '.join(x for x in ('لا يوجد رقم موديل مطبوع في الكتالوج', p['note']) if x)
            rows.append([catk, n, f"{CAT[p['cat']][0]} / {CAT[p['cat']][1]}", p['ar'], p['en'], spec, pm, ref,
                         f"{c['ar']} / {c['en']}", note])
        if catk == '2' and not any(v['model'] for v in vs): noprint.append(pid)
        products.append(dict(id=pid, catalog=catk, page=n, pdf_page=n if catk == '1' else n - 1, category=p['cat'], name_ar=p['ar'],
                             name_en=p['en'], specs=p['specs'], image=f'/catalog-2026/img/{pid}.webp', size=list(crop.size),
                             variants=vs, note=p['note']))
    for n in range(C['first'], C['last'] + 1):
        pg = wm.apply(page_img(catk, n))
        save_webp(pg, f"{OUTC}/{C['pages_dir']}/p%03d.webp" % n, 80)
        th = pg.copy(); th.thumbnail((260, 260) if catk == '2' else (184, 260), Image.LANCZOS)
        save_webp(th, f"{OUTC}/{C['pages_dir']}/t%03d.webp" % n, 80)
    srcs.clear()

def stats(ps):
    mc = Counter(v['model'] for pr in ps for v in pr['variants'] if v['kind'] == 'm')
    return dict(products=len(ps), variants=sum(len(x['variants']) for x in ps), unique_models=len(mc),
                printed_model_variants=sum(1 for pr in ps for v in pr['variants'] if v['kind'] == 'm'),
                reference_only_variants=sum(1 for pr in ps for v in pr['variants'] if v['kind'] == 'r')), mc
cats = []
for k, a, e in CATS:
    ps = [x for x in products if x['category'] == k]
    if ps: cats.append(dict(key=k, ar=a, en=e, products=len(ps), models=sum(len(x['variants']) for x in ps),
                            by_catalog={c: sum(1 for x in ps if x['catalog'] == c) for c in CATALOGS}))
allst, mc_all = stats(products)
raw1 = {v['model_raw'] for pr in products if pr['catalog'] == '1' for v in pr['variants']}
collisions = sorted({v['model'] for pr in products if pr['catalog'] == '2' for v in pr['variants'] if v['kind'] == 'm' and v['model_raw'] in raw1})
dups = sorted(k for k, n in Counter(v['model'] for pr in products if pr['catalog'] == '1' for v in pr['variants'] if v['kind'] == 'm').items() if n > 1)
catmeta = []
for c in CATALOGS.values():
    st, _ = stats([x for x in products if x['catalog'] == c['key']])
    catmeta.append(dict(key=c['key'], title_ar=c['ar'], title_en=c['en'], model_prefix=c['prefix'], first_page=c['first'], last_page=c['last'],
                        pages=c['last'] - c['first'] + 1, source_pdf='/catalog-2026/' + c['pdf'], pdf_bytes=os.path.getsize(c['pdf_src']), **st))
catmeta[1].update(original_pages=C2_TOTAL, removed_pages=[1, C2_TOTAL],
                  page_note='page = original page number = printed "PAGE N" label; trimmed-PDF page = page - 1 (original p.32 is printed "PAGE 31", p.146 is printed "PAGE 52")',
                  reference_note='Catalogue 2 prints model numbers for two products only (F-191, P207 -> NF-191, NP207). All other variants have model = "" and a reference code N-P<page>-<k>[-<colour #>] used in the request list.')
meta = dict(title_ar='كتالوج الهدايا ٢٠٢٦', title_en='BoxTech gifts catalog 2026',
            model_prefix_note='Catalogue 1 model numbers are prefixed with "O" (O19030-411 = code 19030-411); catalogue 2 printed model numbers are prefixed with "N" (NF-191 = F-191).',
            catalogs=catmeta, uncertain=uncertain, duplicate_models_catalog1=dups, collisions_catalog2_vs_1=collisions,
            catalog2_products_without_printed_model=len(noprint), **allst)
full = dict(meta=meta, categories=cats, products=products)
for path in (os.path.join(HERE, 'models.json'), f'{SITE}/catalog-data/models.json'):
    json.dump(full, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for path in (os.path.join(HERE, 'models.csv'), f'{SITE}/catalog-data/models.csv'):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['catalog', 'page', 'category', 'name_ar', 'name_en', 'specs', 'model', 'ref', 'color', 'note']); w.writerows(rows)
# compact data for the page
colors = {}
for pr in products:
    for v in pr['variants']: colors[v['color']['key']] = [v['color']['ar'], v['color']['en'], v['color']['hex']]
site = dict(cats=[[c['key'], c['ar'], c['en']] for c in cats], colors=colors,
            catalogs=[[c['key'], c['ar'], c['en'], c['first'], c['last'], c['pages_dir'], c['pdf'], os.path.getsize(c['pdf_src']), c['prefix']]
                      for c in CATALOGS.values()],
            items=[[pr['id'], pr['page'], pr['category'], pr['name_ar'], pr['name_en'], pr['specs'], pr['size'],
                    [[v['id'], v['model'] or v['ref'], v['color']['key'], v['label'], v['kind']] for v in pr['variants']], pr['note'], pr['catalog']]
                   for pr in products])
site['pdf'] = site['catalogs'][0][7]
open(f'{OUTC}/data.json', 'w', encoding='utf8').write(json.dumps(site, ensure_ascii=False, separators=(',', ':')))
for c in CATALOGS.values(): shutil.copy(c['pdf_src'], f"{OUTC}/{c['pdf']}")
print(json.dumps(dict(all=allst, catalogs=[{k: m[k] for k in ('key', 'pages', 'products', 'variants', 'unique_models', 'pdf_bytes')} for m in catmeta],
                      uncertain=len(uncertain), collisions=collisions, dups=dups, cat2_no_model=len(noprint)), ensure_ascii=False))
