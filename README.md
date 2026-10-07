# BoxTech gifts — كتالوج ٢٠٢٦ (static GitHub Pages build)

Arabic-first (RTL, with an English toggle) catalog of corporate & welcome gifts, published as a
**client-only SPA** on GitHub Pages.

**Live:** https://boxtech-gift.github.io/

- Routes: `/`, `/list` (request list), `/collection/:slug` (10 collections), `/product/:id` (34 products).
- **`/catalog-2026/`** — the full printed gifts catalog 2026 (static page, vanilla JS): 265 products,
  996 model/colour variants in 18 categories, model-number search, colour chips, page-by-page viewer
  (111 WebP pages) and the PDF download. Every catalog model number carries the prefix **O**
  (`O19030-411` = printed code `19030-411`); search works with or without the O.
- Catalog items are added to the same request list (`localStorage` key `boxtech-gifts-list`), so they show up
  on `/list` and in the quote form with their O-model numbers in the WhatsApp / copy / print text.
- Model-number data: [`/catalog-data/models.csv`](catalog-data/models.csv) and
  [`/catalog-data/models.json`](catalog-data/models.json).
- No login, no server: requests are sent via WhatsApp (`wa.me`), copy-to-clipboard, or print.
- `index.html`, `404.html` and every route folder contain the same SPA shell; `404.html` is the deep-link fallback.
- Images are WebP (q80–82, visually lossless); `og.jpg` stays an optimised JPEG for link previews.

## Rebuild
```sh
OUT=. python3 tools/build.py / https://boxtech-gift.github.io
```
`tools/build.py` regenerates the tree from the original app build (`$SRC`) and the catalog export (`$CATALOG_SRC`).
The catalog sources are in `tools/catalog-2026/`: `data.py` (transcription of every product, model and colour),
`export.py` (writes models.json/csv, WebP crops/pages, data.json) and `web/` (the `/catalog-2026/` page).
