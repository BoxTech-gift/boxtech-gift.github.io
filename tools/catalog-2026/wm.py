"""BoxTech gifts watermark: the site's logo (brand/watermark.png, rendered from the header mark + wordmark)
placed in the calmest corner of an image (~15% of its width, slight transparency), so it does not cover
products or model numbers. Always applied to clean source pixels (never to an already-watermarked image)."""
import os
from PIL import Image, ImageFilter, ImageChops, ImageStat
HERE = os.path.dirname(os.path.abspath(__file__))
_LOGO = None
def logo():
    global _LOGO
    if _LOGO is None: _LOGO = Image.open(os.path.join(HERE, 'brand', 'watermark.png')).convert('RGBA')
    return _LOGO
def apply(im, frac=0.15, min_w=96, max_w=230, opacity=0.88, corners=('bl', 'br', 'tl', 'tr'), force=None):
    im = im.convert('RGB'); W, H = im.size
    lw = int(max(min_w, min(max_w, W * frac))); lw = min(lw, int(W * 0.4))
    L = logo(); lh = round(L.height * lw / L.width)
    mk = L.resize((lw, lh), Image.LANCZOS)
    if opacity < 1:
        a = mk.getchannel('A').point(lambda v: int(v * opacity)); mk.putalpha(a)
    m = max(6, round(min(W, H) * 0.025))
    pos = {'bl': (m, H - lh - m), 'br': (W - lw - m, H - lh - m), 'tl': (m, m), 'tr': (W - lw - m, m)}
    if force: best = force
    else:
        g = im.convert('L').filter(ImageFilter.FIND_EDGES)
        def busy(c):
            x, y = pos[c]; pad = m // 2
            box = (max(0, x - pad), max(0, y - pad), min(W, x + lw + pad), min(H, y + lh + pad))
            return ImageStat.Stat(g.crop(box)).mean[0]
        scores = [(busy(c) + i * 0.4, c) for i, c in enumerate(corners)]  # slight preference for the order given
        best = min(scores)[1]
    out = im.copy(); out.paste(mk, pos[best], mk)
    return out
