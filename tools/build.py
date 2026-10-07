#!/usr/bin/env python3
"""Build the static GitHub Pages tree for BoxTech gifts.
Usage: build.py [BASE] [SITE_URL]
  BASE      '/' for the user/org root site (boxtech-gift.github.io), or '/<repo>/' for a project site.
  SITE_URL  absolute site URL for og:image and sitemap (optional).
Sources: the original app build in $SRC (assets, catalog, og.jpg, favicon.svg, app icon) and the
2026 gifts catalog in $CATALOG_SRC (tools/catalog-2026: data.py transcription, export.py, web/ page;
site/ = exported WebP crops + pages, data.json, models.json/csv, PDF).
All site images are WebP (q82, visually lossless) except og.jpg, which stays an optimised JPEG for link previews.
"""
import os, sys, shutil, re, json
SRC = os.environ.get('SRC', '/workspace/boxgift-mirror')
CATALOG_SRC = os.environ.get('CATALOG_SRC', '/workspace/gift_catalog')
OUT = os.environ.get('OUT', '/workspace/boxgift-pages')
BASE = sys.argv[1] if len(sys.argv) > 1 else '/theboxgift/'
if not BASE.startswith('/'): BASE = '/' + BASE
if not BASE.endswith('/'): BASE += '/'
SITE = (sys.argv[2] if len(sys.argv) > 2 else '').rstrip('/')
BP = BASE.rstrip('/')  # router basepath: '' for root, '/theboxgift' for project

COLLECTIONS = 'boxes carry desk drink mark nature prayer scent tech welcome'.split()
PRODUCTS = ('welcome-folio welcome-gray welcome-green box-flying box-drawer box-handle nature-cork nature-trio nature-seed '
            'tech-bank tech-multi tech-adapter tech-mag tech-note drink-cork drink-thermos drink-infuser desk-pen desk-note '
            'desk-stand prayer-agate prayer-stone prayer-promo scent-reed scent-car scent-burner carry-sleeve carry-certificate '
            'carry-tote carry-pouch mark-key mark-card mark-lanyard mark-brooch').split()
ROUTES = ['list'] + ['collection/' + c for c in COLLECTIONS] + ['product/' + p for p in PRODUCTS]

# clean OUT but keep .git
os.makedirs(OUT, exist_ok=True)
for n in os.listdir(OUT):
    if n in ('.git', 'README.md'): continue
    p = os.path.join(OUT, n)
    shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
shutil.copytree(f'{SRC}/assets', f'{OUT}/assets')
shutil.copy(f'{SRC}/favicon.svg', f'{OUT}/favicon.svg')
shutil.copy(f'{SRC}/__grok/icon-180.png', f'{OUT}/apple-touch-icon.png')
from PIL import Image
# collection photos -> WebP (same 1600x1200 resolution, q82); og.jpg stays JPEG (link previews) but re-encoded progressive/optimised if smaller
os.makedirs(f'{OUT}/catalog', exist_ok=True)
for n in COLLECTIONS:
    Image.open(f'{SRC}/catalog/{n}.jpg').convert('RGB').save(f'{OUT}/catalog/{n}.webp', 'WEBP', quality=82, method=6)
shutil.copy(f'{SRC}/og.jpg', f'{OUT}/og.jpg')
Image.open(f'{SRC}/og.jpg').convert('RGB').save(f'{OUT}/og.tmp.jpg', 'JPEG', quality=85, optimize=True, progressive=True)
if os.path.getsize(f'{OUT}/og.tmp.jpg') < os.path.getsize(f'{OUT}/og.jpg'): os.replace(f'{OUT}/og.tmp.jpg', f'{OUT}/og.jpg')
else: os.remove(f'{OUT}/og.tmp.jpg')

def patch(name, pairs):
    p = f'{OUT}/assets/{name}'
    s = open(p, encoding='utf8').read()
    for a, b, n in pairs:
        if isinstance(a, re.Pattern):
            s, c = a.subn(b, s)
            assert c == n, (name, a.pattern[:60], c, n)
            continue
        c = s.count(a)
        assert c == n, (name, a[:60], c, n)
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8').write(s)

