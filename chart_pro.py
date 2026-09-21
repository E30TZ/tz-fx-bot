# -*- coding: utf-8 -*-
"""TZ FX white desk chart — high-res TrueType. Exclusive ICT 2022."""
from __future__ import print_function

import io
import math
import os
import ssl

try:
    from urllib.request import Request, urlopen
except Exception:
    from urllib2 import Request, urlopen

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 2560, 1600
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
LOGO_DIR = os.path.join(HERE, "logos")
_logo_mem = {}

PAPER = (242, 238, 230)
INK = (18, 17, 16)
MUTED = (92, 86, 76)
DIM = (156, 148, 136)
HAIR = (226, 218, 204)
GRID = (232, 226, 214)
GOLD = (168, 128, 46)
GOLD2 = (196, 158, 78)
TEAL = (14, 132, 88)
TEAL_DK = (10, 104, 70)
ROSE = (186, 44, 48)
ROSE_DK = (148, 30, 36)
BLUE = (36, 96, 186)
ORANGE = (196, 118, 32)
PURPLE = (118, 78, 176)
IVORY = (255, 252, 246)
SHEET = (255, 253, 248)
LINE = (214, 204, 186)


def _font(name, size):
    path = os.path.join(FONTS, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _tw(draw, s, font):
    b = draw.textbbox((0, 0), s, font=font)
    return b[2] - b[0], b[3] - b[1]


def _round(draw, xy, r, fill=None, outline=None, width=1):
    try:
        draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)
    except Exception:
        draw.rectangle(xy, fill=fill, outline=outline, width=width)


def _dash_h(draw, y, x0, x1, color, on=10, off=7, width=2):
    y = int(round(y))
    x = int(x0)
    x1 = int(x1)
    while x < x1:
        draw.line([(x, y), (min(x + on, x1), y)], fill=color, width=width)
        x += on + off


def _pair_meta(pair):
    names = {
        "XAUUSD": ("Gold", "XAU / USD"),
        "EURUSD": ("Euro", "EUR / USD"),
        "GBPUSD": ("Sterling", "GBP / USD"),
        "BTCUSDT": ("Bitcoin", "BTC / USDT"),
        "ETHUSDT": ("Ethereum", "ETH / USDT"),
        "SOLUSDT": ("Solana", "SOL / USDT"),
        "BNBUSDT": ("BNB", "BNB / USDT"),
        "XRPUSDT": ("XRP", "XRP / USDT"),
        "DOGEUSDT": ("Dogecoin", "DOGE / USDT"),
        "ADAUSDT": ("Cardano", "ADA / USDT"),
        "TONUSDT": ("Toncoin", "TON / USDT"),
        "ARBUSDT": ("Arbitrum", "ARB / USDT"),
        "PEPEUSDT": ("Pepe", "PEPE / USDT"),
        "LINKUSDT": ("Chainlink", "LINK / USDT"),
        "AVAXUSDT": ("Avalanche", "AVAX / USDT"),
    }
    if pair in names:
        return names[pair]
    p = (pair or "").upper()
    if p.endswith("USDT"):
        base = p[:-4]
        return (base, base + " / USDT")
    return (p or "FX", p or "FX")


def _logo_code(pair):
    p = (pair or "").upper()
    if p == "XAUUSD":
        return "gold"
    if p == "EURUSD":
        return "eur"
    if p == "GBPUSD":
        return "gbp"
    if p.endswith("USDT"):
        b = p[:-4]
        if b.startswith("1000"):
            b = b[4:]
        return b.lower()
    return (p or "fx").lower()


def _logo_urls(pair):
    code = _logo_code(pair)
    urls = []
    flags = {"eur": "eu", "gbp": "gb", "usd": "us"}
    if code in flags:
        urls.append("https://flagcdn.com/w160/%s.png" % flags[code])
    if code == "gold":
        urls.append(
            "https://cdn.jsdelivr.net/gh/spothq/cryptocurrency-icons@master/128/color/gold.png"
        )
    urls.append(
        "https://cdn.jsdelivr.net/gh/spothq/cryptocurrency-icons@master/128/color/%s.png"
        % code
    )
    urls.append("https://assets.coincap.io/assets/icons/%s@2x.png" % code)
    urls.append(
        "https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/128/color/%s.png"
        % code
    )
    return urls


