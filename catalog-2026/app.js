/* BoxTech gifts — catalog 2026 (vanilla JS, no dependencies).
   Request-list items are written to the site's own persisted list (localStorage "boxtech-gifts-list"),
   so they appear on /list with their codes in the WhatsApp / copy / print text: catalogue 1 model numbers are
   O-prefixed (O19030-411); catalogue 2 printed model numbers are N-prefixed (NF-191) and its products without a
   printed model number use a reference code (N-P004-1-3). */
(function () {
  'use strict';
  var LIST_KEY = 'boxtech-gifts-list', LANG_KEY = 'boxtech-gifts-lang';
  var T = {
    home: ['الرئيسية', 'Home'], viewer: ['عارض الصفحات', 'Page viewer'], toList: ['قائمة الطلب', 'Request list'],
    list: ['قائمة الطلب', 'Request list'], kicker: ['BoxTech gifts · الإصدار ٢٠٢٦', 'BoxTech gifts · 2026 edition'],
    title: ['كتالوج الهدايا ٢٠٢٦', 'Gifts catalog 2026'], browse: ['تصفّح المنتجات', 'Browse products'],
    pdf: ['تحميل الكتالوج PDF', 'Download the PDF'], pdf1: ['تحميل الكتالوج ١ PDF', 'Download catalogue 1 (PDF)'], pdf2: ['تحميل الكتالوج ٢ PDF', 'Download catalogue 2 (PDF)'],
    c1: ['الكتالوج ١', 'Catalogue 1'], c2: ['الكتالوج ٢', 'Catalogue 2'], cAll: ['الكل', 'All'], cshort1: ['ك١', 'C1'], cshort2: ['ك٢', 'C2'],
    ref: ['رمز مرجعي', 'Reference'], noPrinted: ['لا يوجد رقم موديل مطبوع في الكتالوج ٢ — استخدم الرمز المرجعي', 'No model number is printed in catalogue 2 — use the reference code'],
    v2note: ['أرقام الصفحات كما هي مطبوعة في الكتالوج ٢ (حُذفت صفحة الغلاف والصفحة الأخيرة).', 'Page numbers as printed in catalogue 2 (the cover and the last page are removed).'],
    cset: ['اختر الكتالوج', 'Choose the catalogue'], files: ['ملفات أرقام الموديلات:', 'Model-number files:'],
    prefix: ['أرقام موديلات الكتالوج ١ تبدأ بالحرف O (مثال: \u2066O19030-411\u2069)، وأرقام موديلات الكتالوج ٢ تبدأ بالحرف N (مثال: \u2066NF-191\u2069). يمكن البحث مع الحرف أو بدونه. معظم منتجات الكتالوج ٢ بلا رقم موديل مطبوع، فلكل منها رمز مرجعي مثل \u2066N-P004-1\u2069.',
             'Catalogue 1 model numbers start with the letter O (e.g. O19030-411) and catalogue 2 model numbers start with N (e.g. NF-191); search works with or without the letter. Most catalogue 2 products have no printed model number, so each has a reference code such as N-P004-1.'],
    search: ['بحث', 'Search'], ph: ['ابحث برقم الموديل \u206619030-413\u2069 أو \u2066F-191\u2069 أو الاسم', 'Search by model number (19030-413, F-191) or name'],
    empty: ['لا توجد نتائج مطابقة. جرّب رقم موديل آخر أو كلمة مختلفة.', 'No matches. Try another model number or word.'],
    viewerTitle: ['تصفّح الكتالوج صفحة بصفحة', 'Browse the catalog page by page'], prev: ['السابقة', 'Previous'], next: ['التالية', 'Next'],
    page: ['صفحة', 'Page'], all: ['الكل', 'All'], add: ['أضف إلى القائمة', 'Add to list'], inList: ['✓ في القائمة — إزالة', '✓ In list — remove'],
    added: ['أُضيف إلى قائمة الطلب', 'Added to the request list'], removed: ['أُزيل من القائمة', 'Removed from the list'],
    qty: ['الكمية', 'Quantity'], model: ['رقم الموديل', 'Model'], color: ['اللون', 'Colour'], noModel: ['بدون رقم موديل مطبوع', 'No printed model number'],
    onPage: ['منتجات هذه الصفحة:', 'Products on this page:'], openPage: ['عرض الصفحة', 'View page'], close: ['إغلاق', 'Close'],
    stat: ['%p منتج · %m موديل/لون', '%p product(s) · %m model(s)/colour(s)'], variants: ['%n موديل', '%n models'],
    lede: ['%p منتجًا و%m موديل/لون في %c قسمًا من كتالوجين: الكتالوج ١ (%a منتجًا، 111 صفحة) والكتالوج ٢ (%b منتجًا، 221 صفحة). اختر اللون/الموديل وأضفه إلى قائمة الطلب، ثم أرسلها عبر واتساب من صفحة القائمة.',
           '%p products and %m models/colours in %c categories from two catalogues: catalogue 1 (%a products, 111 pages) and catalogue 2 (%b products, 221 pages). Pick a colour/model, add it to the request list, then send it on WhatsApp from the list page.']
  };
  var lang = localStorage.getItem(LANG_KEY) === 'en' ? 'en' : 'ar';
  function t(k) { return T[k][lang === 'ar' ? 0 : 1]; }
  function L(ar, en) { return lang === 'ar' ? ar : (en || ar); }
  var $ = function (s, r) { return (r || document).querySelector(s); };
  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) { var v = attrs[k]; if (v == null || v === false) continue;
      if (k === 'text') e.textContent = v; else if (k === 'class') e.className = v; else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), v); else e.setAttribute(k, v === true ? '' : v); }
    (kids || []).forEach(function (c) { if (c != null) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }
  function pad(n) { return ('00' + n).slice(-3); }
  function norm(s) {
    return String(s || '').toLowerCase().replace(/[\u0660-\u0669]/g, function (d) { return d.charCodeAt(0) - 0x660; })
      .replace(/[\u06f0-\u06f9]/g, function (d) { return d.charCodeAt(0) - 0x6f0; })
      .replace(/[أإآ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه').replace(/[\u064b-\u0652\u0640]/g, '')
      .replace(/[×x]/g, 'x').replace(/\s+/g, ' ').trim();
  }
  function digits(s) { return String(s).replace(/[^\d?]/g, ''); }

  /* ---------- request list (shared with the main site) ---------- */
  function readStore() {
    try { var o = JSON.parse(localStorage.getItem(LIST_KEY) || 'null'); if (o && o.state && Array.isArray(o.state.items)) return o; } catch (e) {}
    return { state: { items: [] }, version: 0 };
  }
  function items() { return readStore().state.items; }
  function saveItems(arr) { var o = readStore(); o.state.items = arr; localStorage.setItem(LIST_KEY, JSON.stringify(o)); refreshCounts(); }
  function inList(id) { return items().some(function (i) { return i.id === id; }); }
  function addItem(prod, v, qty) {
    var arr = items().filter(function (i) { return i.id !== v.id; });
    var c = DATA.colors[v.color] || [v.color, v.color];
    var lab = v.label ? ' — ' + v.label : '';
    arr.push({ id: v.id, qty: qty, color: v.color, cat: {
      code: v.kind === '?' ? (L('بدون رقم', 'No code') + ' (' + L('ص', 'p.') + ' ' + prod.page + ')') : v.model,
      name: { ar: prod.ar + lab, en: prod.en + lab }, color: { ar: c[0], en: c[1] }, page: prod.page, product: prod.id, catalog: prod.c } });
    saveItems(arr);
  }
  function removeItem(id) { saveItems(items().filter(function (i) { return i.id !== id; })); }
  function setQty(id, q) { saveItems(items().map(function (i) { return i.id === id ? Object.assign({}, i, { qty: q }) : i; })); }
  function refreshCounts() {
    var n = items().length; $('#count').textContent = n; $('#fabn').textContent = n; $('#fab').hidden = n === 0;
    cards.forEach(function (c) { c.sync(); });
  }
  var toastTimer;
  function toast(msg) { var e = $('#toast'); e.textContent = msg; e.hidden = false; clearTimeout(toastTimer); toastTimer = setTimeout(function () { e.hidden = true; }, 2200); }

  /* ---------- rendering ---------- */
  var DATA, PRODUCTS = [], cards = [], catSel = 'all', query = '', catalog = 'all', CATALOG = {};
  function swatch(key) {
    var c = DATA.colors[key], h = c ? c[2] : ['#ccc'], bg;
    if (h.length === 1) bg = h[0].indexOf('gradient') >= 0 ? h[0] : h[0];
    else { var st = 100 / h.length, parts = []; h.forEach(function (x, i) { parts.push(x + ' ' + (i * st) + '% ' + ((i + 1) * st) + '%'); }); bg = 'linear-gradient(135deg,' + parts.join(',') + ')'; }
    var s = el('span', { class: 'sw', 'aria-hidden': 'true' }); s.style.background = bg; return s;
  }
  function catName(k) { for (var i = 0; i < DATA.cats.length; i++) if (DATA.cats[i][0] === k) return L(DATA.cats[i][1], DATA.cats[i][2]); return k; }
  function colorName(k) { var c = DATA.colors[k]; return c ? L(c[0], c[1]) : k; }

  function Card(p) {
    var self = this; this.p = p; this.sel = 0; this.hits = {};
    var img = el('img', { src: 'img/' + p.id + '.webp', alt: p.ar, loading: 'lazy', decoding: 'async', width: p.size[0], height: p.size[1] });
    var media = el('button', { type: 'button', class: 'media', 'aria-label': p.ar, onclick: function () { zoom(p); } }, [img, el('span', { class: 'pg', text: t('cshort' + p.c) + ' · ' + t('page') + ' ' + p.page })]);
    this.chips = p.v.map(function (v, i) {
      var b = el('button', { type: 'button', class: 'v' + (v.kind === 'r' ? ' v-r' : ''), title: (v.kind === 'r' ? v.model + ' — ' : '') + colorName(v.color) + (v.label ? ' — ' + v.label : ''), onclick: function () { self.select(i); } },
        [swatch(v.color), el('span', { text: v.kind === '?' ? '—' : v.kind === 'r' ? colorName(v.color) : v.model }), v.label ? el('small', { text: v.label }) : null]);
      return b;
    });
    this.selCode = el('span', { class: 'sel-code' }); this.selMeta = el('div', { class: 'sel-meta' }); this.selLab = el('span', { class: 'sel-meta' });
    this.selNote = el('div', { class: 'sel-meta sel-note', hidden: true });
    this.qty = el('input', { class: 'qty', inputmode: 'numeric', value: '50', 'aria-label': t('qty'),
      oninput: function () { var q = Math.min(9999, Math.max(1, parseInt(digits(self.qty.value), 10) || 1)); if (inList(self.cur().id)) setQty(self.cur().id, q); } });
    this.btn = el('button', { type: 'button', class: 'btn btn-ink', onclick: function () { self.toggle(); } });
    this.el = el('article', { class: 'card', id: p.id }, [media,
      el('p', { class: 'c-cat', text: catName(p.cat) }),
      el('h3', { class: 'c-name', text: L(p.ar, p.en) }),
      el('p', { class: 'c-sub', text: lang === 'ar' ? p.en : p.ar }),
      p.specs ? el('p', { class: 'c-spec', text: p.specs }) : null,
      p.note ? el('p', { class: 'c-note', text: p.note }) : null,
      el('div', { class: 'vars', role: 'group', 'aria-label': t('model') }, this.chips),
      el('div', { class: 'sel' }, [el('div', null, [this.selLab, this.selCode]), this.selNote, this.selMeta,
        el('div', { class: 'row' }, [this.qty, this.btn])])]);
    this.select(0, true);
  }
  Card.prototype.cur = function () { return this.p.v[this.sel]; };
  Card.prototype.select = function (i, quiet) {
    this.sel = i; var v = this.cur();
    this.chips.forEach(function (c, j) { c.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
    this.selLab.textContent = (v.kind === 'r' ? t('ref') : t('model')) + ': ';
    this.selCode.textContent = v.kind === '?' ? t('noModel') : v.model;
    this.selNote.hidden = v.kind !== 'r'; this.selNote.textContent = t('noPrinted');
    this.selMeta.textContent = t('color') + ': ' + colorName(v.color);
    if (v.label) { this.selMeta.appendChild(document.createTextNode(' · ')); this.selMeta.appendChild(el('bdi', { text: v.label })); }
    var it = items().filter(function (x) { return x.id === v.id; })[0]; if (it) this.qty.value = it.qty;
    this.sync();
  };
  Card.prototype.sync = function () {
    var self = this, ids = {}; items().forEach(function (i) { ids[i.id] = 1; });
    this.chips.forEach(function (c, j) { c.classList.toggle('in', !!ids[self.p.v[j].id]); c.classList.toggle('hit', !!self.hits[j]); });
    var on = !!ids[this.cur().id]; this.btn.textContent = on ? t('inList') : t('add'); this.btn.classList.toggle('added', on);
  };
  Card.prototype.toggle = function () {
    var v = this.cur();
    if (inList(v.id)) { removeItem(v.id); toast(t('removed')); return; }
    addItem(this.p, v, Math.min(9999, Math.max(1, parseInt(digits(this.qty.value), 10) || 50)));
    toast(t('added') + ': ' + (v.kind === '?' ? L(this.p.ar, this.p.en) : v.model));
  };

  function buildIndex(p) {
    var txt = [p.ar, p.en, p.specs, p.note, catName(p.cat)];
    DATA.cats.forEach(function (c) { if (c[0] === p.cat) txt.push(c[1], c[2]); });
    txt.push(L(T['c' + p.c][0], ''), T['c' + p.c][1]);
    p.v.forEach(function (v) { var c = DATA.colors[v.color]; if (c) txt.push(c[0], c[1]); txt.push(v.label); v.keys = codeKeys(v); txt.push(v.keys.join(' ')); });
    p.hay = norm(txt.join(' '));
    p.dig = ' ' + p.v.filter(function (v) { return v.kind === 'm'; }).map(function (v) { return digits(v.model); }).join(' ') + ' ';
  }
  /* every searchable form of a code: with / without the O or N prefix, with / without hyphens */
  function codeKeys(v) {
    if (v.kind === '?') return [];
    var m = norm(v.model), bare = m.replace(/^[on]-?/, ''), out = [m, bare, m.replace(/-/g, ''), bare.replace(/-/g, '')];
    return out.filter(function (x, i) { return x && out.indexOf(x) === i; });
  }
  function tokenize(q) {
    return norm(q).split(' ').filter(Boolean).map(function (tk) {
      tk = tk.replace(/^[on](?=[\d\u0660-\u0669])/, '');
      return { s: tk, d: /^[\d-]+$/.test(tk) && digits(tk).length >= 3 ? digits(tk) : '' };
    });
  }
  function apply(fromUser) {
    var toks = tokenize(query), shown = 0, models = 0, perCat = {};
    cards.forEach(function (c) {
      var p = c.p, ok = toks.every(function (tk) { return p.hay.indexOf(tk.s) >= 0 || (tk.d && p.dig.indexOf(tk.d) >= 0); });
      c.hits = {};
      if (ok && toks.length) p.v.forEach(function (v, j) { var d = v.kind === 'm' ? digits(v.model) : '', ks = v.keys || [];
        toks.forEach(function (tk) { if ((tk.d && d.indexOf(tk.d) >= 0) || (/\d/.test(tk.s) && ks.some(function (k) { return k.indexOf(tk.s) >= 0; }))) c.hits[j] = 1; }); });
      ok = ok && (catalog === 'all' || p.c === catalog);
      if (ok) perCat[p.cat] = (perCat[p.cat] || 0) + 1;
      var vis = ok && (catSel === 'all' || p.cat === catSel);
      c.el.hidden = !vis;
      if (vis) { shown++; models += p.v.length; var hk = Object.keys(c.hits); if (hk.length && !c.hits[c.sel]) c.select(+hk[0], true); else c.sync(); }
    });
    var total = 0; Object.keys(perCat).forEach(function (k) { total += perCat[k]; });
    document.querySelectorAll('.cat').forEach(function (b) { var k = b.dataset.k; b.querySelector('span').textContent = k === 'all' ? total : (perCat[k] || 0);
      b.hidden = k !== 'all' && catalog !== 'all' && !PRODUCTS.some(function (p) { return p.cat === k && p.c === catalog; }); });
    $('#stat').textContent = t('stat').replace('%p', shown).replace('%m', models);
    $('#empty').hidden = shown > 0;
    if (fromUser) { var u = new URL(location.href); query ? u.searchParams.set('q', query) : u.searchParams.delete('q');
      catSel !== 'all' ? u.searchParams.set('cat', catSel) : u.searchParams.delete('cat');
      catalog !== 'all' ? u.searchParams.set('c', catalog) : u.searchParams.delete('c'); history.replaceState(null, '', u.pathname + u.search + u.hash); }
  }
  function renderCatalogs() {
    var box = $('#cset'); box.textContent = '';
    ['1', '2', 'all'].forEach(function (k) {
      var n = PRODUCTS.filter(function (p) { return k === 'all' || p.c === k; }).length;
      box.appendChild(el('button', { type: 'button', class: 'cs', role: 'tab', 'data-c': k, 'aria-selected': catalog === k ? 'true' : 'false',
        onclick: function () { setCatalog(k, true); } }, [k === 'all' ? t('cAll') : t('c' + k), el('span', { text: n })]));
    });
  }
  function setCatalog(k, fromUser) {
    catalog = k;
    document.querySelectorAll('.cs').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.c === k ? 'true' : 'false'); });
    if (catSel !== 'all' && k !== 'all' && !PRODUCTS.some(function (p) { return p.cat === catSel && p.c === k; })) {
      catSel = 'all'; document.querySelectorAll('.cat').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.k === 'all' ? 'true' : 'false'); });
    }
    apply(fromUser);
    if (k !== 'all' && k !== vcat) { vcat = k; buildThumbs(); showPage(CATALOG[k].first); }
  }
  function renderCats() {
    var box = $('#cats'); box.textContent = '';
    [['all', T.all[0], T.all[1]]].concat(DATA.cats).forEach(function (c) {
      box.appendChild(el('button', { type: 'button', class: 'cat', role: 'tab', 'data-k': c[0], 'aria-selected': catSel === c[0] ? 'true' : 'false',
        onclick: function () { catSel = c[0]; document.querySelectorAll('.cat').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.k === catSel ? 'true' : 'false'); }); apply(true); } },
        [L(c[1], c[2]), el('span')]));
    });
  }

  /* ---------- zoom + page viewer ---------- */
  function zoom(p) {
    var d = el('dialog', { class: 'zoom' }, [el('img', { src: 'img/' + p.id + '.webp', alt: p.ar }),
      el('form', { method: 'dialog' }, [el('a', { href: '#pages', text: t('openPage') + ' ' + p.page + ' · ' + t('c' + p.c), onclick: function (e) { e.preventDefault(); d.close(); openPage(p.c, p.page); } }),
        el('button', { class: 'btn btn-line', text: t('close') })])]);
    d.addEventListener('close', function () { d.remove(); }); d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    document.body.appendChild(d); d.showModal();
  }
  var page = 1, thumbs = [], vcat = '1';
  function C() { return CATALOG[vcat]; }
  function pageSrc(n, kind) { return C().dir + '/' + (kind || 'p') + pad(n) + '.webp'; }
  function openPage(c, n) { if (c !== vcat) { vcat = c; buildThumbs(); } showPage(n, true); }
  function showPage(n, scroll) {
    var cc = C(); page = Math.min(cc.last, Math.max(cc.first, n | 0 || cc.first));
    var im = $('#pimg'); im.src = pageSrc(page); im.alt = t('c' + vcat) + ' — ' + t('page') + ' ' + page;
    if (vcat === '2') { im.width = 1166; im.height = 827; } else { im.width = 826; im.height = 1167; }
    $('#pno').value = page;
    thumbs.forEach(function (b) { b.setAttribute('aria-current', +b.dataset.n === page ? 'true' : 'false'); });
    var tb = thumbs[page - cc.first]; if (tb && tb.parentNode) { var box = tb.parentNode; box.scrollLeft = tb.offsetLeft - box.clientWidth / 2 + tb.clientWidth / 2; }
    var pp = $('#ponpage'); pp.textContent = '';
    var on = PRODUCTS.filter(function (p) { return p.c === vcat && p.page === page; });
    if (on.length) { pp.appendChild(el('span', { class: 'sel-meta', text: t('onPage') }));
      on.forEach(function (p) { pp.appendChild(el('a', { href: '#' + p.id, text: L(p.ar, p.en), onclick: function (e) { e.preventDefault(); focusCard(p.id); } })); }); }
    if (scroll) { history.replaceState(null, '', (vcat === '2' ? '#c2-page-' : '#page-') + page); toPages(); }
    if (page < cc.last) { var pre = new Image(); pre.src = pageSrc(page + 1); }
  }
  function toPages() {
    var go = function () { $('#pages').scrollIntoView({ block: 'start' }); };
    go(); requestAnimationFrame(go); setTimeout(go, 250); setTimeout(go, 700);
  }
  function focusCard(id) {
    query = ''; $('#q').value = ''; catSel = 'all'; document.querySelectorAll('.cat').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.k === 'all' ? 'true' : 'false'); });
    var pr = PRODUCTS.filter(function (p) { return p.id === id; })[0];
    if (pr && catalog !== 'all' && pr.c !== catalog) { catalog = 'all'; document.querySelectorAll('.cs').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.c === 'all' ? 'true' : 'false'); }); }
    apply(true); var c = document.getElementById(id); if (!c) return;
    var go = function () { c.scrollIntoView({ block: 'start' }); }; go(); setTimeout(go, 250); c.classList.add('flash'); setTimeout(function () { c.classList.remove('flash'); }, 1800);
  }
  function buildThumbs() {
    var box = $('#thumbs'), cc = C(), land = vcat === '2'; box.textContent = ''; thumbs = [];
    $('#viewer').classList.toggle('land', land);
    $('#ptot').textContent = land ? '\u2066(' + cc.first + '–' + cc.last + ')\u2069' : '/ ' + cc.last;
    $('#v2note').hidden = !land;
    document.querySelectorAll('.vc').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.c === vcat ? 'true' : 'false'); });
    for (var i = cc.first; i <= cc.last; i++) (function (n) {
      var b = el('button', { type: 'button', 'data-n': n, 'aria-label': t('page') + ' ' + n, onclick: function () { showPage(n); } },
        [el('img', { src: pageSrc(n, 't'), alt: '', loading: 'lazy', decoding: 'async', width: land ? 130 : 92, height: land ? 92 : 130 }), el('span', { text: n })]);
      thumbs.push(b); box.appendChild(b);
    })(i);
  }
  function buildViewer() {
    var vb = $('#vcats'); vb.textContent = '';
    ['1', '2'].forEach(function (k) { vb.appendChild(el('button', { type: 'button', class: 'vc', 'data-c': k, 'aria-pressed': 'false',
      onclick: function () { if (vcat !== k) { vcat = k; buildThumbs(); showPage(CATALOG[k].first); } } }, [t('c' + k)])); });
    buildThumbs();
    $('#prev').onclick = function () { showPage(page - 1); }; $('#next').onclick = function () { showPage(page + 1); };
    $('#pno').onchange = function () { showPage(parseInt(digits(this.value), 10)); };
    var x0 = null, im = $('#pimg');
    im.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    im.addEventListener('touchend', function (e) { if (x0 == null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) showPage(page + ((dx < 0) === (document.dir === 'rtl') ? -1 : 1)); });
    document.addEventListener('keydown', function (e) { if (/INPUT|TEXTAREA/.test(document.activeElement.tagName) || document.querySelector('dialog[open]')) return;
      var r = $('#pages').getBoundingClientRect(); if (r.top > innerHeight || r.bottom < 0) return;
      if (e.key === 'ArrowLeft') showPage(page + (document.dir === 'rtl' ? 1 : -1)); if (e.key === 'ArrowRight') showPage(page + (document.dir === 'rtl' ? -1 : 1)); });
  }

  /* ---------- i18n ---------- */
  function applyLang() {
    document.documentElement.lang = lang; document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-t]').forEach(function (e) { e.textContent = t(e.dataset.t); });
    document.querySelectorAll('[data-ta]').forEach(function (e) { e.setAttribute('aria-label', t(e.dataset.ta)); });
    $('#lang').textContent = lang === 'ar' ? 'EN' : 'ع'; $('#q').placeholder = t('ph');
    document.title = t('title') + ' — BoxTech gifts';
    if (DATA) {
      var nm = PRODUCTS.reduce(function (a, p) { return a + p.v.length; }, 0);
      var n1 = PRODUCTS.filter(function (p) { return p.c === '1'; }).length;
      $('#lede').textContent = t('lede').replace('%p', PRODUCTS.length).replace('%m', nm).replace('%c', DATA.cats.length).replace('%a', n1).replace('%b', PRODUCTS.length - n1);
      ['1', '2'].forEach(function (k) { var c = CATALOG[k]; if (!c) return; var a = $('#pdf' + k); a.href = c.pdf; $('#pdfsize' + k).textContent = '(' + (c.bytes / 1048576).toFixed(1) + ' MB)'; });
      document.querySelectorAll('.vc').forEach(function (b) { b.textContent = t('c' + b.dataset.c); });
    }
  }
  $('#lang').onclick = function () {
    lang = lang === 'ar' ? 'en' : 'ar'; localStorage.setItem(LANG_KEY, lang); applyLang();
    var g = $('#grid'); g.textContent = ''; cards = PRODUCTS.map(function (p) { var c = new Card(p); g.appendChild(c.el); return c; });
    PRODUCTS.forEach(buildIndex); renderCatalogs(); renderCats(); apply(false); buildThumbs(); showPage(page);
  };

  /* ---------- boot ---------- */
  applyLang();
  fetch('data.json?v=' + (document.querySelector('script[src^="app.js"]').src.split('v=')[1] || ''), { credentials: 'same-origin' })
    .then(function (r) { return r.json(); }).then(function (d) {
      DATA = d;
      (d.catalogs || []).forEach(function (c) { CATALOG[c[0]] = { key: c[0], ar: c[1], en: c[2], first: c[3], last: c[4], dir: c[5], pdf: c[6], bytes: c[7], prefix: c[8] }; });
      PRODUCTS = d.items.map(function (a) { return { id: a[0], page: a[1], cat: a[2], ar: a[3], en: a[4], specs: a[5], size: a[6],
        v: a[7].map(function (v) { return { id: v[0], model: v[1], color: v[2], label: v[3], kind: v[4] || (v[1].indexOf('?') >= 0 ? '?' : 'm') }; }), note: a[8], c: a[9] || '1' }; });
      PRODUCTS.forEach(buildIndex);
      var sp = new URLSearchParams(location.search); query = sp.get('q') || ''; var c0 = sp.get('cat'), k0 = sp.get('c');
      if (k0 === '1' || k0 === '2') { catalog = k0; vcat = k0; }
      if (c0 && d.cats.some(function (c) { return c[0] === c0; })) catSel = c0;
      $('#q').value = query;
      var g = $('#grid'), frag = document.createDocumentFragment();
      cards = PRODUCTS.map(function (p) { var c = new Card(p); frag.appendChild(c.el); return c; }); g.appendChild(frag);
      var h = location.hash, m = /^#(c2-)?page-(\d+)$/.exec(h);
      if (m) vcat = m[1] ? '2' : '1';
      renderCatalogs(); renderCats(); applyLang(); apply(false); buildViewer();
      showPage(m ? +m[2] : C().first, !!m);
      if (/^#[pn]\d{3}-\d+$/.test(h)) setTimeout(function () { focusCard(h.slice(1)); }, 50);
      refreshCounts();
      var tmr; $('#q').addEventListener('input', function () { clearTimeout(tmr); var v = this.value; tmr = setTimeout(function () { query = v; apply(true); }, 120); });
      $('#q').addEventListener('keydown', function (e) { if (e.key === 'Enter') { query = this.value; apply(true); $('#products').scrollIntoView(); } });
      document.querySelectorAll('a[href="#pages"]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); history.replaceState(null, '', (vcat === '2' ? '#c2-page-' : '#page-') + page); toPages(); }); });
      window.addEventListener('storage', function (e) { if (e.key === LIST_KEY) refreshCounts(); });
      document.documentElement.dataset.ready = '1';
    }).catch(function (e) { $('#stat').textContent = 'Error: ' + e.message; });
})();
