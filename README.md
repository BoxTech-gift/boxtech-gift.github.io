# BoxTech gifts — كتالوج ٢٠٢٦ (static GitHub Pages build)

Arabic-first (RTL, with an English toggle) catalog of corporate & welcome gifts, published as a
**client-only SPA** on GitHub Pages.

**Live:** https://boxtech-gift.github.io/

- Routes: `/`, `/list` (request list), `/collection/:slug` (10 collections), `/product/:id` (34 products).
- **`/catalog-2026/`** — both printed gift catalogues on one static page (vanilla JS): 405 products and
  1,435 model/colour variants in 24 categories, with a catalogue switcher (الكتالوج ١ / الكتالوج ٢ / الكل),
  model-number and name search, colour chips, a page-by-page viewer per catalogue and both PDF downloads.
  - **Catalogue 1** (111 pages): 265 products, 996 variants; every model number carries the prefix **O**
    (`O19030-411` = printed code `19030-411`).
  - **Catalogue 2** (221 pages: the original 223-page PDF without its first and last page): 140 products,
    439 variants. Its two printed model numbers carry the prefix **N** (`NF-191`, `NP207`); the catalogue prints no
    model number for the other products, so each of their variants has a reference code `N-P<page>-<k>[-<colour #>]`
    (e.g. `N-P004-1-3`). Page numbers are the printed ones (2–222); trimmed-PDF page = page − 1.
  - Search works with or without the O / N prefix (and with or without hyphens).
  - Every product photo and page image carries the BoxTech gifts watermark (`tools/catalog-2026/wm.py`).
- Catalog items are added to the same request list (`localStorage` key `boxtech-gifts-list`), so they show up
  on `/list` and in the quote form with their model / reference codes in the WhatsApp / copy / print text.
- Model-number data: [`/catalog-data/models.csv`](catalog-data/models.csv) and
  [`/catalog-data/models.json`](catalog-data/models.json) (`catalog`, `model` and `ref` columns).
- No login, no server: requests are sent via WhatsApp (`wa.me`), copy-to-clipboard, or print.
- `index.html`, `404.html` and every route folder contain the same SPA shell; `404.html` is the deep-link fallback.
- Images are WebP (q80–82, visually lossless); `og.jpg` stays an optimised JPEG for link previews.

## Rebuild
```sh
OUT=. python3 tools/build.py / https://boxtech-gift.github.io
```
`tools/build.py` regenerates the tree from the original app build (`$SRC`) and the catalog export (`$CATALOG_SRC`).
The catalog sources are in `tools/catalog-2026/`: `data.py` / `data2.py` (transcription of every product, model and
colour of catalogue 1 / 2), `export.py` (writes models.json/csv, watermarked WebP crops/pages, data.json and the PDFs;
catalogue 2 is rendered from its PDF with `pdftoppm` and trimmed with `qpdf --pages . 2-222`), `wm.py` + `brand/`
(the watermark) and `web/` (the `/catalog-2026/` page). Re-export with `FORCE=1 python3 export.py`.