def _http_png(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 TZFX", "Accept": "image/png,image/*"})
    ctx = ssl._create_unverified_context()
    r = urlopen(req, timeout=8, context=ctx)
    data = r.read()
    if not data or len(data) < 200:
        return None
    im = Image.open(io.BytesIO(data))
    im.load()
    return im.convert("RGBA")


def _load_logo(pair):
    code = _logo_code(pair) or "fx"
    if code in _logo_mem:
        return _logo_mem[code]
    try:
        if not os.path.isdir(LOGO_DIR):
            os.makedirs(LOGO_DIR)
    except Exception:
        pass
    cache = os.path.join(LOGO_DIR, code + ".png")
    im = None
    if os.path.isfile(cache) and os.path.getsize(cache) > 200:
        try:
            im = Image.open(cache).convert("RGBA")
            im.load()
        except Exception:
            im = None
    if im is None:
        for url in _logo_urls(pair):
            try:
                im = _http_png(url)
                if im is not None:
                    try:
                        im.save(cache, format="PNG")
                    except Exception:
                        pass
                    break
            except Exception:
                im = None
    _logo_mem[code] = im
    return im


def _resample():
    return getattr(Image, "LANCZOS", getattr(Image, "ANTIALIAS", 1))


def _circle_logo(src, size, ring=None):
    size = int(size)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    if src is None:
        return canvas
    im = src.convert("RGBA")
    im.thumbnail((size - 4, size - 4), _resample())
    cx = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ox = (size - im.size[0]) // 2
    oy = (size - im.size[1]) // 2
    cx.paste(im, (ox, oy), im)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    pad = 2
    md.ellipse((pad, pad, size - 1 - pad, size - 1 - pad), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(cx, (0, 0))
    out.putalpha(mask)
    if ring:
        d = ImageDraw.Draw(out)
        d.ellipse((1, 1, size - 2, size - 2), outline=ring + (240,), width=max(3, size // 26))
        d.ellipse((4, 4, size - 5, size - 5), outline=IVORY + (90,), width=1)
    return out


def _comma(s):
    s = str(s)
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if "." in s:
        a, b = s.split(".", 1)
    else:
        a, b = s, None
    out = ""
    while len(a) > 3:
        out = "," + a[-3:] + out
        a = a[:-3]
    a = a + out
    if b is None:
        return ("-" if neg else "") + a
    return ("-" if neg else "") + a + "." + b


def _fmt(pair, p, fmt_px):
    try:
        s = fmt_px(pair, p)
    except Exception:
        s = ("%.2f" if pair == "XAUUSD" else "%.5f") % float(p)
    try:
        if abs(float(p)) >= 1000:
            return _comma(s)
    except Exception:
        pass
    return s


def _nice_ticks(lo, hi, n=7):
    span = float(hi) - float(lo)
    if span <= 0:
        return [lo], span or 1.0
    raw = span / float(max(3, n))
    mag = 10 ** int(math.floor(math.log10(raw))) if raw > 0 else 1.0
    step = mag
    for m in (1.0, 2.0, 2.5, 5.0, 10.0):
        if m * mag >= raw * 0.82:
            step = m * mag
            break
    start = math.floor(lo / step) * step
    ticks = []
    for i in range(0, 48):
        v = start + i * step
        if v < lo - step * 0.02:
            continue
        if v > hi + step * 0.02:
            break
        ticks.append(v)
    if not ticks:
        ticks = [lo, hi]
    return ticks, step


def _spread(ys, box_h, y0, y1, gap):
    n = len(ys)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: ys[i])
    pos = [float(y) for y in ys]
    for k, i in enumerate(order):
        y = pos[i]
        if k:
            prev = pos[order[k - 1]]
            if y < prev + gap:
                y = prev + gap
        pos[i] = y
    last = pos[order[-1]]
    if last > y1 - box_h * 0.5:
        shift = last - (y1 - box_h * 0.5)
        for i in range(n):
            pos[i] -= shift
    first = pos[order[0]]
    if first < y0 + box_h * 0.5:
        shift = (y0 + box_h * 0.5) - first
        for i in range(n):
            pos[i] += shift
    if pos[order[-1]] > y1 - box_h * 0.5 and n > 1:
        span = (y1 - y0) - box_h
        step = span / float(n - 1) if n > 1 else 0
        for k, i in enumerate(order):
            pos[i] = y0 + box_h * 0.5 + k * step
    return pos


def _session_name(raw):
    s = str(raw or "")
    if u"لندن" in s:
        return "LONDON"
    if u"نیویورک" in s:
        return "NEW YORK"
    return None


def _kz_name(raw):
    return _session_name(raw)


def _pct(vals, p):
    if not vals:
        return 0.0
    s = sorted(vals)
    i = int(round((len(s) - 1) * p))
    i = max(0, min(len(s) - 1, i))
    return float(s[i])


def _smart_range(rows, extras):
    highs = [float(r["h"]) for r in rows]
    lows = [float(r["l"]) for r in rows]
    closes = [float(r["c"]) for r in rows]
    n = len(rows)
    lo = _pct(lows, 0.07)
    hi = _pct(highs, 0.93)
    rec = rows[-18:] if n > 18 else rows
    lo = min(lo, min(float(r["l"]) for r in rec))
    hi = max(hi, max(float(r["h"]) for r in rec))
    lo = min(lo, closes[-1])
    hi = max(hi, closes[-1])
    for v in extras:
        try:
            lo = min(lo, float(v))
            hi = max(hi, float(v))
        except Exception:
            pass
    pad = (hi - lo) * 0.09 or 1.0
    return lo - pad, hi + pad


def _vignette(im):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = im.size
    for i, a in enumerate((18, 12, 7, 3)):
        d.rectangle((i, i, w - 1 - i, h - 1 - i), outline=(70, 52, 20, a))
    return Image.alpha_composite(im, layer)


def _band(im, box, rgb, a_top, a_bot):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    w = max(1, x1 - x0)
    h = max(1, y1 - y0)
    g = Image.new("RGBA", (1, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for y in range(h):
        t = y / float(max(1, h - 1))
        a = int(a_top + (a_bot - a_top) * t)
        gd.point((0, y), fill=rgb + (a,))
    g = g.resize((w, h), Image.NEAREST)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    layer.paste(g, (x0, y0), g)
    return Image.alpha_composite(im, layer)


def _glow(im, xy, rgb, radius=14, alpha=70):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(xy, fill=rgb + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius))
    return Image.alpha_composite(im, layer)


def _spread_text(d, x, y, text, font, fill, tracking=3):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += _tw(d, ch, font)[0] + tracking
    return x


def _chip(d, x1, y, text, font, fg, bg, ol, live=False):
    tw, th = _tw(d, text, font)
    extra = 22 if live else 0
    pad_x = 16
    h = th + 18
    x0 = x1 - tw - pad_x * 2 - extra
    _round(d, (x0, y, x1, y + h), 16, fill=bg, outline=ol, width=1)
    if live:
        d.ellipse((x0 + 14, y + h // 2 - 5, x0 + 24, y + h // 2 + 5), fill=(255, 255, 255))
        d.text((x0 + 32, y + 8), text, font=font, fill=fg)
    else:
        d.text((x0 + pad_x, y + 8), text, font=font, fill=fg)
    return x0 - 10


def render(rows, pair, sig=None, label="15m", fmt_px=None, tehran_fmt=None, in_killzone=None, fonts=None):
    global FONTS
    if fonts:
        FONTS = fonts
    if fmt_px is None:

        def fmt_px(p, x):
            return ("%.2f" if p == "XAUUSD" else "%.5f") % float(x)

    if tehran_fmt is None:
        import time as _t

        def tehran_fmt(ts=None, fmt="%H:%M"):
            st = _t.gmtime((_t.time() if ts is None else ts) + 12600)
            if fmt == "latin":
                return _t.strftime("%Y/%m/%d %H:%M", st)
            return _t.strftime(fmt if "%" in str(fmt) else "%H:%M", st)

    if in_killzone is None:

        def in_killzone(ts):
            try:
                import time as _t

                hour = _t.gmtime(int(ts)).tm_hour
            except Exception:
                return None
            if 7 <= hour < 10:
                return u"لندن"
            if 12 <= hour < 16:
                return u"نیویورک"
            return None

    rows = [r for r in (rows or []) if r and "c" in r]
    if len(rows) < 5:
        im = Image.new("RGB", (W, H), PAPER)
        d = ImageDraw.Draw(im)
        d.text((80, 80), "No market data", font=_font("Inter-Medium.ttf", 42), fill=MUTED)
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True)
        return buf.getvalue()

    rows = rows[-128:]
    n = len(rows)
    last = float(rows[-1]["c"])
    first = float(rows[0]["c"])
    chg = ((last - first) / first * 100.0) if first else 0.0
    delta = last - first
    side = (sig or {}).get("side") or ""
    sc = (sig or {}).get("score")
    if side == "SELL":
        accent = ROSE
        smark = "SELL"
        live = True
    elif side == "BUY":
        accent = TEAL
        smark = "BUY"
        live = True
    else:
        accent = TEAL if last >= first else ROSE
        smark = "WAIT"
        live = False

    name, ticker = _pair_meta(pair)
    quote = "USDT" if str(pair or "").upper().endswith("USDT") else "USD"

    levels = []
    extras = []
    if sig:
        for key, col, nm in (("tp", TEAL, "TP"), ("sl", ROSE, "SL")):
            if sig.get(key) is None:
                continue
            try:
                pv = float(sig[key])
            except Exception:
                continue
            levels.append({"pv": pv, "col": col, "nm": nm, "px": _fmt(pair, pv, fmt_px), "solid": True})
            extras.append(pv)

    lo, hi = _smart_range(rows, extras)
    span = hi - lo or 1.0

    im = Image.new("RGB", (W, H), PAPER).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")

    f_kicker = _font("Inter-Medium.ttf", 20)
    f_brand = _font("Inter-SemiBold.ttf", 26)
    f_name = _font("Outfit-Bold.ttf", 78)
    f_price = _font("Outfit-Bold.ttf", 108)
    f_quote = _font("Inter-SemiBold.ttf", 22)
    f_sub = _font("Inter-Medium.ttf", 22)
    f_small = _font("Inter-Regular.ttf", 20)
    f_tiny = _font("Inter-Medium.ttf", 19)
    f_micro = _font("Inter-SemiBold.ttf", 16)
    f_mono = _font("JetBrainsMono-Medium.ttf", 22)
    f_mono_sm = _font("JetBrainsMono-Regular.ttf", 18)
    f_logo = _font("Outfit-Bold.ttf", 28)
    f_pill = _font("Inter-SemiBold.ttf", 20)
    f_pill_sm = _font("Inter-SemiBold.ttf", 17)
    f_ohlc_k = _font("Inter-SemiBold.ttf", 16)
    f_track = _font("Inter-SemiBold.ttf", 14)

    # paper frame — hairline only, no cheap gold spine
    d.rectangle((0, 0, W - 1, H - 1), outline=GOLD + (80,), width=2)
    d.rectangle((8, 8, W - 9, H - 9), outline=GOLD + (28,), width=1)

    # logo
    logo_raw = _load_logo(pair)
    mark = _circle_logo(logo_raw, 88, ring=GOLD)
    lx, ly = 44, 34
    im = _glow(im, (lx - 8, ly - 8, lx + 96, ly + 96), GOLD, 16, 40)
    d = ImageDraw.Draw(im, "RGBA")
    if logo_raw is None:
        _round(d, (lx, ly, lx + 88, ly + 88), 44, fill=GOLD)
        initials = (ticker.split()[0] if ticker else "FX")[:4]
        tw, th = _tw(d, initials, f_logo)
        d.text((lx + (88 - tw) / 2, ly + (88 - th) / 2 - 4), initials, font=f_logo, fill=IVORY)
    else:
        im.paste(mark, (lx, ly), mark)
        d = ImageDraw.Draw(im, "RGBA")
    d.text((148, 46), ticker, font=f_brand, fill=INK)
    d.text((148, 82), "TZ DESK  ·  ICT 2022", font=f_kicker, fill=MUTED)

    try:
        raw_now = in_killzone(int(rows[-1]["t"])) or ""
    except Exception:
        raw_now = ""
    sess = _session_name(raw_now) or "OFF SESSION"
    cx = W - 48
    cy = 44
    sess_fg = GOLD if sess != "OFF SESSION" else MUTED
    sess_ol = GOLD if sess != "OFF SESSION" else HAIR
    cx = _chip(d, cx, cy, sess, f_micro, sess_fg, SHEET, sess_ol, False)
    if live:
        cx = _chip(d, cx, cy, smark, f_micro, (255, 255, 255), accent, accent, True)
    else:
        cx = _chip(d, cx, cy, smark, f_micro, MUTED, SHEET, HAIR, False)
    _chip(d, cx, cy, str(label).upper(), f_micro, INK, SHEET, HAIR, False)

    # name + price
    d.text((44, 132), name, font=f_name, fill=INK)
    last_s = _fmt(pair, last, fmt_px)
    pw, ph = _tw(d, last_s, f_price)
    d.text((W - 48 - pw, 118), last_s, font=f_price, fill=INK)
    qw, qh = _tw(d, quote, f_quote)
    d.text((W - 48 - pw - qw - 16, 168), quote, font=f_quote, fill=MUTED)
    # gold underline under price
    d.line([(W - 48 - pw, 232), (W - 48, 232)], fill=GOLD + (120,), width=2)

    # OHLC tape
    lb = rows[-1]
    rng_v = float(lb["h"]) - float(lb["l"])
    tape = [
        ("O", _fmt(pair, lb["o"], fmt_px), MUTED),
        ("H", _fmt(pair, lb["h"], fmt_px), TEAL),
        ("L", _fmt(pair, lb["l"], fmt_px), ROSE),
        ("C", _fmt(pair, lb["c"], fmt_px), INK),
        ("RNG", _fmt(pair, rng_v, fmt_px), MUTED),
    ]
    tx = 48
    ty = 222
    for k, v, col in tape:
        kw, kh = _tw(d, k, f_ohlc_k)
        d.text((tx, ty), k, font=f_ohlc_k, fill=DIM)
        d.text((tx + kw + 8, ty - 2), v, font=f_mono, fill=col)
        vw, vh = _tw(d, v, f_mono)
        tx = tx + kw + 8 + vw + 36
        d.line([(tx - 18, ty - 2), (tx - 18, ty + 22)], fill=HAIR, width=1)

    chg_s = "%s%.2f%%" % ("+" if chg >= 0 else "", chg)
    dlt_s = "%s%s" % ("+" if delta >= 0 else "", _fmt(pair, delta, fmt_px))
    cw, chh = _tw(d, chg_s, f_pill)
    dw, dh = _tw(d, dlt_s, f_pill)
    _round(d, (W - 48 - cw - 32, 236, W - 48, 236 + chh + 18), 13, fill=accent)
    d.text((W - 48 - cw - 16, 244), chg_s, font=f_pill, fill=(255, 255, 255))
    _round(
        d,
        (W - 48 - cw - 32 - dw - 44, 236, W - 48 - cw - 40, 236 + dh + 18),
        13,
        outline=HAIR,
        width=1,
    )
    d.text((W - 48 - cw - 32 - dw - 28, 244), dlt_s, font=f_pill, fill=accent)

    head_bottom = 272
    RAIL = 176 if levels else 136
    card = (32, head_bottom, W - 32, H - 64)
    # card shadow
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    _round(sd, (card[0] + 10, card[1] + 14, card[2] + 10, card[3] + 16), 28, fill=(40, 28, 12, 28))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    im = Image.alpha_composite(im, sh)
    d = ImageDraw.Draw(im, "RGBA")
    _round(d, card, 28, fill=SHEET)
    _round(d, card, 28, outline=HAIR, width=1)
    # studio highlight on card top
    d.line([(card[0] + 28, card[1] + 2), (card[2] - 28, card[1] + 2)], fill=(255, 255, 255, 180), width=2)

    pl, pt = 56, card[1] + 36
    pr, pb = W - 32 - 18 - RAIL, card[3] - 52

    def yp(p):
        return pt + (hi - float(p)) / span * (pb - pt)

    ticks, step = _nice_ticks(lo, hi, 12)
    for i, p in enumerate(ticks):
        y = yp(p)
        if y < pt + 2 or y > pb - 2:
            continue
        d.line([(pl, int(y)), (pr, int(y))], fill=GRID, width=1)
        ax = _fmt(pair, p, fmt_px)
        d.text((pr + 16, int(y) - 10), ax, font=f_mono_sm, fill=DIM)
    d.line([(pr, pt), (pr, pb)], fill=LINE, width=1)
    d.line([(pl, pb), (pr, pb)], fill=LINE, width=1)

    # watermark — lower left, quiet
    if logo_raw is not None:
        wm_size = 240
        wm = _circle_logo(logo_raw, wm_size)
        alpha = wm.split()[-1].point(lambda a: int(a * 0.14))
        wm.putalpha(alpha)
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        layer.paste(wm, (int(pl + 24), int(pb - wm_size - 18)), wm)
        im = Image.alpha_composite(im, layer)
        d = ImageDraw.Draw(im, "RGBA")

    # killzone washes
    slot = float(pr - pl) / n
    runs = []
    cur = None
    for i, r in enumerate(rows):
        try:
            kz = _kz_name(in_killzone(int(r["t"])))
        except Exception:
            kz = None
        if kz:
            if cur and cur[0] == kz:
                cur[2] = i
            else:
                if cur:
                    runs.append(cur)
                cur = [kz, i, i]
        else:
            if cur:
                runs.append(cur)
                cur = None
    if cur:
        runs.append(cur)
    for kz, a, b in runs:
        x0 = pl + a * slot
        x1 = pl + (b + 1) * slot
        if kz == "LONDON":
            im = _band(im, (x0, pt, x1, pb), (168, 128, 46), 38, 10)
            lab_col = GOLD + (150,)
        else:
            im = _band(im, (x0, pt, x1, pb), (36, 96, 186), 32, 8)
            lab_col = BLUE + (140,)
        d = ImageDraw.Draw(im, "RGBA")
        if (b - a) >= 5:
            _spread_text(d, x0 + 12, pt + 10, kz, f_track, lab_col, 4)
            d.line([(x0, pt), (x1, pt)], fill=lab_col, width=3)

    # ICT levels behind candles
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for lv in levels:
        y = yp(lv["pv"])
        if y < pt or y > pb:
            continue
        col = lv["col"] + (160,)
        if lv["solid"]:
            ld.line([(pl, int(y)), (pr, int(y))], fill=col, width=2)
        else:
            _dash_h(ld, y, pl, pr, col, 8, 7, 2)
    im = Image.alpha_composite(im, layer)
    d = ImageDraw.Draw(im, "RGBA")

    # EMA 20 silk
    if n >= 20:
        closes = [float(r["c"]) for r in rows]
        k = 2.0 / 21.0
        ema = [closes[0]]
        for v in closes[1:]:
            ema.append(v * k + ema[-1] * (1.0 - k))
        epts = [(pl + i * slot + slot * 0.5, yp(v)) for i, v in enumerate(ema)]
        epts = [(x, y) for x, y in epts if pt <= y <= pb]
        if len(epts) >= 2:
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.line(epts, fill=GOLD + (110,), width=2)
            im = Image.alpha_composite(im, layer)
            d = ImageDraw.Draw(im, "RGBA")

    # last-price band
    yl = yp(last)
    if pt <= yl <= pb:
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rectangle((pl, int(yl) - 7, pr, int(yl) + 7), fill=accent + (18,))
        im = Image.alpha_composite(im, layer)
        d = ImageDraw.Draw(im, "RGBA")
        _dash_h(d, yl, pl, pr, accent + (200,), 12, 7, 2)

    # candles
    body_w = max(7, int(round(slot * 0.64)))
    if body_w % 2 == 0:
        body_w += 1
    max_wick = (pb - pt) * 0.22

    def _vis_ext(key, higher):
        best = None
        bv = None
        for i, r in enumerate(rows):
            v = float(r[key])
            y = yp(v)
            if y < pt + 6 or y > pb - 6:
                continue
            if best is None or (v > bv if higher else v < bv):
                best, bv = i, v
        if best is None:
            best = max(range(n), key=lambda i: float(rows[i][key])) if higher else min(
                range(n), key=lambda i: float(rows[i][key])
            )
        return best

    hi_i = _vis_ext("h", True)
    lo_i = _vis_ext("l", False)

    # last-bar glow
    last_x = int(round(pl + (n - 1) * slot + slot * 0.5))
    im = _glow(im, (last_x - 18, pt, last_x + 18, pb), GOLD, 16, 22)
    d = ImageDraw.Draw(im, "RGBA")
    d.line([(last_x, int(pt)), (last_x, int(pb))], fill=GOLD + (38,), width=1)

    for i, r in enumerate(rows):
        x = int(round(pl + i * slot + slot * 0.5))
        o, c, h_, l_ = float(r["o"]), float(r["c"]), float(r["h"]), float(r["l"])
        up = c >= o
        fill = TEAL if up else ROSE
        wick = TEAL_DK if up else ROSE_DK
        last_bar = i == n - 1
        yh, yl_ = yp(h_), yp(l_)
        y_o, y_c = yp(o), yp(c)
        y_o = min(pb, max(pt, y_o))
        y_c = min(pb, max(pt, y_c))
        body_top = min(y_o, y_c)
        body_bot = max(y_o, y_c)
        clipped_h = yh < pt - 1 or (body_top - yh) > max_wick
        clipped_l = yl_ > pb + 1 or (yl_ - body_bot) > max_wick
        if (body_top - yh) > max_wick:
            yh = body_top - max_wick
        if (yl_ - body_bot) > max_wick:
            yl_ = body_bot + max_wick
        yh = min(pb, max(pt, yh))
        yl_ = min(pb, max(pt, yl_))
        ww = 3 if last_bar else 2
        d.line([(x, int(round(yh))), (x, int(round(yl_)))], fill=wick, width=ww)
        if clipped_h:
            d.line([(x - 6, int(yh)), (x + 6, int(yh))], fill=wick, width=2)
        if clipped_l:
            d.line([(x - 6, int(yl_)), (x + 6, int(yl_))], fill=wick, width=2)
        top, bot = min(y_o, y_c), max(y_o, y_c)
        if bot - top < 3:
            mid = int(round((top + bot) / 2.0))
            d.line([(x - body_w // 2, mid), (x + body_w // 2, mid)], fill=fill, width=3)
        else:
            x0 = x - body_w // 2
            x1 = x + body_w // 2
            _round(d, (x0, int(round(top)), x1, int(round(bot))), 2, fill=fill)
            if up:
                d.line([(x0 + 1, int(round(top)) + 1), (x1 - 1, int(round(top)) + 1)], fill=(180, 230, 200), width=1)
            if last_bar:
                _round(
                    d,
                    (x0, int(round(top)), x1, int(round(bot))),
                    2,
                    outline=GOLD,
                    width=2,
                )

    def _hl_tag(i, key, prefix, dy):
        r = rows[i]
        x = int(round(pl + i * slot + slot * 0.5))
        raw_y = yp(float(r[key]))
        y = min(pb - 18, max(pt + 18, raw_y))
        txt = "%s  %s" % (prefix, _fmt(pair, r[key], fmt_px))
        tw, th = _tw(d, txt, f_tiny)
        if x < pl + tw + 16:
            tx = x + 12
        elif x > pr - tw - 16:
            tx = x - tw - 12
        else:
            tx = x - tw // 2
        tx = max(pl + 8, min(pr - tw - 8, tx))
        if y < pt + 40:
            ty = y + 10
        elif y > pb - 40:
            ty = y - th - 10
        elif dy < 0:
            ty = y - th - 10
        else:
            ty = y + 10
        ty = max(pt + 8, min(pb - th - 14, ty))
        d.ellipse((x - 5, int(y) - 5, x + 5, int(y) + 5), fill=INK)
        d.ellipse((x - 2, int(y) - 2, x + 2, int(y) + 2), fill=SHEET)
        d.text((tx, ty), txt, font=f_tiny, fill=MUTED)

    _hl_tag(hi_i, "h", "H", -26)
    _hl_tag(lo_i, "l", "L", 12)

    # right-rail pills
    pills = []
    if pt <= yl <= pb:
        pills.append({"y": yl, "col": accent, "txt": last_s, "kind": "last"})
    for lv in levels:
        y = yp(lv["pv"])
        if y < pt - 8 or y > pb + 8:
            continue
        lab = "%s  %s" % (lv["nm"], lv["px"])
        pills.append({"y": y, "col": lv["col"], "txt": lab, "kind": lv["nm"]})
    if pills:
        for p in pills:
            tw, th = _tw(d, p["txt"], f_pill_sm)
            p["tw"] = tw
            p["th"] = th
            p["bh"] = th + 16
        placed = _spread([p["y"] for p in pills], 32, pt + 8, pb - 8, 36)
        for p, y in zip(pills, placed):
            tw, th, bh = p["tw"], p["th"], p["bh"]
            bx = pr + 8
            by = int(y - bh / 2.0)
            _round(d, (bx, by, bx + tw + 24, by + bh), 11, fill=p["col"])
            d.text((bx + 12, by + 7), p["txt"], font=f_pill_sm, fill=(255, 255, 255))
            cy = int(y)
            d.polygon([(pr, cy), (bx, cy - 6), (bx, cy + 6)], fill=p["col"])

    # time axis
    def tlab(ts):
        try:
            return tehran_fmt(int(ts), "%H:%M")
        except Exception:
            return ""

    chosen = []
    for i, r in enumerate(rows):
        lab = tlab(r["t"])
        if not lab:
            continue
        try:
            hh, mm = lab.split(":")
            if mm == "00" and int(hh) % 2 == 0:
                chosen.append((i, lab, True))
            elif mm == "00":
                chosen.append((i, lab, False))
        except Exception:
            pass
    if len(chosen) < 4:
        chosen = []
        for frac in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
            idx = int(round((n - 1) * frac))
            chosen.append((idx, tlab(rows[idx]["t"]), False))
    last_lab = tlab(rows[-1]["t"])
    last_tw, last_th = _tw(d, last_lab or "00:00", f_micro)
    last_lx = last_x - last_tw / 2.0
    last_lx = max(pl, min(pr - last_tw, last_lx))
    seen_x = []
    for idx, lab, major in chosen:
        x = pl + idx * slot + slot * 0.5
        tw, th = _tw(d, lab, f_mono_sm)
        tx = x - tw / 2.0
        if last_lab and abs((tx + tw / 2.0) - (last_lx + last_tw / 2.0)) < tw + last_tw:
            continue
        skip = False
        for sx in seen_x:
            if abs(tx - sx) < tw + 10:
                skip = True
                break
        if skip:
            continue
        seen_x.append(tx)
        d.line([(int(x), pb), (int(x), pb + 8)], fill=LINE, width=1)
        d.text((tx, pb + 14), lab, font=f_mono_sm, fill=INK if major else DIM)

    if last_lab:
        _round(d, (last_lx - 8, pb + 12, last_lx + last_tw + 8, pb + 12 + last_th + 10), 8, fill=GOLD)
        d.text((last_lx, pb + 16), last_lab, font=f_micro, fill=IVORY)

    # footer
    d.line([(48, H - 52), (W - 48, H - 52)], fill=HAIR, width=1)
    try:
        dt = tehran_fmt(None, "latin") + "   Tehran"
    except Exception:
        dt = ""
    d.text((48, H - 38), dt, font=f_small, fill=DIM)

    handle = "@Tz_fx_bot"
    tw, th = _tw(d, handle, f_pill)
    hx = W / 2.0 - (tw + 40) / 2.0
    _round(d, (hx, H - 48, hx + tw + 40, H - 14), 16, fill=SHEET, outline=GOLD, width=1)
    d.text((hx + 20, H - 40), handle, font=f_pill, fill=GOLD)

    rx = W - 48
    rr_txt = None
    if sig and sig.get("risk_pips") and sig.get("reward_pips"):
        try:
            risk = float(sig["risk_pips"])
            rew = float(sig["reward_pips"])
            if risk > 0:
                rr_txt = "1 : %.2f R" % (rew / risk)
        except Exception:
            rr_txt = None
    if rr_txt:
        tw, th = _tw(d, rr_txt, f_small)
        d.text((rx - tw, H - 38), rr_txt, font=f_small, fill=MUTED)
        rx = rx - tw - 24
    if sc is not None:
        try:
            s = max(0, min(int(sc), 6))
        except Exception:
            s = 0
        badge = "ICT  %s / 6" % s
        tw, th = _tw(d, badge, f_small)
        d.text((rx - tw, H - 38), badge, font=f_small, fill=MUTED)
        rx = rx - tw - 16
        pip = 11
        sx = rx - (6 * pip + 5 * 4)
        for i in range(6):
            x0 = sx + i * (pip + 4)
            fill = GOLD if i < s else HAIR
            _round(d, (x0, H - 34, x0 + pip, H - 23), 3, fill=fill)

    im = _vignette(im)
    buf = io.BytesIO()
    im.convert("RGB").save(buf, format="PNG", optimize=True)
    return buf.getvalue()
