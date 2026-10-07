#!/usr/bin/env python3
"""Export the transcribed 2026 gifts catalog (data.py) to models.json / models.csv and the static
/catalog-2026/ assets (product crops + page images as WebP, data.json, PDF).
Every PDF-catalog model number is published with the prefix "O" (e.g. O19030-411)."""
import os, re, json, csv, shutil, io
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get('SITE_OUT', os.path.join(HERE, 'site'))
PREFIX = 'O'
ns = {}; exec(open(os.path.join(HERE, 'data.py'), encoding='utf8').read(), ns); D = ns['D']

CATS = [  # key, ar, en (display order)
 ('caps','كابات','Caps'), ('drinkware','زمزميات وأكواب','Drinkware'), ('mugs','مجات','Mugs'), ('pens','أقلام','Pens'),
 ('keychains','ميداليات','Keychains'), ('notebooks','دفاتر ونوت بوك','Notebooks'), ('giftboxes','علب هدايا','Gift boxes'),
 ('bags','أكياس وشنط','Bags'), ('promo','هدايا دعائية','Promo items'), ('badges','بروشات وبطاقات وعلاقات','Badges, lanyards & ID'),
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
}
def color(key):
    if key in COL: a, e, h = COL[key]; return dict(key=key, ar=a, en=e, hex=[h])
    parts = key.split('/'); cs = [COL[p] for p in parts]
    return dict(key=key, ar=' / '.join(c[0] for c in cs), en=' / '.join(c[1] for c in cs), hex=[c[2] for c in cs])
def pub(m):  # published model number
    return PREFIX + m if re.match(r'^\d', m) else m

os.makedirs(f'{SITE}/catalog-2026/img', exist_ok=True); os.makedirs(f'{SITE}/catalog-2026/pages', exist_ok=True)
os.makedirs(f'{SITE}/catalog-data', exist_ok=True)
srcs = {}
def page_img(i):
    if i not in srcs: srcs[i] = Image.open(os.path.join(HERE, 'pg-%03d.jpg' % i)).convert('RGB')
    return srcs[i]
def save_webp(im, path, q):
    if os.path.exists(path) and os.environ.get('FORCE') != '1': return
    im.save(path, 'WEBP', quality=q, method=6)

products, rows, uncertain = [], [], []
order = {k: n for n, (k, _, _) in enumerate(CATS)}
cnt = {}
for p in D:
    idx = p['page']; pdfp = idx + 1
    cnt[idx] = cnt.get(idx, 0) + 1
    pid = 'p%03d-%d' % (pdfp, cnt[idx])
    t, b, l, r = p['box']; im = page_img(idx); W, H = im.size
    crop = im.crop((round(l * W), round(t * H), round(r * W), round(b * H)))
    save_webp(crop, f'{SITE}/catalog-2026/img/{pid}.webp', 82)
    vs = []
    for j, v in enumerate(p['variants']):
        m, ck = v[0], v[1]; lab = v[2] if len(v) > 2 else ''
        c = color(ck); pm = pub(m)
        vid = pm if '?' not in m else 'O?-%s-%d' % (pid, j + 1)
        vs.append(dict(id=vid, model=pm, model_raw=m, color=c, label=lab))
        if '?' in m: uncertain.append(dict(page=pdfp, name_ar=p['ar'], model=m, color=c['ar'], label=lab, note=p['note']))
        spec = ' | '.join(x for x in (p['specs'], lab) if x)
        rows.append([pdfp, f"{CAT[p['cat']][0]} / {CAT[p['cat']][1]}", p['ar'], p['en'], spec, pm, f"{c['ar']} / {c['en']}"])
    products.append(dict(id=pid, page=pdfp, category=p['cat'], name_ar=p['ar'], name_en=p['en'], specs=p['specs'],
                         image=f'/catalog-2026/img/{pid}.webp', size=list(crop.size), variants=vs, note=p['note']))
for i in range(111):
    im = page_img(i)
    save_webp(im, f'{SITE}/catalog-2026/pages/p%03d.webp' % (i + 1), 80)
    th = im.copy(); th.thumbnail((184, 260), Image.LANCZOS)
    save_webp(th, f'{SITE}/catalog-2026/pages/t%03d.webp' % (i + 1), 80)
srcs.clear()

from collections import Counter
mc = Counter(v['model'] for pr in products for v in pr['variants'] if '?' not in v['model'])
dups = sorted(k for k, n in mc.items() if n > 1)
cats = [dict(key=k, ar=a, en=e, products=sum(1 for x in products if x['category'] == k),
             models=sum(len(x['variants']) for x in products if x['category'] == k)) for k, a, e in CATS]
cats = [c for c in cats if c['products']]
meta = dict(title_ar='كتالوج الهدايا ٢٠٢٦', title_en='BoxTech gifts catalog 2026', source_pdf='/catalog-2026/BoxTech-gifts-catalog-2026.pdf',
            pages=111, model_prefix=PREFIX, model_prefix_note='All model numbers from the PDF catalog are prefixed with "O" (O19030-411 = catalog code 19030-411).',
            products=len(products), variants=sum(len(x['variants']) for x in products), unique_models=len(mc),
            uncertain=uncertain, duplicate_models=dups)
full = dict(meta=meta, categories=cats, products=products)
for path in (os.path.join(HERE, 'models.json'), f'{SITE}/catalog-data/models.json'):
    json.dump(full, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for path in (os.path.join(HERE, 'models.csv'), f'{SITE}/catalog-data/models.csv'):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['page', 'category', 'name_ar', 'name_en', 'specs', 'model', 'color']); w.writerows(rows)
# compact data for the page
colors = {}
for pr in products:
    for v in pr['variants']: colors[v['color']['key']] = [v['color']['ar'], v['color']['en'], v['color']['hex']]
site = dict(cats=[[c['key'], c['ar'], c['en']] for c in cats], colors=colors,
            items=[[pr['id'], pr['page'], pr['category'], pr['name_ar'], pr['name_en'], pr['specs'], pr['size'],
                    [[v['id'], v['model'], v['color']['key'], v['label']] for v in pr['variants']], pr['note']] for pr in products])
pdf_src = os.path.join(HERE, 'pdfc', 'qpdf.pdf'); pdf_src = pdf_src if os.path.exists(pdf_src) else os.path.join(HERE, 'catalog.pdf')
site['pdf'] = os.path.getsize(pdf_src)
open(f'{SITE}/catalog-2026/data.json', 'w', encoding='utf8').write(json.dumps(site, ensure_ascii=False, separators=(',', ':')))
shutil.copy(pdf_src, f'{SITE}/catalog-2026/BoxTech-gifts-catalog-2026.pdf')
print(json.dumps({k: meta[k] for k in ('products', 'variants', 'unique_models')}), 'uncertain', len(uncertain), 'dups', dups)