# 1) entry bundle: client-only createRoot (no SSR hydration), router basepath, head links
patch('index-DLFO-8IC.js', [
    ('e.hydrateRoot=function(e,t,n){if(!o(e))throw Error(a(299));',
     'e.createRoot=function(e,t){if(!o(e))throw Error(a(299));var r=!1,i=``,s=Oc,c=kc,l=Ac,u=null;return t!=null&&(!0===t.unstable_strictMode&&(r=!0),t.identifierPrefix!==void 0&&(i=t.identifierPrefix),t.onUncaughtError!==void 0&&(s=t.onUncaughtError),t.onCaughtError!==void 0&&(c=t.onCaughtError),t.onRecoverableError!==void 0&&(l=t.onRecoverableError)),t=lh(e,1,!1,null,null,r,i,u,s,c,l,Uh),t.context=uh(null),e[Pt]=t.current,Wf(e),new Wh(t)},e.hydrateRoot=function(e,t,n){if(!o(e))throw Error(a(299));', 1),
    ('e.stores.ids.get().length||await Zn(e),e}var iv=rv', 'e}var iv=rv', 1),
    ('(0,cv.hydrateRoot)(document,(0,R.jsx)(L.StrictMode,{children:(0,R.jsx)(sv,{})}))',
     '(0,cv.createRoot)(document).render((0,R.jsx)(L.StrictMode,{children:(0,R.jsx)(sv,{})}))', 1),
    ('e.update({basepath:``,serializationAdapters:t})', 'e.update({basepath:`%s`,serializationAdapters:t})' % BP, 1),
    ('{rel:`manifest`,href:`/__grok/manifest.webmanifest`},{rel:`apple-touch-icon`,href:`/__grok/icon-180.png`}',
     '{rel:`manifest`,href:`%smanifest.webmanifest`},{rel:`apple-touch-icon`,href:`%sapple-touch-icon.png`}' % (BASE, BASE), 1),
    ('href:`/favicon.svg`}', 'href:`%sfavicon.svg`},{rel:`icon`,href:`%sfavicon.ico`,sizes:`48x48`}' % (BASE, BASE), 1),
    ('`/assets/styles-C6nPWCr9.css`', '`%sassets/styles-C6nPWCr9.css`' % BASE, 1),
])
# 2) Vite dynamic-import preload base
patch('preload-helper-CTNSAW6c.js', [('B=function(e){return`/`+e}', 'B=function(e){return`%s`+e}' % BASE, 1)])
# 3) catalog image paths
IMG = re.compile(r'`/catalog/([a-z]+)\.jpg`')
patch('locale-LgrRR7N2.js', [(IMG, r'`%scatalog/\1.webp`' % BASE, 11)])
patch('routes-T_lj7gbW.js', [(IMG, r'`%scatalog/\1.webp`' % BASE, 2)])

# 4) 2026 gifts catalog (static page at /catalog-2026/) wired into the app
CAT_URL = BASE + 'catalog-2026/'
CAT_INFO = json.load(open(f'{CATALOG_SRC}/models.json', encoding='utf8'))['meta']
NP, NM = CAT_INFO['products'], CAT_INFO['variants']
#  a) header link (every route)
patch('index-DLFO-8IC.js', [
    ('children:r(T.indexLabel)}),',
     'children:r(T.indexLabel)}),(0,R.jsx)(`a`,{href:`%s`,className:`hidden h-11 items-center px-2 text-sm text-seal sm:inline-flex`,style:{whiteSpace:`nowrap`},children:r({ar:`كتالوج ٢٠٢٦`,en:`Catalog 2026`})}),' % CAT_URL, 1),
    #  index drawer entry (also the way in on small screens)
    ('},e.slug))}),(0,R.jsx)(`button`,{type:`button`,onClick:S,className:`${i} mt-10 text-start text-3xl`',
     '},e.slug))}),(0,R.jsxs)(`a`,{href:`%s`,className:`flex items-baseline gap-4 border-b border-line py-4 text-seal`,children:[(0,R.jsx)(`span`,{className:`text-xs text-muted tabular-nums`,children:`2026`}),(0,R.jsx)(`span`,{className:`${i} text-3xl leading-none`,children:r({ar:`كتالوج الهدايا ٢٠٢٦`,en:`Gifts catalog 2026`})})]}),(0,R.jsx)(`button`,{type:`button`,onClick:S,className:`${i} mt-10 text-start text-3xl`' % CAT_URL, 1),
    #  b) quote form: include catalog items from the request list (model number + name + colour + qty)
    ('re.forEach((e,r)=>{n.push(`${r+1}. ${e.code} — ${t(e.name)} × ${s[e.id]}`)}),',
     're.forEach((e,r)=>{n.push(`${r+1}. ${e.code} — ${t(e.name)} × ${s[e.id]}`)}),z_.getState().items.filter(e=>e&&e.cat).forEach((e,r)=>{n.push(`${re.length+r+1}. ${e.cat.code} — ${t(e.cat.name)}${e.cat.color?` — `+t(e.cat.color):``} × ${e.qty}`)}),', 1),
    ('if(!re.length){S(t(T.pickOne));return}', 'if(!re.length&&!z_.getState().items.some(e=>e&&e.cat)){S(t(T.pickOne));return}', 1),
])
#  c) home page: catalog 2026 banner above the collections
patch('routes-T_lj7gbW.js', [
    ('(0,h.jsxs)(`section`,{id:`work`,',
     '(0,h.jsx)(`section`,{className:`mx-auto mt-24 max-w-7xl px-5`,children:(0,h.jsxs)(`a`,{href:`%s`,className:`group grid items-center gap-8 border border-ink bg-paper-2 p-6 lg:grid-cols-12`,children:[(0,h.jsxs)(`div`,{className:`lg:col-span-8`,children:[(0,h.jsx)(`p`,{className:`text-sm text-seal`,children:n({ar:`جديد · الكتالوج الكامل`,en:`New · full catalog`})}),(0,h.jsx)(`h2`,{className:`${c} mt-3 text-4xl leading-tight sm:text-5xl group-hover:text-seal`,children:n({ar:`كتالوج الهدايا ٢٠٢٦`,en:`Gifts catalog 2026`})}),(0,h.jsx)(`p`,{className:`mt-3 max-w-xl text-sm text-pretty text-muted`,children:n({ar:`%d منتجًا و%d رقم موديل بكل الألوان، مع البحث برقم الموديل وعارض الصفحات وتحميل الكتالوج PDF.`,en:`%d products and %d model numbers in every colour, with model-number search, a page viewer and the PDF download.`})}),(0,h.jsx)(`span`,{className:`mt-6 inline-flex h-11 items-center bg-ink px-5 text-sm text-on-seal`,children:n({ar:`افتح الكتالوج`,en:`Open the catalog`})})]}),(0,h.jsx)(`div`,{className:`lg:col-span-4`,children:(0,h.jsx)(`img`,{src:`%spages/t001.webp`,alt:``,loading:`lazy`,width:184,height:260,style:{width:`auto`,maxHeight:`260px`,margin:`0 auto`,boxShadow:`0 10px 30px rgba(28,25,21,.25)`}})})]})}),(0,h.jsxs)(`section`,{id:`work`,' % (CAT_URL, NP, NM, NP, NM, CAT_URL), 1),
])
#  d) request list: render catalog items (not in the 34-product data) with their O-model code; safe colour lookup
patch('list-BeZjhFSD.js', [
    ('F=h.map(e=>{let t=s(e.id);return t?{item:e,product:t}:null}).filter(e=>!!e);',
     'F=h.map(e=>{let t=s(e.id);return t?{item:e,product:t}:e&&e.cat?{item:e,product:{id:e.id,code:e.cat.code,name:e.cat.name,cat:e.cat}}:null}).filter(e=>!!e),Q=(t,n)=>n.cat?n.cat.color?e(n.cat.color):``:i[t.color]?e(i[t.color]):``;', 1),
    ('${e(n.name)}  × ${t.qty}  ${e(i[t.color])}', '${e(n.name)}  × ${t.qty}  ${Q(t,n)}', 1),
    ('(0,p.jsx)(n,{to:`/product/$id`,params:{id:a.id},className:`text-lg font-medium`,children:e(a.name)})',
     'a.cat?(0,p.jsx)(`a`,{href:`%s?q=${encodeURIComponent(a.code)}${a.cat.product?`#`+a.cat.product:``}`,className:`text-lg font-medium`,children:e(a.name)}):(0,p.jsx)(n,{to:`/product/$id`,params:{id:a.id},className:`text-lg font-medium`,children:e(a.name)})' % CAT_URL, 1),
    ('children:[e(r.color),`: `,e(i[t.color])]', 'children:[e(r.color),`: `,Q(t,a)]', 1),
])
#  e) static files
shutil.copytree(f'{CATALOG_SRC}/site/catalog-2026', f'{OUT}/catalog-2026')
shutil.copytree(f'{CATALOG_SRC}/site/catalog-data', f'{OUT}/catalog-data')
import hashlib
ver = hashlib.sha1(b''.join(open(f'{CATALOG_SRC}/{f}', 'rb').read() for f in ('web/app.js', 'web/app.css', 'site/catalog-2026/data.json'))).hexdigest()[:10]
for f in ('index.html', 'app.js', 'app.css'):
    t = open(f'{CATALOG_SRC}/web/{f}', encoding='utf8').read().replace('__V__', ver).replace('__OG__', (SITE + '/og.jpg') if SITE else (BASE + 'og.jpg'))
    open(f'{OUT}/catalog-2026/{f}', 'w', encoding='utf8').write(t)
os.makedirs(f'{OUT}/tools/catalog-2026/web', exist_ok=True)
for f in ('data.py', 'export.py', 'web/index.html', 'web/app.js', 'web/app.css'):
    shutil.copy(f'{CATALOG_SRC}/{f}', f'{OUT}/tools/catalog-2026/{f}')

og = (SITE + '/og.jpg') if SITE else (BASE + 'og.jpg')
shell = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>BoxTech gifts — كتالوج ٢٠٢٦</title>
<meta name="description" content="كتالوج BoxTech gifts ٢٠٢٦ للهدايا الدعائية وأطقم الترحيب."/>
<meta name="theme-color" content="#F6F1E7"/>
<meta property="og:title" content="BoxTech gifts"/>
<meta property="og:description" content="كتالوج BoxTech gifts ٢٠٢٦ للهدايا الدعائية وأطقم الترحيب."/>
<meta property="og:image" content="{og}"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="icon" type="image/svg+xml" href="{BASE}favicon.svg"/>
<link rel="icon" href="{BASE}favicon.ico" sizes="48x48"/>
<link rel="apple-touch-icon" href="{BASE}apple-touch-icon.png"/>
<link rel="manifest" href="{BASE}manifest.webmanifest"/>
<link rel="stylesheet" href="{BASE}assets/styles-C6nPWCr9.css"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&amp;family=Fraunces:ital,wght@0,500;0,600;1,500&amp;family=IBM+Plex+Sans+Arabic:wght@400;500;600&amp;display=swap"/>
<link rel="modulepreload" href="{BASE}assets/index-DLFO-8IC.js"/>
<link rel="modulepreload" href="{BASE}assets/locale-LgrRR7N2.js"/>
<link rel="modulepreload" href="{BASE}assets/routes-T_lj7gbW.js"/>
<script>window["$_TSR"]=window["$_TSR"]||{{buffer:[],initialized:!1,e:function(){{}},c:function(){{}},p:function(e){{this.initialized?e():this.buffer.push(e)}},h:function(){{this.initialized=!0;var b=this.buffer.splice(0);for(var i=0;i<b.length;i++)b[i]()}},router:{{manifest:{{routes:{{}}}},matches:[]}}}};</script>
</head>
<body>
<div id="root"></div>
<script type="module" src="{BASE}assets/index-DLFO-8IC.js"></script>
</body>
</html>
'''
for r in [''] + ROUTES:
    os.makedirs(f'{OUT}/{r}', exist_ok=True)
    open(f'{OUT}/{r}/index.html' if r else f'{OUT}/index.html', 'w', encoding='utf8').write(shell)
open(f'{OUT}/404.html', 'w', encoding='utf8').write(shell)  # deep-link fallback (GitHub Pages serves it for any missing path)
json.dump({"name": "BoxTech gifts", "short_name": "BoxTech gifts", "lang": "ar", "dir": "rtl", "id": BASE, "start_url": BASE,
           "scope": BASE, "display": "standalone", "background_color": "#F6F1E7", "theme_color": "#F6F1E7",
           "icons": [{"src": BASE + "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]},
          open(f'{OUT}/manifest.webmanifest', 'w', encoding='utf8'), ensure_ascii=False, indent=2)
open(f'{OUT}/robots.txt', 'w').write('User-agent: *\nAllow: /\n')
if SITE:
    urls = [SITE + '/', SITE + '/catalog-2026/'] + [f'{SITE}/{r}' for r in ROUTES]
    open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(f'{OUT}/robots.txt', 'a').write(f'Sitemap: {SITE}/sitemap.xml\n')
open(f'{OUT}/.nojekyll', 'w').close()
try:
    Image.open(f'{OUT}/apple-touch-icon.png').convert('RGBA').save(f'{OUT}/favicon.ico', sizes=[(32, 32), (48, 48)])
except Exception as e:
    print('favicon.ico skipped:', e)
os.makedirs(f'{OUT}/tools', exist_ok=True)
shutil.copy(os.path.abspath(__file__), f'{OUT}/tools/build.py')
print(f'built {OUT} with BASE={BASE} basepath={BP!r} routes={len(ROUTES)+1}')
