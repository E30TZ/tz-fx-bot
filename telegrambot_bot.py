# -*- coding: utf-8 -*-
"""TZ FX BOT — ICT. Python 3.8."""
from __future__ import print_function

import fcntl
import hashlib
import hmac
import json
import os
import re
import struct
import sys
import time
import traceback
import zipfile
import zlib

sys.path.insert(0, os.path.dirname(__file__))

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    import i18n as _i18n_mod
except Exception:
    _i18n_mod = None
TOKEN_FILE = os.path.join(HERE, ".telegram_token")
GEMINI_FILE = os.path.join(HERE, ".gemini_key")
GEMINI_MODEL = "gemini-flash-lite-latest"
GEMINI_MODELS = (
    "gemini-flash-lite-latest",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
)
GEMINI_CHAT_MODELS = (
    "gemini-3.5-flash",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
)
GEMINI_TTS_MODELS = (
    "gemini-3.1-flash-tts-preview",
    "gemini-2.5-flash-preview-tts",
)
GEMINI_STT_MODELS = (
    "gemini-3.5-flash",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
)
STATE_FILE = os.path.join(HERE, ".bot_state.json")
POSTED_FILE = os.path.join(HERE, ".channel_state.json")
LAST_FILE = os.path.join(HERE, ".last_trade.json")
CHAT_FILE = os.path.join(HERE, ".chat_mem.json")
MEM_DIR = os.path.join(HERE, ".mem")
EDU_AUDIO_DIR = os.path.join(HERE, ".edu_audio")
COACH_REF_FILE = os.path.join(HERE, ".coach_ref.wav")
COACH_REF_TEXT = (
    u"رفیق، من مربی تی زد اف ایکس هستم. آروم و خودمونی حرف می‌زنم، مثل آدم واقعی توی ویس تلگرام."
)
TRADES_FILE = os.path.join(HERE, ".open_trades.json")
PAPER_FILE = os.path.join(HERE, ".paper.json")
PAPER_START = 10000.0
PAPER_RISK = 0.01
PAPER_MAX_OPEN = 2
LIVE_BRIDGE_URL = "https://ehsantz.pingbaz.space/bot/index.cgi?app=bridge"
LOG_FILE = os.path.join(HERE, "bot.log")
VENDOR_DIR = os.path.join(HERE, "vendor")
VENDOR_ZIP = os.path.join(HERE, "vendor_py.zip")
LOCK_FILE = os.path.join(HERE, "bot.lock")
WEBHOOK_URL = "https://ehsantz.pingbaz.space/bot/index.cgi"
APP_URL = "https://ehsantz.pingbaz.space/bot/?app=1"
APP_FILE = os.path.join(HERE, "miniapp.html")
MENU_FLAG = os.path.join(HERE, ".menu_app_v2")
WEBHOOK_FLAG = os.path.join(HERE, ".webhook_on")
WEBHOOK_SECRET_FILE = os.path.join(HERE, ".webhook_secret")

OWNER_ID = 8351722954
BOT_VERSION = "3.0.0"
ENGINE_GEN = 6
BOT_USER = "Tz_fx_bot"
BOT_URL = "https://t.me/Tz_fx_bot"
CHANNEL = "@TZ_FX_CH"
CHANNEL_ID = -1004359115565
CHANNEL_URL = "https://t.me/TZ_FX_CH"
PRO_CHANNEL = "@tz_fx_pro"
PRO_CHANNEL_ID = -1003534722182
PRO_URL = "https://t.me/+uWnJTwhqC_FhMmM8"
CRYPTO_CHANNEL_URL = "https://t.me/+8hM_fEp9y7Y0ZmQ8"
CRYPTO_CHANNEL_FILE = os.path.join(HERE, ".crypto_channel.json")
ALERTS_FILE = os.path.join(HERE, ".price_alerts.json")
WEBHOOK_V_FILE = os.path.join(HERE, ".webhook_v19")
CRYPTO_NUDGE = os.path.join(HERE, ".crypto_nudge")
CRYPTO_UNIV_FILE = os.path.join(HERE, ".crypto_univ.json")
CRYPTO_WATCH_FILE = os.path.join(HERE, ".crypto_watch.json")
GROUP_FILE = os.path.join(HERE, ".group_id.json")
PUBLIC_FLAG = os.path.join(HERE, ".public_v3")
CMDS_FLAG = os.path.join(HERE, ".cmds_v10")
PE_CLEAN = os.path.join(HERE, ".pe_clean_v1")
LAUNCH_FLAG = os.path.join(HERE, ".launch_posted")
TICK_FILE = os.path.join(HERE, ".channel_tick")
OHLC_DISK = os.path.join(HERE, ".ohlc_disk.json")
BRIEF_FILE = os.path.join(HERE, ".hourly_brief")
WATCH_FILE = os.path.join(HERE, ".watch.json")
PE_FILE = os.path.join(HERE, ".pe.json")
HB_FILE = os.path.join(HERE, ".heartbeat")
SUBS_FILE = os.path.join(HERE, ".subs.json")
USERS_FILE = os.path.join(HERE, ".users.json")
PLANS_FILE = os.path.join(HERE, ".plans.json")
PAY_FILE = os.path.join(HERE, ".pay.json")
WAIT_FILE = os.path.join(HERE, ".wait.json")
RCP_FILE = os.path.join(HERE, ".receipts.json")
SUP_FILE = os.path.join(HERE, ".support.json")
ADMIN_KEY_FILE = os.path.join(HERE, ".admin_key")
MIN_CHANNEL_SCORE = 5
FREE_CHANNEL_SCORE = 6
TEHRAN_OFF = 12600  # UTC+3:30, no DST
_rate = {}
_hour = {}
_FA_DIG = dict((ord(str(i)), u) for i, u in enumerate(u"۰۱۲۳۴۵۶۷۸۹"))
_JMONTH = (
    u"فروردین",
    u"اردیبهشت",
    u"خرداد",
    u"تیر",
    u"مرداد",
    u"شهریور",
    u"مهر",
    u"آبان",
    u"آذر",
    u"دی",
    u"بهمن",
    u"اسفند",
)


def tehran_tuple(ts=None):
    if ts is None:
        ts = time.time()
    return time.gmtime(float(ts) + TEHRAN_OFF)


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    gy2 = gy + 1 if gm > 2 else gy
    days = (
        (365 * gy)
        + ((gy2 + 3) // 4)
        - ((gy2 + 99) // 100)
        + ((gy2 + 399) // 400)
        - 80
        + gd
        + g_d_m[gm - 1]
    )
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + (days % 31)
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + ((days - 186) % 30)
    return jy, jm, jd


def fa_num(s):
    return str(s).translate(_FA_DIG)


def fa_money(n):
    try:
        n = int(float(n))
    except Exception:
        n = 0
    raw = "{:,}".format(n)
    return fa_num(raw) + u" تومان"


def tehran_fmt(ts=None, fmt="%Y-%m-%d %H:%M"):
    t = tehran_tuple(ts)
    jy, jm, jd = gregorian_to_jalali(t.tm_year, t.tm_mon, t.tm_mday)
    if fmt == "%H:%M":
        return "%02d:%02d" % (t.tm_hour, t.tm_min)
    if fmt == "%Y-%m-%d %H:%M:%S ":
        return "%04d/%02d/%02d %02d:%02d:%02d " % (
            jy,
            jm,
            jd,
            t.tm_hour,
            t.tm_min,
            t.tm_sec,
        )
    if fmt == "latin":
        return "%04d/%02d/%02d %02d:%02d" % (jy, jm, jd, t.tm_hour, t.tm_min)
    return u"%s %s %s، ساعت %s" % (
        fa_num(jd),
        _JMONTH[jm - 1],
        fa_num(jy),
        fa_num("%02d:%02d" % (t.tm_hour, t.tm_min)),
    )

PAIRS = {
    "EURUSD": {
        "yahoo": "EURUSD=X",
        "kraken": "EURUSD",
        "pip": 0.0001,
        "emoji": "💶",
        "name": "یورو / دلار",
        "digits": 5,
    },
    "GBPUSD": {
        "yahoo": "GBPUSD=X",
        "kraken": "GBPUSD",
        "pip": 0.0001,
        "emoji": "💷",
        "name": "پوند / دلار",
        "digits": 5,
    },
    "XAUUSD": {"yahoo": "GC=F", "pip": 0.1, "emoji": "🥇", "name": "طلا", "digits": 2},
    "BTCUSDT": {
        "yahoo": "BTC-USD",
        "binance": "BTCUSDT",
        "kraken": "XBTUSD",
        "pip": 1.0,
        "emoji": "₿",
        "name": "بیت‌کوین",
        "digits": 1,
        "asset": "crypto",
    },
    "ETHUSDT": {
        "yahoo": "ETH-USD",
        "binance": "ETHUSDT",
        "kraken": "ETHUSD",
        "pip": 0.1,
        "emoji": "⟠",
        "name": "اتریوم",
        "digits": 2,
        "asset": "crypto",
    },
    "SOLUSDT": {
        "yahoo": "SOL-USD",
        "binance": "SOLUSDT",
        "kraken": "SOLUSD",
        "pip": 0.01,
        "emoji": "◎",
        "name": "سولانا",
        "digits": 3,
        "asset": "crypto",
    },
}
FX_PAIRS = ("EURUSD", "GBPUSD", "XAUUSD")
CRYPTO_CORE = (
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT",
    "ADAUSDT", "AVAXUSDT", "WIFUSDT", "TRXUSDT", "LINKUSDT", "DOTUSDT",
    "LTCUSDT", "NEARUSDT", "APTUSDT", "SUIUSDT", "ARBUSDT", "OPUSDT",
    "PEPEUSDT", "SHIBUSDT", "UNIUSDT", "AAVEUSDT", "FILUSDT", "INJUSDT",
    "XLMUSDT", "ATOMUSDT", "BCHUSDT", "ETCUSDT", "LDOUSDT", "WLDUSDT",
    "TAOUSDT", "RENDERUSDT", "FETUSDT", "TIAUSDT", "SEIUSDT", "JUPUSDT",
    "ONDOUSDT", "ENAUSDT", "WIFUSDT", "POLUSDT", "TRUMPUSDT", "PENGUUSDT",
)
CRYPTO_PAIRS = CRYPTO_CORE

def is_crypto_pair(pair):
    if (PAIRS.get(pair) or {}).get("asset") == "crypto":
        return True
    s = str(pair or "").upper()
    return s.endswith("USDT") and s not in FX_PAIRS



_CRYPTO_EMO = {
    "BTC": u"₿", "ETH": u"⟠", "SOL": u"◎", "BNB": u"🟡", "XRP": u"💧",
    "DOGE": u"🐶", "ADA": u"🔷", "AVAX": u"🔺", "TON": u"💎", "TRX": u"🔴",
    "LINK": u"🔗", "DOT": u"🟣", "PEPE": u"🐸", "SHIB": u"🐕", "LTC": u"🥈",
    "NEAR": u"🌈", "APT": u"🅰", "SUI": u"🌊", "ARB": u"🔵", "OP": u"🔴",
    "WIF": u"🐶", "UNI": u"🦄", "AAVE": u"👻", "FIL": u"📁", "INJ": u"💉",
    "TAO": u"🧠", "FET": u"🤖", "RENDER": u"🎨", "POL": u"🟣", "MATIC": u"🟣",
    "ATOM": u"⚛️", "ETC": u"🟢", "BCH": u"🪙", "XLM": u"🌟", "HBAR": u"ℏ",
    "ALGO": u"🔷", "VET": u"🔷", "QNT": u"📘", "MKR": u"DAI", "CRV": u"🌀",
    "LDO": u"🌊", "STX": u"🧱", "TIA": u"✨", "SEI": u"⚡", "RUNE": u"⚔️",
    "BONK": u"🐶", "FLOKI": u"🐶", "WLD": u"🌍", "ONDO": u"💠", "JUP": u"🪐",
    "PYTH": u"🔮", "ORDI": u"🟠", "NOT": u"🪙", "ENA": u"💠", "EIGEN": u"🔷",
}
_CRYPTO_FA = {
    "btc": "BTCUSDT", "bitcoin": "BTCUSDT", u"بیت": "BTCUSDT", u"بیتکوین": "BTCUSDT",
    u"بیت‌کوین": "BTCUSDT", "eth": "ETHUSDT", "ethereum": "ETHUSDT", u"اتریوم": "ETHUSDT",
    u"اتر": "ETHUSDT", "sol": "SOLUSDT", "solana": "SOLUSDT", u"سولانا": "SOLUSDT",
    u"سول": "SOLUSDT", "bnb": "BNBUSDT", u"بایننس": "BNBUSDT", "xrp": "XRPUSDT",
    u"ریپل": "XRPUSDT", "doge": "DOGEUSDT", u"دوج": "DOGEUSDT", u"دوج‌کوین": "DOGEUSDT",
    "ada": "ADAUSDT", u"کاردانو": "ADAUSDT", "avax": "AVAXUSDT", u"آوالانچ": "AVAXUSDT",
    "ton": "TONUSDT", u"تون": "TONUSDT", "trx": "TRXUSDT", u"ترون": "TRXUSDT",
    "link": "LINKUSDT", u"چین‌لینک": "LINKUSDT", u"چینلینک": "LINKUSDT",
    "dot": "DOTUSDT", u"پولکادات": "DOTUSDT", "ltc": "LTCUSDT", u"لایت": "LTCUSDT",
    "pepe": "PEPEUSDT", u"پپه": "PEPEUSDT", "shib": "SHIBUSDT", u"شیبا": "SHIBUSDT",
    "wif": "WIFUSDT", "bonk": "BONKUSDT", "floki": "FLOKIUSDT", "sui": "SUIUSDT",
    "arb": "ARBUSDT", "op": "OPUSDT", "apt": "APTUSDT", "near": "NEARUSDT",
    "inj": "INJUSDT", "fil": "FILUSDT", "uni": "UNIUSDT", "aave": "AAVEUSDT",
    "tao": "TAOUSDT", "fet": "FETUSDT", "render": "RENDERUSDT", "pol": "POLUSDT",
    "matic": "POLUSDT", u"پالیگان": "POLUSDT", "atom": "ATOMUSDT",
    "bch": "BCHUSDT", "etc": "ETCUSDT", "xlm": "XLMUSDT", "hbar": "HBARUSDT",
    "not": "NOTUSDT", "jup": "JUPUSDT", "pyth": "PYTHUSDT", "ondo": "ONDOUSDT",
    "wld": "WLDUSDT", "sei": "SEIUSDT", "tia": "TIAUSDT", "rune": "RUNEUSDT",
}
_CRYPTO_STOP = set(
    "IN ON UP IT ME NOW ALL BUY GAS ONE FOR THE AND ARE YES NO OK HI HEY GO TO OF OR IF AT BY AM IS BE US WE SO AN".split()
)
_crypto_univ_mem = {"at": 0, "data": None}
_crypto_hot_mem = {"at": 0, "rows": []}


def _binance_hosts():
    return ("data-api.binance.vision", "api.binance.com")


def _crypto_base(sym):
    s = (sym or "").upper()
    if s.endswith("USDT"):
        return s[:-4]
    return s


def _norm_crypto_sym(text):
    t = (text or "").strip().upper()
    t = t.replace("$", "").replace("/", "").replace("-", "").replace(" ", "").replace("_", "")
    if t.endswith("PERP"):
        t = t[:-4]
    if t.endswith("USD") and not t.endswith("USDT") and not t.endswith("USDC"):
        t = t[:-3] + "USDT"
    if t.endswith("USDC"):
        t = t[:-4] + "USDT"
    if (not t.endswith("USDT")) and t.replace("1000", "").isalnum() and 2 <= len(t) <= 16:
        t = t + "USDT"
    return t


def _pip_digits(px, tick):
    try:
        tick = float(tick) if tick else None
    except Exception:
        tick = None
    try:
        px = float(px) if px else None
    except Exception:
        px = None
    if px is None or px <= 0:
        if tick and tick > 0:
            s = ("%.12f" % tick).rstrip("0")
            d = len(s.split(".")[-1]) if "." in s else 0
            return tick, max(0, min(d, 8))
        return 0.0001, 4
    if px >= 1000:
        pip, d = 1.0, 1
    elif px >= 100:
        pip, d = 0.1, 2
    elif px >= 10:
        pip, d = 0.01, 3
    elif px >= 1:
        pip, d = 0.001, 4
    elif px >= 0.1:
        pip, d = 0.0001, 5
    elif px >= 0.01:
        pip, d = 0.00001, 6
    elif px >= 0.001:
        pip, d = 0.000001, 7
    else:
        pip, d = 1e-8, 8
    if tick and tick > 0:
        s = ("%.12f" % tick).rstrip("0")
        td = len(s.split(".")[-1]) if "." in s else 0
        d = max(d, min(td, 8))
    return pip, d


def load_crypto_universe(force=False):
    now = time.time()
    hit = _crypto_univ_mem.get("data")
    if (not force) and hit and now - float(_crypto_univ_mem.get("at") or 0) < 3600:
        return hit
    disk = _jload_safe(CRYPTO_UNIV_FILE, None)
    if isinstance(disk, dict) and (
        "USDCUSDT" in (disk.get("syms") or {}) or "USD1USDT" in (disk.get("syms") or {})
    ):
        force = True
    if (not force) and isinstance(disk, dict) and disk.get("syms"):
        try:
            if now - float(disk.get("at") or 0) < 6 * 3600:
                _crypto_univ_mem["data"] = disk
                _crypto_univ_mem["at"] = now
                return disk
        except Exception:
            pass
    data = {"at": now, "syms": {}, "bases": {}}
    blob = None
    last_err = None
    for host in _binance_hosts():
        try:
            r = http().get(
                "https://%s/api/v3/exchangeInfo" % host,
                timeout=12,
                headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 TZFX"},
            )
            r.raise_for_status()
            blob = r.json() or {}
            if blob.get("symbols"):
                break
        except Exception as e:
            last_err = e
            blob = None
    if not blob:
        if last_err:
            log("crypto univ %s" % str(last_err)[:80])
        if isinstance(disk, dict) and disk.get("syms"):
            _crypto_univ_mem["data"] = disk
            _crypto_univ_mem["at"] = now
            return disk
        return data
    for s in blob.get("symbols") or []:
        try:
            if s.get("status") != "TRADING":
                continue
            if s.get("quoteAsset") != "USDT":
                continue
            if s.get("isSpotTradingAllowed") is False:
                continue
            base = str(s.get("baseAsset") or "")
            if not base or not re.match(r"^[A-Z0-9]{2,16}$", base):
                continue
            if base.endswith(("UP", "DOWN", "BULL", "BEAR")):
                continue
            if base in (
                "USDT", "USDC", "BUSD", "DAI", "TUSD", "FDUSD", "EUR", "TRY", "BRL",
                "USDP", "USDD", "USD1", "USDE", "USDS", "AEUR", "EURI", "PAXG",
            ) or base.startswith("USD"):
                continue
            sym = str(s.get("symbol") or "")
            if not sym.endswith("USDT"):
                continue
            tick = None
            for f in s.get("filters") or []:
                if f.get("filterType") == "PRICE_FILTER" and f.get("tickSize"):
                    try:
                        tick = float(f["tickSize"])
                    except Exception:
                        tick = None
                    break
            rec = {"base": base, "tick": tick}
            data["syms"][sym] = rec
            data["bases"][base] = sym
        except Exception:
            continue
    try:
        _jsave(CRYPTO_UNIV_FILE, data)
    except Exception:
        pass
    _crypto_univ_mem["data"] = data
    _crypto_univ_mem["at"] = now
    log("crypto univ n=%s" % len(data.get("syms") or {}))
    return data


def crypto_hot(limit=24):
    now = time.time()
    if _crypto_hot_mem.get("rows") and now - float(_crypto_hot_mem.get("at") or 0) < 900:
        return list(_crypto_hot_mem["rows"])[:limit]
    rows = []
    for host in _binance_hosts():
        try:
            r = http().get(
                "https://%s/api/v3/ticker/24hr" % host,
                timeout=12,
                headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 TZFX"},
            )
            r.raise_for_status()
            blob = r.json() or []
            tmp = []
            for rec in blob:
                sym = rec.get("symbol") or ""
                if not sym.endswith("USDT"):
                    continue
                base = sym[:-4]
                if not re.match(r"^[A-Z0-9]{2,16}$", base):
                    continue
                if base.startswith("USD") or base in (
                    "DAI", "TUSD", "FDUSD", "BUSD", "EUR", "AEUR", "EURI", "PAXG"
                ):
                    continue
                try:
                    vol = float(rec.get("quoteVolume") or 0)
                    pct = float(rec.get("priceChangePercent") or 0)
                    last = float(rec.get("lastPrice") or 0)
                except Exception:
                    continue
                tmp.append((vol, sym, pct, last))
            tmp.sort(reverse=True)
            rows = tmp[:180]
            break
        except Exception as e:
            log("crypto hot %s" % str(e)[:80])
    _crypto_hot_mem["rows"] = rows
    _crypto_hot_mem["at"] = now
    return rows[:limit]


def _refine_crypto_meta(pair, px):
    meta = PAIRS.get(pair)
    if not meta or meta.get("asset") != "crypto":
        return
    try:
        pip, digits = _pip_digits(px, meta.get("tick"))
        meta["pip"] = pip
        meta["digits"] = int(digits)
        PAIRS[pair] = meta
    except Exception:
        pass


def ensure_crypto_pair(raw, px=None, probe=False):
    if not raw:
        return None
    key = (raw or "").strip()
    low = key.replace(u"ي", u"ی").lower().replace("$", "").strip()
    if low in _CRYPTO_FA:
        key = _CRYPTO_FA[low]
    s = _norm_crypto_sym(key)
    if s in FX_PAIRS:
        return s
    if s in PAIRS and is_crypto_pair(s):
        return s
    univ = load_crypto_universe() or {}
    rec = (univ.get("syms") or {}).get(s)
    if not rec:
        base = _crypto_base(s)
        mapped = (univ.get("bases") or {}).get(base)
        if mapped:
            s = mapped
            rec = (univ.get("syms") or {}).get(s)
    if not rec:
        if not probe:
            return None
        base = _crypto_base(s)
        if not re.match(r"^[A-Z0-9]{2,16}$", base) or base in _CRYPTO_STOP:
            return None
        ysym = "%s-USD" % base
        PAIRS[s] = {
            "yahoo": ysym,
            "binance": None,
            "pip": 0.0001,
            "emoji": _CRYPTO_EMO.get(base) or u"🪙",
            "name": base,
            "digits": 4,
            "asset": "crypto",
            "tick": None,
        }
        TV_SYMBOL[s] = ysym
        try:
            rows = _fetch_yahoo(s, "15m", "10d")
        except Exception:
            rows = []
        if len(rows) < 12:
            PAIRS.pop(s, None)
            return None
        _refine_crypto_meta(s, rows[-1]["c"])
        _ohlc_cache[s + "|15m"] = rows
        _ohlc_cache_at[s + "|15m"] = time.time()
        return s
    tick = rec.get("tick")
    pip, digits = _pip_digits(px, tick)
    base = rec.get("base") or _crypto_base(s)
    PAIRS[s] = {
        "yahoo": ("%s-USD" % base) if base in ("BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "LTC", "LINK", "AVAX", "DOT", "TON", "TRX", "UNI", "AAVE", "NEAR", "APT", "SUI", "ATOM", "BCH", "ETC", "XLM", "FIL", "SHIB", "PEPE") else None,
        "binance": s,
        "pip": pip,
        "emoji": _CRYPTO_EMO.get(base) or u"🪙",
        "name": base,
        "digits": digits,
        "asset": "crypto",
        "tick": tick,
    }
    TV_SYMBOL[s] = "BINANCE:" + s
    return s


def search_crypto(q, limit=24):
    raw = (q or "").strip()
    if not raw:
        return []
    low = raw.replace(u"ي", u"ی").lower().replace("$", "").strip()
    out = []
    if low in _CRYPTO_FA:
        out.append(_CRYPTO_FA[low])
    univ = load_crypto_universe() or {}
    bases = univ.get("bases") or {}
    uq = raw.upper().replace("$", "").replace("/", "").replace("-", "").replace(" ", "")
    if uq.endswith("USDT"):
        uq = uq[:-4]
    if uq in bases:
        out.append(bases[uq])
    if len(uq) >= 2:
        for base, sym in bases.items():
            if base == uq or base.startswith(uq) or uq in base:
                out.append(sym)
    seen = set()
    uniq = []
    for s in out:
        if s in seen:
            continue
        seen.add(s)
        uniq.append(s)
        if len(uniq) >= limit:
            break
    return uniq


def remember_crypto_watch(pair):
    if not pair or not is_crypto_pair(pair):
        return
    d = _jload_safe(CRYPTO_WATCH_FILE, {}) or {}
    lst = [x for x in (d.get("pairs") or []) if x != pair]
    lst.insert(0, pair)
    d["pairs"] = lst[:24]
    d["at"] = time.time()
    try:
        _jsave(CRYPTO_WATCH_FILE, d)
    except Exception:
        pass


def crypto_scan_list():
    d = _jload_safe(CRYPTO_WATCH_FILE, {}) or {}
    extra = list(d.get("pairs") or [])
    hot = []
    try:
        hot = [x[1] for x in crypto_hot(150)]
    except Exception:
        hot = []
    univ = []
    try:
        univ = sorted(((load_crypto_universe() or {}).get("syms") or {}).keys())
    except Exception:
        univ = []
    rot = []
    n = len(univ)
    if n:
        start = int(time.time() // 120) % n
        for i in range(0, min(90, n)):
            rot.append(univ[(start + i) % n])
    out = list(CRYPTO_CORE) + extra + hot + rot
    seen = set()
    uniq = []
    for s in out:
        if not s or s in seen:
            continue
        seen.add(s)
        try:
            if ensure_crypto_pair(s):
                uniq.append(s)
        except Exception:
            continue
        if len(uniq) >= 140:
            break
    return uniq


def kb_crypto_page(page=0, kind="all"):
    univ = load_crypto_universe() or {}
    if kind == "hot":
        items = [x[1] for x in crypto_hot(48)]
        title_more = u"داغ"
    else:
        items = sorted((univ.get("syms") or {}).keys())
        title_more = u"همه"
    n = len(items)
    per = 12
    pages = max(1, (n + per - 1) // per)
    page = max(0, min(int(page or 0), pages - 1))
    chunk = items[page * per : page * per + per]
    rows = []
    row = []
    for sym in chunk:
        ensure_crypto_pair(sym)
        meta = PAIRS.get(sym) or {}
        base = _crypto_base(sym)
        lab = u"%s %s" % (meta.get("emoji") or u"🪙", base)
        row.append(btn(lab[:18], "sig_%s" % sym))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    nav = []
    if page > 0:
        nav.append(btn(u"⬅️", "cxp_%s_%s" % (kind, page - 1)))
    nav.append(btn(u"%s %s/%s" % (title_more, page + 1, pages), "cxp_%s_%s" % (kind, page)))
    if page < pages - 1:
        nav.append(btn(u"➡️", "cxp_%s_%s" % (kind, page + 1)))
    if nav:
        rows.append(nav)
    rows.append(
        [
            btn(u"🔎 جستجو", "cx_find", style="success"),
            btn(u"🔥 داغ", "cx_hot", style="primary"),
            btn(u"📋 همه", "cx_all"),
        ]
    )
    rows.append([btn(u"₿ کریپتو", "crypto_menu", style="primary")])
    return {"inline_keyboard": rows}


def handle_crypto_query(token, user_id, chat_id, text, reply_to=None):
    q = (text or "").strip()
    pair = ensure_crypto_pair(q, probe=True)
    if not pair:
        hits = search_crypto(q, 18)
        if not hits:
            send_message(
                token,
                chat_id,
                u"🪙 <b>%s</b> را در اسپات USDT بایننس پیدا نکردم.\n"
                u"انگلیسی بفرست: <code>PEPE</code> <code>WIF</code> <code>ARB</code> <code>1000SATS</code>"
                % (q[:40] or u"این اسم"),
                kb_crypto(),
                reply_to=reply_to,
            )
            return
        if len(hits) == 1:
            pair = ensure_crypto_pair(hits[0])
        else:
            rows = []
            row = []
            for sym in hits:
                ensure_crypto_pair(sym)
                meta = PAIRS.get(sym) or {}
                lab = u"%s %s" % (meta.get("emoji") or u"🪙", _crypto_base(sym))
                row.append(btn(lab[:18], "sig_%s" % sym))
                if len(row) == 3:
                    rows.append(row)
                    row = []
            if row:
                rows.append(row)
            rows.append([btn(u"🔎 دوباره", "cx_find", style="success")])
            rows.append([btn(u"₿ کریپتو", "crypto_menu")])
            send_message(
                token,
                chat_id,
                u"🔎 چند تا پیدا شد برای <b>%s</b> — یکی را بزن:" % q[:40],
                {"inline_keyboard": rows},
                reply_to=reply_to,
            )
            return
    if not pair:
        return
    if not gate(token, user_id, chat_id):
        return
    remember_crypto_watch(pair)
    deliver_one(token, chat_id, pair, tf="mtf", reply_to=reply_to, user_id=user_id)


def looks_like_crypto_query(text):
    t = (text or "").strip()
    if not t or t.startswith("/"):
        return False
    if t.startswith("$"):
        return True
    low = t.replace(u"ي", u"ی").lower()
    if low in _CRYPTO_FA:
        return True
    if "USDT" in t.upper() or "USDC" in t.upper():
        return True
    if len(t.split()) > 3:
        return False
    token = t.replace("$", "").replace("/", "").replace("-", "").strip()
    if not re.match(r"^[A-Za-z0-9]{2,16}$", token):
        return False
    u = token.upper()
    if u in _CRYPTO_STOP:
        return False
    univ = load_crypto_universe() or {}
    base = u[:-4] if u.endswith("USDT") else u
    if base in (univ.get("bases") or {}):
        return True
    return False



def fx_pairs():
    return FX_PAIRS


def beat_heartbeat(force=False):
    try:
        hb = 0.0
        if os.path.isfile(HB_FILE):
            hb = float(open(HB_FILE).read().strip() or 0)
        if force or (time.time() - hb > 90):
            with open(HB_FILE, "w") as f:
                f.write(str(time.time()))
    except Exception:
        pass


def _jload_safe(path, default):
    try:
        if os.path.isfile(path):
            with open(path, "r") as f:
                return json.load(f)
    except Exception:
        return default
    return default


def crypto_channel_id():
    d = _jload_safe(CRYPTO_CHANNEL_FILE, {}) or {}
    try:
        return int(d.get("id") or 0)
    except Exception:
        return 0


def bind_crypto_channel(chat):
    chat = chat or {}
    if chat.get("type") != "channel":
        return False
    try:
        cid = int(chat.get("id") or 0)
    except Exception:
        return False
    if not cid or cid in (int(CHANNEL_ID), int(PRO_CHANNEL_ID)):
        return False
    blob = {
        "id": cid,
        "title": chat.get("title") or "TZ Crypto",
        "ts": time.time(),
    }
    try:
        with open(CRYPTO_CHANNEL_FILE, "w") as f:
            json.dump(blob, f)
        log("crypto channel bound %s %s" % (cid, blob.get("title")))
        return True
    except Exception:
        log("crypto bind fail " + traceback.format_exc())
        return False


def maybe_bind_crypto_member(token, mcm):
    chat = (mcm or {}).get("chat") or {}
    if chat.get("type") != "channel":
        return
    nw = (mcm or {}).get("new_chat_member") or {}
    st = nw.get("status") or ""
    user = nw.get("user") or {}
    if not user.get("is_bot"):
        return
    if st not in ("administrator", "creator"):
        return
    if bind_crypto_channel(chat):
        try:
            send_message(
                token,
                OWNER_ID,
                u"✅ کانال کریپتو بتا ثبت شد.\\n%s\\n<code>%s</code>"
                % (chat.get("title") or "", chat.get("id")),
            )
        except Exception:
            pass


def in_crypto_asia(ts):
    hour = time.gmtime(ts).tm_hour
    if 0 <= hour < 4:
        return u"آسیا · ۰۳:۳۰–۰۷:۳۰ تهران"
    return None


def next_session_line(ts=None):
    ts = int(ts or time.time())
    kz = in_killzone(ts) or in_crypto_asia(ts)
    if kz:
        return u"الان داخل سشن است: %s" % kz
    hour = time.gmtime(ts).tm_hour
    starts = [(0, u"آسیا"), (7, u"لندن"), (12, u"نیویورک")]
    for h, name in starts:
        if hour < h:
            wait = (h - hour)
            return u"سشن بعدی %s حدود %s ساعت دیگر (UTC %02d:00)" % (name, wait, h)
    return u"سشن بعدی آسیا بعد از نیمه‌شب UTC"


def news_window(ts=None):
    g = time.gmtime(ts or time.time())
    # NFP typically first Friday 12:30 UTC. Soft warn Fridays 12:00–14:30 UTC.
    if g.tm_wday == 4 and 12 <= g.tm_hour < 15:
        return u"پنجره خبر جمعه (NFP/CPI محتمل) — سایز را نصف کن"
    if g.tm_wday == 2 and 17 <= g.tm_hour < 20:
        return u"پنجره چهارشنبه (FOMC محتمل) — احتیاط"
    return None


def fx_open_line(ts=None):
    if market_is_open(ts):
        return u"فارکس باز است"
    g = time.gmtime(ts or time.time())
    if g.tm_wday == 5:
        return u"فارکس شنبه تعطیل است — دوشنبه ۲۲:۳۰ تهران باز می‌شود"
    if g.tm_wday == 6 and g.tm_hour < 21:
        return u"فارکس یکشنبه هنوز بسته است — ۲۲:۳۰ تهران باز می‌شود"
    if g.tm_wday == 4 and g.tm_hour >= 21:
        return u"فارکس جمعه بسته شد"
    return u"فارکس تعطیل است"


_KRAKEN_IV = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240, "1d": 1440}

_bot_error = None
_last_signal = "not yet"
_last_poll = "-"
_ohlc_cache = {}
_ohlc_cache_at = {}
_http = None
_member_cache = {}
_last_channel_tick = 0
_CACHE_TTL = {
    "1m": 15,
    "5m": 25,
    "15m": 35,
    "30m": 50,
    "1h": 80,
    "4h": 120,
    "1d": 180,
    "1wk": 300,
}


def log(msg):
    line = tehran_fmt(None, "%Y-%m-%d %H:%M:%S ") + str(msg)
    try:
        line = re.sub(r"bot\d{6,}:[A-Za-z0-9_-]{20,}", "bot…", line)
        line = re.sub(r"AIza[0-9A-Za-z_-]{20,}", "AIza…", line)
    except Exception:
        pass
    try:
        if os.path.isfile(LOG_FILE) and os.path.getsize(LOG_FILE) > 250000:
            open(LOG_FILE, "w").close()
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def ensure_requests():
    if os.path.isdir(VENDOR_DIR) and VENDOR_DIR not in sys.path:
        sys.path.insert(0, VENDOR_DIR)
    try:
        import requests  # noqa: F401
        return
    except ImportError:
        pass
    if os.path.isfile(VENDOR_ZIP):
        with zipfile.ZipFile(VENDOR_ZIP, "r") as z:
            z.extractall(VENDOR_DIR)
        if VENDOR_DIR not in sys.path:
            sys.path.insert(0, VENDOR_DIR)
    import requests  # noqa: F401


def load_token():
    env = os.environ.get("TELEGRAM_TOKEN", "").strip()
    if env:
        return env
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            val = f.read().strip()
        if val:
            return val
    return ""


def tg_api(token):
    return "https://api.telegram.org/bot" + token


def http():
    global _http
    ensure_requests()
    if _http is None:
        import requests
        from requests.adapters import HTTPAdapter

        s = requests.Session()
        try:
            ad = HTTPAdapter(pool_connections=16, pool_maxsize=16)
            s.mount("https://", ad)
            s.mount("http://", ad)
        except Exception:
            pass
        s.headers["User-Agent"] = "Mozilla/5.0"
        _http = s
    return _http


def _jload(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default


def _jsave(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


def load_plans():
    d = _jload(PLANS_FILE, None)
    if not d or not isinstance(d, dict):
        d = {
            "w1": {"days": 7, "amount": 0, "title": u"۷ روزه"},
            "m1": {"days": 30, "amount": 0, "title": u"۳۰ روزه"},
            "m3": {"days": 90, "amount": 0, "title": u"۹۰ روزه"},
        }
        _jsave(PLANS_FILE, d)
        return d
    changed = False
    for pid, p in list(d.items()):
        if not isinstance(p, dict):
            continue
        if "amount" not in p:
            p["amount"] = int(p.get("price") or 0)
            changed = True
        p.setdefault("days", 30)
        p.setdefault("title", pid)
    if changed:
        _jsave(PLANS_FILE, d)
    return d


def save_plans(d):
    _jsave(PLANS_FILE, d)


def load_pay():
    d = _jload(PAY_FILE, None)
    if not d or not isinstance(d, dict):
        d = {"card": "", "holder": ""}
        _jsave(PAY_FILE, d)
    d.setdefault("card", "")
    d.setdefault("holder", "")
    return d


def save_pay(d):
    _jsave(PAY_FILE, d)


def load_wait():
    return _jload(WAIT_FILE, {})


def set_wait(uid, kind, extra=None):
    w = load_wait()
    rec = {"kind": kind, "ts": time.time()}
    if extra:
        rec.update(extra)
    w[str(uid)] = rec
    _jsave(WAIT_FILE, w)


def pop_wait(uid):
    w = load_wait()
    rec = w.pop(str(uid), None)
    _jsave(WAIT_FILE, w)
    return rec


def get_wait(uid):
    rec = load_wait().get(str(uid)) or {}
    if not rec:
        return {}
    try:
        age = time.time() - float(rec.get("ts") or 0)
    except Exception:
        age = 99999
    if age > 8 * 3600:
        pop_wait(uid)
        return {}
    return rec


def load_rcps():
    return _jload(RCP_FILE, {})


def save_rcps(d):
    _jsave(RCP_FILE, d)


def card_pretty(num):
    s = "".join(ch for ch in str(num or "") if ch.isdigit())
    if not s:
        return u"ست نشده"
    chunks = [s[i : i + 4] for i in range(0, len(s), 4)]
    return " ".join(chunks)


def unban_vip(token, uid):
    try:
        http().post(
            tg_api(token) + "/unbanChatMember",
            json={
                "chat_id": PRO_CHANNEL_ID,
                "user_id": int(uid),
                "only_if_banned": True,
            },
            timeout=8,
        )
    except Exception:
        pass


def load_subs():
    return _jload(SUBS_FILE, {})


def save_subs(data):
    _jsave(SUBS_FILE, data)


def load_users():
    return _jload(USERS_FILE, {})


def touch_user(uid):
    if not uid:
        return
    u = load_users()
    k = str(uid)
    rec = u.get(k) or {}
    rec["id"] = int(uid)
    rec["seen"] = time.time()
    u[k] = rec
    if len(u) > 5000:
        items = sorted(u.items(), key=lambda kv: (kv[1] or {}).get("seen") or 0)
        u = dict(items[-4000:])
    _jsave(USERS_FILE, u)


def is_owner(uid):
    try:
        return int(uid) == OWNER_ID
    except Exception:
        return False


def sub_until(uid):
    rec = load_subs().get(str(uid)) or {}
    try:
        return float(rec.get("until") or 0)
    except Exception:
        return 0


def is_pro(uid):
    if is_owner(uid):
        return True
    return sub_until(uid) > time.time()


def grant_sub(uid, days, plan="admin"):
    subs = load_subs()
    k = str(uid)
    rec = subs.get(k) or {}
    now = time.time()
    base = max(now, float(rec.get("until") or 0))
    rec["until"] = base + int(days) * 86400
    rec["plan"] = plan
    rec["granted"] = now
    subs[k] = rec
    save_subs(subs)
    return rec["until"]


def revoke_sub(uid):
    subs = load_subs()
    k = str(uid)
    if k in subs:
        subs[k]["until"] = 0
        save_subs(subs)


def admin_key():
    if os.path.isfile(ADMIN_KEY_FILE):
        try:
            return open(ADMIN_KEY_FILE).read().strip()
        except Exception:
            pass
    key = os.urandom(12).hex()
    try:
        with open(ADMIN_KEY_FILE, "w") as f:
            f.write(key)
        os.chmod(ADMIN_KEY_FILE, 0o600)
    except Exception:
        pass
    return key


def kb_pay():
    rows = []
    plans = load_plans()
    for pid, p in plans.items():
        amt = p.get("amount") or 0
        label = u"%s — %s" % (p.get("title") or pid, fa_money(amt) if amt else u"مبلغ ست نشده")
        rows.append([btn(u"💳 " + label, "buy_" + pid, style="success")])
    rows.append([btn(u"📣 کانال رایگان", url=CHANNEL_URL, style="primary")])
    rows.append([btn(u"🏠 TZ FX", "home")])
    return {"inline_keyboard": rows}


def kb_admin():
    return {
        "inline_keyboard": [
            [
                btn(u"👥 اعضا", "ad_users", style="primary"),
                btn(u"💎 اشتراک‌ها", "ad_subs", style="success"),
            ],
            [
                btn(u"💳 کارت و پلن", "ad_pay", style="success"),
                btn(u"📥 رسیدها", "ad_rcp", style="primary"),
            ],
            [
                btn(u"📣 پیام همگانی", "ad_bc"),
                btn(u"📊 وضعیت", "ad_stat", style="primary"),
            ],
            [btn(u"🛟 صندوق پشتیبانی", "ad_sup", style="success")],
            [btn(u"🔙 منو", "help")],
        ]
    }


def kb_admin_pay():
    rows = [
        [
            btn(u"💳 ست کارت", "ad_setcard", style="primary"),
            btn(u"👤 نام صاحب کارت", "ad_setholder"),
        ]
    ]
    for pid, p in load_plans().items():
        rows.append(
            [
                btn(u"💰 مبلغ " + (p.get("title") or pid), "ad_amt_" + pid, style="success"),
                btn(u"⏱ روز", "ad_day_" + pid),
                btn(u"✏️ عنوان", "ad_ttl_" + pid),
            ]
        )
    rows.append([btn(u"🔙 پنل", "ad_stat")])
    return {"inline_keyboard": rows}


def admin_pay_text():
    pay = load_pay()
    card = card_pretty(pay.get("card"))
    holder = pay.get("holder") or u"—"
    lines = [
        u"💳 <b>تنظیم پرداخت</b>",
        u"────────────",
        u"کارت: <code>%s</code>" % card,
        u"به نام: <b>%s</b>" % holder,
        u"",
        u"پلن‌ها:",
    ]
    for pid, p in load_plans().items():
        lines.append(
            u"• <code>%s</code>  %s  ·  %s روز  ·  %s"
            % (
                pid,
                p.get("title") or pid,
                fa_num(p.get("days") or 0),
                fa_money(p.get("amount") or 0),
            )
        )
    lines += [
        u"",
        u"دستورها:",
        u"<code>/card شماره‌کارت</code>",
        u"<code>/holder نام صاحب کارت</code>",
        u"<code>/price m1 900000</code>",
        u"<code>/days m1 30</code>",
        u"<code>/title m1 سی روزه</code>",
        u"",
        u"یا از دکمه‌ها بزن و بعدش عدد/متن را بفرست.",
    ]
    return u"\n".join(lines)


def txt_paywall(uid):
    left = sub_until(uid) - time.time()
    if left > 0:
        days = int(left / 86400) + 1
        st = T("txt.paywall_active") % (
            tehran_fmt(sub_until(uid)),
            fa_num(days) if get_lang(uid) == "fa" else str(days),
        )
    else:
        st = T("txt.paywall_none")
    pay = load_pay()
    card = card_pretty(pay.get("card"))
    extra = u""
    if pay.get("card"):
        extra = u"\nکارت: <code>%s</code>" % card
        if pay.get("holder"):
            extra += u"\nبه نام: %s" % pay.get("holder")
    return (
        tz_head(T("head.sub"))
        + u"%s\n%s\n\n"
        + T("txt.paywall_body")
        + u"\n"
        + tz_foot()
    ) % (st, extra)


def txt_invoice(uid, pid):
    p = load_plans().get(pid) or {}
    pay = load_pay()
    card = card_pretty(pay.get("card"))
    holder = pay.get("holder") or u"—"
    days = int(p.get("days") or 30)
    amt = p.get("amount") or 0
    title = p.get("title") or pid
    if not pay.get("card") or not amt:
        return (
            u"⚠️ کارت یا مبلغ این پلن هنوز از پنل ادمین ست نشده.\n"
            u"به ادمین پیام بده.\n"
            u"آیدی تو: <code>%s</code>" % uid
        )
    until_guess = time.time() + days * 86400
    return (
        u"💳 <b>پرداخت اشتراک %s</b>\n"
        u"────────────\n"
        u"مدت: <b>%s روز</b>\n"
        u"مبلغ: <b>%s</b>\n"
        u"اگر الان تایید شود تا: %s\n\n"
        u"به این کارت واریز کن:\n"
        u"<code>%s</code>\n"
        u"به نام: <b>%s</b>\n\n"
        u"۱) واریز کن\n"
        u"۲) <b>عکس رسید</b> را همین‌جا بفرست\n"
        u"۳) صبر کن تا ادمین تایید کند\n\n"
        u"<i>روی شماره کارت بزن تا کپی شود</i>"
    ) % (title, fa_num(days), fa_money(amt), tehran_fmt(until_guess), card, holder)


def kb_join():
    return {
        "inline_keyboard": [
            [btn(T("btn.join_ch"), url=CHANNEL_URL, style="primary")],
            [btn(T("btn.joined"), "check_join", style="success")],
            [btn(T("btn.lang"), "lang_toggle")],
        ]
    }


def send_stars_invoice(token, chat_id, uid, pid):
    plans = load_plans()
    p = plans.get(pid)
    if not p:
        return False
    payload = {
        "chat_id": chat_id,
        "title": "TZ FX " + str(p.get("title") or pid),
        "description": "اشتراک سیگنال و کانال VIP — %s روز" % p.get("days"),
        "payload": "sub:%s:%s" % (uid, pid),
        "currency": "XTR",
        "prices": [{"label": p.get("title") or pid, "amount": int(p.get("stars") or 1)}],
    }
    try:
        r = http().post(tg_api(token) + "/sendInvoice", json=payload, timeout=12)
        js = r.json() if r.content else {}
        if js.get("ok"):
            return True
        log("invoice fail " + str(js)[:200])
        return False
    except Exception:
        log("invoice error " + traceback.format_exc())
        return False


def handle_pre_checkout(token, pcq):
    cid = pcq.get("id")
    try:
        http().post(
            tg_api(token) + "/answerPreCheckoutQuery",
            json={"pre_checkout_query_id": cid, "ok": True},
            timeout=8,
        )
    except Exception:
        log("precheckout " + traceback.format_exc())


def handle_payment(token, msg):
    uid = (msg.get("from") or {}).get("id")
    chat_id = (msg.get("chat") or {}).get("id")
    pay = msg.get("successful_payment") or {}
    payload = str(pay.get("invoice_payload") or "")
    pid = "m1"
    parts = payload.split(":")
    if len(parts) >= 3:
        pid = parts[2]
    p = load_plans().get(pid) or {"days": 30, "title": pid}
    until = grant_sub(uid, int(p.get("days") or 30), pid)
    try:
        http().post(
            tg_api(token) + "/unbanChatMember",
            json={
                "chat_id": PRO_CHANNEL_ID,
                "user_id": int(uid),
                "only_if_banned": True,
            },
            timeout=8,
        )
    except Exception:
        pass
    send_message(
        token,
        chat_id,
        "✅ اشتراک <b>%s</b> فعال شد تا %s تهران.\nکانال VIP: %s"
        % (p.get("title"), tehran_fmt(until), PRO_URL),
        kb_main(uid),
    )


def protect_pro(token, cm):
    chat = cm.get("chat") or {}
    if int(chat.get("id") or 0) != int(PRO_CHANNEL_ID):
        return
    nw = cm.get("new_chat_member") or {}
    user = nw.get("user") or {}
    uid = user.get("id")
    if not uid or user.get("is_bot"):
        return
    st = nw.get("status")
    if st not in ("member", "restricted"):
        return
    if is_pro(uid):
        return
    try:
        http().post(
            tg_api(token) + "/banChatMember",
            json={"chat_id": PRO_CHANNEL_ID, "user_id": int(uid)},
            timeout=8,
        )
        log("ban non-sub %s" % uid)
    except Exception:
        log("ban fail " + traceback.format_exc())
    send_message(
        token,
        uid,
        "⛔️ کانال VIP فقط برای مشترکین است.\nاشتراک بخر تا عضویت آزاد شود.",
        kb_pay(),
    )


def admin_stats_text():
    users = load_users()
    subs = load_subs()
    now = time.time()
    active = sum(1 for v in subs.values() if float((v or {}).get("until") or 0) > now)
    return (
        "🛠 <b>پنل TZ FX</b>\n"
        "────────────\n"
        "کاربران دیده‌شده: <b>%s</b>\n"
        "اشتراک فعال: <b>%s</b>\n"
        "کانال رایگان: %s\n"
        "کانال VIP: %s\n"
        "کارت: <code>%s</code>\n"
        "نسخه: <code>%s</code>\n"
        "الان: %s\n\n"
        "دستورها:\n"
        "<code>/grant 8351722954 30</code>\n"
        "<code>/revoke 8351722954</code>\n"
        "<code>/say متن همگانی</code>\n"
        "<code>/card /holder /price /days</code>"
        % (
            len(users),
            active,
            CHANNEL,
            PRO_CHANNEL,
            card_pretty((load_pay() or {}).get("card")),
            BOT_VERSION,
            tehran_fmt(),
        )
    )


def btn(text, callback=None, url=None, style=None, web_app=None):
    """Bot API 9.4: style = primary (blue) / success (green) / danger (red)."""
    d = {"text": text}
    if callback:
        d["callback_data"] = callback
    if url:
        d["url"] = url
    if web_app:
        d["web_app"] = {"url": web_app}
    if style:
        d["style"] = style
    return d


_pe_map = {u"👍": "5368324170671202286"}
_pe_off = [False]
_pe_tried = [False]


def pe(ch):
    return ch


def _strip_pe(text):
    if not text or "<tg-emoji" not in text:
        return text
    out = []
    i = 0
    n = len(text)
    while i < n:
        a = text.find("<tg-emoji", i)
        if a < 0:
            out.append(text[i:])
            break
        out.append(text[i:a])
        b = text.find(">", a)
        c = text.find("</tg-emoji>", b if b >= 0 else a)
        if b < 0 or c < 0:
            out.append(text[a:])
            break
        out.append(text[b + 1 : c])
        i = c + 11
    return "".join(out)


def _pe_save():
    try:
        _jsave(PE_FILE, _pe_map)
    except Exception:
        pass


def _pe_load_file():
    if not os.path.isfile(PE_CLEAN):
        keep = {u"👍": "5368324170671202286"}
        _pe_map.clear()
        _pe_map.update(keep)
        _pe_save()
        try:
            with open(PE_CLEAN, "w") as f:
                f.write("1")
        except Exception:
            pass
        log("pe map reset (pack poison)")
        return
    d = _jload(PE_FILE, {})
    if not isinstance(d, dict):
        return
    for k, v in d.items():
        if k and v:
            _pe_map[k] = str(v)


def emojify(text, limit=16):
    """No premium custom emoji — Unicode only."""
    return text
    if not text or _pe_off[0] or not _pe_map:
        return text
    items = sorted(
        ((k, v) for k, v in _pe_map.items() if k and v),
        key=lambda kv: -len(kv[0]),
    )
    used = [0]

    def wrap_plain(s):
        if used[0] >= limit or not s:
            return s
        out = s
        for ch, cid in items:
            if used[0] >= limit:
                break
            if not ch or ch in out[:0] or ch not in out:
                continue
            if "<" in ch or ">" in ch:
                continue
            tag = u'<tg-emoji emoji-id="%s">%s</tg-emoji>' % (cid, ch)
            cnt = out.count(ch)
            nrep = min(cnt, limit - used[0])
            if nrep <= 0:
                continue
            out = out.replace(ch, tag, nrep)
            used[0] += nrep
        return out

    parts = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "<":
            j = text.find(">", i)
            if j < 0:
                parts.append(text[i:])
                break
            parts.append(text[i : j + 1])
            i = j + 1
            continue
        j = text.find("<", i)
        if j < 0:
            parts.append(wrap_plain(text[i:]))
            break
        parts.append(wrap_plain(text[i:j]))
        i = j
    return "".join(parts)


def ingest_pe_pack(token, name):
    name = (name or "").strip()
    if "addemoji/" in name:
        name = name.split("addemoji/", 1)[-1]
    name = name.split("?")[0].split()[0].strip().strip("/")
    if not name or len(name) > 64:
        return 0
    n = 0
    try:
        r = http().get(
            tg_api(token) + "/getStickerSet",
            params={"name": name},
            timeout=10,
        )
        js = r.json() if r.content else {}
        if not js.get("ok"):
            return 0
        for st in (js.get("result") or {}).get("stickers") or []:
            cid = st.get("custom_emoji_id")
            emo = st.get("emoji")
            if cid and emo:
                _pe_map[emo] = str(cid)
                n += 1
    except Exception:
        return 0
    if n:
        _pe_save()
    return n


def harvest_pe(msg):
    text = msg.get("text") or msg.get("caption") or ""
    ents = list(msg.get("entities") or []) + list(msg.get("caption_entities") or [])
    if not text or not ents:
        return 0
    blob = text.encode("utf-16-le")
    n = 0
    for e in ents:
        if e.get("type") != "custom_emoji":
            continue
        try:
            off = int(e.get("offset") or 0)
            ln = int(e.get("length") or 0)
            ch = blob[off * 2 : (off + ln) * 2].decode("utf-16-le")
        except Exception:
            continue
        cid = str(e.get("custom_emoji_id") or "")
        if ch and cid:
            if _pe_map.get(ch) != cid:
                n += 1
            _pe_map[ch] = cid
    if n:
        _pe_save()
    return n


def send_pe_echo(token, chat_id, msg):
    """Echo harvested premium emoji via entities (Bot API 9.4 / owner Premium)."""
    ents = [e for e in (msg.get("entities") or []) if e.get("type") == "custom_emoji"]
    text = msg.get("text") or ""
    if not ents or not text:
        return False
    pref = u"ست شد. این ایموجی‌های پریمیوم ذخیره شدن:\n"
    pref_u16 = len(pref.encode("utf-16-le")) // 2
    new_ents = []
    for e in ents:
        cid = str(e.get("custom_emoji_id") or "")
        if not cid:
            continue
        new_ents.append(
            {
                "type": "custom_emoji",
                "offset": int(e.get("offset") or 0) + pref_u16,
                "length": int(e.get("length") or 0),
                "custom_emoji_id": cid,
            }
        )
    if not new_ents:
        return False
    payload = {
        "chat_id": chat_id,
        "text": pref + text,
        "entities": new_ents,
        "disable_web_page_preview": True,
        "allow_sending_without_reply": True,
    }
    try:
        r = http().post(tg_api(token) + "/sendMessage", json=payload, timeout=12)
        js = r.json() if r.content else {}
        if js.get("ok"):
            log("pe echo ok n=%s map=%s" % (len(new_ents), len(_pe_map)))
            return True
        log("pe echo fail " + str(js)[:220])
    except Exception:
        log("pe echo " + traceback.format_exc())
    return False


def load_pe_sets(token):
    """Load harvested premium emoji only. Do not scan random sticker packs."""
    _pe_load_file()
    _pe_tried[0] = True


def tz_head(line=None):
    s = u"<b>TZ FX</b>"
    if line:
        s += u" · " + line
    return s + u"\n"


def tz_foot():
    return u"\n<blockquote>%s</blockquote>" % T("brand.foot")


def share_url():
    try:
        from urllib.parse import quote
    except ImportError:
        from urllib import quote
    text = (
        u"TZ FX — ICT برای یورو، پوند، طلا و کریپتو بتا. "
        u"آموزشی است، مشاوره مالی نیست."
    )
    return "https://t.me/share/url?url=%s&text=%s" % (
        quote(BOT_URL, safe=""),
        quote(text),
    )


def kb_home():
    return {"inline_keyboard": [[btn(u"🏠 TZ FX", "home", style="primary")]]}



def _live_mod():
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import live_exec

    live_exec.HERE = HERE
    return live_exec


def kb_connect():
    try:
        lx = _live_mod()
        cfg = lx.load_cfg()
    except Exception:
        cfg = {"demo": True, "crypto_on": False, "mt5_on": False, "crypto_venue": "binance"}
    cv = cfg.get("crypto_venue") or "binance"
    on_c = bool(cfg.get("crypto_on"))
    on_m = bool(cfg.get("mt5_on"))
    def mark(code, lab):
        return (u"✓ " + lab) if cv == code else lab
    return {
        "inline_keyboard": [
            [
                btn(mark("binance", "Binance"), "lv_v_binance", style="success" if cv == "binance" else "primary"),
                btn(mark("bybit", "Bybit"), "lv_v_bybit", style="success" if cv == "bybit" else "primary"),
                btn(mark("okx", "OKX"), "lv_v_okx", style="success" if cv == "okx" else "primary"),
            ],
            [
                btn(mark("bitget", "Bitget"), "lv_v_bitget", style="success" if cv == "bitget" else "primary"),
                btn(mark("bingx", "BingX"), "lv_v_bingx", style="success" if cv == "bingx" else "primary"),
            ],
            [
                btn(u"کلید API", "lv_keys", style="primary"),
                btn(u"بریج MT5", "lv_bridge", style="success"),
            ],
            [
                btn(u"صرافی " + (u"روشن" if on_c else u"خاموش"), "lv_crypto_tog", style="success" if on_c else "primary"),
                btn(u"MT5 " + (u"روشن" if on_m else u"خاموش"), "lv_mt5_tog", style="success" if on_m else "primary"),
            ],
            [btn(u"🏠 خانه", "home", style="primary")],
        ]
    }


def txt_connect():
    try:
        lx = _live_mod()
        cfg = lx.load_cfg()
        cv = cfg.get("crypto_venue") or "binance"
        has = lx.has_keys(cv)
        body = (
            u"دمو است. سفارش به حساب واقعی نمی‌رود.\n"
            u"صرافی: <b>%s</b> · کلید %s\n"
            u"MT5: %s\n"
            u"ریسک ۱٪ · حد ضرر اجباری"
            % (
                lx.venue_label(cv),
                u"هست" if has else u"نیست — بفرست",
                u"روشن" if cfg.get("mt5_on") else u"خاموش",
            )
        )
    except Exception:
        body = u"اتصال آماده است. صرافی را بزن، بعد کلید."
    return tz_head(u"اتصال") + body + u"\n" + tz_foot()


def live_on_signal(token, sig, pair=None):
    try:
        lx = _live_mod()
        cfg = lx.load_cfg()
        if not (cfg.get("crypto_on") or cfg.get("mt5_on")):
            return
        if lx.open_count() >= 2:
            return
        reps = lx.on_signal(sig, pair, 10000.0)
        if not reps:
            return
        for rec in reps:
            send_message(
                token,
                OWNER_ID,
                (
                    tz_head(u"اجرا " + (u"دمو" if rec.get("demo") else u"زنده"))
                    + u"%s <b>%s</b>  %s\n"
                    u"ورود %s  SL %s  TP %s\n"
                    u"%s · %s\n"
                    u"<i>حد ضرر اجباری · سیگنال الکی نیست</i>"
                    % (
                        rec.get("venue") or "",
                        rec.get("pair"),
                        rec.get("side"),
                        rec.get("entry"),
                        rec.get("sl"),
                        rec.get("tp"),
                        rec.get("status"),
                        rec.get("note") or "",
                    )
                ),
                kb_connect(),
            )
    except Exception:
        log("live sig " + traceback.format_exc())


def _scrub_msg(token, chat_id, mid):
    try:
        http().post(
            tg_api(token) + "/deleteMessage",
            json={"chat_id": chat_id, "message_id": int(mid)},
            timeout=6,
        )
    except Exception:
        pass


def handle_exch_wait(token, user_id, chat_id, text, mid):
    if not is_owner(user_id):
        return False
    w = get_wait(user_id)
    kind = w.get("kind") or ""
    if not kind.startswith("exch_"):
        return False
    venue = w.get("venue") or "binance"
    step = w.get("step") or "key"
    raw = (text or "").strip()
    if not raw or raw.startswith("/"):
        return False
    _scrub_msg(token, chat_id, mid)
    try:
        lx = _live_mod()
    except Exception:
        send_message(token, chat_id, u"ماژول اتصال لود نشد.", kb_connect())
        pop_wait(user_id)
        return True
    if step == "key":
        set_wait(user_id, "exch_secret", extra={"venue": venue, "step": "secret", "key": raw})
        send_message(token, chat_id, u"حالا Secret را بفرست.", kb_connect())
        return True
    if step == "secret":
        key = w.get("key") or ""
        if lx.needs_passphrase(venue):
            set_wait(
                user_id,
                "exch_pass",
                extra={"venue": venue, "step": "pass", "key": key, "secret": raw},
            )
            send_message(token, chat_id, u"Passphrase را بفرست.", kb_connect())
            return True
        lx.save_keys(venue, key, raw)
        pop_wait(user_id)
        send_message(token, chat_id, u"کلید %s ذخیره شد. تست اتصال را بزن." % venue, kb_connect())
        return True
    if step == "pass":
        lx.save_keys(venue, w.get("key") or "", w.get("secret") or "", raw)
        pop_wait(user_id)
        send_message(token, chat_id, u"کلید %s ذخیره شد." % venue, kb_connect())
        return True
    pop_wait(user_id)
    return True


def send_bridge_file(token, chat_id):
    path = os.path.join(HERE, "tz_mt5_bridge.py")
    try:
        lx = _live_mod()
        tok = lx.load_cfg().get("bridge_token") or ""
    except Exception:
        tok = ""
    cap = (
        u"روی ویندوز کنار MT5:\n"
        u"pip install MetaTrader5 requests\n"
        u"python tz_mt5_bridge.py %s %s\n"
        u"اول حساب دمو بروکر را در متاتریدر باز کن."
        % (LIVE_BRIDGE_URL, tok)
    )
    try:
        with open(path, "rb") as f:
            http().post(
                tg_api(token) + "/sendDocument",
                data={"chat_id": str(chat_id), "caption": cap[:1000]},
                files={"document": ("tz_mt5_bridge.py", f, "text/x-python")},
                timeout=30,
            )
        return True
    except Exception:
        log("bridge file " + traceback.format_exc())
        send_message(token, chat_id, cap, kb_connect(), parse_mode=None)
        return False


def handle_bridge_http(environ, start_response):
    try:
        lx = _live_mod()
        token = _qs_get(environ, "token")
        ack = _qs_get(environ, "ack")
        if ack:
            ok = lx.bridge_ack(token, ack, _qs_get(environ, "status"), _qs_get(environ, "note"))
            body = json.dumps({"ok": bool(ok)}).encode("utf-8")
            start_response("200 OK", [("Content-Type", "application/json")])
            return [body]
        snap = lx.bridge_snapshot(token)
        if snap is None:
            start_response("403 Forbidden", [("Content-Type", "application/json")])
            return [b'{"ok":false}']
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(snap).encode("utf-8")]
    except Exception:
        log("bridge http " + traceback.format_exc())
        start_response("500 OK", [("Content-Type", "application/json")])
        return [b'{"ok":false}']


def kb_main(uid=None):
    if uid:
        try:
            use_lang(uid)
        except Exception:
            pass
    rows = [
        [btn(T("btn.miniapp"), web_app=APP_URL, style="success")],
        [
            btn(T("btn.eur"), "sig_EURUSD", style="primary"),
            btn(T("btn.gbp"), "sig_GBPUSD", style="primary"),
            btn(T("btn.xau"), "sig_XAUUSD", style="success"),
        ],
        [
            btn(T("btn.crypto"), "crypto_menu", style="success"),
            btn(T("btn.all3"), "sig_ALL", style="success"),
        ],
        [
            btn(T("btn.coach"), "chat_ai", style="primary"),
            btn(T("btn.learn"), "edu_menu"),
        ],
        [
            btn(T("btn.wr"), "wr_menu", style="success"),
            btn(T("btn.sub"), "my_sub" if (uid and is_pro(uid)) else "sub_me", style="primary"),
        ],
        [
            btn(T("btn.support"), "support", style="primary"),
            btn(T("btn.donate"), "donate"),
            btn(T("btn.lang"), "lang_toggle"),
        ],
    ]
    if uid and is_owner(uid):
        rows.append(
            [
                btn(T("btn.connect"), "connect_menu", style="success"),
                btn(T("btn.paper"), "paper_menu"),
            ]
        )
    return {"inline_keyboard": rows}


def kb_after():
    return {
        "inline_keyboard": [
            [
                btn(T("btn.eur"), "sig_EURUSD", style="primary"),
                btn(T("btn.gbp"), "sig_GBPUSD", style="primary"),
                btn(T("btn.xau"), "sig_XAUUSD", style="success"),
            ],
            [
                btn(T("btn.crypto"), "crypto_menu", style="success"),
                btn(T("btn.coach"), "chat_ai", style="primary"),
            ],
            [btn(T("btn.hear"), "hear", style="success"), btn(T("btn.lang"), "lang_toggle")],
            [btn(T("btn.home"), "home", style="primary")],
        ]
    }


def kb_open_bot(start="signal"):
    """Channel/group buttons: always open private chat with the bot."""
    u = BOT_URL + "?start=" + start
    return {
        "inline_keyboard": [
            [btn(u"🚀 باز کردن TZ FX", url=u, style="success")],
            [
                btn(u"💶 یورو", url=BOT_URL + "?start=eur", style="primary"),
                btn(u"💷 پوند", url=BOT_URL + "?start=gbp", style="primary"),
                btn(u"🥇 طلا", url=BOT_URL + "?start=gold", style="success"),
            ],
            [
                btn(u"🎓 آموزش", url=BOT_URL + "?start=learn"),
                btn(u"📐 معامله", url=BOT_URL + "?start=trade", style="primary"),
            ],
            [btn(u"📊 وین‌ریت", url=BOT_URL + "?start=wr", style="primary")],
            [btn(u"🛟 پشتیبانی", url=BOT_URL + "?start=support", style="primary")],
            [btn(u"📤 معرفی TZ FX", url=share_url(), style="primary")],
        ]
    }


def kb_risk():
    return {
        "inline_keyboard": [
            [
                {"text": "$100", "callback_data": "risk_100"},
                {"text": "$250", "callback_data": "risk_250"},
                {"text": "$500", "callback_data": "risk_500"},
            ],
            [
                {"text": "$1,000", "callback_data": "risk_1000"},
                {"text": "$2,500", "callback_data": "risk_2500"},
                {"text": "$5,000", "callback_data": "risk_5000"},
            ],
            [{"text": "🔙 بازگشت", "callback_data": "help"}],
        ]
    }


def kb_edu():
    return {
        "inline_keyboard": [
            [btn(T("btn.lvl1"), "edul1", style="primary")],
            [btn(T("btn.lvl2"), "edul2", style="primary")],
            [btn(T("btn.lvl3"), "edul3", style="success")],
            [btn(T("btn.lvl4"), "edul4")],
            [btn(T("btn.lvl5"), "edul5", style="success")],
            [btn(T("btn.ask_all"), "eq_0", style="success")],
            [btn(u"🏠 TZ FX", "home", style="primary")],
        ]
    }


EDU_LEVELS = {
    "1": ["edu_1", "edu_2", "edu_3", "edu_4", "edu_5"],
    "2": ["edu_6", "edu_7", "edu_8", "edu_9", "edu_10", "edu_11", "edu_12"],
    "3": ["edu_13", "edu_14", "edu_15", "edu_16", "edu_17", "edu_18", "edu_19"],
    "4": ["edu_20", "edu_21", "edu_22", "edu_23", "edu_24"],
    "5": ["edu_25", "edu_26"],
}

EDU_TITLE = {
    "edu_1": u"ترید یعنی چه؟",
    "edu_2": u"پیپ، لات، اسپرد، مارجین",
    "edu_3": u"متاتریدر از صفر",
    "edu_4": u"ورود، حد ضرر، حد سود",
    "edu_5": u"مدیریت سرمایه ۱٪",
    "edu_6": u"مدل ICT",
    "edu_7": u"نقدینگی BSL و SSL",
    "edu_8": u"سوئیپ و Judas Swing",
    "edu_9": u"جابجایی (Displacement)",
    "edu_10": u"FVG شکاف ارزش",
    "edu_11": u"پرمیوم و دیسکانت",
    "edu_12": u"مدل کامل یک ستاپ ICT",
    "edu_13": u"OTE ناحیه طلایی",
    "edu_14": u"اوردر بلاک و بریکر",
    "edu_15": u"کیل‌زون لندن و نیویورک",
    "edu_16": u"Silver Bullet",
    "edu_17": u"جهت تایم بالا D1/H4/H1",
    "edu_18": u"طلا در ICT",
    "edu_19": u"چه زمانی معامله نکنیم",
    "edu_20": u"روانشناسی ترید",
    "edu_21": u"مدیریت پوزیشن بعد ورود",
    "edu_22": u"دفتر معامله",
    "edu_23": u"کار با TZ FX BOT",
    "edu_24": u"چک‌لیست قبل از کلیک",
    "edu_25": u"کلید API صرافی",
    "edu_26": u"اتصال به بروکر و ربات",
}

EDU_SPEAK = {
    "edu_1": (
        u"رفیق، درس یک. ترید یعنی خرید یا فروش با پیش‌بینی جهت قیمت. "
        u"میز فارکس یورو، پوند و طلاست. کریپتو بتا جداست. "
        u"هر معامله سه عدد اجباری دارد: ورود، حد ضرر، حد سود. بدون این سه تا قمار است. "
        u"بیشتر حساب‌های تازه‌کار با حجم زیاد و بدون حد ضرر صفر می‌شوند. قول سود نمی‌دهیم."
    ),
    "edu_2": (
        u"درس دو. پیپ کوچک‌ترین حرکت قیمت است. یورو و پوند رقم چهارم، طلا حدود یک دهم دلار. "
        u"لات حجم معامله است. برای حساب کوچک از صفر ممیز صفر یک شروع کن. "
        u"اسپرد هزینه ورود بروکر است. اهرم سود را بزرگ نمی‌کند، اشتباه را سریع‌تر می‌کشد. "
        u"اگر ضرر به مارجین برسد حساب را اجباری می‌بندند."
    ),
    "edu_3": (
        u"درس سه. متاتریدر را روی دمو باز کن، نه حساب واقعی. "
        u"نماد را پیدا کن، چارت را روی یک‌ساعته یا پانزده‌دقیقه بگذار. "
        u"سفارش جدید: حجم، حد ضرر، حد سود. بدون حد ضرر دکمه را نزن. "
        u"ربات سیگنال می‌دهد؛ اجرای بروکر روی ویندوز با بریج است. سرور ربات متاتریدر ندارد."
    ),
    "edu_4": (
        u"درس چهار. ورود جایی است که ستاپ کامل شده، نه هر جایی که دلت خواست. "
        u"حد ضرر آن‌سوی ویکی است که نقدینگی را جارو کرده. "
        u"حد سود نقدینگی داخلی طرف مقابل. بدون حد ضرر ورود ممنوع. تعقیب قیمت بعد از حرکت ممنوع."
    ),
    "edu_5": (
        u"درس پنج. حداکثر یک درصد حساب در هر معامله. "
        u"اگر حد ضرر بزند، حساب زنده می‌ماند. اگر دو درصد و پنج درصد بزنی، یک سری باخت حساب را تمام می‌کند. "
        u"حجم را از فاصله ورود تا حد ضرر حساب کن، نه از حس. پیپر برای تمرین است، پول واقعی نیست."
    ),
    "edu_6": (
        u"درس شش. مدل ما فقط آی سی تی ICT است. مولتی‌ستاپ نداریم. "
        u"ترتیب: جهت تایم بالا، جاروی جوداس، تغییر ساختار با جابجایی، ورود داخل شکاف ارزش یا او تی ای، "
        u"حد ضرر پشت ویک جارو، حد سود نقدینگی داخلی. اگر یکی ناقص است، صبر."
    ),
    "edu_7": (
        u"درس هفت. نقدینگی بالای سقف‌ها بی اس ال است، زیر کف‌ها اس اس ال. "
        u"بازار می‌رود این سفارش‌های استاپ را شکار کند، بعد برمی‌گردد. "
        u"تو دنبال نقدینگی نرو؛ صبر کن شکار بشود، بعد با جهت اصلی همراه شو."
    ),
    "edu_8": (
        u"درس هشت. جوداس سوینگ یعنی یک حرکت فیک بالای سقف یا زیر کف سشن، برای شکار نقدینگی. "
        u"بعد از جارو باید تغییر ساختار با بدنه قوی ببینی. اگر فقط ویک زد و برگشت ضعیف بود، هنوز ستاپ نیست."
    ),
    "edu_9": (
        u"درس نه. جابجایی یعنی کندل‌های قوی با بدنه بزرگ بعد از جارو. "
        u"بدون جابجایی، تغییر ساختار ضعیف است. ربات بدون این جابجایی سیگنال زنده نمی‌دهد."
    ),
    "edu_10": (
        u"درس ده. شکاف ارزش همان اف وی جی است: کندلی که بین سایه قبلی و بعدی فاصله می‌گذارد. "
        u"ورود فقط داخل این شکاف. اگر قیمت شکاف را رد کرد و رفت، تعقیب نکن. صبر کن ستاپ بعدی."
    ),
    "edu_11": (
        u"درس یازده. نیمه رنج را بکش. بالای نیمه پرمیوم است، پایین دیسکانت. "
        u"خرید را در دیسکانت با جهت صعودی تایم بالا بخواه. فروش را در پرمیوم با جهت نزولی. "
        u"خرید در پرمیوم یعنی دنبال قیمت دویدن."
    ),
    "edu_12": (
        u"درس دوازده. ستاپ کامل ICT این است: جهت تایم بالا، جاروی جوداس، تغییر ساختار، "
        u"شکاف ارزش، ورود داخل شکاف، حد ضرر پشت ویک، حد سود نقدینگی داخلی. "
        u"امتیاز زیر چهار یعنی دست نزن. سیگنال الکی نمی‌سازیم."
    ),
    "edu_13": (
        u"درس سیزده. او تی ای ناحیه طلایی برگشت است، معمولا بین شصت و دو تا هفتاد و نه درصد اصلاح. "
        u"اگر با شکاف ارزش یکی شد، ورود تمیزتر است. اجباری نیست اگر بقیه مدل کامل باشد."
    ),
    "edu_14": (
        u"درس چهارده. اوردر بلاک آخرین کندل مخالف قبل از جابجایی است. بریکر بلاک کندل تغییر ساختار. "
        u"ورود اصلی ما شکاف ارزش است؛ بلاک فقط تایید. بدون جارو و جابجایی، بلاک به درد نمی‌خورد."
    ),
    "edu_15": (
        u"درس پانزده. کیل‌زون لندن و نیویورک جایی است که نقدینگی شکار می‌شود. "
        u"خارج از این پنجره‌ها صبر کن. تهران را ملاک ساعت ربات بگذار. "
        u"سیلور بولت یک پنجره کوتاه داخل نیویورک است، نه جادو."
    ),
    "edu_16": (
        u"درس شانزده. سیلور بولت همان مدل ICT داخل یک پنجره زمانی خاص است. "
        u"اگر جارو و شکاف نباشد، اسم سیلور بولت چیزی را عوض نمی‌کند. تعقیب نکن."
    ),
    "edu_17": (
        u"درس هفده. اول روزانه، بعد چهارساعته، بعد یک‌ساعته. "
        u"اگر روزانه صعودی است، دنبال خرید در دیسکانت پانزده‌دقیقه باش. خلاف روزانه یعنی صبر."
    ),
    "edu_18": (
        u"درس هجده. طلا پرنوسان است. همان مدل ICT، اما حد ضرر را گشاد نگذار که یک درصد را ببلعد. "
        u"اسپرد طلا از یورو بیشتر است. خبر سنگین طلا را با حجم کوچک یا اصلا نزن."
    ),
    "edu_19": (
        u"درس نوزده. نزن اگر: خارج کیل‌زون، خلاف تایم بالا، بدون جارو، بدون شکاف، "
        u"اسپرد پهن، خبر یک دقیقه دیگر، یا دلت شور می‌زند. نزدن خودش معامله است."
    ),
    "edu_20": (
        u"درس بیست. بعد از باخت انتقام نزن. حجم را دو برابر نکن. "
        u"اگر دو باخت پشت هم شد، برو پیاده. مربی برای چک‌لیست است، برای دلداری قمار نیست."
    ),
    "edu_21": (
        u"درس بیست و یک. بعد ورود، حد ضرر را دستکاری نکن که باز بماند. "
        u"اگر خواستی حد را بیاور روی ورود، فقط بعد از رسیدن به حد سود اول. "
        u"از معامله برنده یک بازنده نساز."
    ),
    "edu_22": (
        u"درس بیست و دو. هر معامله را بنویس: نماد، جهت، ورود، حد ضرر، حد سود، چرا، نتیجه. "
        u"بدون دفتر، اشتباه را تکرار می‌کنی. درصد الکی در دفتر ننویس."
    ),
    "edu_23": (
        u"درس بیست و سه. ربات تی زد اف ایکس سیگنال آی سی تی می‌دهد، چارت، مربی و آموزش. "
        u"سیگنال کانال فقط هشت و نیم تا بیست و نیم تهران. داخل ربات بیست‌وچهار ساعته. "
        u"شنبه فارکس بسته است. کریپتو بتا جداست."
    ),
    "edu_24": (
        u"درس بیست و چهار. قبل کلیک: جهت تایم بالا؟ جارو شد؟ تغییر ساختار؟ داخل شکاف؟ "
        u"حد ضرر گذاشتی؟ یک درصد؟ اگر دو تا نه است، نزن. برای مربی بفرست تا با هم خط بزنیم."
    ),
    "edu_25": (
        u"درس بیست و پنج. کلید ای پی آی صرافی فقط مال خودت. در ربات بفرست، پیام پاک می‌شود، لاگ نمی‌شود. "
        u"اول دمو. تا ننویسی لایو، سفارش واقعی نمی‌رود. بیت‌گت و بینگ‌ایکس هم در اتصال هستند. "
        u"کلید را برای کسی نفرست."
    ),
    "edu_26": (
        u"درس بیست و شش. بروکر متاتریدر روی ویندوز است، نه روی سرور ربات. "
        u"از اتصال، بریج را بردار، روی همان پی‌سی که متاتریدر باز است اجرا کن. "
        u"حد ضرر اجباری. پیپر تمرین است. تا لایو ننویسی واقعی نمی‌شود."
    ),
}

EDU_ORDER = (
    EDU_LEVELS["1"]
    + EDU_LEVELS["2"]
    + EDU_LEVELS["3"]
    + EDU_LEVELS["4"]
    + EDU_LEVELS["5"]
)


def _edu_n(key):
    try:
        return int(str(key).split("_")[-1])
    except Exception:
        return 0


def kb_edu_level(lv):
    lv = str(lv)
    keys = EDU_LEVELS.get(lv) or []
    rows = []
    for k in keys:
        n = _edu_n(k)
        rows.append([btn(u"📖 %s. %s" % (fa_num(n), EDU_TITLE.get(k, k)), k, style="primary")])
    rows.append([btn(T("btn.ask_level"), "eq_l" + lv, style="success")])
    rows.append([btn(T("btn.catalog"), "edu_menu"), btn(T("btn.home"), "home")])
    return {"inline_keyboard": rows}


def kb_lesson(key):
    keys = EDU_ORDER
    try:
        i = keys.index(key)
    except Exception:
        i = -1
    prev_k = keys[i - 1] if i > 0 else None
    next_k = keys[i + 1] if 0 <= i < len(keys) - 1 else None
    n = _edu_n(key)
    nav = []
    if prev_k:
        nav.append(btn(u"⬅️ قبلی", prev_k))
    if next_k:
        nav.append(btn(u"بعدی ➡️", next_k, style="primary"))
    rows = [
        [btn(T("btn.ask_lesson"), "eq_%s" % n, style="success")],
        [btn(T("btn.hear_lesson"), "he_%s" % n, style="primary")],
    ]
    if key in ("edu_25", "edu_26"):
        rows.append([btn(u"🔗 رفتن به اتصال", "connect_menu", style="success")])
    if nav:
        rows.append(nav)
    lv = "1"
    for a, ks in EDU_LEVELS.items():
        if key in ks:
            lv = a
            break
    rows.append(
        [
            btn(u"📚 همین سطح", "edul" + lv),
            btn(u"📚 فهرست", "edu_menu"),
            btn(u"🏠 TZ FX", "home"),
        ]
    )
    return {"inline_keyboard": rows}


def edu_intro():
    return (
        tz_head(T("head.learn"))
        + T("txt.edu_intro")
        + u"\n"
        + tz_foot()
    )


EDU = {
    "edu_1": (
        u"🎓 <b>درس ۱ — ترید یعنی چه؟</b>\n"
        u"سطح ۱ · مبتدی\n"
        u"────────────\n"
        u"ترید یعنی خرید یا فروش یک نماد با پیش‌بینی جهت قیمت.\n"
        u"میز فارکس: یورو، پوند، طلا. کریپتو بتا جدا است.\n\n"
        u"• <b>BUY</b> = انتظار رشد. ارزان می‌خری، گران می‌فروشی.\n"
        u"• <b>SELL</b> = انتظار ریزش. گران می‌فروشی، ارزان می‌خری.\n\n"
        u"بازار ۲۴ ساعته است (دوشنبه تا جمعه). بانک‌ها و صندوق‌ها حجم اصلی را می‌سازند، نه تو.\n\n"
        u"<b>سه عدد اجباری هر معامله:</b>\n"
        u"۱) ورود  ۲) حد ضرر  ۳) حد سود\n"
        u"بدون این سه تا، قمار است نه ترید.\n\n"
        u"<b>حقیقت تلخ:</b> بیشتر حساب‌های تازه‌کار به خاطر حجم زیاد و نداشتن حد ضرر صفر می‌شوند، نه به خاطر «نمی‌دانستند بازار کجا می‌رود».\n\n"
        u"هدف این دوره: بفهمی ICT چطور نقدینگی را شکار می‌کند، کی وارد شوی، کی اصلاً دست نزنی.\n\n"
        u"<i>قول سود نمی‌دهیم. درصد دقت الکی نیست.</i>"
    ),
    "edu_2": (
        u"🎓 <b>درس ۲ — پیپ، لات، اسپرد، مارجین</b>\n"
        u"سطح ۱ · مبتدی\n"
        u"────────────\n"
        u"<b>پیپ</b> کوچک‌ترین حرکت قیمت است که با آن ضرر/سود را می‌سنجیم.\n"
        u"• یورو و پوند: ۱ پیپ = ۰.۰۰۰۱ (رقم چهارم)\n"
        u"• طلا: در این ربات ۱ واحد = ۰.۱ دلار\n\n"
        u"<b>لات</b> حجم معامله است.\n"
        u"۱.۰۰ لات استاندارد ≈ ۱۰۰٬۰۰۰ واحد ارز، یا ۱۰۰ اونس طلا.\n"
        u"۰.۱۰ لات = مینی · ۰.۰۱ لات = میکرو.\n"
        u"برای حساب کوچک تقریباً همیشه با ۰.۰۱ شروع کن.\n\n"
        u"<b>اسپرد</b> فاصله خرید و فروش بروکر است — هزینه ورود.\n"
        u"یورو معمولاً حدود ۱ پیپ، طلا چند دهم دلار. اسپرد پهن = ورود گران‌تر.\n\n"
        u"<b>اهرم</b> یعنی با پول کم، حجم بزرگ باز کنی. ۱:۱۰۰ یعنی با ۱۰۰ دلار می‌توانی حدود ۱۰٬۰۰۰ دلار کنترل کنی.\n"
        u"اهرم سود را بزرگ نمی‌کند؛ <b>اشتباه را سریع‌تر می‌کشد</b>.\n\n"
        u"<b>مارجین</b> وثیقه‌ای است که بروکر قفل می‌کند. اگر ضرر به مارجین برسد، کال‌مارجین و بسته شدن اجباری.\n\n"
        u"دکمه 📐 اطلاعات معامله همین‌ها را برای سیگنال زنده حساب می‌کند."
    ),
    "edu_3": (
        u"🎓 <b>درس ۳ — متاتریدر از صفر</b>\n"
        u"سطح ۱ · مبتدی\n"
        u"────────────\n"
        u"متاتریدر ۴ یا ۵ نرم‌افزار بروکر است. ربات سیگنال می‌دهد؛ اجرا با توست.\n\n"
        u"<b>مسیر سفارش:</b>\n"
        u"۱) نماد را پیدا کن: EURUSD / GBPUSD / XAUUSD\n"
        u"۲) New Order\n"
        u"۳) Volume = همان لات محاسبه‌شده\n"
        u"۴) Buy سبز یا Sell قرمز — طبق سیگنال\n"
        u"۵) فوری Stop Loss و Take Profit را روی عدد سیگنال بگذار\n\n"
        u"<b>مارکت</b> = همین الان پر می‌شود (اسپرد را می‌پردازی).\n"
        u"<b>پندینگ</b> = صبر می‌کند قیمت به سطح برسد. ICT اغلب ورود داخل FVG است؛ اگر قیمت رفته، تعقیب نکن.\n\n"
        u"<b>قانون اجرا:</b>\n"
        u"عدد سیگنال را عوض نکن تا «شاید بهتر شود». اگر اسپرد زنده خیلی پهن بود، نزن.\n"
        u"اول حساب <b>دمو</b>. واقعی فقط وقتی ۲۰ معامله دمو را با قانون ۱٪ تمام کردی.\n\n"
        u"اگر بلد نیستی دکمه اطلاعات معامله را بزن — مرحله‌به‌مرحله می‌گوید چه دکمه‌ای را بزن."
    ),
    "edu_4": (
        u"🎓 <b>درس ۴ — ورود، حد ضرر، حد سود</b>\n"
        u"سطح ۱ · مبتدی\n"
        u"────────────\n"
        u"هر ستاپ ICT سه نقطه دارد:\n\n"
        u"🎯 <b>ورود</b> جایی است که قیمت به ناحیه ارزش (معمولاً FVG یا OTE) برگشته.\n"
        u"🛡 <b>حد ضرر (SL)</b> پشت جاروی نقدینگی. اگر آنجا رفت، ایده باطل است — نه اینکه «یک کم دیگر صبر کن».\n"
        u"🏁 <b>حد سود (TP)</b> نقدینگی مخالف: سقف/کف قبلی که حد ضررها آنجا نشسته‌اند.\n\n"
        u"<b>R:R</b> یعنی نسبت ریوارد به ریسک.\n"
        u"اگر ۱۰ دلار ریسک می‌کنی و هدف ۲۰ دلار است، R:R = ۱:۲.\n"
        u"زیر ۱:۱.۳ در این ربات سیگنال نمی‌آید چون نمی‌ارزد.\n\n"
        u"<b>قانون طلایی:</b> حد ضرر را جابه‌جا نکن تا «شاید برگردد». این رایج‌ترین راه صفر شدن حساب است.\n\n"
        u"ورود را هم به امید قیمت بهتر عقب ننداز اگر ستاپ دارد از دست می‌رود — یا طبق پلن هستی، یا بیرون."
    ),
    "edu_5": (
        u"🎓 <b>درس ۵ — مدیریت سرمایه ۱٪</b>\n"
        u"سطح ۱ · مبتدی\n"
        u"────────────\n"
        u"قانون اصلی TZ FX: در هر معامله حداکثر <b>۱٪ حساب</b> را ریسک کن.\n\n"
        u"مثال: حساب ۱۰۰۰ دلار، ریسک ۱٪ = ۱۰ دلار.\n"
        u"اگر حد ضرر ۲۲ پیپ باشد، حجم طوری انتخاب می‌شود که ۲۲ پیپ ≈ ۱۰ دلار ضرر شود.\n"
        u"دکمه 📐 اطلاعات معامله همین را حساب می‌کند.\n\n"
        u"<b>چرا ۱٪؟</b>\n"
        u"۱۰ ضرر پشت‌سرهم با ۱٪ ≈ ۹۰٪ حساب هنوز زنده است.\n"
        u"۱۰ ضرر با ۱۰٪ = نابودی.\n"
        u"تریدر می‌ماند چون اندازه اشتباه نمی‌میرد، بعد مهارت می‌آید.\n\n"
        u"<b>قوانین اضافی:</b>\n"
        u"• ۳ ضرر پشت‌سرهم = همان روز تعطیل\n"
        u"• یک نماد، یک پوزیشن — روی هم سوار نکن\n"
        u"• اگر اسپرد بخش بزرگی از فاصله SL است، نزن\n"
        u"• اهرم بالا مجوز حجم بالا نیست\n\n"
        u"مدیریت سرمایه استراتژی نیست؛ اجازه می‌دهد استراتژی زنده بماند."
    ),
    "edu_6": (
        u"🎓 <b>درس ۶ — ICT</b>\n"
        u"سطح ۲ · ICT پایه\n"
        u"────────────\n"
        u"ICT روش مایکل هادلستون است. ICT روی این زنجیره تاکید دارد:\n\n"
        u"<b>نقدینگی → سوئیپ → جابجایی + FVG → برگشت به FVG → ورود</b>\n"
        u"جهت را از تایم بالا (روزانه / ۴ساعته / ۱ساعته) می‌گیری، اجرا در ۱۵دقیقه.\n\n"
        u"ایده مرکزی: بازار می‌رود جایی که حد ضرر جمع شده (نقدینگی)، آن را برمی‌دارد، بعد به سمت هدف واقعی حرکت می‌کند.\n\n"
        u"<b>آنچه ICT نیست:</b>\n"
        u"اندیکاتور رنگارنگ، تقاطع میانگین، سیگنال جادویی، درصد برد تبلیغاتی.\n\n"
        u"این ربات همان مدل را پیاده می‌کند: سوئیپ SSL/BSL، FVG جابجایی، OTE، کیل‌زون، پرمیوم/دیسکانت ۱ساعته، امتیاز ۰ تا ۶.\n"
        u"<b>زیر ۴ را معامله نکن.</b> کانال رایگان حتی سخت‌گیرتر است.\n\n"
        u"مایکل تکرار می‌کند: صبر بخشی از ستاپ است. نبود سیگنال هم سیگنال است."
    ),
    "edu_7": (
        u"🎓 <b>درس ۷ — نقدینگی BSL و SSL</b>\n"
        u"سطح ۲ · ICT پایه\n"
        u"────────────\n"
        u"نقدینگی = انبوه سفارش حد ضرر و پندینگ که بالای سقف‌ها و پایین کف‌ها نشسته.\n\n"
        u"🟢 <b>BSL — Buy Side Liquidity</b>\n"
        u"بالای سقف سوئینگ. کسانی که Sell دارند آنجا حد ضرر دارند؛ کسانی که شکست می‌خواهند آنجا Buy Stop گذاشته‌اند.\n"
        u"قیمت دوست دارد آن سقف را بزند تا سوخت Buy بگیرد.\n\n"
        u"🔴 <b>SSL — Sell Side Liquidity</b>\n"
        u"پایین کف سوئینگ. حد ضرر خریدارها و Sell Stopها.\n"
        u"زدن کف = سوخت Sell.\n\n"
        u"<b>نگاه ICT:</b> سقف و کف «حمایت/مقاومت مقدس» نیستند؛ انبار سوخت‌اند.\n"
        u"قبل از حرکت واقعی، معمولاً یک سمت نقدینگی جارو می‌شود.\n\n"
        u"روی چارت ربات اگر سیگنال باشد، نقدینگی خرید و فروش را می‌بینی. هدف TP غالباً نقدینگی مخالف است، نه یک عدد رند تصادفی."
    ),
    "edu_8": (
        u"🎓 <b>درس ۸ — سوئیپ و Judas Swing</b>\n"
        u"سطح ۲ · ICT پایه\n"
        u"────────────\n"
        u"<b>سوئیپ</b> یعنی قیمت سطح نقدینگی را می‌زند و برمی‌گردد؛ بدنه کندل آن طرف سطح نمی‌ماند.\n"
        u"مثال: کف را می‌شکند (SSL)، دم بلند می‌گذارد، می‌بندد بالای کف. خریدارهای استاپ‌خورده سوخت شدند.\n\n"
        u"<b>Judas Swing</b> (منتورشیپ): حرکت فریب اول سشن — معمولاً لندن — که خلاف جهت روز می‌رود، نقدینگی را برمی‌دارد، بعد برمی‌گردد به جهت واقعی.\n"
        u"اگر اول لندن همه را ریخت پایین و بعد برگشت بالا، آن ریزش ممکن است Judas باشد نه شروع روند نزولی.\n\n"
        u"<b>سوئیپ به‌تنهایی سیگنال نیست.</b>\n"
        u"باید بعدش جابجایی و FVG بیاید. وگرنه فقط یک شکن ساختگی است.\n\n"
        u"ربات دنبال سوئیپ ۱۶ کندل اخیر ۱۵دقیقه است. اگر جارو نباشد: NO SIGNAL."
    ),
    "edu_9": (
        u"🎓 <b>درس ۹ — جابجایی (Displacement)</b>\n"
        u"سطح ۲ · ICT پایه\n"
        u"────────────\n"
        u"جابجایی = کندل قوی با بدنه بزرگ که بازار را از یک سمت به سمت دیگر پرتاب می‌کند.\n"
        u"نشان می‌دهد پول هوشمند تصمیم گرفته، نه یک نوسان ضعیف.\n\n"
        u"نشانه‌ها:\n"
        u"• بدنه بخش زیادی از کل کندل است (سایه کوچک)\n"
        u"• معمولاً یک یا چند FVG پشت سر جا می‌گذارد\n"
        u"• ساختار قبلی را می‌شکند\n\n"
        u"بدون جابجایی، FVG ضعیف است — شکاف تصادفی، نه ردپای سفارش بزرگ.\n\n"
        u"ربات کندل FVG را چک می‌کند: اگر نسبت بدنه به دامنه کافی باشد امتیاز «جابجایی» می‌گیرد.\n\n"
        u"<b>تمرین:</b> در ۱۵دقیقه یورو، دنبال کندلی بگرد که بعد از زدن کف، با بدنه سبز قوی برگردد. همان کاندیدای displacement صعودی است."
    ),
    "edu_10": (
        u"🎓 <b>درس ۱۰ — FVG شکاف ارزش منصفانه</b>\n"
        u"سطح ۲ · ICT پایه\n"
        u"────────────\n"
        u"FVG یعنی بین کندل ۱ و ۳ یک شکاف می‌ماند که کندل وسط نپوشانده.\n\n"
        u"🟢 FVG صعودی: کف کندل ۳ بالاتر از سقف کندل ۱. خریدارها عجله داشتند.\n"
        u"🔴 FVG نزولی: سقف کندل ۳ پایین‌تر از کف کندل ۱.\n\n"
        u"<b>ورود حرفه‌ای داخل FVG است</b> نه بعد از اینکه قیمت فرار کرده.\n"
        u"اگر شکاف کاملاً پر شد و قیمت آن طرف بست، ستاپ غالباً سوخته.\n\n"
        u"ربات بعد از سوئیپ فقط FVG هم‌جهت جابجایی را می‌گیرد. اگر قیمت خیلی از شکاف دور شده باشد صبر می‌دهد تا برگردد.\n\n"
        u"روی چارت، ناحیه رنگی همان FVG است. ورود بین سقف و کف همان ناحیه است.\n\n"
        u"FVG تنها کافی نیست: سوئیپ قبلش + جهت تایم بالا + کیل‌زون = ستاپ کامل."
    ),
    "edu_11": (
        u"🎓 <b>درس ۱۱ — پرمیوم و دیسکانت</b>\n"
        u"سطح ۲ · ICT پایه\n"
        u"────────────\n"
        u"در یک نوسان مشخص (این ربات: حدود ۲۴ کندل ۱ساعته):\n"
        u"وسط دامنه = تعادل (Equilibrium).\n"
        u"پایین وسط = <b>دیسکانت</b> (ارزان‌تر) · بالای وسط = <b>پرمیوم</b> (گران‌تر).\n\n"
        u"قانون ساده ICT:\n"
        u"• BUY را در دیسکانت بخواه، نه در پرمیوم.\n"
        u"• SELL را در پرمیوم بخواه، نه در دیسکانت.\n\n"
        u"خرید در گرانی یعنی تو داری نقدینگی فروشنده‌ها را می‌دهی.\n\n"
        u"ربات این را روی ۱ساعته فیلتر می‌کند. اگر BUY در پرمیوم باشد هشدار می‌آید و امتیاز کامل نمی‌شود.\n"
        u"کانال رایگان ستاپ خلاف پرمیوم/دیسکانت را معمولاً پست نمی‌کند.\n\n"
        u"اول بپرس: «قیمت الان ارزان است یا گران نسبت به نوسان اخیر؟» بعد سمت را انتخاب کن."
    ),
    "edu_12": (
        u"🎓 <b>درس ۱۲ — مدل کامل یک ستاپ ICT</b>\n"
        u"سطح ۲ · ICT پایه\n"
        u"────────────\n"
        u"زنجیره را از حفظ بگو:\n\n"
        u"۱) جهت روزانه / ۴ساعته را بخوان (درس ۱۷)\n"
        u"۲) صبر کن قیمت به کیل‌زون برسد (درس ۱۵)\n"
        u"۳) نقدینگی مخالف جهت را جارو کند (سوئیپ)\n"
        u"۴) جابجایی + FVG هم‌جهت ساخته شود\n"
        u"۵) قیمت به FVG / OTE برگردد\n"
        u"۶) ورود، حد ضرر پشت سوئیپ، حد سود نقدینگی مخالف\n"
        u"۷) اگر امتیاز زیر ۴ یا R:R ضعیف یا خلاف روزانه: نزن\n\n"
        u"مثال آموزشی (نه قیمت زنده):\n"
        u"روزانه صعودی است. لندن کف آسیا را می‌زند و برمی‌گردد (SSL sweep).\n"
        u"کندل قوی سبز FVG می‌سازد. قیمت به نیمه FVG برمی‌گردد.\n"
        u"BUY، SL زیر دم سوئیپ، TP سقف دیروز (BSL).\n\n"
        u"اگر یکی از حلقه‌ها نباشد، ستاپ نیست — صبر است."
    ),
    "edu_13": (
        u"🎓 <b>درس ۱۳ — OTE ناحیه طلایی</b>\n"
        u"سطح ۳ · پیشرفته\n"
        u"────────────\n"
        u"OTE = Optimal Trade Entry. برگشت قیمت داخل ۶۲ تا ۷۹ درصد حرکت جابجایی.\n\n"
        u"بعد از سوئیپ و پرتاب، بازار معمولاً بخشی از مسیر را برمی‌گردد تا سفارش‌های جا مانده را پر کند.\n"
        u"ورود در این برگشت بهتر از تعقیب سقف/کف است.\n\n"
        u"برای BUY: از سقف جابجایی پایین بیا؛ ناحیه ۰.۶۲ تا ۰.۷۹ همان OTE است (نزدیک FVG).\n"
        u"برای SELL: از کف جابجایی بالا بیا؛ همان نسبت.\n\n"
        u"ربات اگر قیمت یا وسط FVG داخل OTE باشد امتیاز OTE می‌دهد.\n\n"
        u"<b>اشتباه رایج:</b> ورود وسط پرتاب، چون «جا نمانم». ICT می‌گوید جا ماندن بهتر از ورود هیجانی است. ستاپ بعدی می‌آید."
    ),
    "edu_14": (
        u"🎓 <b>درس ۱۴ — اوردر بلاک و بریکر</b>\n"
        u"سطح ۳ · پیشرفته\n"
        u"────────────\n"
        u"<b>Order Block</b> آخرین کندل مخالف قبل از جابجایی قوی است.\n"
        u"مثال: چند کندل قرمز، بعد پرتاب سبز. آخرین قرمز ≈ اوردر بلاک صعودی. قیمت غالباً برای پر کردن سفارش به آن برمی‌گردد.\n\n"
        u"<b>Breaker</b> وقتی اوردر بلاک می‌شکند و نقش عوض می‌کند.\n"
        u"حمایت شکسته شده می‌تواند مقاومت شود (و برعکس). ورود روی بریکر یعنی سوار شدن روی کسانی که در بلاک قبلی گیر کردند.\n\n"
        u"ربات فعلاً هسته ICT را روی سوئیپ+FVG می‌چرخاند؛ بلاک و بریکر را برای چشم توست تا سیگنال را تایید کنی.\n\n"
        u"اگر FVG داخل یک اوردر بلاک هم‌جهت تایم بالا باشد، تلاقی قوی‌تر است.\n"
        u"اگر بلاک واضح خلاف جهت روزانه است، آن را بهانه ورود خلاف جریان نکن."
    ),
    "edu_15": (
        u"🎓 <b>درس ۱۵ — کیل‌زون لندن و نیویورک</b>\n"
        u"سطح ۳ · پیشرفته\n"
        u"────────────\n"
        u"نقدینگی وقتی جابه‌جا می‌شود که لندن و نیویورک بازند. آسیا غالباً رنج می‌سازد؛ لندن آن را شکار می‌کند.\n\n"
        u"وقت تهران (بدون DST):\n"
        u"• لندن ≈ ۱۰:۳۰ تا ۱۳:۳۰\n"
        u"• نیویورک ≈ ۱۵:۳۰ تا ۱۹:۳۰\n"
        u"همپوشانی لندن-نیویورک معمولاً پرنوسان‌ترین تکه روز است.\n\n"
        u"خارج کیل‌زون هم حرکت هست، ولی سوخت بانک کمتر است. ربات اگر خارج کیل‌زون باشد امتیاز آن را نمی‌دهد.\n\n"
        u"<b>آسیا:</b> سقف و کف آسیا همان نقدینگی Judas لندن است. اول لندن اغلب یکی از دو طرف آسیا را می‌زند.\n\n"
        u"اگر نیمه شب بیدار شدی و سیگنال ضعیف دیدی، زور نزن. صبر تا کیل‌زون بخشی از استراتژی است."
    ),
    "edu_16": (
        u"🎓 <b>درس ۱۶ — Silver Bullet</b>\n"
        u"سطح ۳ · پیشرفته\n"
        u"────────────\n"
        u"Silver Bullet پنجره زمانی ICT است که غالباً یک FVG قابل معامله در جهت نقدینگی می‌سازد.\n\n"
        u"پنجره‌های معروف (ساعت جهانی تقریباً):\n"
        u"• لندن باز\n"
        u"• نیویورک باز (حدود ۱۰ صبح نیویورک)\n"
        u"• بعدازظهر نیویورک\n\n"
        u"ربات اگر ساعت جاری یکی از این پنجره‌ها باشد امتیاز Silver Bullet می‌دهد.\n\n"
        u"این جادو نیست. فقط احتمال حضور سفارش بزرگ بیشتر است.\n"
        u"داخل پنجره هم اگر سوئیپ و FVG نباشد، نزن.\n"
        u"خارج پنجره هم ستاپ عالی را فقط به خاطر ساعت رد نکن — فقط امتیازش کمتر است."
    ),
    "edu_17": (
        u"🎓 <b>درس ۱۷ — جهت تایم بالا D1 / H4 / H1</b>\n"
        u"سطح ۳ · پیشرفته\n"
        u"────────────\n"
        u"۱۵دقیقه بدون جهت بالا = نویز.\n\n"
        u"ترتیب خواندن:\n"
        u"۱) <b>روزانه</b>: سوئینگ‌ها بالا می‌روند یا پایین؟ خلاف روزانه معامله نکن مگر شاگرد پیشرفته با دلیل.\n"
        u"۲) <b>۴ساعته</b>: آیا با روزانه هم‌جهت است؟\n"
        u"۳) <b>۱ساعته</b>: پرمیوم یا دیسکانت؟ ورود را اینجا زمان‌بندی کن.\n"
        u"۴) <b>۱۵دقیقه</b>: سوئیپ + FVG اجرا.\n\n"
        u"ربات روی سیگنال، جهت ۱ساعته و ۴ساعته و روزانه را نشان می‌دهد.\n"
        u"اگر خلاف روزانه باشد امتیاز سقف ۳ می‌گیرد و هشدار می‌آید — یعنی ترجیحاً رد.\n\n"
        u"دکمه مولتی‌تایم زیر سیگنال را بزن تا همه تایم‌ها را یک‌جا ببینی.\n"
        u"هم‌جهت بودن تایم‌ها = اجازه. اختلاف آن‌ها = صبر."
    ),
    "edu_18": (
        u"🎓 <b>درس ۱۸ — طلا در ICT</b>\n"
        u"سطح ۳ · پیشرفته\n"
        u"────────────\n"
        u"طلا (XAUUSD) همان منطق نقدینگی را دارد، با سه تفاوت:\n\n"
        u"۱) <b>نوسان بزرگ‌تر</b> — حد ضرر دلاری سریع‌تر پر می‌شود. حجم را کوچک‌تر بگیر.\n"
        u"۲) <b>اسپرد</b> معمولاً از یورو پهن‌تر است. اسپرد را حتماً در اطلاعات معامله وارد کن (۰.۳۰ تا ۰.۸۰ دلار رایج است؛ اگر ۳۵ نوشتی یعنی ۰.۳۵ دلار).\n"
        u"۳) <b>خبر</b> (NFP، نرخ بهره، CPI) طلا را بی‌منطق می‌کشد. نزدیک خبر بزرگ ستاپ تکنیکال را تعقیب نکن.\n\n"
        u"سوئیپ سقف/کف جلسه قبلی روی طلا خیلی رایج است. FVG طلا را مثل یورو بخوان؛ فقط واحد حرکت ۰.۱ دلار است نه پیپ چهار رقمی.\n\n"
        u"اگر حسابت کوچک است، طلا را آخر یاد بگیر نه اول."
    ),
    "edu_19": (
        u"🎓 <b>درس ۱۹ — چه زمانی معامله نکنیم</b>\n"
        u"سطح ۳ · پیشرفته\n"
        u"────────────\n"
        u"حرفه‌ای بودن یعنی زیاد زدن نیست؛ زیاد رد کردن است.\n\n"
        u"<b>لیست قرمز TZ FX:</b>\n"
        u"• امتیاز زیر ۴\n"
        u"• NO SIGNAL\n"
        u"• خلاف جهت روزانه\n"
        u"• BUY در پرمیوم یا SELL در دیسکانت ۱ساعته\n"
        u"• R:R بعد اسپرد زیر ۱.۲\n"
        u"• اسپرد پهن نسبت به حد ضرر\n"
        u"• ۳ ضرر امروز قبلاً خورده‌ای\n"
        u"• خبر دقیقه ۹۰\n"
        u"• خواب‌آلود، عصبانی، می‌خواهی «در بیاوری»\n"
        u"• سیگنال رفته و تو می‌خواهی از وسط روند سوار شوی\n\n"
        u"ربات بعضی از این‌ها را فیلتر می‌کند. بقیه‌اش کار توست.\n"
        u"روز بدون معامله، روز موفق است اگر قانون را نگه داشتی."
    ),
    "edu_20": (
        u"🎓 <b>درس ۲۰ — روانشناسی ترید</b>\n"
        u"سطح ۴ · اجرا و ذهن\n"
        u"────────────\n"
        u"سیستم بدون ذهن، روی کاغذ است.\n\n"
        u"<b>انتقام:</b> بعد ضرر، حجم را دو برابر می‌کنی تا «پس بگیری». این حساب را می‌کشد. قانون: بعد ضرر، حجم را کمتر کن یا همان روز تمام.\n\n"
        u"<b>FOMO:</b> سیگنال را دیدی که رفته، می‌پری داخل. ICT می‌گوید صبر برای برگشت به FVG. نرسید = جا ماندی. اشکال ندارد.\n\n"
        u"<b>اعتمادبه‌نفس کاذب:</b> سه برد پشت‌سرهم ≠ تو نابغه‌ای. قانون ۱٪ را همان موقع سفت‌تر بگیر.\n\n"
        u"<b>ترید برای هیجان:</b> اگر حوصله‌ات سر رفته، آموزش بخوان یا بازار را فقط نگاه کن. کلیک از روی کسالت = مالیات به بروکر.\n\n"
        u"مربی همین‌جاست. اگر قبل از کلیک دلت شور می‌زند، بنویس چه می‌خواهی بزنی — با هم چک‌لیست را می‌رویم."
    ),
    "edu_21": (
        u"🎓 <b>درس ۲۱ — مدیریت پوزیشن بعد ورود</b>\n"
        u"سطح ۴ · اجرا و ذهن\n"
        u"────────────\n"
        u"ورود تازه شروع است.\n\n"
        u"<b>پیشنهاد ICT-محور برای تازه‌کار:</b>\n"
        u"• حد ضرر را تا قبل از رسیدن به نقطه سربه‌سر جابه‌جا نکن\n"
        u"• اگر خواستی قفل سود کنی، فقط وقتی قیمت ساختار مخالف را شکست، SL را به ورود بیاور — نه زودتر که با نویز بیرونت کند\n"
        u"• نصف حجم را روی TP1 (مثلاً ۱:۱) نبند مگر پلن از قبل نوشته باشی. تغییر پلن وسط راه یعنی پلن نداری\n\n"
        u"ربات ستاپ باز را دنبال می‌کند و اگر قیمت به TP یا SL برسد خبر می‌دهد. این بهانه برای دستکاری دستی حد ضرر نیست.\n\n"
        u"اگر خبر ناگهانی آمد و اسپرد منفجر شد، عاقلانه است خارج شوی — این با «جابه‌جا کردن SL از روی امید» فرق دارد."
    ),
    "edu_22": (
        u"🎓 <b>درس ۲۲ — دفتر معامله</b>\n"
        u"سطح ۴ · اجرا و ذهن\n"
        u"────────────\n"
        u"بدون دفتر، داری روی تردمیل می‌دوی.\n\n"
        u"برای هر معامله این‌ها را بنویس:\n"
        u"• تاریخ و ساعت تهران\n"
        u"• نماد و سمت\n"
        u"• امتیاز ربات و چرا زدی (سوئیپ؟ FVG؟ کیل‌زون؟)\n"
        u"• ورود / SL / TP / لات / ریسک دلار\n"
        u"• نتیجه: TP، SL، یا خروج دستی\n"
        u"• احساس قبل از کلیک (آرام / عصبانی / جا ماندم)\n"
        u"• یک جمله: قانون را شکستم یا نه؟\n\n"
        u"هفته‌ای یک‌بار فقط ستون «قانون را شکستم» را بخوان. اگر بله زیاد است، مشکل استراتژی نیست؛ اجراست.\n\n"
        u"۲۰ معامله دمو با دفتر، قبل از پول واقعی. این مذاکره‌پذیر نیست."
    ),
    "edu_23": (
        u"🎓 <b>درس ۲۳ — کار با TZ FX BOT</b>\n"
        u"سطح ۴ · اجرا و ذهن\n"
        u"────────────\n"
        u"ربات مربی و اسکنر ICT است، ورود خودکار نیست.\n\n"
        u"• یورو / پوند / طلا / هر ۳ نماد\n"
        u"• چارت سفید با TP / IN / SL\n"
        u"• مولتی‌تایم\n"
        u"• 📐 اطلاعات معامله: موجودی، اسپرد، ریسک، اهرم → لات و دستور متاتریدر\n"
        u"• دنبال کردن تا حد سود یا حد ضرر\n"
        u"• مربی با حافظه: حرف قبلی‌ات را یادش می‌ماند\n"
        u"• کانال رایگان فقط ستاپ خیلی سخت‌گیر · VIP خصوصی با اشتراک\n\n"
        u"<b>امتیاز:</b> ۴ قابل بررسی · ۵–۶ قوی‌تر · زیر ۴ دست نزن.\n"
        u"قول درصد برد نمی‌دهیم. NO SIGNAL یعنی امروز شکارچی نباش.\n\n"
        u"سیگنال را در چت کانال اجرا نکن. دکمه را بزن، خصوصی باز شود، بعد اطلاعات معامله."
    ),
    "edu_24": (
        u"🎓 <b>درس ۲۴ — چک‌لیست قبل از کلیک</b>\n"
        u"سطح ۴ · اجرا و ذهن\n"
        u"────────────\n"
        u"قبل از Buy/Sell این را از حفظ برو:\n\n"
        u"☐ جهت روزانه مخالف نیست\n"
        u"☐ ۱ساعته: BUY در دیسکانت یا SELL در پرمیوم\n"
        u"☐ سوئیپ نقدینگی دیده شد\n"
        u"☐ FVG جابجایی هم‌جهت زنده است (پر نشده)\n"
        u"☐ امتیاز ۴ یا بیشتر\n"
        u"☐ کیل‌زون یا دلیل زمانی داری\n"
        u"☐ R:R بعد اسپرد معقول است\n"
        u"☐ لات با ۱٪ حساب جور است\n"
        u"☐ اسپرد زنده دیوانه نیست\n"
        u"☐ خبر بزرگ در دقیقه نیست\n"
        u"☐ امروز ۳ ضرر نخوردی\n"
        u"☐ حال روحی‌ات انتقام نیست\n\n"
        u"اگر حتی دو تا خالی ماند: نزن. برای مربی بفرست تا با هم خط بزنیم.\n\n"
        u"<i>آموزشی است · مشاوره مالی نیست · سرمایه در خطر است</i>"
    ),
    "edu_25": (
        u"🎓 <b>درس ۲۵ — کلید API صرافی</b>\n"
        u"سطح ۵ · اتصال\n"
        u"────────────\n"
        u"API یعنی ربات به‌جای تو به صرافی وصل شود.\n"
        u"کلید را فقط داخل همین بات بفرست.\n\n"
        u"<b>Binance</b>  پروفایل → API Management → Create\n"
        u"Spot روشن. برداشت خاموش.\n\n"
        u"<b>Bybit</b>  API → Create New Key → Spot\n\n"
        u"<b>OKX</b>  API → Create → Trading. Passphrase را نگه دار.\n\n"
        u"خانه → اتصال → صرافی → کلید API.\n"
        u"اول دمو است. تا LIVE ننویسی سفارش واقعی نمی‌رود."
    ),
    "edu_26": (
        u"🎓 <b>درس ۲۶ — اتصال به بروکر و ربات</b>\n"
        u"سطح ۵ · اتصال\n"
        u"────────────\n"
        u"<b>صرافی</b>\n"
        u"خانه → اتصال → صرافی را انتخاب کن → کلید → روشن.\n"
        u"حد ضرر اجباری. ریسک ۱٪.\n\n"
        u"<b>بروکر MT5 (همه بروکرها)</b>\n"
        u"متاتریدر دمو را باز کن.\n"
        u"اتصال → بریج MT5 را دانلود کن.\n"
        u"روی ویندوز: pip install MetaTrader5 requests\n"
        u"اسکریپت را اجرا کن.\n\n"
        u"پیپر تمرین است، پول واقعی نیست.\n"
        u"دکمه پایین = رفتن به اتصال."
    ),
}


def edu_audio_path(key, ext="mp3"):
    try:
        if not os.path.isdir(EDU_AUDIO_DIR):
            os.makedirs(EDU_AUDIO_DIR)
    except Exception:
        pass
    safe = "".join(ch for ch in str(key) if ch.isalnum() or ch == "_")
    return os.path.join(EDU_AUDIO_DIR, safe + "." + ext)


def coach_lesson_script(key):
    if is_en() and _i18n_mod is not None:
        en = _i18n_mod.edu_speak("en", key, u"")
        if en:
            return en
    spoken = EDU_SPEAK.get(key) or u""
    if spoken:
        return spoken.strip()
    title = EDU_TITLE.get(key) or u"درس"
    n = _edu_n(key)
    raw = _plain_for_speech(EDU.get(key) or "")
    lines = []
    for ln in raw.split("\n"):
        s = ln.strip()
        if not s:
            continue
        if u"────────" in s or u"━━" in s:
            continue
        if u"آموزشی است" in s or u"مشاوره مالی" in s or u"سرمایه در خطر" in s:
            continue
        if s.startswith(u"سطح "):
            continue
        if s.startswith(u"درس ") and (u"—" in s or u"-" in s):
            continue
        lines.append(s)
    body = u" ".join(lines)
    while u"  " in body:
        body = body.replace(u"  ", u" ")
    if len(body) > 420:
        cut = body.rfind(u"،", 0, 420)
        body = body[: cut if cut > 80 else 420].strip()
    opener = u"رفیق، درس %s. %s. " % (fa_num(n), title)
    closer = u" تعقیب نکن. حداکثر یک درصد حساب."
    return (opener + body + closer).strip()


def build_edu_audio(key, fmt="mp3"):
    text = _speech_fa(coach_lesson_script(key))
    if not text:
        return b""
    wav = _ai_fa_tts(text, quick=False)
    if wav and len(wav) > 4000:
        ogg = _wav_to_ogg(wav)
        return ogg or wav
    parts = _split_speech(text, 260)
    wavs = []
    for bit in parts[:4]:
        w = b""
        try:
            w = _gemini_tts_chunk(bit)
        except Exception:
            w = b""
        if w:
            wavs.append(w)
        else:
            break
        time.sleep(0.4)
    if wavs:
        out = _concat_wavs(wavs) if len(wavs) > 1 else wavs[0]
        if out and len(out) > 4000:
            ogg = _wav_to_ogg(out)
            return ogg or out
    log("edu tts miss %s" % key)
    return b""


def load_edu_audio(key, fmt="mp3", build=True):
    if key not in EDU:
        return b""
    for ext in ("ogg", "wav", "mp3"):
        path = edu_audio_path(key, ext)
        try:
            if os.path.isfile(path) and os.path.getsize(path) > 2000:
                with open(path, "rb") as f:
                    return f.read()
        except Exception:
            pass
    if not build:
        return b""
    raw = build_edu_audio(key, fmt=fmt)
    if raw and len(raw) > 2000:
        if raw[:4] == b"OggS":
            ext = "ogg"
        elif raw[:4] == b"RIFF":
            ext = "wav"
        else:
            ext = "mp3"
        path = edu_audio_path(key, ext)
        try:
            with open(path, "wb") as f:
                f.write(raw)
            log("edu audio saved %s %s n=%s" % (key, ext, len(raw)))
        except Exception:
            log("edu audio save " + traceback.format_exc())
    return raw or b""


def strip_html(text):
    t = text or ""
    for a, b in (
        ("<b>", ""),
        ("</b>", ""),
        ("<i>", ""),
        ("</i>", ""),
        ("<code>", ""),
        ("</code>", ""),
        ("<blockquote>", ""),
        ("</blockquote>", ""),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("&amp;", "&"),
    ):
        t = t.replace(a, b)
    return t


def lesson_context(key):
    if key == "edu_all" or key == "edu_0":
        return u"شاگرد کل دوره ICT را می‌پرسد. از درس مرتبط جواب بده و اگر مبهم بود بپرس کدام سطح."
    if str(key).startswith("l"):
        lv = str(key)[1:]
        titles = [EDU_TITLE.get(k, k) for k in (EDU_LEVELS.get(lv) or [])]
        return u"شاگرد روی سطح %s است. درس‌ها: %s" % (lv, u"، ".join(titles))
    title = EDU_TITLE.get(key) or key
    body = strip_html(EDU.get(key) or "")[:1200]
    return u"درس باز: %s\n%s" % (title, body)


def start_edu_ask(token, user_id, chat_id, lesson_key):
    rec = mem_touch(user_id, topic=lesson_key)
    set_wait(user_id, "edu_chat", {"lesson": lesson_key})
    title = EDU_TITLE.get(lesson_key) or u"آموزش ICT"
    if lesson_key in ("edu_0", "edu_all"):
        msg = (
            u"💬 <b>مربی TZ FX</b>\n"
            u"روی کل دوره آماده‌ام. بپرس — از پیپ تا Silver Bullet.\n"
            u"حرف‌های قبلی‌ات یادم می‌ماند.\n\n"
            u"همین‌جا بنویس."
        )
        kb = kb_edu()
    elif str(lesson_key).startswith("edu_l") or str(lesson_key).startswith("l"):
        lv = str(lesson_key).replace("edu_l", "").replace("l", "")
        msg = (
            u"💬 مربی روی <b>سطح %s</b> آماده‌ست.\n"
            u"از همین سطح بپرس. یادم می‌ماند کجا بودیم.\n\n"
            u"سوالت را بنویس."
            % fa_num(lv)
        )
        kb = kb_edu_level(lv)
    else:
        msg = (
            u"💬 مربی روی درس «<b>%s</b>» آماده‌ست.\n"
            u"هرچی از این درس گنگ است بپرس — با مثال جلو می‌رویم.\n"
            u"گفتگوی قبلی‌ات پاک نمی‌شود.\n\n"
            u"سوالت را بنویس یا ویس بفرست."
            % title
        )
        kb = kb_lesson(lesson_key)
    send_message(token, chat_id, msg, kb)


def handle_edu_callback(token, user_id, chat_id, data, cq_id):
    if not gate(token, user_id, chat_id, need_pro=False):
        answer_callback(token, cq_id, u"اول کانال را عضو شو")
        return True
    if data == "edu_menu":
        answer_callback(token, cq_id)
        send_message(token, chat_id, edu_intro(), kb_edu())
        return True
    if data.startswith("edul") and len(data) >= 5 and data[4:].isdigit():
        answer_callback(token, cq_id)
        lv = data[4:]
        names = {
            "1": u"سطح ۱ — مبتدی از صفر",
            "2": u"سطح ۲ — ICT پایه",
            "3": u"سطح ۳ — ICT پیشرفته",
            "4": u"سطح ۴ — اجرا و ذهن",
            "5": u"سطح ۵ — API و اتصال",
        }
        send_message(
            token,
            chat_id,
            u"📚 <b>%s</b>\nدرس را باز کن. زیر هر درس می‌توانی از مربی بپرسی."
            % names.get(lv, lv),
            kb_edu_level(lv),
        )
        return True
    if data.startswith("eq_"):
        answer_callback(token, cq_id)
        rest = data[3:]
        if rest in ("0", "all"):
            start_edu_ask(token, user_id, chat_id, "edu_0")
        elif rest.startswith("l") and rest[1:].isdigit():
            start_edu_ask(token, user_id, chat_id, rest)
        elif rest.isdigit():
            start_edu_ask(token, user_id, chat_id, "edu_" + rest)
        else:
            start_edu_ask(token, user_id, chat_id, "edu_0")
        return True
    if data.startswith("edu_") and data[4:].isdigit():
        answer_callback(token, cq_id)
        body = EDU.get(data) or u"درس پیدا نشد."
        send_message(token, chat_id, body, kb_lesson(data))
        return True
    return False

def send_photo(token, chat_id, png, caption=None, markup=None, reply_to=None):
    if not png:
        return False
    files = {"photo": ("chart.png", png, "image/png")}
    data = {
        "chat_id": str(chat_id),
        "allow_sending_without_reply": "true",
    }
    if caption:
        caption = emojify(caption, 8)
        cap = caption[:1024]
        data["caption"] = cap
        if "<" in cap:
            data["parse_mode"] = "HTML"
    if markup:
        data["reply_markup"] = json.dumps(markup)
    if reply_to:
        data["reply_to_message_id"] = str(int(reply_to))
    try:
        r = http().post(tg_api(token) + "/sendPhoto", data=data, files=files, timeout=20)
        js = r.json() if r.content else {}
        if js.get("ok"):
            return (js.get("result") or {}).get("message_id") or True
        desc = str(js).lower()
        if caption and "<tg-emoji" in str(caption) and "parse_mode" in data:
            data["caption"] = _strip_pe(caption)[:1024]
            r_pe = http().post(tg_api(token) + "/sendPhoto", data=data, files=files, timeout=20)
            js_pe = r_pe.json() if r_pe.content else {}
            if js_pe.get("ok"):
                log("pe photo fallback unicode")
                return (js_pe.get("result") or {}).get("message_id") or True
        if "parse_mode" in data:
            data.pop("parse_mode", None)
            if caption:
                data["caption"] = _strip_pe(caption)[:1024]
            r2 = http().post(tg_api(token) + "/sendPhoto", data=data, files=files, timeout=20)
            js2 = r2.json() if r2.content else {}
            if js2.get("ok"):
                return (js2.get("result") or {}).get("message_id") or True
        log("send_photo fail " + str(js)[:240])
        return False
    except Exception:
        log("send_photo error " + traceback.format_exc())
        return False


def send_photo_id(token, chat_id, file_id, caption=None, markup=None):
    payload = {
        "chat_id": chat_id,
        "photo": file_id,
        "allow_sending_without_reply": True,
    }
    if caption:
        payload["caption"] = caption[:1024]
        payload["parse_mode"] = "HTML"
    if markup:
        payload["reply_markup"] = markup
    try:
        r = http().post(tg_api(token) + "/sendPhoto", json=payload, timeout=16)
        js = r.json() if r.content else {}
        if js.get("ok"):
            return (js.get("result") or {}).get("message_id") or True
        payload.pop("parse_mode", None)
        r2 = http().post(tg_api(token) + "/sendPhoto", json=payload, timeout=16)
        js2 = r2.json() if r2.content else {}
        return bool(js2.get("ok"))
    except Exception:
        log("send_photo_id " + traceback.format_exc())
        return False


def send_chart(token, chat_id, rows, pair, sig, label, caption, markup=None, reply_to=None):
    png = None
    try:
        png = render_chart(rows, pair, sig, label)
    except Exception:
        log("chart " + traceback.format_exc())
    if png:
        mid = send_photo(token, chat_id, png, caption, markup, reply_to)
        if mid:
            return mid
    return send_message(token, chat_id, caption, markup, reply_to=reply_to)


_UI = {"desk": False, "mid": None, "chat": None}


def ui_desk(chat_id, message_id=None):
    _UI["desk"] = True
    _UI["chat"] = chat_id
    try:
        _UI["mid"] = int(message_id) if message_id else None
    except Exception:
        _UI["mid"] = None


def ui_desk_off():
    _UI["desk"] = False
    _UI["mid"] = None
    _UI["chat"] = None


def delete_message(token, chat_id, message_id):
    if not message_id:
        return
    try:
        http().post(
            tg_api(token) + "/deleteMessage",
            json={"chat_id": chat_id, "message_id": int(message_id)},
            timeout=8,
        )
    except Exception:
        pass


def _remember_desk(chat_id, mid):
    if not mid or mid is True:
        return
    try:
        _UI["mid"] = int(mid)
        _UI["chat"] = chat_id
        rec = load_user_mem(chat_id)
        rec["desk_mid"] = int(mid)
        save_user_mem(chat_id, rec)
    except Exception:
        pass


def send_message(token, chat_id, text, markup=None, parse_mode="HTML", reply_to=None, force_new=False):
    if not text:
        return False
    text = _strip_pe(text)[:4096]
    lang = "fa"
    try:
        lang = _LANG.get("code") or "fa"
    except Exception:
        pass
    rich = {"html": text, "is_rtl": lang != "en", "skip_entity_detection": True}

    def _edit(mid):
        body = {
            "chat_id": chat_id,
            "message_id": int(mid),
            "rich_message": rich,
            "link_preview_options": {"is_disabled": True},
        }
        if markup is not None:
            body["reply_markup"] = markup
        try:
            r = http().post(tg_api(token) + "/editMessageText", json=body, timeout=12)
            d = r.json() if r.content else {}
            if d.get("ok") or "not modified" in str(d).lower():
                return int(mid)
            body2 = {
                "chat_id": chat_id,
                "message_id": int(mid),
                "text": text[:4000],
                "disable_web_page_preview": True,
                "parse_mode": parse_mode or "HTML",
            }
            if markup is not None:
                body2["reply_markup"] = markup
            r2 = http().post(tg_api(token) + "/editMessageText", json=body2, timeout=12)
            d2 = r2.json() if r2.content else {}
            if d2.get("ok") or "not modified" in str(d2).lower():
                return int(mid)
        except Exception:
            log("edit fail " + traceback.format_exc().split("\n")[0][:120])
        return None

    def _send():
        body = {"chat_id": chat_id, "rich_message": rich}
        if markup:
            body["reply_markup"] = markup
        if reply_to is not None:
            try:
                body["reply_parameters"] = {
                    "message_id": int(reply_to),
                    "allow_sending_without_reply": True,
                }
            except Exception:
                pass
        try:
            r = http().post(tg_api(token) + "/sendRichMessage", json=body, timeout=12)
            d = r.json() if r.content else {}
            if d.get("ok"):
                return (d.get("result") or {}).get("message_id")
            log("rich fail " + str(d)[:180])
        except Exception:
            log("rich err " + traceback.format_exc().split("\n")[0][:120])
        payload = {
            "chat_id": chat_id,
            "text": text[:4000],
            "disable_web_page_preview": True,
            "allow_sending_without_reply": True,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if markup:
            payload["reply_markup"] = markup
        if reply_to is not None:
            try:
                payload["reply_to_message_id"] = int(reply_to)
            except Exception:
                pass
        try:
            r = http().post(tg_api(token) + "/sendMessage", json=payload, timeout=12)
            data = r.json() if r.content else {}
            if data.get("ok"):
                return (data.get("result") or {}).get("message_id") or True
            desc = str(data).lower()
            if "chat not found" in desc or "forbidden" in desc or "blocked by the user" in desc or "kicked" in desc:
                return False
            payload.pop("parse_mode", None)
            payload["text"] = _strip_pe(text)[:4000]
            r2 = http().post(tg_api(token) + "/sendMessage", json=payload, timeout=12)
            d2 = r2.json() if r2.content else {}
            if d2.get("ok"):
                return (d2.get("result") or {}).get("message_id") or True
            log("send retry fail " + str(d2)[:180])
            return False
        except Exception:
            log("send error " + traceback.format_exc())
            return False

    if (not force_new) and _UI.get("desk") and _UI.get("chat") == chat_id and _UI.get("mid"):
        got = _edit(_UI["mid"])
        if got:
            _remember_desk(chat_id, got)
            return got
    old = _UI.get("mid") if (_UI.get("desk") and _UI.get("chat") == chat_id) else None
    nid = _send()
    if nid and old and old != nid:
        delete_message(token, chat_id, old)
    if nid:
        _remember_desk(chat_id, nid)
    return nid


_EDGE_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4"
_EDGE_CHROME = "143.0.3650.75"


def _sec_ms_gec():
    ticks = time.time() + 11644473600
    ticks -= ticks % 300
    ticks *= 1e9 / 100
    s = "%.0f%s" % (ticks, _EDGE_TOKEN)
    return hashlib.sha256(s.encode("ascii")).hexdigest().upper()


def _recvn(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise IOError("eof")
        buf += chunk
    return buf


def _ws_send(sock, opcode, payload):
    if not isinstance(payload, bytes):
        payload = payload.encode("utf-8")
    length = len(payload)
    hdr = bytearray([0x80 | opcode])
    if length < 126:
        hdr.append(0x80 | length)
    elif length < 65536:
        hdr.append(0x80 | 126)
        hdr.extend(struct.pack(">H", length))
    else:
        hdr.append(0x80 | 127)
        hdr.extend(struct.pack(">Q", length))
    mask = os.urandom(4)
    hdr.extend(mask)
    payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    sock.sendall(bytes(hdr) + payload)


def _ws_read(sock):
    while True:
        h = _recvn(sock, 2)
        fin = h[0] & 0x80
        opcode = h[0] & 0x0F
        masked = h[1] & 0x80
        length = h[1] & 0x7F
        if length == 126:
            length = struct.unpack(">H", _recvn(sock, 2))[0]
        elif length == 127:
            length = struct.unpack(">Q", _recvn(sock, 8))[0]
        if masked:
            mk = _recvn(sock, 4)
        chunk = _recvn(sock, length)
        if masked:
            chunk = bytes(b ^ mk[i % 4] for i, b in enumerate(chunk))
        if opcode == 8:
            return 8, chunk
        if opcode == 9:
            _ws_send(sock, 10, chunk)
            continue
        data = chunk
        while not fin:
            h = _recvn(sock, 2)
            fin = h[0] & 0x80
            length = h[1] & 0x7F
            if length == 126:
                length = struct.unpack(">H", _recvn(sock, 2))[0]
            elif length == 127:
                length = struct.unpack(">Q", _recvn(sock, 8))[0]
            data += _recvn(sock, length)
        return opcode, data


def _plain_for_speech(text):
    t = strip_html(text or "")
    for a, b in (
        ("────────────", ". "),
        ("━━━━━━━━━━━━━━", ". "),
        ("• ", ". "),
        ("☐ ", ". "),
        ("🎯 ", ""),
        ("🛡 ", ""),
        ("🏁 ", ""),
        ("📐 ", ""),
        ("💬 ", ""),
        ("🎓 ", ""),
    ):
        t = t.replace(a, b)
    out = []
    for ch in t:
        o = ord(ch)
        if (0 <= o <= 8) or (11 <= o <= 12) or (14 <= o <= 31):
            out.append(" ")
        else:
            out.append(ch)
    t = "".join(out)
    while "  " in t:
        t = t.replace("  ", " ")
    return t.strip()


def _speech_fa(text):
    t = _plain_for_speech(text)
    reps = (
        ("Silver Bullet", u"سیلور بولت"),
        ("Judas Swing", u"جوداس سوینگ"),
        ("Displacement", u"دیسپلیسمنت"),
        ("EURUSD", u"یورو دلار"),
        ("GBPUSD", u"پوند دلار"),
        ("XAUUSD", u"طلا"),
        ("BUY", u"خرید"),
        ("SELL", u"فروش"),
        ("FVG", u"اف وی جی"),
        ("ICT", u"آی سی تی"),
        ("OTE", u"او تی ای"),
        ("SSL", u"اس اس ال"),
        ("BSL", u"بی اس ال"),
        ("MSS", u"ام اس اس"),
        ("SMT", u"اس ام تی"),
        ("PDH", u"سقف دیروز"),
        ("PDL", u"کف دیروز"),
        ("H4", u"چهار ساعته"),
        ("H1", u"یک ساعته"),
        ("D1", u"روزانه"),
        ("TP", u"حد سود"),
        ("SL", u"حد ضرر"),
        ("NO SIGNAL", u"سیگنال نیست"),
        ("WAIT", u"صبر"),
        ("1%", u"یک درصد"),
        (u"۱٪", u"یک درصد"),
        (" / ", u"، "),
        ("=", u" یعنی "),
    )
    for a, b in reps:
        t = t.replace(a, b)
    while "  " in t:
        t = t.replace("  ", " ")
    return t.strip()


def _split_speech(text, n=240):
    text = (text or "").strip()
    out = []
    buf = text
    while buf:
        if len(buf) <= n:
            out.append(buf)
            break
        cut = -1
        for sep in (u"؟", "!", ".", u"،", "\n"):
            cut = max(cut, buf.rfind(sep, 0, n))
        if cut < 40:
            cut = buf.rfind(" ", 0, n)
        if cut < 40:
            cut = n
        bit = buf[: cut + 1].strip()
        if bit:
            out.append(bit)
        buf = buf[cut + 1 :].strip()
    return [x for x in out if x]


def _edge_tts_chunk(text, voice="fa-IR-FaridNeural", fmt="mp3"):
    import ssl
    import socket
    import uuid
    import base64

    text = (text or "").strip()
    if not text:
        return b""
    cid = uuid.uuid4().hex
    gec = _sec_ms_gec()
    path = (
        "/consumer/speech/synthesize/readaloud/edge/v1"
        "?TrustedClientToken=%s&ConnectionId=%s"
        "&Sec-MS-GEC=%s&Sec-MS-GEC-Version=1-%s"
        % (_EDGE_TOKEN, cid, gec, _EDGE_CHROME)
    )
    host = "speech.platform.bing.com"
    raw = socket.create_connection((host, 443), timeout=20)
    sock = ssl.create_default_context().wrap_socket(raw, server_hostname=host)
    wskey = base64.b64encode(os.urandom(16)).decode("ascii")
    muid = os.urandom(16).hex().upper()
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
    )
    req = (
        "GET %s HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: %s\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "Pragma: no-cache\r\n"
        "Cache-Control: no-cache\r\n"
        "Origin: chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold\r\n"
        "User-Agent: %s\r\n"
        "Accept-Language: fa-IR,fa;q=0.9,en;q=0.8\r\n"
        "Cookie: muid=%s;\r\n"
        "\r\n"
    ) % (path, host, wskey, ua, muid)
    sock.sendall(req.encode("ascii"))
    resp = b""
    while b"\r\n\r\n" not in resp:
        resp += sock.recv(4096)
    if b"101" not in resp.split(b"\r\n", 1)[0]:
        sock.close()
        raise IOError("tts handshake")
    ts = time.strftime(
        "%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)",
        time.gmtime(),
    )
    outfmt = (
        "webm-24khz-16bit-mono-opus"
        if str(fmt).lower() in ("ogg", "opus", "voice")
        else "audio-24khz-48kbitrate-mono-mp3"
    )
    cfg = (
        "X-Timestamp:%s\r\nContent-Type:application/json; charset=utf-8\r\n"
        "Path:speech.config\r\n\r\n"
        '{"context":{"synthesis":{"audio":{"metadataoptions":{'
        '"sentenceBoundaryEnabled":"false","wordBoundaryEnabled":"false"},'
        '"outputFormat":"%s"}}}}\r\n'
        % (ts, outfmt)
    )
    _ws_send(sock, 1, cfg)
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    ssml = (
        "X-RequestId:%s\r\nContent-Type:application/ssml+xml\r\n"
        "X-Timestamp:%sZ\r\nPath:ssml\r\n\r\n"
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='fa-IR'>"
        "<voice name='%s'><prosody pitch='+0Hz' rate='-8%%' volume='+0%%'>%s</prosody></voice></speak>"
        % (uuid.uuid4().hex, ts, voice, safe)
    )
    _ws_send(sock, 1, ssml)
    audio = b""
    t0 = time.time()
    while time.time() - t0 < 35:
        op, data = _ws_read(sock)
        if op == 8:
            break
        if op == 1:
            if b"turn.end" in data:
                break
        elif op == 2 and len(data) >= 2:
            hl = struct.unpack(">H", data[:2])[0]
            body = data[hl + 2 :]
            if body:
                audio += body
    try:
        sock.close()
    except Exception:
        pass
    return audio


def pcm16_wav(pcm, rate=24000):
    n = len(pcm)
    return (
        b"RIFF"
        + struct.pack("<I", 36 + n)
        + b"WAVEfmt "
        + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16)
        + b"data"
        + struct.pack("<I", n)
        + pcm
    )


def _gemini_tts_chunk(text, models=None, timeout=20):
    import base64

    text = (text or "").strip()
    if not text:
        return b""
    key = load_gemini()
    if not key:
        return b""
    models = models or GEMINI_TTS_MODELS
    lang_opts = ("fa-IR", "fa", None)
    for model in models:
        for lang in lang_opts:
            speech = {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Charon"}}
            }
            if lang:
                speech["languageCode"] = lang
            body = {
                "contents": [{"parts": [{"text": text}]}],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": speech,
                },
            }
            try:
                r = http().post(
                    "https://generativelanguage.googleapis.com/v1beta/models/"
                    + model
                    + ":generateContent",
                    headers={"Content-Type": "application/json", "X-goog-api-key": key},
                    json=body,
                    timeout=timeout,
                )
            except Exception as e:
                log("tts gemini fail %s %s" % (model, str(e)[:80]))
                break
            if r.status_code == 429:
                log("tts gemini 429 %s" % model)
                break
            if r.status_code == 400 and lang:
                continue
            if r.status_code != 200:
                log("tts gemini http %s %s" % (r.status_code, model))
                break
            try:
                data = r.json()
            except Exception:
                break
            cand = (data.get("candidates") or [{}])[0]
            parts = ((cand.get("content") or {}).get("parts") or [])
            for part in parts:
                idt = part.get("inlineData") or part.get("inline_data") or {}
                b64 = idt.get("data")
                if not b64:
                    continue
                pcm = base64.b64decode(b64)
                mime = idt.get("mimeType") or idt.get("mime_type") or ""
                rate = 24000
                if "rate=" in mime:
                    try:
                        rate = int(mime.split("rate=")[-1].split(";")[0])
                    except Exception:
                        rate = 24000
                log("tts gemini ok %s lang=%s n=%s" % (model, lang or "-", len(pcm)))
                return pcm16_wav(pcm, rate)
    return b""



def _wav_pcm(wav):
    if not wav or wav[:4] != b"RIFF" or len(wav) < 44:
        return b"", 22050
    rate = 22050
    try:
        rate = struct.unpack("<I", wav[24:28])[0] or 22050
    except Exception:
        rate = 22050
    i = 12
    pcm = wav[44:]
    while i + 8 <= len(wav):
        kind = wav[i : i + 4]
        try:
            sz = struct.unpack("<I", wav[i + 4 : i + 8])[0]
        except Exception:
            break
        if kind == b"data":
            pcm = wav[i + 8 : i + 8 + sz]
            break
        i += 8 + max(0, sz)
        if sz % 2:
            i += 1
    return pcm, rate


def _concat_wavs(wavs):
    pcms = []
    rate = 22050
    for w in wavs:
        pcm, rt = _wav_pcm(w)
        if pcm:
            pcms.append(pcm)
            rate = rt or rate
    if not pcms:
        return b""
    return pcm16_wav(b"".join(pcms), rate)


def _gradio_wav(base, endpoint, data, timeout=90):
    try:
        r = http().post(
            base.rstrip("/") + "/gradio_api/call/" + endpoint,
            json={"data": data},
            timeout=30,
            headers={"User-Agent": "TZFX/1"},
        )
        eid = (r.json() or {}).get("event_id")
        if not eid:
            return b""
        r2 = http().get(
            base.rstrip("/") + "/gradio_api/call/" + endpoint + "/" + eid,
            timeout=timeout,
            headers={"User-Agent": "TZFX/1"},
        )
        text = r2.text if hasattr(r2, "text") else r2.content.decode("utf-8", "replace")
        fileurl = None
        for line in text.splitlines():
            if not line.startswith("data:"):
                continue
            try:
                arr = json.loads(line[5:].strip())
            except Exception:
                continue
            if isinstance(arr, list) and arr and isinstance(arr[0], dict):
                fileurl = arr[0].get("url") or arr[0].get("path")
                if fileurl:
                    break
            if isinstance(arr, dict):
                fileurl = arr.get("url")
                if fileurl:
                    break
        if not fileurl:
            return b""
        if fileurl.startswith("/"):
            fileurl = base.rstrip("/") + fileurl
        r3 = http().get(fileurl, timeout=45, headers={"User-Agent": "TZFX/1"})
        raw = r3.content or b""
        if raw[:4] == b"RIFF" and len(raw) > 2000:
            return raw
    except Exception:
        log("gradio tts " + traceback.format_exc())
    return b""


def _vits_fa_tts(text):
    """Natural Persian male VITS (same voice for coach + lessons)."""
    text = _speech_fa(text)
    if not text:
        return b""
    parts = _split_speech(text, 170)
    wavs = []
    for bit in parts[:7]:
        w = b""
        for _try in range(2):
            w = _gradio_wav(
                "https://abdulhossein-persian-tts-coquitts.hf.space",
                "predict",
                [bit, "VITS Male 1 (Best)"],
            )
            if w:
                break
            w = _gradio_wav(
                "https://gyroing-persian-tts-piper.hf.space",
                "synthesize_speech",
                [bit],
            )
            if w:
                break
            time.sleep(1.2)
        if not w:
            break
        wavs.append(w)
        time.sleep(0.25)
    if not wavs:
        return b""
    if len(wavs) == 1:
        return wavs[0]
    return _concat_wavs(wavs)


def _chatter_fa_tts(text):
    """AI Persian Chatterbox (realistic, not classic TTS)."""
    text = _speech_fa(text)
    if not text:
        return b""
    parts = _split_speech(text, 240)
    wavs = []
    for bit in parts[:8]:
        w = b""
        for _try in range(2):
            w = _gradio_wav(
                "https://ameerhossein-chatterbox-tts-persian.hf.space",
                "generate_audio",
                [bit],
                timeout=120,
            )
            if w:
                break
            time.sleep(1.0)
        if not w:
            break
        wavs.append(w)
        time.sleep(0.25)
    if not wavs:
        return b""
    if len(wavs) == 1:
        return wavs[0]
    return _concat_wavs(wavs)


_f5_uploaded = {"path": None, "t": 0}


def _gradio_upload(base, fpath, name="ref.wav"):
    try:
        with open(fpath, "rb") as f:
            r = http().post(
                base.rstrip("/") + "/gradio_api/upload",
                files={"files": (name, f, "audio/wav")},
                timeout=40,
                headers={"User-Agent": "TZFX/1"},
            )
        js = r.json()
        if isinstance(js, list) and js:
            return js[0]
        if isinstance(js, str) and js:
            return js
    except Exception:
        log("gradio upload " + traceback.format_exc())
    return None


def _f5_clone_tts(text):
    """Clone Charon AI voice via F5-TTS (same man, not classic TTS)."""
    global _f5_uploaded
    text = _speech_fa(text)
    if not text:
        return b""
    if not os.path.isfile(COACH_REF_FILE) or os.path.getsize(COACH_REF_FILE) < 8000:
        return b""
    base = "https://mrfakename-e2-f5-tts.hf.space"
    now = time.time()
    if not _f5_uploaded.get("path") or now - float(_f5_uploaded.get("t") or 0) > 600:
        remote = _gradio_upload(base, COACH_REF_FILE, "charon.wav")
        if not remote:
            return b""
        _f5_uploaded = {"path": remote, "t": now}
    filedata = {
        "path": _f5_uploaded["path"],
        "orig_name": "charon.wav",
        "meta": {"_type": "gradio.FileData"},
    }
    parts = _split_speech(text, 160)
    wavs = []
    for bit in parts[:8]:
        w = b""
        for _try in range(2):
            w = _gradio_wav(
                base,
                "predict",
                [filedata, COACH_REF_TEXT, bit, True],
                timeout=120,
            )
            if w:
                break
            remote = _gradio_upload(base, COACH_REF_FILE, "charon.wav")
            if remote:
                _f5_uploaded = {"path": remote, "t": time.time()}
                filedata["path"] = remote
            time.sleep(0.8)
        if not w:
            break
        wavs.append(w)
        time.sleep(0.2)
    if not wavs:
        return b""
    if len(wavs) == 1:
        return wavs[0]
    return _concat_wavs(wavs)


def _ai_fa_tts(text, quick=True):
    """Gemini Charon Persian. Slow fallbacks only when building lesson cache."""
    text = _speech_fa(text)
    if not text:
        return b""
    models = GEMINI_TTS_MODELS[:1] if quick else GEMINI_TTS_MODELS
    try:
        wav = _gemini_tts_chunk(text, models=models, timeout=18 if quick else 22)
        if wav and len(wav) > 4000:
            return wav
    except Exception:
        log("ai gemini " + traceback.format_exc())
    if quick:
        return b""
    try:
        wav = _chatter_fa_tts(text)
        if wav and len(wav) > 4000:
            return wav
    except Exception:
        log("ai chatter " + traceback.format_exc())
    return b""


def tts_fa(text, fmt="mp3", quick=True):
    text = _speech_fa(text)
    if not text:
        return b""
    capn = 420 if quick else 700
    if len(text) > capn:
        cut = text.rfind(".", 0, capn)
        if cut < 80:
            cut = text.rfind(u"؟", 0, capn)
        if cut < 80:
            cut = text.rfind(u"،", 0, capn)
        text = text[: cut if cut > 80 else capn].strip()
    wav = _ai_fa_tts(text, quick=quick)
    if not wav:
        return b""
    if fmt in ("ogg", "opus", "voice"):
        ogg = _wav_to_ogg(wav)
        if ogg:
            return ogg
    return wav


def _ffmpeg_exe():
    cands = (
        os.path.join(HERE, "ffmpeg"),
        os.path.join(HERE, "bin", "ffmpeg"),
        "/usr/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
    )
    for pth in cands:
        try:
            if os.path.isfile(pth) and os.access(pth, os.X_OK):
                return pth
        except Exception:
            pass
    return ""


def _wav_to_ogg(wav):
    if not wav:
        return b""
    if wav[:4] == b"OggS":
        return wav
    if wav[:4] != b"RIFF":
        return b""
    exe = _ffmpeg_exe()
    if not exe:
        return b""
    import subprocess
    import tempfile

    src = dst = None
    try:
        fd, src = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        fd2, dst = tempfile.mkstemp(suffix=".ogg")
        os.close(fd2)
        with open(src, "wb") as f:
            f.write(wav)
        cmd = [
            exe, "-y", "-i", src,
            "-ac", "1", "-ar", "48000",
            "-c:a", "libopus", "-b:a", "24k",
            "-application", "voip", dst,
        ]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(dst, "rb") as f:
            out = f.read()
        if out[:4] == b"OggS" and len(out) > 1500:
            return out
    except Exception:
        log("wav ogg " + traceback.format_exc())
    finally:
        for pth in (src, dst):
            try:
                if pth and os.path.isfile(pth):
                    os.remove(pth)
            except Exception:
                pass
    return b""


def send_document_bytes(token, chat_id, raw, filename, mime, caption=None, markup=None):
    if not raw:
        return False
    files = {"document": (filename, raw, mime)}
    data = {
        "chat_id": str(chat_id),
        "allow_sending_without_reply": "true",
    }
    if caption:
        data["caption"] = strip_html(caption)[:900]
    if markup:
        data["reply_markup"] = json.dumps(markup)
    try:
        r = http().post(tg_api(token) + "/sendDocument", data=data, files=files, timeout=40)
        js = r.json() if r.content else {}
        if js.get("ok"):
            return True
        log("send_doc fail " + str(js)[:160])
        return False
    except Exception:
        log("send_doc " + traceback.format_exc())
        return False


def send_audio_mp3(token, chat_id, mp3, caption=None, markup=None):
    if not mp3:
        return False
    if (mp3[:4] == b"RIFF"):
        files = {"audio": ("coach.wav", mp3, "audio/wav")}
    else:
        files = {"audio": ("coach.mp3", mp3, "audio/mpeg")}
    data = {
        "chat_id": str(chat_id),
        "title": u"مربی TZ FX",
        "performer": "TZ FX",
        "allow_sending_without_reply": "true",
    }
    if caption:
        data["caption"] = strip_html(caption)[:900]
    if markup:
        data["reply_markup"] = json.dumps(markup)
    try:
        r = http().post(
            tg_api(token) + "/sendAudio", data=data, files=files, timeout=40
        )
        js = r.json() if r.content else {}
        if js.get("ok"):
            return True
        if "parse_mode" in data:
            data.pop("parse_mode", None)
            r2 = http().post(
                tg_api(token) + "/sendAudio", data=data, files=files, timeout=40
            )
            js2 = r2.json() if r2.content else {}
            if js2.get("ok"):
                return True
            log("send_audio fail " + str(js2)[:200])
            return False
        log("send_audio fail " + str(js)[:200])
        return False
    except Exception:
        log("send_audio " + traceback.format_exc())
        return False


def send_voice_note(token, chat_id, raw, caption=None, markup=None):
    if not raw:
        return False
    if raw[:4] == b"RIFF":
        ogg = _wav_to_ogg(raw)
        if ogg:
            raw = ogg
        else:
            return False
    if raw[:4] == b"OggS":
        files = {"voice": ("coach.ogg", raw, "audio/ogg")}
    elif raw[:4] == b"\x1aE\xdf\xa3":
        files = {"voice": ("coach.ogg", raw, "audio/ogg")}
    elif raw[:3] == b"ID3" or (len(raw) > 1 and raw[0] == 0xFF and (raw[1] & 0xE0) == 0xE0):
        files = {"voice": ("coach.mp3", raw, "audio/mpeg")}
    else:
        files = {"voice": ("coach.ogg", raw, "audio/ogg")}
    data = {
        "chat_id": str(chat_id),
        "allow_sending_without_reply": "true",
    }
    if caption:
        data["caption"] = strip_html(caption)[:900]
    if markup:
        data["reply_markup"] = json.dumps(markup)
    try:
        r = http().post(tg_api(token) + "/sendVoice", data=data, files=files, timeout=40)
        js = r.json() if r.content else {}
        if js.get("ok"):
            return True
        log("send_voice fail " + str(js)[:200])
        return False
    except Exception:
        log("send_voice " + traceback.format_exc())
        return False


def speak_text(token, chat_id, text, markup=None, caption=None):
    if too_soon("tts:%s" % chat_id, 2):
        return False
    try:
        http().post(
            tg_api(token) + "/sendChatAction",
            json={"chat_id": chat_id, "action": "record_voice"},
            timeout=6,
        )
    except Exception:
        pass
    cap = caption if caption is not None else ""
    raw = tts_fa(text, fmt="ogg", quick=True)
    if not raw:
        return False
    if send_voice_note(token, chat_id, raw, caption=cap, markup=markup):
        return True
    if send_audio_mp3(token, chat_id, raw, caption=cap, markup=markup):
        return True
    mime = "audio/ogg" if raw[:4] == b"OggS" else "audio/wav"
    name = "coach.ogg" if mime == "audio/ogg" else "coach.wav"
    return send_document_bytes(token, chat_id, raw, name, mime, caption=cap, markup=markup)


def remember_last_ans(uid, text):
    if not uid or not text:
        return
    rec = load_user_mem(uid)
    rec["last_ans"] = text[:2500]
    save_user_mem(uid, rec)


def tg_download_file(token, file_id):
    try:
        r = http().get(
            tg_api(token) + "/getFile",
            params={"file_id": file_id},
            timeout=12,
        )
        path = ((r.json() or {}).get("result") or {}).get("file_path") or ""
        if not path:
            return None, ""
        raw = http().get(
            "https://api.telegram.org/file/bot%s/%s" % (token, path),
            timeout=30,
        )
        if raw.status_code != 200:
            return None, path
        return raw.content, path
    except Exception:
        log("tg file " + traceback.format_exc())
        return None, ""


def transcribe_audio(raw, mime="audio/ogg"):
    global _gemini_block_until
    import base64

    if not raw:
        return None
    key = load_gemini()
    if not key:
        return None
    if len(raw) > 3 * 1024 * 1024:
        raw = raw[: 3 * 1024 * 1024]
    b64 = base64.b64encode(raw).decode("ascii")
    prompt = (
        u"این پیام صوتی شاگرد ترید است. فقط رونوشت دقیق گفتار را بنویس. "
        u"اگر فارسی حرف زده فارسی بنویس. اعداد را رقم لاتین بنویس (مثلا 1000). "
        u"هیچ توضیح، عنوان یا نقل‌قول اضافه نده."
    )
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime, "data": b64}},
                ],
            }
        ],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 512},
    }
    models = GEMINI_STT_MODELS
    for model in models:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + model
            + ":generateContent"
        )
        try:
            r = http().post(
                url,
                headers={"Content-Type": "application/json", "X-goog-api-key": key},
                json=body,
                timeout=18,
            )
        except Exception as e:
            log("stt fail %s %s" % (model, str(e)[:80]))
            continue
        if r.status_code == 429:
            log("stt 429 %s" % model)
            continue
        if r.status_code != 200:
            log("stt http %s %s" % (r.status_code, model))
            continue
        try:
            data = r.json()
        except Exception:
            continue
        cand = (data.get("candidates") or [{}])[0]
        parts = ((cand.get("content") or {}).get("parts") or [])
        txt = "".join([(p.get("text") or "") for p in parts]).strip()
        if txt:
            log("stt ok %s n=%s" % (model, len(txt)))
            return txt[:1500]
    return None


def ingest_voice(token, user_id, chat_id, msg):
    info = msg.get("voice") or msg.get("audio") or {}
    file_id = info.get("file_id")
    if not file_id:
        return None
    try:
        dur = int(info.get("duration") or 0)
    except Exception:
        dur = 0
    if dur > 90:
        send_message(
            token,
            chat_id,
            u"ویس را کوتاه‌تر بفرست — زیر ۹۰ ثانیه.",
            kb_after(),
        )
        return None
    try:
        http().post(
            tg_api(token) + "/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
            timeout=6,
        )
    except Exception:
        pass
    raw, path = tg_download_file(token, file_id)
    if not raw:
        send_message(token, chat_id, u"ویس نرسید. دوباره بفرست.", kb_after())
        return None
    mime = info.get("mime_type") or "audio/ogg"
    pl = (path or "").lower()
    if pl.endswith(".mp3") or "mpeg" in (mime or ""):
        mime = "audio/mp3"
    elif pl.endswith(".wav"):
        mime = "audio/wav"
    elif "ogg" in (mime or "") or pl.endswith(".oga") or pl.endswith(".ogg"):
        mime = "audio/ogg"
    elif "mp4" in (mime or "") or pl.endswith(".m4a"):
        mime = "audio/mp4"
    text = transcribe_audio(raw, mime)
    if not text:
        send_message(
            token,
            chat_id,
            u"نتونستم ویس را بفهمم. یک بار دیگه واضح‌تر بفرست، یا بنویس.",
            kb_after(),
        )
        return None
    return text.strip()


def answer_callback(token, cq_id, text="", url=None):
    import requests

    payload = {"callback_query_id": cq_id, "cache_time": 1}
    if url:
        payload["url"] = url
    elif text:
        payload["text"] = text
    requests.post(tg_api(token) + "/answerCallbackQuery", json=payload, timeout=12)



_ohlc_disk_ok = [False]
_ohlc_disk_dirty = [False]
_ohlc_disk_saved = [0.0]


def _ohlc_disk_prime():
    if _ohlc_disk_ok[0]:
        return
    _ohlc_disk_ok[0] = True
    data = _jload(OHLC_DISK, {})
    if not isinstance(data, dict):
        return
    now = time.time()
    for key, rec in data.items():
        if not isinstance(rec, dict):
            continue
        rows = rec.get("rows")
        ts = float(rec.get("ts") or 0)
        iv = (key.split("|") + [""])[-1]
        ttl = _CACHE_TTL.get(iv, 40) * 3
        if rows and now - ts < ttl:
            _ohlc_cache[key] = rows
            _ohlc_cache_at[key] = ts


def _ohlc_disk_flush(force=False):
    if not _ohlc_disk_dirty[0] and not force:
        return
    now = time.time()
    if not force and now - _ohlc_disk_saved[0] < 12:
        return
    blob = {}
    for k, rows in _ohlc_cache.items():
        if not rows:
            continue
        blob[k] = {"ts": _ohlc_cache_at.get(k, now), "rows": rows[-220:]}
    try:
        _jsave(OHLC_DISK, blob)
        _ohlc_disk_dirty[0] = False
        _ohlc_disk_saved[0] = now
    except Exception:
        pass


def _resample_ohlc(rows, minutes):
    if not rows or minutes < 1:
        return []
    bucket = int(minutes) * 60
    out = []
    cur = None
    for r in rows:
        try:
            t0 = (int(r["t"]) // bucket) * bucket
        except Exception:
            continue
        if cur is None or cur["t"] != t0:
            if cur:
                out.append(cur)
            cur = {"t": t0, "o": r["o"], "h": r["h"], "l": r["l"], "c": r["c"]}
        else:
            if r["h"] > cur["h"]:
                cur["h"] = r["h"]
            if r["l"] < cur["l"]:
                cur["l"] = r["l"]
            cur["c"] = r["c"]
    if cur:
        out.append(cur)
    return out


def _fetch_kraken(pair, interval):
    kid = (PAIRS.get(pair) or {}).get("kraken")
    iv = _KRAKEN_IV.get(interval)
    if not kid or not iv:
        return []
    r = http().get(
        "https://api.kraken.com/0/public/OHLC",
        params={"pair": kid, "interval": iv},
        timeout=8,
        headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 TZFX"},
    )
    r.raise_for_status()
    js = r.json() or {}
    if js.get("error"):
        return []
    blob = None
    for k, v in (js.get("result") or {}).items():
        if k == "last":
            continue
        blob = v
        break
    if not blob:
        return []
    rows = []
    for rec in blob:
        try:
            rows.append(
                {
                    "t": int(rec[0]),
                    "o": float(rec[1]),
                    "h": float(rec[2]),
                    "l": float(rec[3]),
                    "c": float(rec[4]),
                }
            )
        except Exception:
            continue
    return _sanitize_ohlc(rows)


def _fetch_yahoo(pair, interval, range_):
    meta = PAIRS.get(pair) or {}
    if not meta.get("yahoo"):
        return []
    last_err = None
    rng = range_
    if interval == "1m":
        rng = "1d"
    for host in ("query1.finance.yahoo.com", "query2.finance.yahoo.com"):
        try:
            r = http().get(
                "https://%s/v8/finance/chart/%s" % (host, meta["yahoo"]),
                params={"range": rng, "interval": interval, "includePrePost": "false"},
                timeout=8,
                headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 TZFX"},
            )
            r.raise_for_status()
            result = r.json()["chart"]["result"][0]
            quote = result["indicators"]["quote"][0]
            ts = result["timestamp"]
            rows = []
            for i, tstamp in enumerate(ts):
                o, h, l, c = quote["open"][i], quote["high"][i], quote["low"][i], quote["close"][i]
                if None in (o, h, l, c):
                    continue
                rows.append(
                    {"t": int(tstamp), "o": float(o), "h": float(h), "l": float(l), "c": float(c)}
                )
            rows = _sanitize_ohlc(rows)
            if rows:
                return rows
        except Exception as e:
            last_err = e
            continue
    if last_err:
        log("yahoo %s %s %s" % (pair, interval, str(last_err)[:80]))
    return []



_BINANCE_IV = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
}


def _fetch_binance(pair, interval):
    meta = PAIRS.get(pair) or {}
    sym = meta.get("binance") or (pair if str(pair).upper().endswith("USDT") else None)
    iv = _BINANCE_IV.get(interval)
    if not sym or not iv:
        return []
    last_err = None
    for host in _binance_hosts():
        try:
            r = http().get(
                "https://%s/api/v3/klines" % host,
                params={"symbol": sym, "interval": iv, "limit": 300},
                timeout=8,
                headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 TZFX"},
            )
            r.raise_for_status()
            blob = r.json() or []
            rows = []
            for rec in blob:
                try:
                    rows.append(
                        {
                            "t": int(rec[0]) // 1000,
                            "o": float(rec[1]),
                            "h": float(rec[2]),
                            "l": float(rec[3]),
                            "c": float(rec[4]),
                        }
                    )
                except Exception:
                    continue
            if len(rows) >= 12:
                return rows
        except Exception as e:
            last_err = e
    if last_err:
        log("binance fail %s %s %s" % (pair, interval, str(last_err)[:80]))
    return []


def fetch_ohlc(pair, interval="15m", range_="10d", cap=None):
    """FX from Kraken (UTC candles). Gold from Yahoo GC=F. Same bars for signal + chart."""
    _ohlc_disk_prime()
    key = pair + "|" + interval
    now = time.time()
    ttl = _CACHE_TTL.get(interval, 40)
    cached = _ohlc_cache.get(key) or []
    if cached and (now - _ohlc_cache_at.get(key, 0)) < ttl:
        if cap and len(cached) > cap:
            return cached[-cap:]
        return cached
    use_cap = cap if cap is not None else (180 if interval == "1m" else 280)
    rows = []
    if str(pair or "").upper().endswith("USDT"):
        try:
            ensure_crypto_pair(pair)
        except Exception:
            pass
    if is_crypto_pair(pair):
        try:
            rows = _fetch_binance(pair, interval)
        except Exception:
            log("binance %s %s %s" % (pair, interval, traceback.format_exc().splitlines()[-1][:80]))
            rows = []
        if len(rows) < 12:
            try:
                k = _fetch_kraken(pair, interval)
                if len(k) > len(rows):
                    rows = k
            except Exception:
                pass
        if len(rows) < 12 and (PAIRS.get(pair) or {}).get("yahoo"):
            y = _fetch_yahoo(pair, interval, range_)
            if len(y) > len(rows):
                rows = y
    else:
        try:
            rows = _fetch_kraken(pair, interval)
        except Exception:
            log("kraken %s %s %s" % (pair, interval, traceback.format_exc().splitlines()[-1][:80]))
            rows = []
        if len(rows) < 12:
            y = _fetch_yahoo(pair, interval, range_)
            if len(y) > len(rows):
                rows = y
        if pair == "XAUUSD" and interval in ("1h", "4h", "30m") and len(rows) < 30:
            src15 = _ohlc_cache.get(pair + "|15m") or _fetch_yahoo(pair, "15m", "10d")
            mins = {"30m": 30, "1h": 60, "4h": 240}[interval]
            rs = _resample_ohlc(src15, mins)
            if len(rs) > len(rows):
                rows = rs
    rows = _sanitize_ohlc(rows)
    if len(rows) > use_cap:
        rows = rows[-use_cap:]
    if rows and is_crypto_pair(pair):
        try:
            _refine_crypto_meta(pair, rows[-1]["c"])
        except Exception:
            pass
    if rows:
        _ohlc_cache[key] = rows
        _ohlc_cache_at[key] = now
        _ohlc_disk_dirty[0] = True
        _ohlc_disk_flush()
        return rows
    if cached:
        return cached[-use_cap:] if cap else cached
    return []


def swing_points(rows, left=3, right=3):
    highs, lows = [], []
    n = len(rows)
    for i in range(left, n - right):
        h, l = rows[i]["h"], rows[i]["l"]
        if all(h >= rows[j]["h"] for j in range(i - left, i + right + 1)):
            highs.append(i)
        if all(l <= rows[j]["l"] for j in range(i - left, i + right + 1)):
            lows.append(i)
    return highs, lows


def fvgs(rows):
    out = []
    for i in range(2, len(rows)):
        if rows[i]["l"] > rows[i - 2]["h"]:
            out.append({"i": i, "side": "BULL", "top": rows[i]["l"], "bot": rows[i - 2]["h"]})
        if rows[i]["h"] < rows[i - 2]["l"]:
            out.append({"i": i, "side": "BEAR", "top": rows[i - 2]["l"], "bot": rows[i]["h"]})
    return out


def in_killzone(ts):
    hour = time.gmtime(ts).tm_hour
    # ICT: London open through lunch + NY AM. No late-NY chop, no Asia.
    if 7 <= hour < 11:
        return u"لندن · ۱۰:۳۰–۱۴:۳۰ تهران"
    if 12 <= hour < 16:
        return u"نیویورک · ۱۵:۳۰–۱۹:۳۰ تهران"
    return None


def in_silver_bullet(ts):
    hour = time.gmtime(ts).tm_hour
    return hour in (7, 14, 18)


def tf_bias(rows):
    if not rows or len(rows) < 18:
        return {"bias": "NEUTRAL", "pd": "-", "mid": None, "hi": None, "lo": None}
    price = rows[-1]["c"]
    window = rows[-24:] if len(rows) >= 24 else rows
    hi = max(r["h"] for r in window)
    lo = min(r["l"] for r in window)
    mid = (hi + lo) / 2.0
    pd = "DISCOUNT" if price <= mid else "PREMIUM"
    sh, slp = swing_points(rows, 2, 2)
    bias = "NEUTRAL"
    if sh and slp:
        if len(sh) >= 2 and rows[sh[-1]]["h"] > rows[sh[-2]]["h"] and price >= rows[sh[-2]]["h"]:
            bias = "BULL"
        elif len(slp) >= 2 and rows[slp[-1]]["l"] < rows[slp[-2]]["l"] and price <= rows[slp[-2]]["l"]:
            bias = "BEAR"
        elif price > rows[sh[-1]]["h"]:
            bias = "BULL"
        elif price < rows[slp[-1]]["l"]:
            bias = "BEAR"
        else:
            bias = "BULL" if price >= mid else "BEAR"
    return {"bias": bias, "pd": pd, "mid": mid, "hi": hi, "lo": lo, "price": price}


_htf_memo = {}


def htf_context(pair, price):
    now = time.time()
    hit = _htf_memo.get(pair)
    if hit and now - hit[0] < 70:
        out = dict(hit[1])
        if hit[1].get("h4"):
            out["h4"] = dict(hit[1]["h4"])
        if hit[1].get("d1"):
            out["d1"] = dict(hit[1]["d1"])
        return out
    h1 = tf_bias(fetch_ohlc(pair, "1h", "60d"))
    h4 = tf_bias(fetch_ohlc(pair, "4h", "60d"))
    d1 = tf_bias(fetch_ohlc(pair, "1d", "2y"))
    h1["h4"] = h4
    h1["d1"] = d1
    _htf_memo[pair] = (now, h1)
    out = dict(h1)
    out["h4"] = dict(h4)
    out["d1"] = dict(d1)
    return out


def is_displacement(row):
    rng = row["h"] - row["l"]
    if rng <= 0:
        return False
    return abs(row["c"] - row["o"]) / rng >= 0.58


def score_setup(sig, inside_fvg, htf):
    pts = []
    sc = 0
    if sig["side"] in ("BUY", "SELL"):
        sc += 1
        pts.append("سوئیپ+FVG")
    if sig.get("mss"):
        sc += 1
        pts.append("MSS")
    if sig.get("disp"):
        sc += 1
        pts.append("جابجایی")
    if sig.get("smt"):
        sc += 1
        pts.append("SMT")
    if sig.get("ob"):
        sc += 1
        pts.append("اوردر بلاک")
    if sig.get("eq"):
        sc += 1
        pts.append("نقدینگی برابر")
    if sig.get("ote"):
        sc += 1
        pts.append("OTE")
    kz = sig.get("killzone")
    if kz and kz != "خارج از کیل‌زون":
        sc += 1
        pts.append("کیل‌زون")
    if in_silver_bullet(int(time.time())):
        sc += 1
        pts.append("Silver Bullet")
    if inside_fvg:
        sc += 1
        pts.append("داخل FVG")
    rr = 0
    if sig.get("risk_pips"):
        rr = sig["reward_pips"] / float(sig["risk_pips"])
    if rr >= 1.5:
        sc += 1
        pts.append("R:R")
    aligned = (sig["side"] == "BUY" and htf.get("pd") == "DISCOUNT") or (
        sig["side"] == "SELL" and htf.get("pd") == "PREMIUM"
    )
    if aligned:
        sc += 1
        pts.append("دیسکانت/پرمیوم 1H")
    h4 = (htf.get("h4") or {}).get("bias")
    d1 = (htf.get("d1") or {}).get("bias")
    if sig["side"] == "BUY" and h4 == "BULL":
        sc += 1
        pts.append("H4")
    if sig["side"] == "SELL" and h4 == "BEAR":
        sc += 1
        pts.append("H4")
    if sig["side"] == "BUY" and d1 == "BULL":
        sc += 1
        pts.append("D1")
    if sig["side"] == "SELL" and d1 == "BEAR":
        sc += 1
        pts.append("D1")
    sc = min(6, sc)
    d1_against = (sig["side"] == "BUY" and d1 == "BEAR") or (
        sig["side"] == "SELL" and d1 == "BULL"
    )
    return sc, pts, aligned, d1_against



def atr_val(rows, n=14):
    if not rows or len(rows) < n + 1:
        return None
    trs = []
    for i in range(len(rows) - n, len(rows)):
        r = rows[i]
        prev = rows[i - 1]["c"]
        tr = max(r["h"] - r["l"], abs(r["h"] - prev), abs(r["l"] - prev))
        trs.append(tr)
    if not trs:
        return None
    return sum(trs) / float(len(trs))


def min_risk_pips(pair, interval=None):
    tf = interval or "15m"
    if is_crypto_pair(pair):
        return 4.0 if tf == "5m" else 8.0
    if pair == "XAUUSD":
        return 12.0 if tf == "5m" else 18.0
    return 6.0 if tf == "5m" else 9.0


def max_risk_pips(pair, interval=None):
    """Session-scale stop beyond Judas wick — not HTF."""
    tf = interval or "15m"
    if is_crypto_pair(pair):
        # ATR*3.4 is the real cap; this only must be larger than session wick.
        return 8000.0 if tf == "5m" else 15000.0
    if pair == "XAUUSD":
        return 45.0 if tf == "5m" else 72.0
    return 14.0 if tf == "5m" else 22.0


def snap_px(pair, x):
    try:
        x = float(x)
    except Exception:
        return x
    meta = PAIRS.get(pair) or {}
    d = int(meta.get("digits") or 5)
    tick = float(meta.get("pip") or 0.0001)
    n = round(x / tick) * tick
    return float(("%." + str(d) + "f") % n)


def _liq_prices(side, entry, price, rows, sh, sls, htf, pair, atr):
    """ICT T1 = IRL only. No H4/D1 24-bar extremes (those never hit in-session)."""
    pip = PAIRS[pair]["pip"]
    pad = max((atr or pip * 12) * 0.15, pip * 4)
    raw = []

    def add(p):
        if p is None:
            return
        try:
            p = float(p)
        except Exception:
            return
        if side == "BUY" and p <= max(entry, price) + pad:
            return
        if side == "SELL" and p >= min(entry, price) - pad:
            return
        raw.append(p)

    win = rows[-48:] if rows else []
    recent_sh = list(sh or [])[-10:]
    recent_sl = list(sls or [])[-10:]
    if side == "BUY":
        for i in recent_sh:
            if 0 <= i < len(rows):
                add(rows[i]["h"])
        if win:
            add(max(r["h"] for r in win))
        add((htf or {}).get("hi"))
        for k in ("pdh", "ash"):
            add((htf or {}).get(k))
        uniq = sorted(set(snap_px(pair, p) for p in raw))
    else:
        for i in recent_sl:
            if 0 <= i < len(rows):
                add(rows[i]["l"])
        if win:
            add(min(r["l"] for r in win))
        add((htf or {}).get("lo"))
        for k in ("pdl", "asl"):
            add((htf or {}).get(k))
        uniq = sorted(set(snap_px(pair, p) for p in raw), reverse=True)
    clean = []
    merge = pad * 0.45
    for p in uniq:
        if not clean or abs(p - clean[-1]) > merge:
            clean.append(p)
    return clean


def choose_tp(side, entry, sl, rows, sh, sls, htf, pip, atr=None, pair=None):
    """Nearest IRL with 1.0R–2.0R. No fake 2.2*risk, no weekly ERL."""
    if pair is None:
        pair = "XAUUSD" if pip >= 0.01 else "EURUSD"
    risk = abs(float(entry) - float(sl))
    if risk <= 0:
        return None
    price = float(entry)
    try:
        if rows:
            price = float(rows[-1]["c"])
    except Exception:
        pass
    cands = _liq_prices(side, float(entry), price, rows or [], sh or [], sls or [], htf or {}, pair, atr)
    atr_v = atr or risk
    cap = min(risk * 2.05, max(atr_v * 2.2, risk * 1.2))
    best = None
    best_rr = 0
    for p in cands:
        dist = abs(p - float(entry))
        rr = dist / risk
        if dist > cap + pip:
            continue
        if 1.2 <= rr <= 2.05:
            if best is None or abs(rr - 1.5) < abs(best_rr - 1.5):
                best = p
                best_rr = rr
    if best is not None:
        return snap_px(pair, best)
    return None


def validate_geometry(sig, price, pair):
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return None, u"ستاپ نیست"
    pip = PAIRS[pair]["pip"]
    side = sig["side"]
    try:
        entry = snap_px(pair, sig["entry"])
        sl = snap_px(pair, sig["sl"])
        tp = snap_px(pair, sig["tp"])
        price = float(price)
    except Exception:
        return None, u"اعداد ناقص"
    if side == "BUY":
        if not (sl < entry and entry < tp):
            return None, u"برای خرید باید حد ضرر زیر ورود و حد سود بالای ورود باشد"
        if sl >= price:
            return None, u"حد ضرر بالای قیمت زنده است"
        if tp <= price:
            return None, u"حد سود پشت قیمت است — ستاپ سوخته"
        if price > entry:
            live_risk = price - sl
            live_rew = tp - price
            if live_risk <= 0 or live_rew / live_risk < 1.15:
                return None, u"قیمت از ورود جلو زده — تعقیب ممنوع"
            if (price - entry) > 0.18 * (entry - sl):
                return None, u"ستاپ در حرکت است — ورود دیر"
    else:
        if not (tp < entry and entry < sl):
            return None, u"برای فروش باید حد سود زیر ورود و حد ضرر بالای ورود باشد"
        if sl <= price:
            return None, u"حد ضرر پایین‌تر از قیمت زنده است"
        if tp >= price:
            return None, u"حد سود پشت قیمت است — ستاپ سوخته"
        if price < entry:
            live_risk = sl - price
            live_rew = price - tp
            if live_risk <= 0 or live_rew / live_risk < 1.15:
                return None, u"قیمت از ورود جلو زده — تعقیب ممنوع"
            if (entry - price) > 0.18 * (sl - entry):
                return None, u"ستاپ در حرکت است — ورود دیر"
    risk = abs(entry - sl) / pip
    reward = abs(tp - entry) / pip
    if risk < min_risk_pips(pair, sig.get("tf")):
        return None, u"حد ضرر کوچک‌تر از نویز این نماد است"
    if risk > max_risk_pips(pair, sig.get("tf")):
        return None, u"حد ضرر خیلی دور — سوئیپ کهنه"
    if abs(entry - sl) < pip * 0.51:
        return None, u"حد ضرر روی ورود است"
    if reward / risk < 1.15:
        return None, u"R:R ضعیف — هدف داخلی حداقل ۱.۲R"
    if reward / risk > 2.15:
        return None, u"حد سود خیلی پرت است — فقط نقدینگی داخلی (IRL)"
    sig = dict(sig)
    sig["entry"] = snap_px(pair, entry)
    sig["sl"] = snap_px(pair, sl)
    sig["tp"] = snap_px(pair, tp)
    sig["risk_pips"] = risk
    sig["reward_pips"] = reward
    return sig, None


def _nosig(pair, price, htf, reason, last=None, extra=None):
    d = {
        "pair": pair,
        "side": "NO SIGNAL",
        "reason": reason,
        "price": price,
        "score": 0,
        "htf": htf,
        "time": tehran_fmt((last or {}).get("t") if last else None) + u" تهران",
        "model": u"ICT",
    }
    if extra:
        d.update(extra)
    return d


def _pdh_pdl(pair):
    try:
        drows = fetch_ohlc(pair, "1d", "60d")
    except Exception:
        return None, None
    if not drows or len(drows) < 2:
        return None, None
    prev = drows[-2]
    return float(prev["h"]), float(prev["l"])


def _session_hl(rows, hours):
    hi = None
    lo = None
    for r in rows[-120:]:
        try:
            hr = time.gmtime(int(r["t"])).tm_hour
        except Exception:
            continue
        if hr not in hours:
            continue
        hi = r["h"] if hi is None else max(hi, r["h"])
        lo = r["l"] if lo is None else min(lo, r["l"])
    return hi, lo


def _equal_levels(rows, idxs, key, pip, atr):
    out = []
    if len(idxs) < 2:
        return out
    tol = max(pip * 6, (atr or pip * 12) * 0.14)
    use = idxs[-8:]
    for a, b in zip(use, use[1:]):
        pa, pb = rows[a][key], rows[b][key]
        if abs(pa - pb) <= tol:
            out.append((b, (pa + pb) / 2.0))
    return out


def _find_sweeps(rows, sh, sls, pip, atr, pdh=None, pdl=None, ash=None, asl=None, look=36):
    start = max(0, len(rows) - int(look or 36))
    found = []
    eq_lo = _equal_levels(rows, sls, "l", pip, atr)
    eq_hi = _equal_levels(rows, sh, "h", pip, atr)

    def add(i, direction, wick, lvl, kind):
        found.append(
            {"dir": direction, "i": i, "wick": wick, "lvl": lvl, "kind": kind}
        )

    for i in range(start, len(rows)):
        r = rows[i]
        prev_sl = [j for j in sls if j < i]
        if prev_sl:
            lvl = rows[prev_sl[-1]]["l"]
            if r["l"] < lvl and r["c"] > lvl:
                add(i, "BULL", r["l"], lvl, "SSL")
        prev_sh = [j for j in sh if j < i]
        if prev_sh:
            lvlh = rows[prev_sh[-1]]["h"]
            if r["h"] > lvlh and r["c"] < lvlh:
                add(i, "BEAR", r["h"], lvlh, "BSL")
        for _, lvl in eq_lo:
            if r["l"] < lvl and r["c"] > lvl:
                add(i, "BULL", r["l"], lvl, "EQL")
        for _, lvl in eq_hi:
            if r["h"] > lvl and r["c"] < lvl:
                add(i, "BEAR", r["h"], lvl, "EQH")
        if pdl is not None and r["l"] < pdl and r["c"] > pdl:
            add(i, "BULL", r["l"], pdl, "PDL")
        if pdh is not None and r["h"] > pdh and r["c"] < pdh:
            add(i, "BEAR", r["h"], pdh, "PDH")
        if asl is not None and r["l"] < asl and r["c"] > asl:
            add(i, "BULL", r["l"], asl, "ASIA_L")
        if ash is not None and r["h"] > ash and r["c"] < ash:
            add(i, "BEAR", r["h"], ash, "ASIA_H")
    return found


def _mss(rows, sweep, sh, sls):
    i0 = sweep["i"]
    if sweep["dir"] == "BULL":
        highs = [j for j in sh if j <= i0]
        if not highs:
            return None
        lvl = rows[highs[-1]]["h"]
        for k in range(i0, len(rows)):
            if rows[k]["c"] > lvl and is_displacement(rows[k]):
                return {"i": k, "lvl": lvl}
    else:
        lows = [j for j in sls if j <= i0]
        if not lows:
            return None
        lvl = rows[lows[-1]]["l"]
        for k in range(i0, len(rows)):
            if rows[k]["c"] < lvl and is_displacement(rows[k]):
                return {"i": k, "lvl": lvl}
    return None


def _smt(pair, sweep):
    other = {"EURUSD": "GBPUSD", "GBPUSD": "EURUSD"}.get(pair)
    if not other or not sweep:
        return False
    try:
        orows = fetch_ohlc(other)
    except Exception:
        return False
    if not orows or len(orows) < 24:
        return False
    osh, osl = swing_points(orows, 2, 2)
    recent = orows[-20:]
    pip = PAIRS[other]["pip"]
    if sweep["dir"] == "BULL":
        if not osl:
            return False
        olvl = orows[osl[-1]]["l"]
        return min(r["l"] for r in recent) >= olvl - pip * 3
    if not osh:
        return False
    olvl = orows[osh[-1]]["h"]
    return max(r["h"] for r in recent) <= olvl + pip * 3


def _pick_sweep(fresh, htf):
    if not fresh:
        return None
    d1 = (htf.get("d1") or {}).get("bias") if htf else None
    h4 = (htf.get("h4") or {}).get("bias") if htf else None
    h1 = htf.get("bias") if htf else None
    want = None
    votes = [d1, h4, h1]
    if votes.count("BULL") >= 2:
        want = "BULL"
    elif votes.count("BEAR") >= 2:
        want = "BEAR"
    elif h4 == "BULL" or d1 == "BULL":
        want = "BULL"
    elif h4 == "BEAR" or d1 == "BEAR":
        want = "BEAR"
    ranked = list(fresh)
    if want:
        matched = [s for s in fresh if s["dir"] == want]
        if matched:
            ranked = matched
    weight = {
        "PDL": 5,
        "PDH": 5,
        "EQL": 4,
        "EQH": 4,
        "ASIA_L": 4,
        "ASIA_H": 4,
        "SSL": 3,
        "BSL": 3,
    }
    ranked.sort(key=lambda s: (weight.get(s.get("kind"), 1), s["i"]))
    return ranked[-1]


def _in_fvg(price, bot, top, pip, atr):
    lo, hi = (bot, top) if bot <= top else (top, bot)
    pad = max(pip * 1.0, (atr or pip * 10) * 0.05)
    return (lo - pad) <= price <= (hi + pad)


def ict_2022(rows, pair, interval="15m", htf=None):
    """ICT — only. Sequence:
    HTF draw → Judas sweep of SSL/BSL (PDH/PDL, Asia, equal, swing)
    → MSS with displacement → FVG of that leg → enter in the FVG/OTE
    → SL beyond sweep wick → TP opposite liquidity (IRL then ERL).
    """
    meta = PAIRS[pair]
    pip = meta["pip"]
    min_n = 24 if interval in ("1h", "4h", "1d") else 32
    if not rows or len(rows) < min_n:
        return None
    sw = 2 if interval in ("1m", "5m", "15m", "30m") else 3
    sh, sls = swing_points(rows, sw, sw)
    ish, isl = swing_points(rows, 2, 2)
    last = rows[-1]
    price = last["c"]
    if htf is None:
        htf = htf_context(pair, price) or {}
    else:
        htf = dict(htf)
        if htf.get("h4"):
            htf["h4"] = dict(htf["h4"])
        if htf.get("d1"):
            htf["d1"] = dict(htf["d1"])
    atr = atr_val(rows) or (pip * (25 if pair == "XAUUSD" else 12))
    extra = {
        "buy_liq": rows[sh[-1]]["h"] if sh else None,
        "sell_liq": rows[sls[-1]]["l"] if sls else None,
        "model": u"ICT",
        "forming": {
            "sweep": 0,
            "mss": 0,
            "fvg": 0,
            "in_fvg": 0,
            "kz": 1 if in_killzone(last["t"]) else 0,
        },
    }
    if not sh or not sls:
        return _nosig(pair, price, htf, u"سوئینگ کافی نیست", last, extra)

    pdh, pdl = _pdh_pdl(pair)
    ash, asl = _session_hl(rows, range(0, 7))
    htf["pdh"] = pdh
    htf["pdl"] = pdl
    htf["ash"] = ash
    htf["asl"] = asl
    extra["buy_liq"] = extra["buy_liq"] or pdh
    extra["sell_liq"] = extra["sell_liq"] or pdl

    look = {"5m": 28, "15m": 24, "30m": 20, "1h": 18, "4h": 14, "1d": 10}.get(interval, 24)
    age = {"5m": 16, "15m": 14, "30m": 12, "1h": 12, "4h": 10, "1d": 8}.get(interval, 14)
    sweeps = _find_sweeps(rows, sh, sls, pip, atr, pdh, pdl, ash, asl, look=look)
    n = len(rows) - 1
    fresh = [s for s in sweeps if (n - s["i"]) <= age]
    if not fresh:
        return _nosig(
            pair,
            price,
            htf,
            u"جاروی نقدینگی تازه نیست (SSL/BSL / سقف‌کف دیروز / آسیا)",
            last,
            extra,
        )
    sweep = _pick_sweep(fresh, htf)
    if not sweep:
        return _nosig(
            pair,
            price,
            htf,
            u"سوئیپ هم‌جهت با تایم بالا نیست",
            last,
            extra,
        )
    extra["forming"]["sweep"] = 1
    extra["sweep_lvl"] = sweep.get("lvl")
    extra["sweep_kind"] = sweep.get("kind")
    mss = _mss(rows, sweep, ish or sh, isl or sls)
    if not mss:
        return _nosig(
            pair,
            price,
            htf,
            u"سوئیپ Judas هست؛ منتظر MSS با جابجایی",
            last,
            extra,
        )
    extra["forming"]["mss"] = 1
    extra["mss_lvl"] = mss.get("lvl")
    mss_age = {"5m": 22, "15m": 18, "1h": 16, "4h": 12}.get(interval, 18)
    if (n - mss["i"]) > mss_age:
        return _nosig(pair, price, htf, u"MSS کهنه است — صبر برای لگ تازه", last, extra)

    want = "BULL" if sweep["dir"] == "BULL" else "BEAR"
    start_i = min(sweep["i"] + 1, mss["i"])
    gaps = [g for g in fvgs(rows) if g["i"] >= start_i and g["side"] == want]
    extra["forming"]["fvg"] = 1 if gaps else 0
    if not gaps:
        return _nosig(
            pair,
            price,
            htf,
            u"MSS هست؛ FVG جابجایی ICT هنوز نیست",
            last,
            extra,
        )
    gap = gaps[-1]
    disp = False
    for idx in (gap["i"], gap["i"] - 1, mss["i"]):
        if 0 <= idx < len(rows) and is_displacement(rows[idx]):
            disp = True
            break
    width = gap["top"] - gap["bot"]
    if width <= 0:
        return _nosig(pair, price, htf, u"FVG نامعتبر", last, extra)
    if width < atr * 0.10 and not disp:
        return _nosig(pair, price, htf, u"FVG بدون جابجایی کافی — ستاپ ICT نیست", last, extra)

    impulse_hi = max(rows[j]["h"] for j in range(sweep["i"], min(len(rows), mss["i"] + 1)))
    impulse_lo = min(rows[j]["l"] for j in range(sweep["i"], min(len(rows), mss["i"] + 1)))
    ir = impulse_hi - impulse_lo
    mid_imp = (impulse_hi + impulse_lo) / 2.0 if ir > 0 else price
    in_ote = False
    if ir > 0:
        if want == "BULL":
            ote_lo = impulse_hi - 0.79 * ir
            ote_hi = impulse_hi - 0.62 * ir
        else:
            ote_lo = impulse_lo + 0.62 * ir
            ote_hi = impulse_lo + 0.79 * ir
        midg = (gap["top"] + gap["bot"]) / 2.0
        in_ote = ote_lo <= price <= ote_hi or ote_lo <= midg <= ote_hi

    ce = (gap["top"] + gap["bot"]) / 2.0
    inside = _in_fvg(price, gap["bot"], gap["top"], pip, atr)
    if want == "BULL":
        if price < gap["bot"] - max(pip * 2, width * 0.12):
            return _nosig(pair, price, htf, u"FVG صعودی پر شده — ستاپ سوخته", last, extra)
        if not inside:
            return _nosig(
                pair,
                price,
                htf,
                u"منتظر برگشت داخل FVG — تعقیب جابجایی ممنوع",
                last,
                extra,
            )
        entry = price
    else:
        if price > gap["top"] + max(pip * 2, width * 0.12):
            return _nosig(pair, price, htf, u"FVG نزولی پر شده — ستاپ سوخته", last, extra)
        if not inside:
            return _nosig(
                pair,
                price,
                htf,
                u"منتظر برگشت داخل FVG — تعقیب جابجایی ممنوع",
                last,
                extra,
            )
        entry = price

    buf = max(atr * 0.22, pip * (8 if pair == "XAUUSD" else 3))
    entry = snap_px(pair, entry)
    if want == "BULL":
        sl = snap_px(pair, float(sweep["wick"]) - buf)
        if sl >= min(entry, price) - pip:
            return _nosig(pair, price, htf, u"حد ضرر روی ورود می‌افتد — سوئیپ نامعتبر", last, extra)
        side = "BUY"
        setup = u"ICT: Judas SSL → MSS → FVG"
        if sweep.get("kind") in ("PDL", "ASIA_L", "EQL"):
            setup = u"ICT: Judas %s → MSS → FVG" % sweep["kind"]
    else:
        sl = snap_px(pair, float(sweep["wick"]) + buf)
        if sl <= max(entry, price) + pip:
            return _nosig(pair, price, htf, u"حد ضرر روی ورود می‌افتد — سوئیپ نامعتبر", last, extra)
        side = "SELL"
        setup = u"ICT: Judas BSL → MSS → FVG"
        if sweep.get("kind") in ("PDH", "ASIA_H", "EQH"):
            setup = u"ICT: Judas %s → MSS → FVG" % sweep["kind"]

    risk_px = abs(entry - sl)
    min_px = max(atr * 0.45, pip * min_risk_pips(pair, interval))
    max_px = pip * max_risk_pips(pair, interval)
    max_px = min(max_px, atr * 3.4)
    if risk_px < min_px or risk_px > max_px or risk_px <= 0:
        return _nosig(pair, price, htf, u"فاصله حد ضرر غیرمنطقی است — سوئیپ خیلی دور/نزدیک", last, extra)

    tp = choose_tp(side, entry, sl, rows, sh, sls, htf, pip, atr=atr, pair=pair)
    if tp is None:
        return _nosig(pair, price, htf, u"هدف نقدینگی منطقی (IRL/ERL) پیدا نشد", last, extra)
    tp = snap_px(pair, tp)

    inside_now = _in_fvg(price, gap["bot"], gap["top"], pip, atr)
    extra["forming"]["fvg"] = 1
    extra["forming"]["in_fvg"] = 1 if inside_now else 0
    sig = {
        "pair": pair,
        "side": side,
        "setup": setup,
        "model": u"ICT",
        "price": price,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "risk_pips": abs(entry - sl) / pip,
        "reward_pips": abs(tp - entry) / pip,
        "fvg_bot": snap_px(pair, gap["bot"]),
        "fvg_top": snap_px(pair, gap["top"]),
        "killzone": in_killzone(last["t"]) or u"خارج از کیل‌زون",
        "time": tehran_fmt(last["t"]) + u" تهران",
        "buy_liq": extra.get("buy_liq"),
        "sell_liq": extra.get("sell_liq"),
        "htf": htf,
        "inside_fvg": inside_now,
        "disp": disp,
        "ote": in_ote,
        "mss": True,
        "smt": _smt(pair, sweep),
        "eq": sweep.get("kind") in ("EQL", "EQH", "PDL", "PDH", "ASIA_L", "ASIA_H"),
        "ob": False,
        "sweep_kind": sweep.get("kind"),
        "sweep_lvl": sweep.get("lvl"),
        "mss_lvl": mss.get("lvl"),
        "forming": extra.get("forming") or {},
        "tf": interval,
    }
    sig, why = validate_geometry(sig, price, pair)
    if not sig:
        return _nosig(pair, price, htf, why or u"حد ضرر/حد سود نامعتبر", last, extra)
    sc, pts, aligned, d1_against = score_setup(sig, inside_now, htf)
    h4b = (htf.get("h4") or {}).get("bias")
    h4_against = (sig.get("side") == "BUY" and h4b == "BEAR") or (
        sig.get("side") == "SELL" and h4b == "BULL"
    )
    if d1_against:
        return _nosig(pair, price, htf, u"خلاف جهت روزانه — وارد نشو", last, extra)
    if not disp:
        return _nosig(pair, price, htf, u"جابجایی کافی نیست — ستاپ ICT نیست", last, extra)
    if not inside_now:
        return _nosig(pair, price, htf, u"قیمت داخل FVG نیست — صبر کن", last, extra)
    warns = []
    if h4_against:
        warns.append(u"۴ساعته مخالف است")
        sc = min(int(sc or 0), 4)
    if not aligned:
        warns.append(u"خارج از پرمیوم/دیسکانت ۱ساعته")
    kz_ok = bool(
        in_killzone(last["t"])
        or in_silver_bullet(last["t"])
        or in_killzone(int(time.time()))
        or in_silver_bullet(int(time.time()))
    )
    if not kz_ok:
        warns.append(u"خارج از کیل‌زون")
    sig["score"] = sc
    sig["confluence"] = pts
    sig["aligned"] = aligned
    if warns:
        sig["warn"] = u" · ".join(warns)
    if sig.get("smt"):
        sig["confluence"] = list(sig.get("confluence") or []) + [u"SMT"]
    if sc < 4:
        return _nosig(pair, price, htf, u"امتیاز زیر ۴ — ستاپ ICT کامل نیست", last, extra)
    return sig


def ict_checklist(sig):
    if not sig:
        return ""
    kz_ok = sig.get("killzone") and u"خارج" not in str(sig.get("killzone") or "")
    if sig.get("side") in ("BUY", "SELL"):
        items = [
            (True, u"Judas"),
            (bool(sig.get("mss")), u"MSS"),
            (sig.get("fvg_bot") is not None, u"FVG"),
            (bool(sig.get("inside_fvg")), u"داخل شکاف"),
            (bool(kz_ok), u"کیل‌زون"),
            (bool(sig.get("aligned")), u"PD"),
            (bool(sig.get("ote")), u"OTE"),
            (bool(sig.get("smt")), u"SMT"),
        ]
    else:
        f = sig.get("forming") or {}
        items = [
            (bool(f.get("sweep")), u"Judas"),
            (bool(f.get("mss")), u"MSS"),
            (bool(f.get("fvg")), u"FVG"),
            (bool(f.get("in_fvg")), u"داخل شکاف"),
            (bool(f.get("kz") or kz_ok), u"کیل‌زون"),
        ]
    return u" · ".join(((u"✅ " if ok else u"⚪ ") + n) for ok, n in items)


def refine_entry_5m(sig, pair):
    """ICT execution: 15m PD array, 5m FVG inside it for tighter entry."""
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return sig
    bot, top = sig.get("fvg_bot"), sig.get("fvg_top")
    if bot is None or top is None:
        return sig
    try:
        rows5 = fetch_ohlc(pair, "5m", "5d")
    except Exception:
        return sig
    if not rows5 or len(rows5) < 24:
        return sig
    want = "BULL" if sig["side"] == "BUY" else "BEAR"
    gaps = [g for g in fvgs(rows5) if g["side"] == want][-4:]
    price = float(sig.get("price") or rows5[-1]["c"])
    pip = PAIRS[pair]["pip"]
    lo15, hi15 = (min(bot, top), max(bot, top))
    picked = None
    for g in reversed(gaps):
        glo, ghi = min(g["bot"], g["top"]), max(g["bot"], g["top"])
        if ghi < lo15 or glo > hi15:
            continue
        if glo >= lo15 - pip and ghi <= hi15 + pip:
            if glo - pip <= price <= ghi + pip:
                picked = g
                break
    if not picked:
        return sig
    sig = dict(sig)
    sig["entry"] = price
    sig["fvg_bot"] = picked["bot"]
    sig["fvg_top"] = picked["top"]
    sig["inside_fvg"] = True
    sig["setup"] = (sig.get("setup") or u"ICT") + u" · ورود ۵م"
    fixed, why = validate_geometry(sig, price, pair)
    if not fixed:
        return sig
    return fixed


def load_watch():
    d = _jload(WATCH_FILE, {})
    return d if isinstance(d, dict) else {}


def save_watch(d):
    _jsave(WATCH_FILE, d)


def watch_add(uid, pair="ALL"):
    d = load_watch()
    key = str(uid)
    cur = d.get(key) or []
    if not isinstance(cur, list):
        cur = []
    if pair not in cur:
        cur.append(pair)
    d[key] = cur
    save_watch(d)


def watch_off(uid):
    d = load_watch()
    d.pop(str(uid), None)
    save_watch(d)


def notify_watchers(token, sig):
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return
    pair = sig.get("pair")
    d = load_watch()
    if not d:
        return
    text = (
        u"👀 <b>ستاپ ICT کامل شد</b>\n"
        u"%s <b>%s</b>  %s\n"
        u"ورود <code>%s</code> · SL <code>%s</code> · TP <code>%s</code>\n"
        u"%s"
        % (
            (PAIRS.get(pair) or {}).get("emoji") or "",
            pair,
            sig.get("side"),
            fmt_px(pair, sig.get("entry")),
            fmt_px(pair, sig.get("sl")),
            fmt_px(pair, sig.get("tp")),
            ict_checklist(sig),
        )
    )
    for uid, pairs in d.items():
        try:
            uid = int(uid)
        except Exception:
            continue
        if not isinstance(pairs, list):
            continue
        if "ALL" not in pairs and pair not in pairs:
            continue
        if too_soon("watch:%s:%s" % (uid, pair), 900):
            continue
        try:
            send_message(token, uid, text, kb_after())
        except Exception:
            log("watch fail " + str(uid))


def live_positions_text(chat_id):
    rows = load_trades()
    mine = [
        t
        for t in rows
        if t.get("status") == "open" and str(t.get("chat_id")) == str(chat_id)
    ]
    if not mine:
        return (
            tz_head(u"📡 معاملات")
            + u"الان معاملهٔ باز ثبت‌شده نداری.\nسیگنال‌های کانال را از بخش وین‌ریت ببین."
            + u"\n"
            + tz_foot()
        )
    lines = [tz_head(u"📡 معاملات باز")]
    for t in mine[-6:]:
        pair = t.get("pair")
        try:
            rows5 = fetch_ohlc(pair, "5m", "1d")
            px = rows5[-1]["c"] if rows5 else None
        except Exception:
            px = None
        px_s = fmt_px(pair, px) if px is not None else "-"
        extra = ""
        try:
            entry, sl, tp = float(t["entry"]), float(t["sl"]), float(t["tp"])
            if px is not None and entry != sl:
                if t.get("side") == "BUY":
                    r = (px - entry) / (entry - sl)
                    left = (tp - px) / (tp - entry) if tp != entry else 0
                else:
                    r = (entry - px) / (sl - entry)
                    left = (px - tp) / (entry - tp) if entry != tp else 0
                extra = u" · R الان %.1f · تا هدف %.0f٪" % (r, max(0, min(100, (1 - left) * 100)))
        except Exception:
            extra = ""
        lines.append(
            u"%s <b>%s</b> %s\n   ورود %s · SL %s · TP %s\n   زنده <code>%s</code>%s"
            % (
                (PAIRS.get(pair) or {}).get("emoji") or "",
                pair,
                t.get("side"),
                fmt_px(pair, t.get("entry")),
                fmt_px(pair, t.get("sl")),
                fmt_px(pair, t.get("tp")),
                px_s,
                extra,
            )
        )
    lines.append(tz_foot())
    return u"\n".join(lines)

_TF_SCAN = (
    ("15m", "10d", u"۱۵م"),
    ("5m", "5d", u"۵م"),
    ("1h", "60d", u"۱ساعته"),
)


def build_signal(rows, pair, interval="15m"):
    sig = ict_2022(rows, pair, interval=interval)
    if sig:
        lab = dict((a, c) for a, b, c in _TF_SCAN).get(interval, interval)
        sig["tf"] = interval
        sig["tf_label"] = lab
        if sig.get("side") in ("BUY", "SELL") and interval != "5m":
            try:
                sig = refine_entry_5m(sig, pair)
            except Exception:
                log("refine5 " + traceback.format_exc())
    return sig


def scan_signal(pair, prefer=None):
    from concurrent.futures import ThreadPoolExecutor

    htf = htf_context(pair, 0) or {}

    def one(spec):
        interval, rng, label = spec
        try:
            rows = fetch_ohlc(pair, interval, rng)
            sig = ict_2022(rows, pair, interval=interval, htf=htf)
            if not sig:
                return None
            sig["tf"] = interval
            sig["tf_label"] = label
            sig["_rows"] = rows
            if sig.get("side") in ("BUY", "SELL") and interval in ("15m", "30m", "1h"):
                try:
                    sig = refine_entry_5m(sig, pair)
                except Exception:
                    pass
            return sig
        except Exception:
            log("scan %s %s %s" % (pair, interval, traceback.format_exc()))
            return None

    with ThreadPoolExecutor(max_workers=5) as ex:
        found = [f.result() for f in [ex.submit(one, s) for s in _TF_SCAN]]
    found = [s for s in found if s]
    live = [s for s in found if s.get("side") in ("BUY", "SELL")]
    if live:
        if prefer in ("5m", "15m", "1h", "4h", "30m"):
            pref = [s for s in live if s.get("tf") == prefer]
            if pref:
                live = pref + [s for s in live if s.get("tf") != prefer]
        live.sort(
            key=lambda s: (
                -int(s.get("score") or 0),
                -int(bool(s.get("inside_fvg"))),
                -int(bool(s.get("aligned"))),
                -int(bool(s.get("ote"))),
                {"15m": 0, "30m": 1, "1h": 2, "5m": 3, "4h": 4}.get(s.get("tf"), 9),
            )
        )
        if prefer in ("5m", "15m", "1h", "4h", "30m"):
            pref = [s for s in live if s.get("tf") == prefer]
            if pref and int(pref[0].get("score") or 0) >= int(live[0].get("score") or 0) - 1:
                return pref[0]
        return live[0]

    def prog(s):
        f = s.get("forming") or {}
        return (
            int(f.get("sweep") or 0)
            + int(f.get("mss") or 0)
            + int(f.get("fvg") or 0)
            + int(f.get("in_fvg") or 0)
        )

    found.sort(key=prog, reverse=True)
    return found[0] if found else None

def fmt_px(pair, x):
    try:
        x = float(x)
    except Exception:
        return "-"
    meta = PAIRS.get(pair) or {}
    try:
        d = int(meta.get("digits") or 0)
    except Exception:
        d = 0
    if d <= 0:
        ax = abs(x)
        d = 1 if ax >= 1000 else (4 if ax >= 1 else 6)
    try:
        return ("%." + str(d) + "f") % x
    except Exception:
        return str(x)


TV_SYMBOL = {
    "EURUSD": "FX:EURUSD",
    "GBPUSD": "FX:GBPUSD",
    "XAUUSD": "OANDA:XAUUSD",
    "BTCUSDT": "BINANCE:BTCUSDT",
    "ETHUSDT": "BINANCE:ETHUSDT",
    "SOLUSDT": "BINANCE:SOLUSDT",
}


def tv_url(pair):
    return "https://www.tradingview.com/chart/?symbol=" + TV_SYMBOL.get(pair, pair)


_F = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "@": (14, 17, 23, 21, 23, 16, 15),
    ".": (0, 0, 0, 0, 0, 0, 4),
    ":": (0, 4, 0, 0, 4, 0, 0),
    "-": (0, 0, 0, 14, 0, 0, 0),
    "+": (0, 4, 4, 31, 4, 4, 0),
    "/": (1, 2, 2, 4, 8, 8, 16),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 2, 4, 8, 31),
    "3": (14, 17, 1, 6, 1, 17, 14),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (6, 8, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 2, 12),
    "A": (14, 17, 17, 31, 17, 17, 17),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 19, 17, 17, 14),
    "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "K": (17, 18, 20, 24, 20, 18, 17),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17),
    "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14),
    "P": (30, 17, 17, 30, 16, 16, 16),
    "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (14, 17, 16, 14, 1, 17, 14),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 21, 10),
    "X": (17, 17, 10, 4, 10, 17, 17),
    "Y": (17, 17, 10, 4, 4, 4, 4),
    "J": (15, 2, 2, 2, 2, 18, 12),
    "Q": (14, 17, 17, 17, 21, 18, 13),
    "Z": (31, 1, 2, 4, 8, 16, 31),
    "%": (17, 18, 4, 4, 4, 9, 17),
    ",": (0, 0, 0, 0, 0, 4, 8),
    "(": (4, 8, 8, 8, 8, 8, 4),
    ")": (4, 2, 2, 2, 2, 2, 4),
    "=": (0, 0, 31, 0, 31, 0, 0),
    "'": (4, 4, 0, 0, 0, 0, 0),
}


def _png(w, h, rgb):
    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    raw = b"".join(b"\x00" + rgb[y * w * 3 : (y + 1) * w * 3] for y in range(h))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 6))
        + chunk(b"IEND", b"")
    )


def _sanitize_ohlc(rows):
    out = []
    for r in rows or []:
        try:
            o = float(r["o"])
            h = float(r["h"])
            l = float(r["l"])
            c = float(r["c"])
            t = int(r["t"])
        except Exception:
            continue
        if h < l:
            h, l = l, h
        h = max(h, o, c)
        l = min(l, o, c)
        if l <= 0 or h <= 0:
            continue
        rec = {"t": t, "o": o, "h": h, "l": l, "c": c}
        if out and rec["t"] <= out[-1]["t"]:
            out[-1] = rec
            continue
        out.append(rec)
    if len(out) >= 2:
        a, b = out[-2], out[-1]
        if b["h"] == b["l"] and abs(b["c"] - a["c"]) < 1e-12:
            out.pop()
    return out


def _ema(vals, n):
    if not vals:
        return []
    k = 2.0 / (n + 1.0)
    out = [vals[0]]
    for v in vals[1:]:
        out.append(v * k + out[-1] * (1.0 - k))
    return out


def _chart_tools(W, H, buf):
    def px(x, y, c):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            buf[i] = c[0]
            buf[i + 1] = c[1]
            buf[i + 2] = c[2]

    def mix(x, y, c, a=90):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            ia = 255 - a
            buf[i] = (buf[i] * ia + c[0] * a) // 255
            buf[i + 1] = (buf[i + 1] * ia + c[1] * a) // 255
            buf[i + 2] = (buf[i + 2] * ia + c[2] * a) // 255

    def fill(x0, y0, x1, y1, c):
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        x0 = max(0, x0)
        x1 = min(W - 1, x1)
        y0 = max(0, y0)
        y1 = min(H - 1, y1)
        for y in range(y0, y1 + 1):
            row = y * W * 3
            for x in range(x0, x1 + 1):
                i = row + x * 3
                buf[i] = c[0]
                buf[i + 1] = c[1]
                buf[i + 2] = c[2]

    def round_fill(x0, y0, x1, y1, c, r=6):
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        rr = r * r
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                dx = min(x - x0, x1 - x)
                dy = min(y - y0, y1 - y)
                if dx < r and dy < r and (r - dx) * (r - dx) + (r - dy) * (r - dy) > rr:
                    continue
                px(x, y, c)

    def hline(y, x0, x1, c, step=1, thick=1):
        if x0 > x1:
            x0, x1 = x1, x0
        for t in range(thick):
            yy = y + t
            if 0 <= yy < H:
                for x in range(max(0, x0), min(W, x1 + 1), step):
                    px(x, yy, c)

    def vline(x, y0, y1, c, thick=1):
        if y0 > y1:
            y0, y1 = y1, y0
        for t in range(thick):
            xx = x + t
            if 0 <= xx < W:
                for y in range(max(0, y0), min(H, y1 + 1)):
                    px(xx, y, c)

    def hdash(y, x0, x1, c, on=6, off=4, thick=1):
        x = x0
        while x <= x1:
            hline(y, x, min(x + on, x1), c, 1, thick)
            x += on + off

    def vdash(x, y0, y1, c, on=4, off=4):
        y = y0
        while y <= y1:
            vline(x, y, min(y + on, y1), c)
            y += on + off

    def glyph(ch, x, y, c, s=1):
        bits = _F.get(ch.upper() if ch.isalpha() else ch, (0,) * 7)
        for ry, row in enumerate(bits):
            for rx in range(5):
                if row & (16 >> rx):
                    for dy in range(s):
                        for dx in range(s):
                            px(x + rx * s + dx, y + ry * s + dy, c)

    def text(s, x, y, c, sc=1):
        s = (s or "").upper()
        for ch in s:
            glyph(ch, x, y, c, sc)
            x += 5 * sc + 1
        return x

    def text_w(s, sc=1):
        return len(s or "") * (5 * sc + 1)

    def mix_fill(x0, y0, x1, y1, c, a=40):
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        x0 = max(0, int(x0))
        x1 = min(W - 1, int(x1))
        y0 = max(0, int(y0))
        y1 = min(H - 1, int(y1))
        ia = 255 - a
        r, g, b = c
        for y in range(y0, y1 + 1):
            row = y * W * 3
            for x in range(x0, x1 + 1):
                i = row + x * 3
                buf[i] = (buf[i] * ia + r * a) // 255
                buf[i + 1] = (buf[i + 1] * ia + g * a) // 255
                buf[i + 2] = (buf[i + 2] * ia + b * a) // 255

    def round_mix(x0, y0, x1, y1, c, a=50, r=8):
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        rr = r * r
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                dx = min(x - x0, x1 - x)
                dy = min(y - y0, y1 - y)
                if dx < r and dy < r and (r - dx) * (r - dx) + (r - dy) * (r - dy) > rr:
                    continue
                mix(x, y, c, a)

    def line_poly(pts, c, a=180):
        if len(pts) < 2:
            return
        for i in range(1, len(pts)):
            x0, y0 = pts[i - 1]
            x1, y1 = pts[i]
            dx = x1 - x0
            dy = y1 - y0
            steps = max(abs(dx), abs(dy), 1)
            for k in range(steps + 1):
                x = x0 + dx * k // steps
                y = y0 + dy * k // steps
                mix(x, y, c, a)
                mix(x, y - 1, c, a // 2)

    T = {
        "px": px,
        "mix": mix,
        "fill": fill,
        "round_fill": round_fill,
        "hline": hline,
        "vline": vline,
        "hdash": hdash,
        "vdash": vdash,
        "text": text,
        "text_w": text_w,
        "line_poly": line_poly,
        "mix_fill": mix_fill,
        "round_mix": round_mix,
    }
    return T


def _paint_price_panel(
    buf,
    W,
    H,
    rows,
    pair,
    sig=None,
    box=None,
    label="15m",
    live_px=None,
    max_bars=96,
    show_levels=True,
    show_ema=True,
    compact=False,
):
    bg = (8, 11, 20)
    card = (12, 18, 32)
    ink = (236, 240, 247)
    muted = (132, 142, 160)
    dim = (58, 68, 88)
    gridc = (28, 36, 52)
    teal = (46, 230, 166)
    rose = (255, 77, 106)
    gold = (232, 196, 106)
    blue = (88, 168, 255)
    orange = (255, 168, 76)
    purple = (176, 132, 255)
    T = _chart_tools(W, H, buf)
    text, text_w = T["text"], T["text_w"]
    fill, round_fill = T["fill"], T["round_fill"]
    hline, vline = T["hline"], T["vline"]
    hdash, mix = T["hdash"], T["mix"]
    line_poly = T["line_poly"]
    mix_fill, round_mix = T["mix_fill"], T["round_mix"]

    if box is None:
        x0, y0, x1, y1 = 0, 0, W - 1, H - 1
    else:
        x0, y0, x1, y1 = box

    fill(x0, y0, x1, y1, bg)
    # corner glow
    gw = (x1 - x0) // 2
    gh = (y1 - y0) // 2
    mix_fill(x1 - gw, y0, x1, y0 + gh, (90, 18, 42), 28)
    mix_fill(x0, y1 - gh, x0 + gw, y1, (16, 40, 90), 22)
    mix_fill(x0, y0, x0 + gw // 2, y0 + gh // 2, (40, 28, 8), 18)

    rows = _sanitize_ohlc(rows)
    nkeep = max(8, int(max_bars or 96))
    rows = rows[-nkeep:]
    n = len(rows)
    if n < 5:
        round_fill(x0 + 24, y0 + 90, x1 - 24, y1 - 40, card, 18)
        text("NO DATA  " + (pair or ""), x0 + 48, y0 + 140, muted, 2)
        return

    last = float(live_px) if live_px is not None else rows[-1]["c"]
    first = rows[0]["c"]
    chg = ((last - first) / first * 100.0) if first else 0.0
    up = last >= first
    side = (sig or {}).get("side") or ""
    sc = (sig or {}).get("score")
    if side == "SELL":
        accent = rose
        smark = "SELL"
    elif side == "BUY":
        accent = teal
        smark = "BUY"
    else:
        accent = teal if up else rose
        smark = "WAIT"

    names = {"XAUUSD": "GOLD", "EURUSD": "EURUSD", "GBPUSD": "GBPUSD"}
    ticks = {"XAUUSD": "XAU", "EURUSD": "EUR", "GBPUSD": "GBP"}
    title = names.get(pair, pair or "")
    tick = ticks.get(pair, (pair or "")[:3])

    head_h = 70 if compact else 132
    foot_h = 36 if compact else 70
    pl = x0 + 28
    pr = x1 - (100 if compact else 148)
    pt = y0 + head_h
    pb = y1 - foot_h
    if pr - pl < 80 or pb - pt < 60:
        return

    candle_lo = min(r["l"] for r in rows)
    candle_hi = max(r["h"] for r in rows)
    crange = (candle_hi - candle_lo) or 1e-6
    mid = (candle_hi + candle_lo) / 2.0
    lo, hi = candle_lo, candle_hi
    levels = []
    offchart = []
    if show_levels and sig:
        for key, col, nm in (("tp", teal, "TP"), ("entry", blue, "IN"), ("sl", rose, "SL")):
            if sig.get(key) is None:
                continue
            try:
                pv = float(sig[key])
            except Exception:
                continue
            lab = "%s  %s" % (nm, fmt_px(pair, pv))
            if abs(pv - mid) <= crange * 1.65:
                levels.append((pv, col, lab))
                lo = min(lo, pv)
                hi = max(hi, pv)
            else:
                offchart.append((pv, col, lab, pv > hi))
        for k, col, nm in (("sweep_lvl", orange, "JUDAS"), ("mss_lvl", purple, "MSS")):
            if sig.get(k) is None:
                continue
            try:
                pv = float(sig[k])
            except Exception:
                continue
            if abs(pv - mid) <= crange * 1.65:
                lo = min(lo, pv)
                hi = max(hi, pv)

    padp = (hi - lo) * (0.10 if compact else 0.14) or 1e-6
    lo -= padp
    hi += padp
    span = hi - lo or 1e-6

    def yp(p):
        return int(pt + (hi - p) / span * (pb - pt))

    # header
    if compact:
        text(title, x0 + 18, y0 + 16, ink, 2)
        last_s = fmt_px(pair, last)
        text(last_s, x1 - 18 - text_w(last_s, 2), y0 + 16, accent, 2)
        chg_s = ("%s%.2f%%" % ("+" if chg >= 0 else "", chg)).replace(" ", "")
        text("%s  %s  %s" % (label, smark, chg_s), x0 + 18, y0 + 42, muted, 1)
    else:
        # asset initials (full logos live on chart_pro desk)
        tick_lab = (tick or title or "FX")[:4]
        round_fill(x0 + 22, y0 + 18, x0 + 66, y0 + 62, gold, 10)
        twl = text_w(tick_lab, 2)
        text(tick_lab, x0 + 22 + max(0, (44 - twl) // 2), y0 + 30, bg, 2)
        text(title, x0 + 78, y0 + 22, gold, 2)
        text("ICT  MARKET", x0 + 78, y0 + 46, muted, 1)
        # pair
        text(title, x0 + 22, y0 + 78, ink, 3)
        twp = text_w(title, 3)
        pillw = text_w(tick, 1) + 16
        round_fill(x0 + 22 + twp + 12, y0 + 80, x0 + 22 + twp + 12 + pillw, y0 + 100, (24, 32, 48), 8)
        T["hline"](y0 + 80, x0 + 22 + twp + 12, x0 + 22 + twp + 12 + pillw, gold, 1, 1)
        T["hline"](y0 + 100, x0 + 22 + twp + 12, x0 + 22 + twp + 12 + pillw, gold, 1, 1)
        text(tick, x0 + 22 + twp + 20, y0 + 84, gold, 1)
        sess = in_killzone(int(time.time())) or ""
        if u"لندن" in sess:
            sess_en = "LONDON"
        elif u"نیویورک" in sess:
            sess_en = "NEW YORK"
        else:
            sess_en = "OFF KZ"
        badge = "%s · %s · %s" % (str(label).upper(), smark, sess_en)
        bw0 = text_w(badge, 1) + 28
        round_fill(x1 - 22 - bw0, y0 + 16, x1 - 22, y0 + 38, (22, 28, 42), 8)
        mix(x1 - 22 - bw0 + 10, y0 + 27, rose if side == "SELL" else teal, 230)
        text(badge, x1 - 22 - bw0 + 18, y0 + 22, muted, 1)
        last_s = fmt_px(pair, last)
        psc = 4 if len(last_s) <= 10 else 3
        tw = text_w(last_s, psc)
        text(last_s, x1 - 22 - tw, y0 + 48, ink, psc)
        text("USD", x1 - 22 - tw - text_w("USD", 1) - 12, y0 + 62, muted, 1)
        chg_s = ("%s%.2f%%" % ("+" if chg >= 0 else "", chg)).replace(" ", "")
        bw = text_w(chg_s, 1) + 22
        round_fill(x1 - 22 - bw, y0 + 96, x1 - 22, y0 + 118, accent, 8)
        text(chg_s, x1 - 22 - bw + 10, y0 + 102, bg, 1)

    # chart card
    round_fill(x0 + 16, pt - 8, x1 - 16, pb + 8, card, 16)
    round_mix(x0 + 16, pt - 8, x1 - 16, pb + 8, (255, 255, 255), 12, 16)

    # grid
    for g in range(4):
        p = lo + span * (g + 1) / 5.0
        y = yp(p)
        hdash(y, pl, pr, gridc, 5, 6, 1)
        ax = fmt_px(pair, p)
        text(ax, pr + 10, y - 3, dim, 1)

    # watermark
    if not compact:
        wm = "TZ FX"
        wx = pl + (pr - pl) // 2 - text_w(wm, 6) // 2
        wy = pt + (pb - pt) // 2 - 18
        for ch_i, ch in enumerate(wm):
            bits = _F.get(ch, (0,) * 7)
            # draw large faded
            text(ch, wx + ch_i * (5 * 6 + 8), wy, (22, 30, 46), 6)

    # FVG zone
    if show_levels and sig and sig.get("fvg_bot") is not None and sig.get("fvg_top") is not None:
        try:
            col = teal if sig.get("side") == "BUY" else rose
            y_a, y_b = yp(float(sig["fvg_top"])), yp(float(sig["fvg_bot"]))
            ya, yb = min(y_a, y_b), max(y_a, y_b)
            ya = max(pt, ya)
            yb = min(pb, yb)
            mix_fill(pl, ya, pr, yb, col, 28)
        except Exception:
            pass

    if show_levels and sig and sig.get("sweep_lvl") is not None:
        try:
            ys = yp(float(sig["sweep_lvl"]))
            if pt <= ys <= pb:
                hdash(ys, pl, pr, orange, 5, 4, 1)
                text("JUDAS", pl + 6, max(pt + 4, ys - 12), orange, 1)
        except Exception:
            pass
    if show_levels and sig and sig.get("mss_lvl") is not None:
        try:
            ym = yp(float(sig["mss_lvl"]))
            if pt <= ym <= pb:
                hdash(ym, pl, pr, purple, 4, 5, 1)
                text("MSS", pl + 6, min(pb - 14, ym + 4), purple, 1)
        except Exception:
            pass

    # area under close
    cw = float(pr - pl) / n
    closes = []
    for i, r in enumerate(rows):
        x = int(pl + i * cw + cw * 0.5)
        closes.append((x, yp(r["c"])))
    if len(closes) >= 2:
        for i in range(1, len(closes)):
            x0c, y0c = closes[i - 1]
            x1c, y1c = closes[i]
            ymid = (y0c + y1c) // 2
            mix_fill(x0c, ymid, x1c, pb, accent, 10)

    if show_ema and n >= 20:
        ema = _ema([r["c"] for r in rows], 20)
        pts = []
        for i, v in enumerate(ema):
            x = int(pl + i * cw + cw * 0.5)
            pts.append((x, yp(v)))
        line_poly(pts, blue, 140)

    # last price line
    yl = yp(last)
    if pt <= yl <= pb:
        hdash(yl, pl, pr, accent, 6, 4, 1)

    # candles
    body_w = max(3, int(cw * (0.52 if compact else 0.58)))
    if body_w % 2 == 0:
        body_w += 1
    body_w = min(body_w, max(3, int(cw) - 2))
    hi_i = max(range(n), key=lambda k: rows[k]["h"])
    lo_i = min(range(n), key=lambda k: rows[k]["l"])
    for i, r in enumerate(rows):
        x = int(pl + i * cw + cw * 0.5)
        col = teal if r["c"] >= r["o"] else rose
        yh, yl_ = yp(r["h"]), yp(r["l"])
        vline(x, yh, yl_, col, 1)
        y_o, y_c = yp(r["o"]), yp(r["c"])
        body0, body1 = (y_c, y_o) if y_c < y_o else (y_o, y_c)
        if body1 - body0 < 2:
            body1 = body0 + 2
        hw = max(1, body_w // 2)
        fill(x - hw, body0, x + hw, body1, col)
        if i == n - 1:
            round_mix(x - hw - 2, body0 - 2, x + hw + 2, body1 + 2, ink, 80, 2)

    # H / L tags
    if not compact:
        rh, rl_ = rows[hi_i], rows[lo_i]
        hx = int(pl + hi_i * cw + cw * 0.5)
        lx = int(pl + lo_i * cw + cw * 0.5)
        ht = "H %s" % fmt_px(pair, rh["h"])
        lt = "L %s" % fmt_px(pair, rl_["l"])
        text(ht, max(pl, hx - text_w(ht, 1) // 2), max(pt + 4, yp(rh["h"]) - 14), muted, 1)
        text(lt, max(pl, lx - text_w(lt, 1) // 2), min(pb - 12, yp(rl_["l"]) + 6), muted, 1)

    # last price pill
    if pt <= yl <= pb:
        tag = fmt_px(pair, last)
        twt = text_w(tag, 1) + 16
        bx = min(pr + 8, x1 - twt - 20)
        round_fill(bx, yl - 10, bx + twt, yl + 10, accent, 8)
        text(tag, bx + 8, yl - 6, bg, 1)

    # time axis
    def _tlab(ts):
        return tehran_fmt(ts, "%H:%M")

    ticks_ax = []
    last_lab = None
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        idx = int(round((n - 1) * frac))
        idx = max(0, min(n - 1, idx))
        lab = _tlab(rows[idx]["t"])
        if lab == last_lab:
            continue
        ticks_ax.append((idx, lab))
        last_lab = lab
    for idx, lab in ticks_ax:
        x = int(pl + idx * cw + cw * 0.5) - text_w(lab, 1) // 2
        text(lab, max(pl, min(pr - text_w(lab, 1), x)), pb + 8, dim, 1)

    # TP IN SL
    placed = []
    for price, col, lab in levels:
        y = yp(price)
        if y < pt or y > pb:
            continue
        hline(y, pl, pr, col, 1, 2)
        ly = y - 8
        for py0 in placed:
            if abs(ly - py0) < 16:
                ly = py0 + 16
        ly = max(pt + 2, min(pb - 14, ly))
        placed.append(ly)
        lw = text_w(lab, 1) + 12
        bx = min(pr + 6, x1 - lw - 18)
        round_fill(bx, ly - 2, bx + lw, ly + 12, col, 5)
        text(lab, bx + 6, ly + 1, bg, 1)

    for pv, col, lab, above in offchart:
        tag = lab + (" ^" if above else " v")
        ly = pt + 4 if above else pb - 14
        lw = text_w(tag, 1) + 12
        bx = min(pr + 6, x1 - lw - 18)
        round_fill(bx, ly - 2, bx + lw, ly + 12, col, 5)
        text(tag, bx + 6, ly + 1, bg, 1)

    # footer
    if not compact:
        dt = tehran_fmt(None, "%Y-%m-%d  %H:%M")
        text(dt, x0 + 24, y1 - 16, dim, 1)
        handle = "@TZ_FX_BOT"
        hw = text_w(handle, 1) + 28
        hx0 = (x0 + x1) // 2 - hw // 2
        round_fill(hx0, y1 - 28, hx0 + hw, y1 - 8, (20, 26, 40), 10)
        round_mix(hx0, y1 - 28, hx0 + hw, y1 - 8, gold, 70, 10)
        text(handle, hx0 + 14, y1 - 22, gold, 1)
        if sc is not None:
            badge = "SCORE %s/6" % sc
            text(badge, x1 - 24 - text_w(badge, 1), y1 - 22, muted, 1)

def render_chart(rows, pair, sig=None, label="15m"):
    try:
        ensure_requests()
        vdir = os.path.join(HERE, "vendor")
        if os.path.isdir(vdir) and vdir not in sys.path:
            sys.path.insert(0, vdir)
        import chart_pro
        png = chart_pro.render(
            rows,
            pair,
            sig,
            label,
            fmt_px=fmt_px,
            tehran_fmt=tehran_fmt,
            in_killzone=in_killzone,
            fonts=os.path.join(HERE, "fonts"),
        )
        if png:
            return png
    except Exception:
        log("chart_pro " + traceback.format_exc())
    return _render_chart_bitmap(rows, pair, sig, label)


def _render_chart_bitmap(rows, pair, sig=None, label="15m"):
    W, H = 1280, 800
    bg = (8, 11, 20)
    buf = bytearray([bg[0], bg[1], bg[2]] * (W * H))
    _paint_price_panel(
        buf,
        W,
        H,
        rows,
        pair,
        sig=sig,
        box=(0, 0, W - 1, H - 1),
        label=label,
        max_bars=88,
        show_levels=True,
        show_ema=True,
        compact=False,
    )
    return _png(W, H, bytes(buf))


def stars(score, cap=6):
    s = max(0, min(int(score), cap))
    return u"🔥" * s + u"☆" * (cap - s)


TF_SPEC = [
    ("1m", "1d", "1m"),
    ("5m", "5d", "5m"),
    ("15m", "10d", "15m"),
    ("30m", "60d", "30m"),
    ("1h", "60d", "1H"),
    ("4h", "60d", "4H"),
    ("1d", "2y", "D1"),
    ("1wk", "5y", "W1"),
]


def tf_meta(code):
    for interval, rng, label in TF_SPEC:
        if code.lower() in (interval.lower(), label.lower(), interval.replace("h", "H")):
            return interval, rng, label
    return "15m", "10d", "15m"


def quick_bias(rows):
    if not rows or len(rows) < 16:
        return None
    price = rows[-1]["c"]
    window = rows[-20:] if len(rows) >= 20 else rows
    hi = max(r["h"] for r in window)
    lo = min(r["l"] for r in window)
    mid = (hi + lo) / 2.0
    pd = "DISCOUNT" if price <= mid else "PREMIUM"
    sh, sl = swing_points(rows, 2, 2)
    bias = "NEUTRAL"
    if sh and sl:
        if price > rows[sh[-1]]["h"]:
            bias = "BULL"
        elif price < rows[sl[-1]]["l"]:
            bias = "BEAR"
        else:
            bias = "BULL" if price >= mid else "BEAR"
    elif price >= mid:
        bias = "BULL"
    else:
        bias = "BEAR"
    return {"bias": bias, "pd": pd, "price": price}


def _one_tf(pair, interval, rng, label):
    try:
        rows = fetch_ohlc(pair, interval, rng)
        b = quick_bias(rows)
        if not b:
            return label, "—"
        if b["bias"] == "BULL":
            mark = "🟢"
        elif b["bias"] == "BEAR":
            mark = "🔴"
        else:
            mark = "⚪️"
        return label, "%s %s · %s" % (mark, b["bias"], b["pd"])
    except Exception:
        log("tf " + pair + " " + label + " " + traceback.format_exc())
        return label, "خطا"


def tf_board(pair, full=False):
    from concurrent.futures import ThreadPoolExecutor

    spec = TF_SPEC if full else [x for x in TF_SPEC if x[2] not in ("1m", "W1")]
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(_one_tf, pair, iv, rng, lab) for iv, rng, lab in spec]
        rows = [f.result() for f in futs]
    return "\n".join("⏱ <b>%s</b>  %s" % (label, val) for label, val in rows)


def kb_tf(pair):
    return {
        "inline_keyboard": [
            [
                {"text": "1m", "callback_data": "tf_%s_1m" % pair},
                {"text": "5m", "callback_data": "tf_%s_5m" % pair},
                {"text": "15m", "callback_data": "tf_%s_15m" % pair},
                {"text": "30m", "callback_data": "tf_%s_30m" % pair},
            ],
            [
                {"text": "1H", "callback_data": "tf_%s_1h" % pair},
                {"text": "4H", "callback_data": "tf_%s_4h" % pair},
                {"text": "D1", "callback_data": "tf_%s_1d" % pair},
                {"text": "📊 مولتی", "callback_data": "tf_%s_mtf" % pair},
            ],
            [
                btn(u"💶 یورو", "sig_EURUSD", style="primary"),
                btn(u"💷 پوند", "sig_GBPUSD", style="primary"),
                btn(u"🥇 طلا", "sig_XAUUSD", style="success"),
            ],
            [btn(u"📐 اطلاعات معامله", "trd_" + pair, style="success")],
            [
                btn(u"🎙️ مربی", "chat_ai", style="primary"),
                btn(u"🏠 TZ FX", "home"),
            ],
        ]
    }


def format_signal(sig):
    pair = sig["pair"]
    meta = PAIRS[pair]
    if is_crypto_pair(pair):
        unit = u"دلار"
    elif pair == "XAUUSD":
        unit = u"واحد"
    else:
        unit = u"پیپ"
    htf = sig.get("htf") or {}
    tf_l = sig.get("tf_label") or u"۱۵م"
    model = sig.get("model") or u"ICT"
    if is_crypto_pair(pair):
        model = u"ICT بتا · کریپتو"
    if sig["side"] == "NO SIGNAL":
        extra = ""
        if sig.get("buy_liq"):
            extra += u"\n🟢 نقدینگی خرید  <code>%s</code>" % fmt_px(pair, sig["buy_liq"])
        if sig.get("sell_liq"):
            extra += u"\n🔴 نقدینگی فروش  <code>%s</code>" % fmt_px(pair, sig["sell_liq"])
        hline = ""
        if htf:
            hline = u"\n🧭 ۱H  <b>%s</b> · %s" % (htf.get("bias") or "-", htf.get("pd") or "-")
        return (
            pe(u"✨")
            + u" <b>TZ FX</b>  ·  %s  <b>%s</b>\n<i>%s · %s · تهران</i>\n────────────\n"
            + pe(u"☕")
            + u"  <b>الان ستاپ کامل نیست</b>\nقیمت  <code>%s</code>%s\n<blockquote>"
            + pe(u"✋")
            + u" %s\nدست نگه دار، تعقیب نکن.</blockquote>%s\n📋 %s\n────────────\n<i>"
            + pe(u"⚖️")
            + u" آموزشی است  ·  مشاوره مالی نیست</i>"
        ) % (
            meta["emoji"],
            meta["name"],
            model,
            tf_l,
            fmt_px(pair, sig["price"]),
            hline,
            sig.get("reason") or u"ستاپ ICT کامل نیست",
            extra,
            ict_checklist(sig),
        )

    if sig["side"] == "BUY":
        head = pe(u"💚") + u"  <b>BUY</b>  بزن بریم"
    else:
        head = pe(u"❤️") + u"  <b>SELL</b>  بزن بریم"
    rr = (sig["reward_pips"] / sig["risk_pips"]) if sig.get("risk_pips") else 0
    sc = int(sig.get("score") or 0)
    if sc >= 5:
        quality = u"قوی"
    elif sc >= 4:
        quality = u"قابل‌قبول"
    else:
        quality = u"ضعیف"
    warn = (u"\n⚠️ " + sig["warn"]) if sig.get("warn") else ""
    verdict = sig.get("ai_verdict") or ""
    if verdict == "CONFIRM":
        ai_line = pe(u"🤖") + u" مربی تأیید کرد " + pe(u"👍") + u"\n"
    elif verdict == "REJECT":
        ai_line = pe(u"🤖") + u" مربی گفت وارد نشو\n"
    else:
        ai_line = ""
    fvg_b = sig.get("fvg_bot")
    fvg_t = sig.get("fvg_top")
    try:
        fvg_s = u"<code>%s</code> — <code>%s</code>" % (fmt_px(pair, fvg_b), fmt_px(pair, fvg_t))
    except Exception:
        fvg_s = u"—"
    return (
        pe(u"✨")
        + u" <b>TZ FX</b>  ·  %s  <b>%s</b>\n<i>%s · %s · تهران</i>\n────────────\n%s    %s  <b>%s/6</b>  %s\n"
        + pe(u"🕒")
        + u" %s\n"
        + pe(u"🌍")
        + u" %s\n"
        + pe(u"🧭")
        + u" ۱H  <b>%s</b> · %s\n────────────\n"
        + pe(u"🎯")
        + u" ورود          <code>%s</code>\n"
        + pe(u"🛡️")
        + u" حد ضرر       <code>%s</code>\n"
        + pe(u"🏁")
        + u" حد سود       <code>%s</code>\n"
        + pe(u"🚫")
        + u" باطل          بسته شدن ۱۵م آن‌سوی حد ضرر\n"
        + pe(u"📦")
        + u" FVG           %s\n"
        + pe(u"💥")
        + u" ریسک <b>%.1f</b> %s   ·   R:R  <b>1:%.1f</b>\n"
        + pe(u"💼")
        + u" حداکثر ۱٪ حساب · نرسید تعقیب نکن · اول دمو\n%s%s────────────\n<i>"
        + pe(u"⚖️")
        + u" آموزشی است  ·  مشاوره مالی نیست</i>"
    ) % (
        meta["emoji"],
        meta["name"],
        model,
        tf_l,
        head,
        stars(sc),
        sc,
        quality,
        sig.get("time") or tehran_fmt(),
        sig.get("killzone") or u"—",
        htf.get("bias") or "-",
        htf.get("pd") or "-",
        fmt_px(pair, sig["entry"]),
        fmt_px(pair, sig["sl"]),
        fmt_px(pair, sig["tp"]),
        fvg_s,
        sig.get("risk_pips") or 0,
        unit,
        rr,
        ai_line,
        warn,
    )


def format_signal_story(sig):
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return ""
    pair = sig["pair"]
    meta = PAIRS[pair]
    side = sig["side"]
    htf = sig.get("htf") or {}
    want = u"خرید" if side == "BUY" else u"فروش"
    steps = []
    steps.append(
        u"1️⃣ جهت تایم بالاتر: <b>%s</b> · %s"
        % (htf.get("bias") or "—", htf.get("pd") or "—")
    )
    kz = sig.get("killzone") or ""
    if kz and u"خارج" not in str(kz):
        steps.append(u"2️⃣ کیل‌زون فعال: %s" % kz)
    else:
        steps.append(u"2️⃣ کیل‌زون ضعیف/خارج — احتیاط")
    steps.append(u"3️⃣ Judas سوئیپ نقدینگی، بعد شکست ساختار (MSS)")
    if sig.get("inside_fvg"):
        steps.append(u"4️⃣ قیمت برگشت داخل FVG — تعقیب نکردیم")
    elif sig.get("ote"):
        steps.append(u"4️⃣ ورود در ناحیه OTE (تخفیف/پرمیوم)")
    else:
        steps.append(u"4️⃣ نزدیک آرایه قیمتی")
    steps.append(
        u"5️⃣ حد ضرر پشت شدوی سوئیپ  <code>%s</code>" % fmt_px(pair, sig["sl"])
    )
    steps.append(
        u"6️⃣ حد سود روی نقدینگی مخالف  <code>%s</code>" % fmt_px(pair, sig["tp"])
    )
    how = (
        u"نزدیک ورود بزن؛ دور شد ولش کن. حداکثر ۱٪ حساب. "
        u"بعد از ۱R حد ضرر را روی ورود بیاور. اول دمو — من کنارت‌ام."
    )
    conf = " · ".join(sig.get("confluence") or [])
    conf_l = (u"\n🔹 " + conf) if conf else ""
    note = (sig.get("ai_note") or "").strip()
    ai = (u"\n🤖 " + note) if note else ""
    warn = (u"\n⚠️ " + sig["warn"]) if sig.get("warn") else ""
    setup = sig.get("setup") or u"ICT"
    return (
        pe(u"🧠")
        + u" <b>داستان همین سیگنال</b>\n%s <b>%s</b>  ·  %s  ·  %s\n<i>%s</i>\n────────────\n%s\n────────────\n📋 %s%s%s%s\n────────────\n"
        + pe(u"💡")
        + u" %s\n<i>"
        + pe(u"🤝")
        + u" آموزشی است · مشاوره مالی نیست</i>"
    ) % (
        meta["emoji"],
        pair,
        want,
        sig.get("tf_label") or u"۱۵م",
        setup,
        u"\n".join(steps),
        ict_checklist(sig),
        conf_l,
        ai,
        warn,
        how,
    )


def in_channel(token, user_id):
    if not user_id:
        return False
    now = time.time()
    hit = _member_cache.get(int(user_id))
    if hit and (now - hit[0]) < 180:
        return hit[1]
    try:
        r = http().get(
            tg_api(token) + "/getChatMember",
            params={"chat_id": CHANNEL_ID, "user_id": int(user_id)},
            timeout=6,
        )
        data = r.json()
        ok = False
        if data.get("ok"):
            status = (data.get("result") or {}).get("status")
            ok = status in ("member", "administrator", "creator")
        _member_cache[int(user_id)] = (now, ok)
        return ok
    except Exception:
        log("in_channel error")
        return False


def txt_join():
    return tz_head(T("head.join")) + T("txt.join")


def txt_start():
    return tz_head(T("head.home")) + T("txt.start") % tehran_fmt() + u"\n" + tz_foot()



def txt_help():
    return tz_head(T("cmd.help")) + T("txt.help") + u"\n" + tz_foot()



def txt_me(uid):
    if is_pro(uid):
        left = sub_until(uid) - time.time()
        days = int(left / 86400) + 1 if left > 0 else 0
        return (
            tz_head(u"اشتراک")
            + T("txt.me_on") % (tehran_fmt(sub_until(uid)), fa_num(days) if get_lang(uid)=="fa" else str(days), PRO_URL)
        )
    return (
        tz_head(u"اشتراک")
        + T("txt.me_off")
    )

def _sig_snap(sig):
    return {
        "pair": sig.get("pair"),
        "side": sig.get("side"),
        "entry": sig.get("entry"),
        "sl": sig.get("sl"),
        "tp": sig.get("tp"),
        "price": sig.get("price"),
        "risk_pips": sig.get("risk_pips"),
        "reward_pips": sig.get("reward_pips"),
        "score": sig.get("score"),
        "ts": time.time(),
    }


def save_last(sig, uid=None):
    rec = _sig_snap(sig)
    data = _jload(LAST_FILE, {})
    if not isinstance(data, dict):
        data = {}
    data["last"] = rec
    if uid:
        data[str(uid)] = rec
    _jsave(LAST_FILE, data)


def load_last(uid=None):
    data = _jload(LAST_FILE, {})
    if not isinstance(data, dict):
        return None
    if uid:
        rec = data.get(str(uid))
        return rec if isinstance(rec, dict) else None
    if data.get("pair"):
        return data
    rec = data.get("last")
    return rec if isinstance(rec, dict) else None


def too_soon(key, sec):
    now = time.time()
    if now - float(_rate.get(key) or 0) < sec:
        return True
    _rate[key] = now
    return False


def over_hour(key, limit):
    now = time.time()
    start, n = _hour.get(key) or (now, 0)
    if now - start > 3600:
        start, n = now, 0
    n += 1
    _hour[key] = (start, n)
    return n > limit


def load_trades():
    data = _jload(TRADES_FILE, [])
    return data if isinstance(data, list) else []


def save_trades(rows):
    now = time.time()
    opens = []
    done = []
    for t in rows:
        if not isinstance(t, dict):
            continue
        st = t.get("status") or "open"
        ts = float(t.get("closed_ts") or t.get("ts") or 0)
        if st == "open":
            opens.append(t)
        elif now - ts < 90 * 86400:
            done.append(t)
    _jsave(TRADES_FILE, opens + done[-350:])


def trade_fingerprint(t):
    try:
        return "%s|%s|%.4f|%.4f" % (
            t.get("pair") or "",
            t.get("side") or "",
            float(t.get("entry") or 0),
            float(t.get("sl") or 0),
        )
    except Exception:
        return str(t.get("msgid") or "") + ":" + str(t.get("ts") or "")


def _as_msgid(raw):
    if raw is True or raw is False or raw is None:
        return None
    try:
        n = int(raw)
    except Exception:
        return None
    if n <= 0:
        return None
    return n


def register_trade(sig, chat_id, msgid, source):
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return
    if not sig.get("sl") or not sig.get("tp"):
        return
    rows = load_trades()
    for t in rows:
        if (
            t.get("status") == "open"
            and t.get("pair") == sig.get("pair")
            and t.get("side") == sig.get("side")
            and str(t.get("chat_id")) == str(chat_id)
        ):
            return
    rec = {
        "pair": sig["pair"],
        "side": sig["side"],
        "entry": sig.get("entry"),
        "sl": sig["sl"],
        "tp": sig["tp"],
        "chat_id": chat_id,
        "msgid": _as_msgid(msgid),
        "source": source,
        "ts": time.time(),
        "status": "open",
        "r1": False,
        "mid": False,
        "near": False,
        "score": sig.get("score"),
        "tf": sig.get("tf") or sig.get("tf_label"),
        "risk_pips": sig.get("risk_pips"),
        "reward_pips": sig.get("reward_pips"),
        "setup": sig.get("setup"),
        "gen": ENGINE_GEN,
        "fp": trade_fingerprint(
            {
                "pair": sig["pair"],
                "side": sig["side"],
                "entry": sig.get("entry"),
                "sl": sig["sl"],
            }
        ),
    }
    rows.append(rec)
    save_trades(rows)


def _notify_trade(token, t, text, kb):
    cid = t.get("chat_id")
    if not cid:
        return False
    rid = _as_msgid(t.get("msgid"))
    ok = send_message(token, cid, text, kb, reply_to=rid)
    if not ok and rid:
        ok = send_message(token, cid, text, kb)
    return ok


def _bars_for_pair(pair):
    path = fetch_ohlc(pair, "5m", "5d", cap=520) or []
    px = path[-1]["c"] if path else None
    if not path:
        path = fetch_ohlc(pair, "15m", "10d") or []
        px = path[-1]["c"] if path else None
    return path, px


def _first_hit(side, sl, tp, walk):
    for bar in walk:
        h = bar.get("h")
        l = bar.get("l")
        if h is None or l is None:
            continue
        if side == "BUY":
            sl_hit = l <= sl
            tp_hit = h >= tp
        else:
            sl_hit = h >= sl
            tp_hit = l <= tp
        if sl_hit and tp_hit:
            return "SL"
        if sl_hit:
            return "SL"
        if tp_hit:
            return "TP"
    return None


def _px_safe(pair, x):
    try:
        return fmt_px(pair, float(x))
    except Exception:
        return "-"


def _trade_result_text(t, hit, px):
    pair = t.get("pair")
    meta = PAIRS.get(pair) or {}
    side = t.get("side") or ""
    try:
        entry = float(t.get("entry") or 0)
        sl = float(t.get("sl") or 0)
        tp = float(t.get("tp") or 0)
        risk = abs(entry - sl) or 1e-9
        if hit == "TP":
            rr = abs(tp - entry) / risk
        else:
            rr = -1.0
    except Exception:
        rr = 0.0
    if hit == "TP":
        return (
            pe(u"🎉") + u" <b>حد سود خورد!</b>\n"
            u"%s <b>%s</b>  ·  %s\n"
            u"ورود <code>%s</code>  →  الان <code>%s</code>\n"
            u"نتیجه  <b>%+.1fR</b>  " + pe(u"✨") + u"\n"
            u"آفرین — این ستاپ ICT بسته شد. آموزشی است."
        ) % (
            meta.get("emoji") or "",
            pair,
            side,
            _px_safe(pair, t.get("entry")),
            _px_safe(pair, px),
            rr,
        )
    if hit == "SL":
        return (
            pe(u"😔") + u" <b>حد ضرر خورد</b>\n"
            u"%s <b>%s</b>  ·  %s\n"
            u"ورود <code>%s</code>  →  الان <code>%s</code>\n"
            u"نتیجه  <b>−۱R</b>\n"
            u"اشکال نداره — ستاپ باطل شد، دنبال نکن. آموزشی است."
        ) % (
            meta.get("emoji") or "",
            pair,
            side,
            _px_safe(pair, t.get("entry")),
            _px_safe(pair, px),
        )
    return (
        pe(u"⏳") + u" <b>این یکی نه برد شد نه باخت</b>\n"
        u"%s <b>%s</b>  ·  %s\n"
        u"۳۶ ساعت گذشت؛ می‌ذاریمش کنار.\n"
        u"تو وین‌ریت نه برد است نه باخت."
    ) % (meta.get("emoji") or "", pair, side)


def monitor_trades(token):
    rows = load_trades()
    if not rows:
        return
    now = time.time()
    cache = {}
    changed = False

    def bars_of(pair):
        if pair not in cache:
            try:
                cache[pair] = _bars_for_pair(pair)
            except Exception:
                cache[pair] = ([], None)
        return cache[pair]

    for t in rows:
        if t.get("status") != "open":
            continue
        try:
            age = now - float(t.get("ts") or 0)
        except Exception:
            age = 0
        pair = t.get("pair")
        src = t.get("source") or ""
        kb = kb_open_bot("wr") if src == "channel" else kb_after()
        if age > 12 * 3600:
            t["status"] = "expired"
            t["closed_ts"] = now
            changed = True
            try:
                _notify_trade(token, t, _trade_result_text(t, "EXP", None), kb)
            except Exception:
                log("trade expire notify " + traceback.format_exc())
            continue
        if pair not in PAIRS:
            continue
        path, px = bars_of(pair)
        since = float(t.get("ts") or 0) - 180
        walk = [b for b in path if int(b.get("t") or 0) >= since]
        if len(walk) < 1:
            walk = path[-12:] if path else []
        try:
            sl = float(t["sl"])
            tp = float(t["tp"])
            entry = float(t.get("entry") or sl)
        except Exception:
            continue
        side = t.get("side")
        hit = _first_hit(side, sl, tp, walk) if walk else None
        if hit:
            t["status"] = hit.lower()
            t["closed_ts"] = now
            t["exit"] = px
            try:
                t["r"] = round(float(_r_of(t)), 2)
            except Exception:
                t["r"] = 0.0
            changed = True
            try:
                ok = _notify_trade(token, t, _trade_result_text(t, hit, px), kb)
                if not ok:
                    log("trade notify fail %s %s chat=%s" % (hit, pair, t.get("chat_id")))
                else:
                    log("trade %s %s chat=%s" % (hit, pair, t.get("chat_id")))
            except Exception:
                log("trade notify " + traceback.format_exc())
            continue
        if px is None:
            continue
        risk = abs(entry - sl) or 1e-9
        if side == "BUY":
            r_now = (px - entry) / risk
            prog = (px - entry) / abs(tp - entry) if tp != entry else 0
        else:
            r_now = (entry - px) / risk
            prog = (entry - px) / abs(entry - tp) if tp != entry else 0
        if r_now >= 1.0 and not t.get("r1"):
            t["r1"] = True
            changed = True
            _notify_trade(
                token,
                t,
                pe(u"🛡️") + u" <b>۱R شد — حد ضرر را روی ورود بیاور</b>\n"
                u"%s <b>%s</b>  ·  زنده <code>%s</code>\n"
                u"نفس بکش؛ الان بی‌ریسکش کن. آموزشی است."
                % ((PAIRS.get(pair) or {}).get("emoji") or "", pair, _px_safe(pair, px)),
                kb,
            )
        if src == "channel":
            continue
        if prog >= 0.5 and not t.get("mid"):
            t["mid"] = True
            changed = True
            _notify_trade(
                token,
                t,
                u"🎯 نیمه راه تا حد سود\n%s <b>%s</b>  ·  زنده <code>%s</code>"
                % ((PAIRS.get(pair) or {}).get("emoji") or "", pair, _px_safe(pair, px)),
                kb,
            )
        if r_now <= -0.7 and not t.get("near"):
            t["near"] = True
            changed = True
            _notify_trade(
                token,
                t,
                u"⚠️ نزدیک حد ضرر\n%s <b>%s</b>  ·  زنده <code>%s</code>\nاگر ساختار شکست، خارج شو."
                % ((PAIRS.get(pair) or {}).get("emoji") or "", pair, _px_safe(pair, px)),
                kb,
            )
    if changed:
        save_trades(rows)


def _paper_fresh(on=False):
    return {
        "on": bool(on),
        "bal": float(PAPER_START),
        "start": float(PAPER_START),
        "risk": float(PAPER_RISK),
        "opened": 0,
        "wins": 0,
        "loss": 0,
        "peak": float(PAPER_START),
    }


def load_paper():
    d = _jload(PAPER_FILE, None)
    if not isinstance(d, dict):
        d = {"accounts": {}, "pos": []}
    if not isinstance(d.get("accounts"), dict):
        d["accounts"] = {}
    if not isinstance(d.get("pos"), list):
        d["pos"] = []
    k = str(OWNER_ID)
    if k not in d["accounts"]:
        d["accounts"][k] = _paper_fresh(True)
        _jsave(PAPER_FILE, d)
    return d


def save_paper(d):
    pos = d.get("pos") or []
    opens = [t for t in pos if t.get("status") == "open"]
    done = [t for t in pos if t.get("status") != "open"][-120:]
    d["pos"] = opens + done
    _jsave(PAPER_FILE, d)


def paper_acc(uid, create=True, on=None):
    d = load_paper()
    k = str(uid)
    acc = d["accounts"].get(k)
    if acc is None and create:
        acc = _paper_fresh(True if is_owner(uid) else False)
        d["accounts"][k] = acc
        save_paper(d)
    if acc is not None and on is not None:
        acc["on"] = bool(on)
        d["accounts"][k] = acc
        save_paper(d)
    return d, acc


def _paper_qty_lab(pair, qty):
    p = (pair or "").upper()
    try:
        q = float(qty)
    except Exception:
        return "-"
    if p.endswith("USDT"):
        return "%.6f %s" % (q, p[:-4])
    if p == "XAUUSD":
        return "%.3f oz" % q
    return "%.2f lot" % (q / 100000.0)


def _paper_usd(x):
    try:
        v = float(x)
    except Exception:
        return "-"
    if abs(v) >= 100:
        return "%s%.0f" % ("+" if v > 0 else "", v)
    return "%s%.2f" % ("+" if v > 0 else "", v)


def kb_paper(uid=None):
    return {
        "inline_keyboard": [
            [
                btn(T("btn.paper_on"), "paper_on", style="success"),
                btn(T("btn.paper_off"), "paper_off", style="danger"),
            ],
            [btn(T("btn.paper_reset"), "paper_reset")],
            [btn(u"🧰 میز", "desk_menu", style="primary")],
        ]
    }


def paper_status_text(uid):
    d, acc = paper_acc(uid, create=True)
    if not acc:
        acc = _paper_fresh(False)
    opens = [
        t
        for t in (d.get("pos") or [])
        if t.get("status") == "open" and str(t.get("uid")) == str(uid)
    ]
    bal = float(acc.get("bal") or 0)
    start = float(acc.get("start") or PAPER_START) or PAPER_START
    pnl = bal - start
    pct = (pnl / start * 100.0) if start else 0.0
    st = u"روشن" if acc.get("on") else u"خاموش"
    lines = [
        tz_head(u"پیپر"),
        u"آزمایشی است · پول واقعی نیست · ریسک ۱٪ · حد ضرر اجباری",
        u"وضعیت: <b>%s</b>" % st,
        u"موجودی <code>%s</code> USDT  ·  %s٪ از شروع"
        % (_paper_usd(bal), _paper_usd(pct)),
        u"باز %s/%s  ·  برد %s  ·  باخت %s"
        % (
            len(opens),
            PAPER_MAX_OPEN,
            int(acc.get("wins") or 0),
            int(acc.get("loss") or 0),
        ),
        "────────────",
    ]
    if not opens:
        lines.append(u"پوزیشن باز نیست.")
    for t in opens[:6]:
        pair = t.get("pair")
        try:
            e_s = fmt_px(pair, t.get("entry")) if pair in PAIRS else t.get("entry")
            sl_s = fmt_px(pair, t.get("sl")) if pair in PAIRS else t.get("sl")
            tp_s = fmt_px(pair, t.get("tp")) if pair in PAIRS else t.get("tp")
        except Exception:
            e_s, sl_s, tp_s = t.get("entry"), t.get("sl"), t.get("tp")
        lines.append(
            u"%s <b>%s</b> %s\nورود %s  SL %s  TP %s\nحجم %s  ·  ریسک %s"
            % (
                (PAIRS.get(pair) or {}).get("emoji") or "",
                pair,
                t.get("side"),
                e_s,
                sl_s,
                tp_s,
                _paper_qty_lab(pair, t.get("qty")),
                _paper_usd(t.get("risk_usd")),
            )
        )
    lines.append(tz_foot())
    return u"\n".join(lines)


def paper_on_signal(token, sig, pair=None):
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return
    if not sig.get("sl") or not sig.get("tp") or not sig.get("entry"):
        return
    try:
        entry = float(sig["entry"])
        sl = float(sig["sl"])
        tp = float(sig["tp"])
    except Exception:
        return
    dist = abs(entry - sl)
    if dist <= 0:
        return
    pair = pair or sig.get("pair")
    if not pair:
        return
    if pair not in PAIRS:
        try:
            ensure_crypto_pair(pair)
        except Exception:
            pass
    d = load_paper()
    now = time.time()
    sent = 0
    for k, acc in list((d.get("accounts") or {}).items()):
        if not acc or not acc.get("on"):
            continue
        try:
            uid = int(k)
        except Exception:
            continue
        if not (is_owner(uid) or is_pro(uid)):
            continue
        bal = float(acc.get("bal") or 0)
        if bal < 80:
            continue
        opens = [
            t
            for t in d["pos"]
            if t.get("status") == "open" and str(t.get("uid")) == k
        ]
        if len(opens) >= PAPER_MAX_OPEN:
            continue
        if any(t.get("pair") == pair for t in opens):
            continue
        risk = min(bal * float(acc.get("risk") or PAPER_RISK), bal * 0.02)
        if risk < 1:
            continue
        qty = risk / dist
        rec = {
            "uid": uid,
            "pair": pair,
            "side": sig["side"],
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "qty": qty,
            "risk_usd": round(risk, 2),
            "ts": now,
            "status": "open",
            "score": sig.get("score"),
            "tf": sig.get("tf") or sig.get("tf_label") or "15m",
        }
        d["pos"].append(rec)
        acc["opened"] = int(acc.get("opened") or 0) + 1
        d["accounts"][k] = acc
        sent += 1
        try:
            e_s = fmt_px(pair, entry) if pair in PAIRS else entry
            sl_s = fmt_px(pair, sl) if pair in PAIRS else sl
            tp_s = fmt_px(pair, tp) if pair in PAIRS else tp
            send_message(
                token,
                uid,
                (
                    tz_head(u"پیپر باز")
                    + u"%s <b>%s</b>  %s\n"
                    u"ورود <code>%s</code>\n"
                    u"SL <code>%s</code>  ·  TP <code>%s</code>\n"
                    u"حجم %s  ·  ریسک %s USDT (۱٪)\n"
                    u"موجودی %s\n"
                    u"<i>آزمایشی است · پول واقعی نیست</i>"
                    % (
                        (PAIRS.get(pair) or {}).get("emoji") or "",
                        pair,
                        sig["side"],
                        e_s,
                        sl_s,
                        tp_s,
                        _paper_qty_lab(pair, qty),
                        _paper_usd(risk),
                        _paper_usd(bal),
                    )
                ),
                kb_paper(uid),
            )
        except Exception:
            log("paper open dm " + traceback.format_exc())
    if sent:
        save_paper(d)
        log("paper open %s %s n=%s" % (pair, sig.get("side"), sent))


def paper_monitor(token):
    d = load_paper()
    rows = [t for t in (d.get("pos") or []) if t.get("status") == "open"]
    if not rows:
        return
    now = time.time()
    cache = {}
    changed = False

    def bars_of(pair):
        if pair not in cache:
            if pair not in PAIRS:
                try:
                    ensure_crypto_pair(pair)
                except Exception:
                    pass
            try:
                cache[pair] = _bars_for_pair(pair)
            except Exception:
                cache[pair] = ([], None)
        return cache[pair]

    for t in rows:
        try:
            age = now - float(t.get("ts") or 0)
        except Exception:
            age = 0
        pair = t.get("pair")
        uid = t.get("uid")
        acc = (d.get("accounts") or {}).get(str(uid))
        if age > 12 * 3600:
            t["status"] = "expired"
            t["closed_ts"] = now
            t["exit"] = t.get("entry")
            t["pnl"] = 0.0
            t["r"] = 0.0
            changed = True
            try:
                send_message(
                    token,
                    uid,
                    tz_head(u"پیپر")
                    + u"%s منقضی شد — ۱۲ ساعت بدون TP/SL.\nموجودی %s"
                    % (pair, _paper_usd((acc or {}).get("bal"))),
                    kb_paper(uid),
                )
            except Exception:
                pass
            continue
        path, px = bars_of(pair)
        since = float(t.get("ts") or 0) - 180
        walk = [b for b in path if int(b.get("t") or 0) >= since]
        if len(walk) < 1:
            walk = path[-12:] if path else []
        try:
            sl = float(t["sl"])
            tp = float(t["tp"])
            entry = float(t["entry"])
            qty = float(t["qty"])
        except Exception:
            continue
        side = t.get("side")
        hit = _first_hit(side, sl, tp, walk) if walk else None
        if not hit:
            continue
        exit_px = sl if hit == "SL" else tp
        direc = 1.0 if side == "BUY" else -1.0
        pnl = qty * (exit_px - entry) * direc
        risk = float(t.get("risk_usd") or 0) or 1.0
        rr = pnl / risk if risk else 0.0
        t["status"] = hit.lower()
        t["closed_ts"] = now
        t["exit"] = exit_px
        t["pnl"] = round(pnl, 2)
        t["r"] = round(rr, 2)
        if acc:
            acc["bal"] = round(float(acc.get("bal") or 0) + pnl, 2)
            if acc["bal"] > float(acc.get("peak") or 0):
                acc["peak"] = acc["bal"]
            if hit == "TP":
                acc["wins"] = int(acc.get("wins") or 0) + 1
            else:
                acc["loss"] = int(acc.get("loss") or 0) + 1
            d["accounts"][str(uid)] = acc
        changed = True
        mark = u"TP" if hit == "TP" else u"SL"
        try:
            e_s = fmt_px(pair, entry) if pair in PAIRS else entry
            x_s = fmt_px(pair, exit_px) if pair in PAIRS else exit_px
            send_message(
                token,
                uid,
                (
                    tz_head(u"پیپر بسته · %s" % mark)
                    + u"%s <b>%s</b>  %s\n"
                    u"ورود %s  ·  خروج %s\n"
                    u"P/L <b>%s</b> USDT  ·  %sR\n"
                    u"موجودی <code>%s</code>\n"
                    u"<i>آزمایشی است · پول واقعی نیست</i>"
                    % (
                        (PAIRS.get(pair) or {}).get("emoji") or "",
                        pair,
                        side,
                        e_s,
                        x_s,
                        _paper_usd(pnl),
                        _paper_usd(rr),
                        _paper_usd((acc or {}).get("bal")),
                    )
                ),
                kb_paper(uid),
            )
        except Exception:
            log("paper close dm " + traceback.format_exc())
        log("paper %s %s %s pnl=%s" % (hit, pair, uid, t.get("pnl")))
    if changed:
        save_paper(d)


def _unique_book(rows):
    best = {}
    for t in rows:
        if not isinstance(t, dict):
            continue
        hour = int(float(t.get("ts") or 0) // 3600)
        k = (t.get("fp") or trade_fingerprint(t)) + "|" + str(hour)
        prev = best.get(k)
        if not prev:
            best[k] = t
            continue
        rank = 2 if t.get("source") == "channel" else 1
        pr = 2 if prev.get("source") == "channel" else 1
        if rank > pr:
            best[k] = t
        elif rank == pr and float(t.get("closed_ts") or 0) > float(prev.get("closed_ts") or 0):
            best[k] = t
    return list(best.values())


def _r_of(t):
    try:
        entry = float(t["entry"])
        sl = float(t["sl"])
        risk = abs(entry - sl) or 1e-9
        st = t.get("status")
        if st == "sl":
            return -1.0
        if st == "tp":
            px = t.get("exit")
            if px is not None:
                px = float(px)
                if (t.get("side") or "") == "SELL":
                    return (entry - px) / risk
                return (px - entry) / risk
            rew = abs(float(t["tp"]) - entry)
            return rew / risk
    except Exception:
        return 0.0
    return 0.0


def tehran_ymd(ts=None):
    t = tehran_tuple(ts)
    return (t.tm_year, t.tm_mon, t.tm_mday)


def jalali_short(ts=None):
    t = tehran_tuple(ts)
    jy, jm, jd = gregorian_to_jalali(t.tm_year, t.tm_mon, t.tm_mday)
    return u"%s %s" % (fa_num(jd), _JMONTH[jm - 1])


def _r_live(t, px):
    try:
        if px is None:
            return 0.0
        entry = float(t["entry"])
        sl = float(t["sl"])
        risk = abs(entry - sl) or 1e-9
        px = float(px)
        if (t.get("side") or "") == "SELL":
            return (entry - px) / risk
        return (px - entry) / risk
    except Exception:
        return 0.0


def _trade_r_row(t, r=None, live=False):
    pair = t.get("pair")
    meta = PAIRS.get(pair) or {}
    ts = t.get("closed_ts") or t.get("ts")
    if live:
        rr = _r_live(t, r)
    elif r is None:
        rr = _r_of(t)
    else:
        rr = r
    return {
        "pair": pair,
        "name": meta.get("name") or pair,
        "emoji": meta.get("emoji") or "",
        "side": t.get("side") or "",
        "status": t.get("status") or "",
        "r": round(float(rr or 0.0), 2),
        "when": tehran_fmt(ts, "%H:%M") if ts else "",
        "date": jalali_short(ts) if ts else "",
    }


def daily_r_blob(px_map=None):
    raw = load_trades()
    rows = _unique_book([t for t in raw if int(t.get("gen") or 0) >= ENGINE_GEN])
    closed = [t for t in rows if t.get("status") in ("tp", "sl")]
    opens = [t for t in rows if t.get("status") == "open"]
    now = time.time()
    today_key = tehran_ymd(now)
    days = []
    today_trades = []
    for i in range(7):
        ts = now - i * 86400
        key = tehran_ymd(ts)
        xs = [
            t
            for t in closed
            if tehran_ymd(float(t.get("closed_ts") or t.get("ts") or 0)) == key
        ]
        rsum = sum(_r_of(t) for t in xs)
        rec = {
            "label": u"امروز" if i == 0 else jalali_short(ts),
            "r": round(rsum, 2),
            "n": len(xs),
            "wins": sum(1 for t in xs if t.get("status") == "tp"),
            "loss": sum(1 for t in xs if t.get("status") == "sl"),
        }
        days.append(rec)
        if i == 0:
            today_trades = [
                _trade_r_row(t)
                for t in sorted(
                    xs, key=lambda z: float(z.get("closed_ts") or z.get("ts") or 0), reverse=True
                )
            ]
    week_r = round(sum(d["r"] for d in days), 2)
    open_rows = []
    open_r = 0.0
    if px_map:
        for t in opens:
            pair = t.get("pair")
            px = px_map.get(pair)
            rr = _r_live(t, px)
            open_r += rr
            row = _trade_r_row(t, px, live=True)
            row["status"] = "open"
            open_rows.append(row)
    tod = days[0] if days else {"r": 0, "n": 0, "wins": 0, "loss": 0, "label": u"امروز"}
    return {
        "today": {
            "r": tod.get("r") or 0,
            "n": tod.get("n") or 0,
            "wins": tod.get("wins") or 0,
            "loss": tod.get("loss") or 0,
            "label": tod.get("label") or u"امروز",
            "date": jalali_short(now),
            "trades": today_trades,
            "open_r": round(open_r, 2),
            "open_n": len(open_rows),
            "opens": open_rows,
        },
        "days": days,
        "week_r": week_r,
    }


def wr_text():
    raw = load_trades()
    rows = _unique_book(
        [t for t in raw if int(t.get("gen") or 0) >= ENGINE_GEN]
    )
    now = time.time()
    closed = [t for t in rows if t.get("status") in ("tp", "sl")]
    expired = [t for t in rows if t.get("status") == "expired"]
    opens = [t for t in rows if t.get("status") == "open"]
    wins = [t for t in closed if t.get("status") == "tp"]
    loss = [t for t in closed if t.get("status") == "sl"]
    n = len(wins) + len(loss)
    lines = [
        tz_head(u"📊 وین‌ریت واقعی"),
        u"از حد سود و حد ضرر واقعی. درصد الکی نمی‌نویسم " + pe(u"💛"),
        u"آمار از نسخهٔ جدید موتور — قبلی‌ها قاطی نمی‌شوند.",
        u"",
    ]
    try:
        dail = daily_r_blob()
        tod = dail.get("today") or {}
        lines.append(
            pe(u"📅")
            + u" امروز  <b>%+.2fR</b>  ·  %s سیگنال  ·  %s برد / %s باخت"
            % (
                float(tod.get("r") or 0),
                tod.get("n") or 0,
                tod.get("wins") or 0,
                tod.get("loss") or 0,
            )
        )
        lines.append(u"۷ روز:  <b>%+.2fR</b>" % float(dail.get("week_r") or 0))
        for tr in (tod.get("trades") or [])[:8]:
            ic = u"✅" if tr.get("status") == "tp" else u"❌"
            lines.append(
                u"%s %s %s %s  <b>%+.2fR</b>  ·  %s"
                % (
                    ic,
                    tr.get("emoji") or "",
                    tr.get("pair") or "",
                    tr.get("side") or "",
                    float(tr.get("r") or 0),
                    tr.get("when") or "",
                )
            )
        lines.append(u"")
    except Exception:
        log("daily r " + traceback.format_exc())
    if n == 0:
        lines.append(pe(u"🌱") + u" هنوز سیگنال بسته‌شده‌ای تو دفتر جدید نیست.")
        lines.append(u"از این به بعد هر سیگنال تا حد سود/ضرر دنبال می‌شود و همین‌جا جمع می‌شود.")
        if expired:
            lines.append(u"منقضی (نه برد نه باخت): %s" % len(expired))
    else:
        pct = 100.0 * len(wins) / n
        avg = sum(_r_of(t) for t in closed) / float(n)
        note = (
            u"نمونه کم است — این عدد را جدی نگیر."
            if n < 8
            else u"برد = حد سود · باخت = حد ضرر · منقضی جداست."
        )
        lines.append(
            u"📈 وین‌ریت  <b>%.0f٪</b>   ·   %s برد  /  %s باخت"
            % (pct, len(wins), len(loss))
        )
        lines.append(u"📉 میانگین R  <b>%+.2f</b>" % avg)
        lines.append(u"⏳ منقضی: %s" % len(expired))
        lines.append(note)

        def window(sec):
            xs = [
                t
                for t in closed
                if now - float(t.get("closed_ts") or t.get("ts") or 0) <= sec
            ]
            w = sum(1 for t in xs if t.get("status") == "tp")
            l = sum(1 for t in xs if t.get("status") == "sl")
            tot = w + l
            if tot == 0:
                return u"—"
            return u"%s برد / %s باخت  (%.0f٪)" % (w, l, 100.0 * w / tot)

        lines.append(u"")
        lines.append(u"۷ روز:  %s" % window(7 * 86400))
        lines.append(u"۳۰ روز:  %s" % window(30 * 86400))
        lines.append(u"")
        for pair, meta in PAIRS.items():
            xs = [t for t in closed if t.get("pair") == pair]
            w = sum(1 for t in xs if t.get("status") == "tp")
            l = sum(1 for t in xs if t.get("status") == "sl")
            tot = w + l
            if tot == 0:
                s = u"—"
            else:
                s = u"%.0f٪   (%s برد / %s باخت)" % (100.0 * w / tot, w, l)
            lines.append(u"%s <b>%s</b>  %s" % (meta["emoji"], meta["name"], s))
        last = sorted(
            closed,
            key=lambda t: float(t.get("closed_ts") or t.get("ts") or 0),
            reverse=True,
        )[:10]
        if last:
            lines.append(u"")
            lines.append(u"<b>۱۰ تای آخر</b>")
            for t in last:
                ic = u"✅" if t.get("status") == "tp" else u"❌"
                pair = t.get("pair")
                lines.append(
                    u"%s %s %s %s  %+0.1fR  ·  %s"
                    % (
                        ic,
                        (PAIRS.get(pair) or {}).get("emoji") or "",
                        pair,
                        t.get("side"),
                        _r_of(t),
                        tehran_fmt(t.get("closed_ts") or t.get("ts")),
                    )
                )
    if opens:
        lines.append(u"")
        lines.append(u"<b>باز الان · %s ستاپ</b>" % len(opens))
        for t in opens[-8:]:
            pair = t.get("pair")
            lines.append(
                u"• %s %s  ورود <code>%s</code> · SL <code>%s</code> · TP <code>%s</code>"
                % (
                    t.get("side"),
                    pair,
                    _px_safe(pair, t.get("entry")),
                    _px_safe(pair, t.get("sl")),
                    _px_safe(pair, t.get("tp")),
                )
            )
    lines.append(u"")
    lines.append(tz_foot())
    return u"\n".join(lines)


def kb_wr():
    return {
        "inline_keyboard": [
            [
                btn(u"🔄 بروزرسانی", "wr_menu", style="success"),
                btn(u"📡 معاملات باز", "live_pos", style="primary"),
            ],
            [
                btn(u"💶 یورو", "sig_EURUSD", style="primary"),
                btn(u"💷 پوند", "sig_GBPUSD", style="primary"),
                btn(u"🥇 طلا", "sig_XAUUSD", style="success"),
            ],
            [btn(u"🏠 TZ FX", "home", style="primary")],
        ]
    }



def kb_crypto():
    try:
        n = len((load_crypto_universe() or {}).get("syms") or {})
    except Exception:
        n = 0
    nlab = u"%s کوین" % n if n else u"همه کوین‌ها"
    return {
        "inline_keyboard": [
            [
                btn(u"₿ BTC", "sig_BTCUSDT", style="success"),
                btn(u"⟠ ETH", "sig_ETHUSDT", style="primary"),
                btn(u"◎ SOL", "sig_SOLUSDT", style="primary"),
                btn(u"🟡 BNB", "sig_BNBUSDT"),
            ],
            [
                btn(u"💧 XRP", "sig_XRPUSDT"),
                btn(u"🐶 DOGE", "sig_DOGEUSDT"),
                btn(u"🐸 PEPE", "sig_PEPEUSDT"),
                btn(u"🐕 SHIB", "sig_SHIBUSDT"),
            ],
            [
                btn(T("btn.find_coin"), "cx_find", style="success"),
            ],
            [
                btn(T("btn.hot"), "cx_hot", style="primary"),
                btn(u"📋 %s" % nlab, "cx_all"),
            ],
            [
                btn(T("btn.crypto_radar"), "radar_crypto", style="primary"),
                btn(T("btn.crypto_brief"), "brief_crypto", style="primary"),
            ],
            [btn(T("btn.crypto_core"), "sig_CRYPTO", style="success")],
            [btn(T("btn.crypto_ch"), url=CRYPTO_CHANNEL_URL, style="success")],
            [btn(u"🏠 TZ FX", "home", style="primary")],
        ]
    }


def kb_desk():
    return {
        "inline_keyboard": [
            [
                btn(T("btn.radar"), "radar_fx", style="success"),
                btn(T("btn.session"), "session_now", style="primary"),
            ],
            [
                btn(T("btn.journal"), "journal_card", style="success"),
                btn(T("btn.tools"), "tools_menu", style="primary"),
            ],
            [
                btn(T("btn.paper"), "paper_menu"),
                btn(T("btn.alerts"), "alert_menu"),
            ],
            [btn(T("btn.connect"), "connect_menu", style="success")],
            [btn(T("btn.home"), "home", style="primary")],
        ]
    }


def kb_tools():
    return {
        "inline_keyboard": [
            [
                btn(u"🧮 " + T("btn.size"), "tool_size", style="primary"),
                btn(u"📐 " + T("btn.rr"), "tool_rr", style="success"),
            ],
            [
                btn(u"📏 " + T("btn.pips"), "tool_pips"),
                btn(u"🕒 " + T("btn.clocks"), "tool_clocks", style="primary"),
            ],
            [
                btn(u"📍 " + T("btn.opens"), "tool_opens"),
                btn(u"✅ " + T("btn.check"), "tool_check", style="success"),
            ],
            [
                btn(u"📡 " + T("btn.bias"), "tool_bias", style="primary"),
                btn(u"🔔 " + T("btn.alerts"), "alert_menu"),
            ],
            [btn(T("btn.desk"), "desk_menu"), btn(T("btn.home"), "home", style="primary")],
        ]
    }


def _sig_levels(uid):
    rec = {}
    try:
        rec = load_user_mem(uid) or {}
    except Exception:
        rec = {}
    sig = rec.get("last_sig") if isinstance(rec, dict) else None
    if not isinstance(sig, dict):
        sig = {}
    return sig


def tool_size_text(uid):
    sig = _sig_levels(uid)
    pair = sig.get("pair") or "XAUUSD"
    entry = sig.get("entry") or sig.get("px")
    sl = sig.get("sl")
    eq = 10000.0
    risk = eq * 0.01
    body = T("txt.tools") + u"\n\n"
    body += u"<b>%s</b>\n" % pair
    if entry and sl:
        dist = abs(float(entry) - float(sl))
        body += u"ورود <code>%s</code> · حد ضرر <code>%s</code>\n" % (entry, sl)
        body += u"فاصله %s\n" % dist
        if dist:
            units = risk / dist
            body += u"حساب نمونه ۱۰٬۰۰۰ · ریسک ۱٪ = %s\n" % int(risk)
            body += u"حجم تقریبی واحد / فاصله = <code>%.4f</code>\n" % units
    else:
        body += u"اول یک سیگنال زنده با حد ضرر بگیر تا حجم از روی فاصله حساب شود.\n"
    body += u"سقف ریسک ۱٪. حد ضرر اجباری است."
    return tz_head(T("head.tools")) + body + u"\n" + tz_foot()


def tool_rr_text(uid):
    sig = _sig_levels(uid)
    e, sl, tp = sig.get("entry"), sig.get("sl"), sig.get("tp")
    body = T("txt.tools") + u"\n\n"
    if e and sl and tp:
        risk = abs(float(e) - float(sl))
        rew = abs(float(tp) - float(e))
        rr = (rew / risk) if risk else 0
        body += u"ورود %s · SL %s · TP %s\n" % (e, sl, tp)
        body += u"R:R <b>%.2f</b>\n" % rr
    else:
        rr = sig.get("rr")
        body += u"R:R ذخیره‌شده: %s\n" % (rr or "—")
        body += u"سیگنال زنده با سه عدد لازم است."
    return tz_head(T("head.tools")) + body + u"\n" + tz_foot()


def tool_pips_text(uid):
    sig = _sig_levels(uid)
    pair = sig.get("pair") or "EURUSD"
    meta = PAIRS.get(pair) or {}
    pip = meta.get("pip") or 0.0001
    px, _rows = _last_px(pair)
    body = T("txt.tools") + u"\n\n<b>%s</b>\nپیپ %s\n" % (pair, pip)
    if px:
        body += u"قیمت زنده <code>%s</code>\n" % px
    e, sl = sig.get("entry"), sig.get("sl")
    if e and sl and pip:
        body += u"فاصله حد ضرر ≈ %.1f پیپ\n" % (abs(float(e) - float(sl)) / float(pip))
    return tz_head(T("head.tools")) + body + u"\n" + tz_foot()


def tool_clocks_text():
    t = tehran_tuple()
    # London UTC+0/+1 approx: Tehran is UTC+3:30 so London = t - 3h30 in winter. Show clock labels only.
    th = t.tm_hour
    tm = t.tm_min
    body = T("txt.tools") + u"\n\n"
    body += u"تهران <b>%02d:%02d</b>\n" % (th, tm)
    try:
        body += session_card_text()
    except Exception:
        body += tehran_fmt()
    return tz_head(T("btn.clocks")) + body + u"\n" + tz_foot()


def tool_opens_text():
    lines = [T("txt.tools"), u""]
    for pair in FX_PAIRS:
        px, rows = _last_px(pair)
        if not rows:
            lines.append(u"%s —" % pair)
            continue
        day = rows[-min(len(rows), 96)]["o"] if len(rows) >= 2 else rows[0]["o"]
        week = rows[0]["o"]
        lines.append(u"<b>%s</b> زنده %s · اوپن تقریبی روز %s" % (pair, px, day))
    return tz_head(T("btn.opens")) + u"\n".join(lines) + u"\n" + tz_foot()


def tool_check_text():
    items = (
        u"۱. جهت تایم بالا؟",
        u"۲. سوئیپ انجام شد؟",
        u"۳. جابجایی / MSS؟",
        u"۴. ورود داخل FVG؟",
        u"۵. حد ضرر گذاشتی؟",
        u"۶. حجم ۱٪؟",
        u"دو تا نه = کلیک نکن.",
    )
    return tz_head(T("btn.check")) + T("txt.tools") + u"\n\n" + u"\n".join(items) + u"\n" + tz_foot()


def tool_bias_text():
    lines = [T("txt.tools"), u""]
    for pair in FX_PAIRS:
        px, rows = _last_px(pair)
        if not rows or len(rows) < 3:
            lines.append(u"%s —" % pair)
            continue
        a, b = rows[-20]["c"] if len(rows) > 20 else rows[0]["c"], rows[-1]["c"]
        bias = u"صعودی" if b >= a else u"نزولی"
        lines.append(u"<b>%s</b> %s · %s" % (pair, px, bias))
    lines.append(u"این جهت خام است. بدون مدل کامل = صبر.")
    return tz_head(T("btn.bias")) + u"\n".join(lines) + u"\n" + tz_foot()


def kb_alerts():
    rows = []
    for pair in FX_PAIRS + CRYPTO_PAIRS:
        meta = PAIRS[pair]
        rows.append([btn(u"%s %s" % (meta["emoji"], meta["name"]), "al_add_%s" % pair)])
    rows.append([btn(u"🗑 پاک کردن هشدارها", "al_clear", style="danger")])
    rows.append([btn(u"🧰 میز", "desk_menu", style="primary")])
    return {"inline_keyboard": rows}


def txt_crypto_intro():
    n = 0
    try:
        n = len((load_crypto_universe() or {}).get("syms") or {})
    except Exception:
        n = 0
    return (
        tz_head(T("head.crypto"))
        + T("txt.crypto") % ((n or T("txt.all_coins")), CRYPTO_CHANNEL_URL) + u"\n"
        + tz_foot()
    )


def txt_desk_intro():
    return (
        tz_head(T("head.desk"))
        + T("txt.desk") + u"\n"
        + tz_foot()
    )


def _last_px(pair):
    rows = _ohlc_cache.get(pair + "|15m") or []
    if not rows:
        try:
            rows = fetch_ohlc(pair, "15m", "10d") or []
        except Exception:
            rows = []
    if not rows:
        return None, []
    return rows[-1]["c"], rows


def session_card_text():
    now = int(time.time())
    kz = in_killzone(now) or in_crypto_asia(now) or u"خارج از کیل‌زون"
    sb = u"بله" if in_silver_bullet(now) else u"نه"
    news = news_window(now) or u"پنجره خبر خاصی روی ساعت نیست"
    return (
        tz_head(u"سشن")
        + u"%s\n" % tehran_fmt()
        + u"%s\n" % fx_open_line(now)
        + u"کیل‌زون: %s\n" % kz
        + u"SB: %s · %s\n" % (sb, next_session_line(now))
        + tz_foot()
    )


def radar_card(pairs):
    lines = [
        tz_head(u"🛰️ رادار ستاپ"),
        u"%s تهران" % tehran_fmt(),
        u"فقط مرحله ساختار — سیگنال جعلی نیست.",
        "────────────",
    ]
    for pair in pairs:
        meta = PAIRS.get(pair) or {}
        try:
            sig = scan_signal(pair)
        except Exception:
            sig = None
        if sig:
            sig.pop("_rows", None)
        side = (sig or {}).get("side") or "—"
        reason = (sig or {}).get("reason") or (sig or {}).get("setup") or u"داده نرسید"
        sc = (sig or {}).get("score") or 0
        mark = u"⏸"
        if side == "BUY":
            mark = u"🟢"
        elif side == "SELL":
            mark = u"🔴"
        lines.append(
            u"%s <b>%s</b>  %s %s  %s/6\n<i>%s</i>"
            % (meta.get("emoji") or "", pair, mark, side, sc, reason[:80])
        )
        if sig and sig.get("warn"):
            lines.append(u"⚠️ %s" % sig.get("warn"))
    lines.append(tz_foot())
    return u"\n".join(lines)


def bias_card_text():
    lines = [tz_head(u"🧭 بایاس روزانه"), u"%s" % tehran_fmt(), "────────────"]
    for pair in FX_PAIRS + CRYPTO_PAIRS:
        meta = PAIRS[pair]
        try:
            htf = htf_context(pair, 0) or {}
        except Exception:
            htf = {}
        d1 = (htf.get("d1") or {}).get("bias") or "—"
        h4 = (htf.get("h4") or {}).get("bias") or "—"
        h1 = htf.get("bias") or "—"
        pd = htf.get("pd") or "—"
        lines.append(
            u"%s <b>%s</b>\n   D1 %s · H4 %s · 1H %s · %s"
            % (meta["emoji"], pair, d1, h4, h1, pd)
        )
    lines.append(tz_foot())
    return u"\n".join(lines)


def smt_card_text():
    try:
        e = htf_context("EURUSD", 0) or {}
        g = htf_context("GBPUSD", 0) or {}
    except Exception:
        e, g = {}, {}
    eb, gb = e.get("bias") or "—", g.get("bias") or "—"
    ed, gd = (e.get("d1") or {}).get("bias") or "—", (g.get("d1") or {}).get("bias") or "—"
    smt = u"نه"
    if eb in ("BULL", "BEAR") and gb in ("BULL", "BEAR") and eb != gb:
        smt = u"بله — یورو و پوند ۱ساعته مخالف‌اند"
    corr = u"همبسته"
    if eb == gb and eb in ("BULL", "BEAR"):
        corr = u"هر دو %s — اگر هر دو را بگیری ریسک دو برابر است" % eb
    return (
        tz_head(u"🔗 SMT یورو / پوند")
        + u"۱H یورو <b>%s</b>  ·  پوند <b>%s</b>\n" % (eb, gb)
        + u"D1 یورو <b>%s</b>  ·  پوند <b>%s</b>\n" % (ed, gd)
        + u"SMT: <b>%s</b>\n" % smt
        + u"%s\n" % corr
        + tz_foot()
    )


def asia_range_text():
    lines = [tz_head(u"🌏 رنج آسیا"), u"۰۰:۰۰–۰۷:۰۰ UTC کندل ۱۵م", "────────────"]
    for pair in FX_PAIRS:
        px, rows = _last_px(pair)
        if not rows:
            lines.append(u"%s داده نیست" % pair)
            continue
        asia = []
        for r in rows:
            hr = time.gmtime(int(r["t"])).tm_hour
            if 0 <= hr < 7:
                asia.append(r)
        asia = asia[-28:]
        if not asia:
            lines.append(u"%s رنج آسیا نیست" % pair)
            continue
        hi = max(r["h"] for r in asia)
        lo = min(r["l"] for r in asia)
        mid = (hi + lo) / 2.0
        pos = u"بالای رنج" if px > hi else (u"زیر رنج" if px < lo else u"داخل رنج")
        lines.append(
            u"%s <b>%s</b>  %s\n   بالا <code>%s</code>  پایین <code>%s</code>  میانه <code>%s</code>"
            % (
                PAIRS[pair]["emoji"],
                pair,
                pos,
                fmt_px(pair, hi),
                fmt_px(pair, lo),
                fmt_px(pair, mid),
            )
        )
    lines.append(tz_foot())
    return u"\n".join(lines)


def news_card_text():
    w = news_window() or u"الان پنجره خبر سنگینی روی ساعت UTC نیست"
    return (
        tz_head(u"📰 پنجره خبر")
        + u"%s\n" % tehran_fmt()
        + u"%s\n\n" % w
        + u"NFP معمولاً جمعه ۱۶:۰۰ تهران. FOMC چهارشنبه شب.\n"
        u"داخل پنجره خبر سایز را نصف کن — سیگنال را حذف نمی‌کنم، فقط هشدار.\n"
        + tz_foot()
    )


def journal_card_text(uid=None):
    rows = load_trades()
    closed = [t for t in rows if t.get("status") in ("tp", "sl", "expired")]
    closed.sort(key=lambda t: float(t.get("closed_ts") or t.get("ts") or 0), reverse=True)
    lines = [tz_head(u"📒 ژورنال ۱۰ تای آخر"), "────────────"]
    if not closed:
        lines.append(u"هنوز معامله بسته‌شده با جن ۶ نیست.")
    for t in closed[:10]:
        st = t.get("status")
        mark = u"✅" if st == "tp" else (u"❌" if st == "sl" else u"⏳")
        r = t.get("r")
        try:
            rs = "%.2fR" % float(r)
        except Exception:
            rs = "—"
        lines.append(
            u"%s %s %s  %s  %s"
            % (mark, t.get("pair"), t.get("side"), st, rs)
        )
    lines.append(tz_foot())
    return u"\n".join(lines)


def risk_dash_text(chat_id):
    rows = load_trades()
    opens = [t for t in rows if t.get("status") == "open"]
    lines = [tz_head(u"🛡️ داشبورد ریسک"), u"%s" % tehran_fmt(), "────────────"]
    if not opens:
        lines.append(u"معامله باز ثبت‌شده نیست.")
    tot = 0.0
    for t in opens:
        try:
            r = float(t.get("r") or 0)
        except Exception:
            r = 0.0
        tot += 1.0
        lines.append(
            u"%s %s  ورود <code>%s</code>  SL <code>%s</code>"
            % (t.get("pair"), t.get("side"), t.get("entry"), t.get("sl"))
        )
    lines.append(u"تعداد باز: <b>%s</b>  — حداکثر ۱٪ هر معامله، همزمان بیش از ۲ تا نگیر." % len(opens))
    lines.append(fx_open_line())
    nw = news_window()
    if nw:
        lines.append(u"⚠️ %s" % nw)
    lines.append(tz_foot())
    return u"\n".join(lines)


def pulse_text():
    lines = [tz_head(u"⚡ پالس بازار"), tehran_fmt(), fx_open_line(), next_session_line(), "────────────"]
    for pair in FX_PAIRS + CRYPTO_PAIRS:
        px, rows = _last_px(pair)
        if px is None:
            lines.append(u"%s داده نیست" % pair)
            continue
        chg = ""
        if len(rows) >= 5 and rows[-5]["c"]:
            pct = (px - rows[-5]["c"]) / rows[-5]["c"] * 100.0
            chg = u"  %+.2f٪" % pct
        lines.append(
            u"%s <b>%s</b>  <code>%s</code>%s"
            % (PAIRS[pair]["emoji"], pair, fmt_px(pair, px), chg)
        )
    lines.append(tz_foot())
    return u"\n".join(lines)


def load_alerts():
    d = _jload_safe(ALERTS_FILE, {}) or {}
    if not isinstance(d, dict):
        return {}
    return d


def save_alerts(d):
    try:
        with open(ALERTS_FILE, "w") as f:
            json.dump(d, f)
    except Exception:
        pass


def add_price_alert(uid, pair):
    px, _rows = _last_px(pair)
    if px is None:
        return None
    d = load_alerts()
    key = str(uid)
    lst = list(d.get(key) or [])
    lst = [x for x in lst if x.get("pair") != pair]
    lst.append({"pair": pair, "price": float(px), "ts": time.time()})
    d[key] = lst[-12:]
    save_alerts(d)
    return px


def clear_alerts(uid):
    d = load_alerts()
    d[str(uid)] = []
    save_alerts(d)


def tick_alerts(token):
    d = load_alerts()
    if not d:
        return
    changed = False
    for uid, lst in list(d.items()):
        keep = []
        for al in lst or []:
            pair = al.get("pair")
            try:
                tgt = float(al.get("price"))
            except Exception:
                continue
            px, _rows = _last_px(pair)
            if px is None:
                keep.append(al)
                continue
            pip = float((PAIRS.get(pair) or {}).get("pip") or 0.0001)
            if abs(px - tgt) <= max(pip * 8, abs(tgt) * 0.0015):
                try:
                    send_message(
                        token,
                        int(uid),
                        u"🚨 قیمت %s به <code>%s</code> رسید (هدف <code>%s</code>)"
                        % (pair, fmt_px(pair, px), fmt_px(pair, tgt)),
                        kb_after(),
                    )
                except Exception:
                    keep.append(al)
                    continue
                changed = True
            else:
                keep.append(al)
        d[uid] = keep
    if changed:
        save_alerts(d)


def crypto_briefing(token, chat_id):
    lines = [
        tz_head(u"₿ حال کریپتو بتا"),
        tehran_fmt(),
        next_session_line(),
        "────────────",
    ]
    for pair in CRYPTO_PAIRS:
        try:
            sig = scan_signal(pair)
        except Exception:
            sig = None
        if sig:
            sig.pop("_rows", None)
        px, _r = _last_px(pair)
        side = (sig or {}).get("side") or "NO SIGNAL"
        reason = (sig or {}).get("reason") or (sig or {}).get("setup") or "—"
        lines.append(
            u"%s <b>%s</b>  <code>%s</code>  %s\n<i>%s</i>"
            % (
                PAIRS[pair]["emoji"],
                pair,
                fmt_px(pair, px) if px is not None else "—",
                side,
                reason[:70],
            )
        )
    lines.append(u"بتا است — قول سود نیست.")
    lines.append(tz_foot())
    send_message(token, chat_id, u"\n".join(lines), kb_crypto())


def deliver_crypto_all(token, chat_id):
    for pair in CRYPTO_PAIRS:
        try:
            deliver_one(token, chat_id, pair, tf="mtf")
        except Exception:
            log("crypto all " + pair + " " + traceback.format_exc())
        time.sleep(0.2)


def scan_crypto_quick(pair):
    try:
        ensure_crypto_pair(pair)
    except Exception:
        pass
    if pair not in PAIRS:
        return None, []
    try:
        htf = htf_context(pair, 0) or {}
    except Exception:
        htf = {}
    try:
        rows = fetch_ohlc(pair, "15m", "10d") or []
    except Exception:
        rows = []
    if len(rows) < 24:
        return None, rows
    try:
        sig = ict_2022(rows, pair, interval="15m", htf=htf)
    except Exception:
        return None, rows
    if sig:
        sig = dict(sig)
        sig["tf"] = "15m"
        sig["tf_label"] = u"۱۵م"
        if sig.get("side") in ("BUY", "SELL"):
            try:
                sig = refine_entry_5m(sig, pair)
            except Exception:
                pass
    return sig, rows


def crypto_tick(token):
    cid = crypto_channel_id()
    if not cid:
        return
    if too_soon("crypto_tick", 75):
        return
    pairs = crypto_scan_list()
    live_n = 0
    post_n = 0
    core = set(CRYPTO_CORE[:10])
    for pair in pairs:
        try:
            if pair in core:
                sig = scan_signal(pair)
                if sig:
                    sig = dict(sig)
                rows = (sig or {}).pop("_rows", None) if sig else None
            else:
                sig, rows = scan_crypto_quick(pair)
                if sig:
                    sig = dict(sig)
        except Exception:
            log("crypto scan " + pair + " " + traceback.format_exc().splitlines()[-1][:90])
            continue
        if not rows:
            try:
                rows = fetch_ohlc(pair, "15m", "10d") or []
            except Exception:
                rows = []
        if not rows:
            continue
        if not sig:
            try:
                sig = build_signal(rows, pair)
            except Exception:
                sig = None
        side = (sig or {}).get("side")
        if side in ("BUY", "SELL"):
            live_n += 1
            log(
                "crypto live %s %s sc=%s %s"
                % (
                    pair,
                    side,
                    (sig or {}).get("score"),
                    ((sig or {}).get("setup") or (sig or {}).get("reason") or "")[:70],
                )
            )
            # geometry only — Gemini cannot veto crypto channel
            if post_to_channel(token, pair, sig, rows, dest="crypto"):
                post_n += 1
    log("crypto tick n=%s live=%s posted=%s" % (len(pairs), live_n, post_n))


def nudge_crypto_owner(token):
    if crypto_channel_id():
        return
    if os.path.isfile(CRYPTO_NUDGE):
        return
    try:
        send_message(
            token,
            OWNER_ID,
            u"₿ کانال TZ Crypto را دیدم.\n"
            u"یک پیام از داخل کانال برایم فوروارد کن تا شناسه ثبت شود و سیگنال بتا همان‌جا برود.\n"
            + CRYPTO_CHANNEL_URL,
        )
        with open(CRYPTO_NUDGE, "w") as f:
            f.write(str(time.time()))
    except Exception:
        pass


def desk_handle_cb(token, user_id, chat_id, data, cq_id):
    if data == "crypto_menu":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        try:
            load_crypto_universe()
        except Exception:
            pass
        send_message(token, chat_id, txt_crypto_intro(), kb_crypto())
        return True
    if data == "cx_find":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        set_wait(user_id, "crypto_find")
        send_message(
            token,
            chat_id,
            u"🔎 اسم کوین را بفرست. مثال: PEPE  WIF  دوج",
            kb_crypto(),
        )
        return True
    if data == "cx_hot":
        answer_callback(token, cq_id, u"داغ‌ترین‌ها...")
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        send_message(
            token,
            chat_id,
            u"🔥 داغ‌ترین اسپات USDT از روی حجم ۲۴ساعته — بتا است، سیگنال جعلی نیست.",
            kb_crypto_page(0, "hot"),
        )
        return True
    if data == "cx_all":
        answer_callback(token, cq_id, u"فهرست...")
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        n = len((load_crypto_universe() or {}).get("syms") or {})
        send_message(
            token,
            chat_id,
            u"📋 همه کوین‌های اسپات USDT بایننس: <b>%s</b> نماد. صفحه را ورق بزن یا جستجو کن." % n,
            kb_crypto_page(0, "all"),
        )
        return True
    if data.startswith("cxp_"):
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        rest = data[4:]
        kind, _, page = rest.partition("_")
        try:
            page = int(page)
        except Exception:
            page = 0
        if kind not in ("all", "hot"):
            kind = "all"
        send_message(token, chat_id, u"📋 صفحه %s" % (page + 1), kb_crypto_page(page, kind))
        return True
    if data == "desk_menu":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        send_message(token, chat_id, txt_desk_intro(), kb_desk())
        return True
    if data == "session_now":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        send_message(token, chat_id, session_card_text(), kb_desk())
        return True
    if data == "radar_fx":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id, u"رادار...")
        send_message(token, chat_id, radar_card(FX_PAIRS), kb_desk())
        return True
    if data == "radar_crypto":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id, u"رادار کوین...")
        send_message(token, chat_id, radar_card(CRYPTO_PAIRS), kb_crypto())
        return True
    if data == "bias_card":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id)
        send_message(token, chat_id, bias_card_text(), kb_desk())
        return True
    if data == "smt_card":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id)
        send_message(token, chat_id, smt_card_text(), kb_desk())
        return True
    if data == "asia_range":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id)
        send_message(token, chat_id, asia_range_text(), kb_desk())
        return True
    if data == "news_card":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        send_message(token, chat_id, news_card_text(), kb_desk())
        return True
    if data == "connect_menu":
        answer_callback(token, cq_id)
        if not is_owner(user_id):
            send_message(token, chat_id, u"فقط مالک.", kb_after())
            return True
        send_message(token, chat_id, txt_connect(), kb_connect())
        return True
    if data == "lv_mode":
        answer_callback(token, cq_id)
        if not is_owner(user_id):
            return True
        lx = _live_mod()
        cfg = lx.load_cfg()
        if cfg.get("demo", True):
            set_wait(user_id, "exch_livearm", extra={"step": "arm"})
            send_message(token, chat_id, u"برای واقعی بنویس: LIVE\nبدون این، دمو می‌ماند.", kb_connect())
            return True
        cfg["demo"] = True
        lx.save_cfg(cfg)
        send_message(token, chat_id, u"برگشت به دمو.", kb_connect())
        return True
    if data == "lv_risk":
        answer_callback(token, cq_id, u"۱٪")
        send_message(token, chat_id, u"ریسک ثابت ۱٪ است. حد ضرر اجباری.", kb_connect())
        return True
    if data.startswith("lv_v_"):
        answer_callback(token, cq_id)
        if not is_owner(user_id):
            return True
        venue = data[5:]
        lx = _live_mod()
        cfg = lx.load_cfg()
        cfg["crypto_venue"] = venue
        lx.save_cfg(cfg)
        send_message(token, chat_id, u"صرافی: %s" % venue, kb_connect())
        return True
    if data == "lv_keys":
        answer_callback(token, cq_id)
        if not is_owner(user_id):
            return True
        lx = _live_mod()
        venue = (lx.load_cfg().get("crypto_venue") or "binance")
        set_wait(user_id, "exch_key", extra={"venue": venue, "step": "key"})
        send_message(token, chat_id, u"API Key مربوط به %s را بفرست.\nبعد Secret. پیام پاک می‌شود." % venue, kb_connect())
        return True
    if data == "lv_ping":
        answer_callback(token, cq_id, u"تست...")
        if not is_owner(user_id):
            return True
        lx = _live_mod()
        cfg = lx.load_cfg()
        ok, msg = lx.ping_venue(cfg.get("crypto_venue") or "binance", bool(cfg.get("demo", True)))
        ok2, msg2 = lx.ping_venue("mt5", True)
        send_message(token, chat_id, u"%s\n%s" % (msg, msg2), kb_connect())
        return True
    if data == "lv_crypto_tog":
        answer_callback(token, cq_id)
        if not is_owner(user_id):
            return True
        lx = _live_mod()
        cfg = lx.load_cfg()
        if not cfg.get("crypto_on") and not lx.has_keys(cfg.get("crypto_venue") or "binance"):
            send_message(token, chat_id, u"اول کلید همین صرافی را بگذار.", kb_connect())
            return True
        cfg["crypto_on"] = not bool(cfg.get("crypto_on"))
        lx.save_cfg(cfg)
        send_message(token, chat_id, txt_connect(), kb_connect())
        return True
    if data == "lv_mt5_tog":
        answer_callback(token, cq_id)
        if not is_owner(user_id):
            return True
        lx = _live_mod()
        cfg = lx.load_cfg()
        cfg["mt5_on"] = not bool(cfg.get("mt5_on"))
        lx.save_cfg(cfg)
        send_message(token, chat_id, txt_connect(), kb_connect())
        return True
    if data == "lv_bridge":
        answer_callback(token, cq_id)
        if not is_owner(user_id):
            return True
        send_bridge_file(token, chat_id)
        return True
    if data == "paper_menu":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return True
        if not (is_owner(user_id) or is_pro(user_id)):
            send_message(token, chat_id, txt_paywall(user_id), kb_pay())
            return True
        send_message(token, chat_id, paper_status_text(user_id), kb_paper(user_id))
        return True
    if data == "paper_on":
        answer_callback(token, cq_id, u"روشن")
        if not (is_owner(user_id) or is_pro(user_id)):
            send_message(token, chat_id, txt_paywall(user_id), kb_pay())
            return True
        paper_acc(user_id, create=True, on=True)
        send_message(token, chat_id, u"پیپر روشن شد. سیگنال کانال را با ۱٪ ریسک آزمایشی می‌گیرد.", kb_paper(user_id))
        return True
    if data == "paper_off":
        answer_callback(token, cq_id, u"خاموش")
        paper_acc(user_id, create=True, on=False)
        send_message(token, chat_id, u"پیپر خاموش شد. پوزیشن باز تا TP/SL می‌ماند.", kb_paper(user_id))
        return True
    if data == "paper_reset":
        answer_callback(token, cq_id)
        d = load_paper()
        on = bool(((d.get("accounts") or {}).get(str(user_id)) or {}).get("on"))
        d["accounts"][str(user_id)] = _paper_fresh(on if (is_owner(user_id) or is_pro(user_id)) else False)
        d["pos"] = [t for t in (d.get("pos") or []) if str(t.get("uid")) != str(user_id)]
        save_paper(d)
        send_message(token, chat_id, u"حساب پیپر ریست شد · ۱۰٬۰۰۰ USDT", kb_paper(user_id))
        return True
    if data == "journal_card":
        if not gate(token, user_id, chat_id, need_pro=False):
            answer_callback(token, cq_id)
            return True
        answer_callback(token, cq_id)
        send_message(token, chat_id, journal_card_text(user_id), kb_desk())
        return True
    if data == "risk_dash":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id)
        send_message(token, chat_id, risk_dash_text(chat_id), kb_desk())
        return True
    if data == "pulse_now":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id)
        send_message(token, chat_id, pulse_text(), kb_desk())
        return True
    if data == "brief_crypto":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id)
        crypto_briefing(token, chat_id)
        return True
    if data == "sig_CRYPTO":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id, u"کریپتو بتا...")
        deliver_crypto_all(token, chat_id)
        return True
    if data == "alert_menu":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        answer_callback(token, cq_id)
        send_message(
            token,
            chat_id,
            u"🚨 هشدار قیمت: نماد را بزن — روی قیمت زنده قفل می‌شود. وقتی نزدیک شد خبرت می‌کنم.",
            kb_alerts(),
        )
        return True
    if data == "al_clear":
        clear_alerts(user_id)
        answer_callback(token, cq_id, u"پاک شد")
        send_message(token, chat_id, u"هشدارها پاک شد.", kb_desk())
        return True
    if data.startswith("al_add_"):
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return True
        pair = data[7:]
        if pair not in PAIRS:
            answer_callback(token, cq_id)
            return True
        px = add_price_alert(user_id, pair)
        answer_callback(token, cq_id)
        if px is None:
            send_message(token, chat_id, u"قیمت %s نرسید." % pair, kb_alerts())
        else:
            send_message(
                token,
                chat_id,
                u"🚨 هشدار %s روی <code>%s</code> ثبت شد." % (pair, fmt_px(pair, px)),
                kb_alerts(),
            )
        return True
    return False


def deliver_one(token, chat_id, pair, tf="mtf", reply_to=None, user_id=None):
    global _last_signal
    uid = user_id or chat_id
    if too_soon("sig:%s:%s" % (chat_id, pair), 5):
        send_message(
            token,
            chat_id,
            "چند ثانیه صبر کن — همین نماد را دارم می‌خوانم.",
            kb_after(),
            reply_to=reply_to,
        )
        return
    if over_hour("sig:%s" % chat_id, 25):
        send_message(
            token,
            chat_id,
            "برای اینکه کیفیت سیگنال پایین نیاید، این ساعت سهمت تمام شد. کمی بعد برگرد.",
            kb_after(),
            reply_to=reply_to,
        )
        return
    try:
        http().post(
            tg_api(token) + "/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
            timeout=6,
        )
    except Exception:
        pass
    board = ""
    prefer = None if tf == "mtf" else tf_meta(tf)[0]
    log("dm scan %s tf=%s" % (pair, tf))
    if not is_crypto_pair(pair) and not market_is_open():
        try:
            send_message(
                token,
                chat_id,
                u"⏸ %s — آخرین ساختار را می‌خوانم."
                % fx_open_line(),
                kb_after(),
                reply_to=reply_to,
            )
        except Exception:
            pass
    try:
        sig = scan_signal(pair, prefer=prefer)
    except Exception:
        log("scan " + traceback.format_exc())
        sig = None
    if sig is None:
        send_message(token, chat_id, "⚠️ دیتای %s نرسید." % pair, kb_tf(pair), reply_to=reply_to)
        return
    rows = sig.pop("_rows", None)
    label = sig.get("tf") or "15m"
    if not rows:
        interval, rng, label2 = tf_meta(label)
        rows = fetch_ohlc(pair, interval, rng)
        label = label2
    if sig.get("side") in ("BUY", "SELL"):
        live = dict(sig)
        try:
            checked = ai_confirm(dict(sig), rows)
        except Exception:
            log("ai_confirm " + traceback.format_exc())
            checked = sig
        if checked.get("side") in ("BUY", "SELL"):
            sig = checked
        else:
            sig = live
            sig["ai_verdict"] = checked.get("ai_verdict") or "REJECT"
            sig["ai_note"] = checked.get("ai_note") or checked.get("reason")
            sig["ai_block"] = True
            log(
                "dm keep %s %s sc=%s ai=%s"
                % (pair, sig.get("side"), sig.get("score"), sig.get("ai_verdict"))
            )
        save_last(sig, uid)
        try:
            mem_touch(uid, pair=pair, last_sig=sig)
        except Exception:
            pass
        try:
            notify_watchers(token, sig)
        except Exception:
            log("watch " + traceback.format_exc())
    _last_signal = pair + ":" + sig["side"]
    try:
        body = format_signal(sig)
    except Exception:
        log("format_signal " + traceback.format_exc())
        body = u"سیگنال آماده شد ولی متن خطا داد. دوباره بزن."
    cap = body
    msgid = send_chart(
        token, chat_id, rows, pair, sig, label, cap, kb_tf(pair), reply_to
    )
    if sig.get("side") in ("BUY", "SELL"):
        try:
            story = format_signal_story(sig)
            if story:
                send_message(token, chat_id, story, kb_tf(pair), reply_to=msgid)
        except Exception:
            log("story " + traceback.format_exc())
    try:
        board = tf_board(pair, full=False)
    except Exception:
        log("board " + traceback.format_exc())
        board = ""
    if board:
        send_message(
            token,
            chat_id,
            "📡 <b>%s</b>  ·  %s\n────────────\n%s"
            % (PAIRS[pair]["name"], sig.get("tf_label") or label, board),
            kb_tf(pair),
        )
    if sig["side"] in ("BUY", "SELL"):
        register_trade(sig, chat_id, msgid, "user")
        try:
            if is_crypto_pair(pair):
                post_to_channel(token, pair, sig, rows, dest="crypto")
            else:
                post_to_channel(token, pair, sig, rows, dest="pro")
                post_to_channel(token, pair, sig, rows, dest="free")
        except Exception:
            log("deliver channel " + traceback.format_exc())


def deliver_all(token, chat_id, reply_to=None):
    for pair in ("EURUSD", "GBPUSD", "XAUUSD"):
        try:
            sig = scan_signal(pair)
            if sig is None:
                send_message(token, chat_id, "⚠️ دیتای %s نرسید." % pair, kb_tf(pair))
                continue
            rows = sig.pop("_rows", None) or fetch_ohlc(pair, "15m", "10d")
            if sig.get("side") in ("BUY", "SELL"):
                live = dict(sig)
                try:
                    checked = ai_confirm(dict(sig), rows)
                except Exception:
                    log("ai_confirm " + traceback.format_exc())
                    checked = sig
                if checked.get("side") in ("BUY", "SELL"):
                    sig = checked
                else:
                    sig = live
                    sig["ai_verdict"] = checked.get("ai_verdict") or "REJECT"
                    sig["ai_note"] = checked.get("ai_note") or checked.get("reason")
                    sig["ai_block"] = True
                save_last(sig, chat_id)
            cap = format_signal(sig)
            msgid = send_chart(
                token, chat_id, rows, pair, sig, "15m", cap, kb_tf(pair), reply_to
            )
            if sig["side"] in ("BUY", "SELL"):
                try:
                    story = format_signal_story(sig)
                    if story:
                        send_message(token, chat_id, story, kb_tf(pair), reply_to=msgid)
                except Exception:
                    log("story all " + traceback.format_exc())
                register_trade(sig, chat_id, msgid, "user")
                try:
                    if is_crypto_pair(pair):
                        post_to_channel(token, pair, sig, rows, dest="crypto")
                    else:
                        post_to_channel(token, pair, sig, rows, dest="pro")
                        post_to_channel(token, pair, sig, rows, dest="free")
                except Exception:
                    log("deliver_all channel " + traceback.format_exc())
            time.sleep(0.25)
        except Exception:
            log("deliver_all " + pair + " " + traceback.format_exc())
            send_message(token, chat_id, "⚠️ %s خطا" % pair, kb_tf(pair))


def briefing(token, chat_id):
    kz = in_killzone(int(time.time())) or "خارج از کیل‌زون"
    sb = "بله ⚡" if in_silver_bullet(int(time.time())) else "نه"
    lines = [
        "⚡ <b>TZ FX</b>  ·  🌍 خلاصه بازار",
        "────────────",
        "⏸ %s" % fx_open_line(),
        "🌍 کیل‌زون الان: <b>%s</b>" % kz,
        "⚡ Silver Bullet: %s" % sb,
        next_session_line(),
        "",
    ]
    for pair, meta in PAIRS.items():
        try:
            rows = fetch_ohlc(pair)
            sig = build_signal(rows, pair)
            px = fmt_px(pair, rows[-1]["c"] if rows else 0)
            if not sig:
                lines.append("%s %s  —  خطا" % (meta["emoji"], meta["name"]))
                continue
            htf = sig.get("htf") or {}
            side = sig["side"]
            if side == "BUY":
                mark = "🟢 BUY"
            elif side == "SELL":
                mark = "🔴 SELL"
            else:
                mark = "⏸ wait"
            sc = sig.get("score") or 0
            lines.append(
                "%s <b>%s</b>  <code>%s</code>\n   %s  · 1H %s/%s  · %s %s/6"
                % (
                    meta["emoji"],
                    pair,
                    px,
                    mark,
                    htf.get("bias") or "-",
                    htf.get("pd") or "-",
                    stars(sc),
                    sc,
                )
            )
        except Exception:
            lines.append("%s %s — خطا" % (meta["emoji"], pair))
    lines += ["", "⚖️ آموزشی است، مشاوره مالی نیست."]
    try:
        raw = llm_ask(
            [],
            u"از روی این خلاصه واقعی ۴ خط فارسی مربی ICT بنویس. عدد جدید نساز. "
            u"اگر ستاپ ضعیف بود بگو صبر کن.\n" + "\n".join(lines)[:1200],
        )
        if raw:
            lines.append("")
            lines.append(u"🤖 " + clean_ai(raw)[:500])
    except Exception:
        log("brief ai " + traceback.format_exc())
    send_message(token, chat_id, "\n".join(lines), kb_main(chat_id))


def calc_risk(token, chat_id, balance):
    last = load_last(chat_id)
    if not last or last.get("side") not in ("BUY", "SELL"):
        send_message(
            token,
            chat_id,
            "اول یک سیگنال BUY/SELL بگیر، بعد حجم را حساب کن.",
            kb_after(),
        )
        return
    txt = format_trade_plan(last, balance, None, 1.0, 100)
    send_message(token, chat_id, txt, kb_after())


_FA2EN = dict((ord(u), str(i)) for i, u in enumerate(u"۰۱۲۳۴۵۶۷۸۹"))


def parse_num(text):
    t = (text or "").strip().translate(_FA2EN)
    t = t.replace(u"٬", "").replace(",", "").replace(u"،", ".")
    t = t.replace("$", "").replace("%", "").strip()
    try:
        return float(t)
    except Exception:
        return None


def parse_spread_price(pair, raw):
    n = parse_num(str(raw))
    if n is None:
        return None
    pip = PAIRS[pair]["pip"]
    if pair == "XAUUSD":
        if n >= 8:
            return abs(n) * 0.01
        return abs(n)
    if n <= 0:
        return 0.0
    if n < 0.01:
        return abs(n)
    return abs(n) * pip


def parse_leverage(text):
    t = (text or "").strip().translate(_FA2EN).replace(" ", "")
    if ":" in t:
        try:
            return max(1, int(float(t.split(":")[-1])))
        except Exception:
            return 100
    n = parse_num(t)
    if not n:
        return 100
    n = abs(n)
    if n < 10:
        return 100
    return int(n)


def contract_usd(pair, lot, price):
    lot = float(lot)
    price = float(price)
    if pair == "XAUUSD":
        return 100.0 * lot * price
    return 100000.0 * lot * price


def format_trade_plan(sig, balance, spread_raw, risk_pct, leverage):
    pair = sig.get("pair")
    if pair not in PAIRS or sig.get("side") not in ("BUY", "SELL"):
        return u"اول یک سیگنال BUY یا SELL بگیر."
    try:
        entry = float(sig["entry"])
        sl = float(sig["sl"])
        tp = float(sig.get("tp") or 0)
        balance = float(balance)
        risk_pct = float(risk_pct)
        leverage = int(leverage or 100)
    except Exception:
        return u"عددها ناقص است. دوباره بفرست."
    if balance <= 0 or risk_pct <= 0:
        return u"موجودی و درصد ریسک باید مثبت باشد."
    pip = PAIRS[pair]["pip"]
    side = sig["side"]
    if not tp:
        dist = abs(entry - sl)
        tp = entry + dist * 2.0 if side == "BUY" else entry - dist * 2.0
    if spread_raw is None:
        spread_price = 0.35 if pair == "XAUUSD" else 1.2 * pip
        spread_note = u"اسپرد پیش‌فرض"
    else:
        spread_price = parse_spread_price(pair, spread_raw)
        if spread_price is None:
            return u"اسپرد را نفهمیدم. برای یورو مثلا ۱.۲ و برای طلا ۰.۳۵ یا ۳۵ بفرست."
        spread_note = u"اسپرد تو"
    if side == "BUY":
        fill = entry + spread_price
        side_fa = u"خرید (BUY) — دکمه سبز Buy"
    else:
        fill = entry - spread_price
        side_fa = u"فروش (SELL) — دکمه قرمز Sell"
    risk_dist = abs(fill - sl)
    rew_dist = abs(tp - fill)
    if risk_dist <= pip * 0.2:
        return u"با این اسپرد حد ضرر تقریباً پر می‌شود — این معامله را نزن."
    risk_pips = risk_dist / pip
    rew_pips = rew_dist / pip
    rr = rew_pips / risk_pips if risk_pips else 0
    risk_money = balance * (risk_pct / 100.0)
    pv = 10.0
    lot = risk_money / (risk_pips * pv) if risk_pips else 0
    lot = max(0.01, min(50.0, round(lot + 1e-12, 2)))
    pip_val = pv * lot
    loss = risk_pips * pip_val
    profit = rew_pips * pip_val
    margin = contract_usd(pair, lot, fill) / float(max(1, leverage))
    unit = u"واحد" if pair == "XAUUSD" else u"پیپ"
    spread_show = spread_price / pip
    sc = sig.get("score") or 0
    warn = []
    if sc and sc < 4:
        warn.append(u"امتیاز سیگنال زیر ۴ است — بهتر است نزنی.")
    if rr < 1.2:
        warn.append(u"بعد از اسپرد R:R ضعیف است — نزن.")
    if spread_price > risk_dist * 0.25:
        warn.append(u"اسپرد نسبت به حد ضرر خیلی پهن است.")
    if margin > balance * 0.5:
        warn.append(u"مارجین زیاد است — حجم را کمتر کن یا اهرم را چک کن.")
    warn_txt = (u"\n⚠️ " + u"\n⚠️ ".join(warn) + u"\n") if warn else u"\n"
    meta = PAIRS[pair]
    return (
        u"📐 <b>اطلاعات معامله</b>\n"
        u"%s  <b>%s</b>  ·  %s\n"
        u"────────────\n"
        u"<b>۱) مبتدی — همین را در متاتریدر بزن</b>\n"
        u"• سفارش: <b>%s</b>\n"
        u"• حجم: <b>%.2f lot</b>\n"
        u"• ورود حدود: <code>%s</code>\n"
        u"  (با اسپرد پر می‌شود ≈ <code>%s</code>)\n"
        u"• حد ضرر: <code>%s</code>\n"
        u"• حد سود: <code>%s</code>\n\n"
        u"در متاتریدر: نماد را باز کن → New Order → "
        u"حجم را بگذار → Buy یا Sell → "
        u"بعد SL و TP را روی همین عددها ست کن.\n"
        u"%s"
        u"────────────\n"
        u"<b>۲) پول</b>\n"
        u"حساب: <b>$%.0f</b>  ·  ریسک <b>%s%%</b> = <b>$%.2f</b>\n"
        u"اگر حد ضرر بخورد ≈ <b>$%.2f</b>\n"
        u"اگر حد سود بخورد ≈ <b>$%.2f</b>\n"
        u"R:R بعد اسپرد: <b>1:%.2f</b>\n\n"
        u"<b>۳) پیشرفته</b>\n"
        u"%s: %.2f %s\n"
        u"فاصله SL: <b>%.1f</b> %s   ·   TP: <b>%.1f</b> %s\n"
        u"ارزش هر %s با این حجم: <b>$%.2f</b>\n"
        u"اهرم 1:%s  ·  مارجین حدودی: <b>$%.2f</b>\n"
        u"امتیاز سیگنال: %s/6\n\n"
        u"<b>۴) قانون</b>\n"
        u"حد ضرر را جابه‌جا نکن. بعد از ورود ولش کن.\n"
        u"حداکثر همین ۱٪ (یا همان درصدی که دادی).\n"
        u"اعداد تقریبی‌اند — با اسپرد زنده بروکر چک کن.\n"
        u"<i>آموزشی است · مشاوره مالی نیست</i>"
        % (
            meta["emoji"],
            pair,
            side,
            side_fa,
            lot,
            fmt_px(pair, entry),
            fmt_px(pair, fill),
            fmt_px(pair, sl),
            fmt_px(pair, tp),
            warn_txt,
            balance,
            ("%.2g" % risk_pct),
            risk_money,
            loss,
            profit,
            rr,
            spread_note,
            spread_show,
            unit,
            risk_pips,
            unit,
            rew_pips,
            unit,
            unit,
            pip_val,
            leverage,
            margin,
            sc,
        )
    )


def kb_trade_bal():
    return {
        "inline_keyboard": [
            [
                btn("$100", "tb_100"),
                btn("$250", "tb_250"),
                btn("$500", "tb_500"),
            ],
            [
                btn("$1,000", "tb_1000", style="primary"),
                btn("$2,500", "tb_2500"),
                btn("$5,000", "tb_5000"),
            ],
            [btn("$10,000", "tb_10000"), btn(u"✏️ عدد خودم", "tb_custom")],
        ]
    }


def kb_trade_spread(pair):
    if pair == "XAUUSD":
        rows = [
            [
                btn("0.20$", "ts_0.20"),
                btn("0.30$", "ts_0.30"),
                btn("0.35$", "ts_0.35", style="primary"),
            ],
            [
                btn("0.50$", "ts_0.50"),
                btn("0.80$", "ts_0.80"),
                btn("1.00$", "ts_1.00"),
            ],
        ]
    else:
        rows = [
            [
                btn(u"0.8 پیپ", "ts_0.8"),
                btn("1.0", "ts_1.0"),
                btn("1.2", "ts_1.2", style="primary"),
            ],
            [
                btn(u"1.5 پیپ", "ts_1.5"),
                btn("2.0", "ts_2.0"),
                btn("3.0", "ts_3.0"),
            ],
        ]
    rows.append([btn(u"✏️ عدد خودم", "ts_custom")])
    return {"inline_keyboard": rows}


def kb_trade_risk():
    return {
        "inline_keyboard": [
            [
                btn("0.5%", "tk_0.5"),
                btn("1%", "tk_1", style="success"),
                btn("1.5%", "tk_1.5"),
                btn("2%", "tk_2"),
            ]
        ]
    }


def kb_trade_lev():
    return {
        "inline_keyboard": [
            [
                btn("1:50", "tl_50"),
                btn("1:100", "tl_100", style="primary"),
                btn("1:200", "tl_200"),
            ],
            [btn("1:500", "tl_500"), btn("1:1000", "tl_1000")],
        ]
    }


def start_trade_wizard(token, user_id, chat_id, pair=None):
    last = load_last(user_id)
    if not last or last.get("side") not in ("BUY", "SELL"):
        last = load_last()
    if pair and last and last.get("pair") != pair:
        alt = load_last()
        if alt and alt.get("pair") == pair and alt.get("side") in ("BUY", "SELL"):
            last = alt
    if not last or last.get("side") not in ("BUY", "SELL"):
        send_message(
            token,
            chat_id,
            u"اول یک سیگنال BUY/SELL بگیر، بعد اطلاعات معامله را بزن.",
            kb_main(user_id),
        )
        return
    pair = last.get("pair")
    extra = {"step": "bal", "pair": pair, "sig": last}
    set_wait(user_id, "trade", extra)
    send_message(
        token,
        chat_id,
        u"📐 <b>اطلاعات معامله %s %s</b>\n"
        u"ورود <code>%s</code>  ·  SL <code>%s</code>  ·  TP <code>%s</code>\n\n"
        u"موجودی حسابت چند دلار است؟\n"
        u"از دکمه بزن یا عدد را بنویس."
        % (
            last.get("pair"),
            last.get("side"),
            fmt_px(pair, last.get("entry") or 0),
            fmt_px(pair, last.get("sl") or 0),
            fmt_px(pair, last.get("tp") or 0),
        ),
        kb_trade_bal(),
    )


def finish_trade(token, user_id, chat_id, st):
    pop_wait(user_id)
    sig = st.get("sig") or load_last(user_id) or {}
    txt = format_trade_plan(
        sig,
        st.get("bal") or 0,
        st.get("spread"),
        st.get("risk") or 1.0,
        st.get("lev") or 100,
    )
    send_message(token, chat_id, txt, kb_after())


def handle_trade_text(token, user_id, chat_id, text):
    st = get_wait(user_id)
    if (st.get("kind") or "") != "trade":
        return False
    step = st.get("step") or "bal"
    n = parse_num(text)
    if step == "bal":
        if n is None or n < 10:
            send_message(
                token,
                chat_id,
                u"موجودی را به دلار عدد بفرست. مثلا 1000",
                kb_trade_bal(),
            )
            return True
        st["bal"] = n
        st["step"] = "spread"
        set_wait(user_id, "trade", st)
        pair = (st.get("sig") or {}).get("pair") or "EURUSD"
        hint = (
            u"اسپرد طلا را به دلار بفرست (۰.۳۵) یا ۳۰ یعنی ۰.۳۰ دلار."
            if pair == "XAUUSD"
            else u"اسپرد را به پیپ بفرست. مثلا 1.2"
        )
        send_message(token, chat_id, u"اسپرد بروکرت؟\n" + hint, kb_trade_spread(pair))
        return True
    if step == "spread":
        pair = (st.get("sig") or {}).get("pair") or "EURUSD"
        if parse_spread_price(pair, text) is None:
            send_message(
                token, chat_id, u"اسپرد را نفهمیدم. دوباره بفرست.", kb_trade_spread(pair)
            )
            return True
        st["spread"] = text
        st["step"] = "risk"
        set_wait(user_id, "trade", st)
        send_message(
            token,
            chat_id,
            u"چند درصد حساب را ریسک می‌کنی؟ پیشنهادی: ۱٪",
            kb_trade_risk(),
        )
        return True
    if step == "risk":
        if n is None or n <= 0 or n > 10:
            send_message(token, chat_id, u"درصد ریسک مثلا 1", kb_trade_risk())
            return True
        st["risk"] = n
        st["step"] = "lev"
        set_wait(user_id, "trade", st)
        send_message(token, chat_id, u"اهرم حساب؟ معمولا 1:100", kb_trade_lev())
        return True
    if step == "lev":
        st["lev"] = parse_leverage(text)
        finish_trade(token, user_id, chat_id, st)
        return True
    return False


def handle_trade_cb(token, user_id, chat_id, data):
    st = get_wait(user_id)
    if (st.get("kind") or "") != "trade":
        start_trade_wizard(token, user_id, chat_id)
        st = get_wait(user_id)
        if (st.get("kind") or "") != "trade":
            return
    if data.startswith("tb_"):
        rest = data[3:]
        if rest == "custom":
            st["step"] = "bal"
            set_wait(user_id, "trade", st)
            send_message(token, chat_id, u"موجودی را به دلار بنویس. مثلا 850")
            return
        try:
            st["bal"] = float(rest)
        except Exception:
            send_message(token, chat_id, u"موجودی نامعتبر.", kb_trade_bal())
            return
        st["step"] = "spread"
        set_wait(user_id, "trade", st)
        pair = (st.get("sig") or {}).get("pair") or "EURUSD"
        send_message(token, chat_id, u"اسپرد بروکرت؟", kb_trade_spread(pair))
        return
    if data.startswith("ts_"):
        rest = data[3:]
        if rest == "custom":
            st["step"] = "spread"
            set_wait(user_id, "trade", st)
            send_message(token, chat_id, u"اسپرد را عدد بفرست.")
            return
        st["spread"] = rest
        st["step"] = "risk"
        set_wait(user_id, "trade", st)
        send_message(token, chat_id, u"چند درصد ریسک؟ پیشنهادی ۱٪", kb_trade_risk())
        return
    if data.startswith("tk_"):
        try:
            st["risk"] = float(data[3:])
        except Exception:
            st["risk"] = 1.0
        st["step"] = "lev"
        set_wait(user_id, "trade", st)
        send_message(token, chat_id, u"اهرم حساب؟", kb_trade_lev())
        return
    if data.startswith("tl_"):
        try:
            st["lev"] = int(data[3:])
        except Exception:
            st["lev"] = 100
        finish_trade(token, user_id, chat_id, st)


def gate(token, user_id, chat_id, need_pro=True):
    touch_user(user_id)
    if is_owner(user_id):
        return True
    if not in_channel(token, user_id):
        send_message(token, chat_id, txt_join(), kb_join())
        return False
    if need_pro and not is_pro(user_id):
        send_message(token, chat_id, txt_paywall(user_id), kb_pay())
        return False
    return True


AI_URL = "https://api.llm7.io/v1/chat/completions"
AI_MODELS = ("fast", "minimax-m2.7")
_llm_block_until = 0
_gemini_block_until = 0
_ai_confirm_cache = {}
AI_SYS = (
    "تو مربی TZ FX هستی. مرد فارسی‌زبان، گرم، رک، کوتاه مثل ویس. "
    "کنار همین یک شاگرد نشسته‌ای. ربات‌بازی نکن. "
    "دو میز: "
    "۱) فارکس ICT — فقط EURUSD، GBPUSD، XAUUSD. "
    "شنبه و یکشنبه فارکس بسته است؛ صادق بگو. پنجره سیگنال کانال فارکس ۸:۳۰–۲۰:۳۰ تهران. "
    "۲) کریپتو بتا — هر کوین اسپات USDT (BTC ETH SOL و بقیه؛ اسم را بگو). "
    "همان هندسه: Judas سوئیپ → MSS → FVG → ورود داخل شکاف، حد ضرر پشت ویک. "
    "کریپتو ۲۴/۷ است و بتا؛ قول ICT مایکل روی کوین نده. "
    "سیگنال الکی نساز. قیمت از خودت درنیار. فقط اگر در «داده بازار» آمده همان را بگو. "
    "بدون حد ضرر ورود نده. امتیاز زیر ۴ یا خلاف روزانه = صبر. "
    "قول سود و درصد دقت الکی ممنوع. "
    "حافظه فقط همین شاگرد. "
    "احوال‌پرسی حداکثر ۳ خط. آموزش حداکثر ۸ خط. "
    "سیگنال زنده نفرست مگر صریح بگوید سیگنال بده. "
    "جمله کوتاه، قابل ویس، بدون جدول و ستاره. "
    "کانال رایگان @TZ_FX_CH · کریپتو بتا جدا."
)


def load_chat():
    try:
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_chat(data):
    try:
        if len(data) > 200:
            items = sorted(data.items(), key=lambda kv: (kv[1] or {}).get("ts") or 0)
            data = dict(items[-200:])
        with open(CHAT_FILE, "w") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


def _blank_mem(uid):
    try:
        uid = int(uid or 0)
    except Exception:
        uid = 0
    return {
        "id": uid,
        "msgs": [],
        "summary": "",
        "facts": [],
        "notes": "",
        "topic": "",
        "topic_title": "",
        "pair": "",
        "name": "",
        "voice": False,
        "last_ans": "",
        "last_sig": None,
        "lang": "fa",
        "desk_mid": None,
        "ts": 0,
    }


_LANG = {"uid": None, "code": "fa"}


def get_lang(uid=None):
    if uid is None:
        uid = _LANG.get("uid")
    rec = {}
    if uid:
        try:
            rec = load_user_mem(uid)
        except Exception:
            rec = {}
    code = rec.get("lang") if isinstance(rec, dict) else None
    if code in ("fa", "en"):
        return code
    return "fa"


def set_lang(uid, code):
    code = "en" if str(code).lower().startswith("en") else "fa"
    rec = load_user_mem(uid)
    rec["lang"] = code
    save_user_mem(uid, rec)
    _LANG["uid"] = uid
    _LANG["code"] = code
    return code


def use_lang(uid, user=None):
    rec = load_user_mem(uid) if uid else {}
    code = rec.get("lang") if isinstance(rec, dict) else None
    if code not in ("fa", "en"):
        lc = ""
        if user:
            lc = str(user.get("language_code") or "")
        code = "en" if lc.lower().startswith("en") else "fa"
        if uid and isinstance(rec, dict):
            rec["lang"] = code
            try:
                save_user_mem(uid, rec)
            except Exception:
                pass
    _LANG["uid"] = uid
    _LANG["code"] = code or "fa"
    return _LANG["code"]


def T(key, **kwargs):
    lang = _LANG.get("code") or "fa"
    if _i18n_mod is None:
        return key
    return _i18n_mod.t(lang, key, **kwargs)


def is_en(uid=None):
    return get_lang(uid) == "en"


def _mem_path(uid):
    return os.path.join(MEM_DIR, "%s.json" % int(uid))


def load_user_mem(uid):
    try:
        uid = int(uid)
    except Exception:
        return _blank_mem(0)
    rec = _jload(_mem_path(uid), None)
    if isinstance(rec, dict):
        rec.setdefault("msgs", [])
        rec.setdefault("facts", [])
        rec["id"] = uid
        return rec
    old = (load_chat() or {}).get(str(uid))
    if isinstance(old, dict):
        old.setdefault("msgs", [])
        old.setdefault("facts", [])
        old["id"] = uid
        save_user_mem(uid, old)
        return old
    return _blank_mem(uid)


def save_user_mem(uid, rec):
    try:
        uid = int(uid)
    except Exception:
        return
    rec = dict(rec or {})
    rec["id"] = uid
    rec["ts"] = time.time()
    rec = compact_chat(rec)
    try:
        if not os.path.isdir(MEM_DIR):
            os.makedirs(MEM_DIR)
    except Exception:
        pass
    _jsave(_mem_path(uid), rec)


def wipe_user_mem(uid):
    try:
        os.remove(_mem_path(int(uid)))
    except Exception:
        pass


def compact_chat(rec):
    msgs = list(rec.get("msgs") or [])
    keep = 24
    if len(msgs) > keep:
        old = msgs[:-keep]
        lines = []
        for m in old:
            role = u"شاگرد" if m.get("role") == "user" else u"مربی"
            bit = str(m.get("content") or "").replace("\n", " ").strip()[:110]
            if bit:
                lines.append(role + ": " + bit)
        blob = u" · ".join(lines)
        prev = rec.get("summary") or ""
        rec["summary"] = (prev + u" · " + blob).strip(u" ·")[-1800:]
        rec["msgs"] = msgs[-keep:]
    facts = rec.get("facts") or []
    if isinstance(facts, list) and len(facts) > 12:
        rec["facts"] = facts[-12:]
    return rec


def _add_fact(rec, fact):
    fact = (fact or "").strip()
    if not fact:
        return rec
    facts = [f for f in (rec.get("facts") or []) if f != fact]
    facts.append(fact[:180])
    rec["facts"] = facts[-12:]
    return rec


def mem_touch(uid, name=None, voice=None, pair=None, topic=None, last_sig=None):
    if not uid:
        return _blank_mem(0)
    rec = load_user_mem(uid)
    if name and not rec.get("name"):
        rec["name"] = str(name)[:40]
    if voice:
        rec["voice"] = True
    if pair:
        rec["pair"] = pair
        rec = _add_fact(rec, u"نماد مورد علاقه: " + pair)
    if topic:
        rec["topic"] = topic
        title = EDU_TITLE.get(topic) or topic
        rec["topic_title"] = title
        prev = rec.get("notes") or ""
        if title and title not in prev:
            rec["notes"] = (prev + u" · " + title).strip(u" ·")[-600:]
    if last_sig and isinstance(last_sig, dict):
        rec["last_sig"] = {
            "pair": last_sig.get("pair"),
            "side": last_sig.get("side"),
            "entry": last_sig.get("entry"),
            "sl": last_sig.get("sl"),
            "tp": last_sig.get("tp"),
            "score": last_sig.get("score"),
        }
    save_user_mem(uid, rec)
    return rec


def memory_pack(uid, rec):
    bits = [u"این پرونده فقط مال همین شاگرد است. شاگرد دیگر را قاطی نکن."]
    if rec.get("name"):
        bits.append(u"نام شاگرد: " + rec.get("name"))
    if rec.get("pair"):
        bits.append(u"نماد مورد علاقه: " + rec.get("pair"))
    facts = rec.get("facts") or []
    if facts:
        bits.append(u"نکات ثابت:\n- " + u"\n- ".join([str(x) for x in facts[-12:]]))
    if rec.get("summary"):
        bits.append(u"خلاصه گفتگوهای قبلی:\n" + rec.get("summary"))
    if rec.get("notes"):
        bits.append(u"درس‌هایی که با هم رفتیم: " + rec.get("notes"))
    topic = rec.get("topic") or ""
    if topic:
        title = rec.get("topic_title") or EDU_TITLE.get(topic) or topic
        bits.append(u"درس باز الان: " + title)
    last = rec.get("last_sig")
    if not last and uid:
        try:
            last = load_last(uid)
        except Exception:
            last = None
    if last and last.get("side") in ("BUY", "SELL"):
        bits.append(
            u"آخرین سیگنال همین شاگرد: %s %s ورود %s حدضرر %s حدسود %s امتیاز %s"
            % (
                last.get("pair"),
                last.get("side"),
                last.get("entry"),
                last.get("sl"),
                last.get("tp"),
                last.get("score"),
            )
        )
    return u"\n".join(bits)[:2400]


def _harvest_facts(rec, text):
    rec = dict(rec or {})
    t = (text or "").replace(u"ي", u"ی")
    pair = detect_pair(t)
    if pair:
        rec["pair"] = pair
        rec = _add_fact(rec, u"نماد مورد علاقه: " + pair)
    low = t.lower()
    if any(w in low for w in (u"مبتدی", u"صفرم", u"تازه‌کار", u"تازه کار", u"از صفر")):
        rec = _add_fact(rec, u"سطح شاگرد: مبتدی")
    if any(w in low for w in (u"پراپ", u"چند ساله", u"حرفه‌ای", u"حساب واقعی")):
        rec = _add_fact(rec, u"سطح شاگرد: با تجربه")
    return rec


def coach_reply(uid, text, topic=None, strong=False):
    rec = load_user_mem(uid)
    rec = _harvest_facts(rec, text)
    if topic:
        rec["topic"] = topic
        rec["topic_title"] = EDU_TITLE.get(topic) or rec.get("topic_title") or topic
    pack = ""
    try:
        pack = memory_pack(uid, rec)
    except Exception:
        pack = ""
    extra = pack or ""
    extra = (
        (extra + u"\n")
        + u"میز زنده: فارکس یورو/پوند/طلا · کریپتو بتا هر USDT · "
        + fx_open_line()
    ).strip()
    top = topic or rec.get("topic") or ""
    if top:
        try:
            extra = (extra + u"\n" + lesson_context(top)).strip()
        except Exception:
            pass
    prompt = (text or "").strip()[:1400]
    if extra:
        prompt = (
            u"حافظه فقط همین شاگرد (قیمت زنده از این متن نساز مگر در داده بازار آمده):\n"
            + extra[:2000]
            + u"\n\nجواب را کوتاه و قابل‌خواندن با ویس مردانه بده.\nسوال شاگرد:\n"
            + prompt
        )
    raw = ""
    try:
        raw = llm_ask(rec.get("msgs") or [], prompt, strong=strong)
    except Exception:
        log("coach llm " + traceback.format_exc())
        raw = ""
    ans = clean_ai(raw) if raw else ""
    if not ans:
        ans = local_brain(text)
        if not raw:
            log("coach fallback local uid=%s" % uid)
    if not ans:
        ans = u"یک لحظه گیر کردم. کوتاه بپرس — یورو، پوند، طلا یا اسم کوین."
    msgs = rec.get("msgs") or []
    msgs.append({"role": "user", "content": (text or "")[:1200]})
    msgs.append({"role": "assistant", "content": ans[:1800]})
    rec["msgs"] = msgs[-36:]
    rec["last_ans"] = ans[:2500]
    save_user_mem(uid, rec)
    return ans, rec


def _safe_market_blob():
    try:
        return market_blob()
    except Exception:
        try:
            return "time=" + tehran_fmt()
        except Exception:
            return ""


def market_blob():
    now = int(time.time())
    lines = [
        "time=" + tehran_fmt(),
        "fx=" + (fx_open_line(now) or ""),
        "kilzone=" + (in_killzone(now) or "out"),
        "silver=" + ("yes" if in_silver_bullet(now) else "no"),
        "desks=FX:EURUSD,GBPUSD,XAUUSD | CRYPTO_BETA:any USDT spot",
    ]
    desk = list(FX_PAIRS) + [p for p in ("BTCUSDT", "ETHUSDT", "SOLUSDT") if p in PAIRS]
    for pair in desk:
        try:
            rows = _ohlc_cache.get(pair + "|15m") or []
            if not rows:
                continue
            px = rows[-1]["c"]
            window = rows[-20:] if len(rows) >= 20 else rows
            hi = max(r["h"] for r in window)
            lo = min(r["l"] for r in window)
            pd = "DISCOUNT" if px <= (hi + lo) / 2.0 else "PREMIUM"
            lines.append(
                "%s px=%s 20h=%s 20l=%s %s"
                % (pair, fmt_px(pair, px), fmt_px(pair, hi), fmt_px(pair, lo), pd)
            )
        except Exception:
            continue
    return " | ".join(lines)


def load_gemini():
    try:
        if os.path.isfile(GEMINI_FILE):
            with open(GEMINI_FILE, "r") as f:
                val = f.read().strip()
            if val:
                return val
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()


def gemini_ask(history, user_text, strong=False):
    global _gemini_block_until
    import requests

    if time.time() < _gemini_block_until:
        return None
    key = load_gemini()
    if not key:
        return None
    keep = 20 if strong else 8
    clip = 1000 if strong else 500
    ulen = 2200 if strong else 1200
    contents = []
    for m in history[-keep:]:
        role = m.get("role")
        txt = str(m.get("content") or "")[:clip]
        if not txt:
            continue
        if role == "user":
            contents.append({"role": "user", "parts": [{"text": txt}]})
        elif role == "assistant":
            contents.append({"role": "model", "parts": [{"text": txt}]})
    contents.append({"role": "user", "parts": [{"text": user_text[:ulen]}]})
    gen = {
        "temperature": 0.28 if strong else 0.35,
        "maxOutputTokens": 1024 if strong else 512,
    }
    models = GEMINI_CHAT_MODELS if strong else GEMINI_MODELS
    cap = 2500 if strong else 1800
    wait = 12 if strong else 8
    for model in models:
        cfg = dict(gen)
        if strong and ("3.5" in model or "3.1" in model) and "lite" not in model:
            cfg["thinkingConfig"] = {"thinkingBudget": 0}
        body = {
            "systemInstruction": {"parts": [{"text": T("ai.sys") + "\nmarket:\n" + _safe_market_blob()}]},
            "contents": contents,
            "generationConfig": cfg,
        }
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + model
            + ":generateContent"
        )
        try:
            r = http().post(
                url,
                headers={"Content-Type": "application/json", "X-goog-api-key": key},
                json=body,
                timeout=wait,
            )
        except Exception as e:
            log("gemini fail %s %s" % (model, str(e)[:80]))
            continue
        if r.status_code == 429:
            _gemini_block_until = time.time() + 90
            log("gemini 429 %s — pause 90s" % model)
            continue
        if r.status_code != 200:
            log("gemini http %s %s" % (r.status_code, model))
            continue
        try:
            data = r.json()
        except Exception:
            continue
        cand = (data.get("candidates") or [{}])[0]
        parts = ((cand.get("content") or {}).get("parts") or [])
        txt = "".join([(p.get("text") or "") for p in parts]).strip()
        if txt:
            log("gemini ok %s n=%s" % (model, len(txt)))
            return txt[:cap]
        log("gemini empty %s fr=%s" % (model, cand.get("finishReason")))
    return None


def llm_ask(history, user_text, strong=False):
    global _llm_block_until
    import requests

    g = gemini_ask(history, user_text, strong=strong)
    if g:
        return g
    if time.time() < _llm_block_until:
        return None
    messages = [{"role": "system", "content": T("ai.sys") + "\nmarket:\n" + market_blob()}]
    keep = 20 if strong else 8
    clip = 1000 if strong else 500
    for m in history[-keep:]:
        role = m.get("role")
        if role in ("user", "assistant") and m.get("content"):
            messages.append({"role": role, "content": str(m["content"])[:clip]})
    messages.append({"role": "user", "content": user_text[:2200 if strong else 1400]})
    for model in AI_MODELS:
        try:
            r = requests.post(
                AI_URL,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 700 if strong else 400,
                    "temperature": 0.3 if strong else 0.35,
                },
                timeout=16 if strong else 12,
            )
        except Exception as e:
            log("llm fail %s %s" % (model, str(e)[:80]))
            continue
        if r.status_code == 429:
            _llm_block_until = time.time() + 20
            log("llm 429 " + model)
            continue
        if r.status_code != 200:
            log("llm http %s %s" % (r.status_code, model))
            continue
        try:
            data = r.json()
        except Exception:
            continue
        txt = (((data.get("choices") or [{}])[0]).get("message") or {}).get("content") or ""
        txt = txt.strip()
        if txt:
            log("llm ok %s n=%s" % (model, len(txt)))
            return txt[:1800]
    return None


def clean_ai(text):
    if not text:
        return ""
    for a, b in (("**", ""), ("__", ""), ("```", ""), ("# ", ""), ("## ", ""), ("### ", "")):
        text = text.replace(a, b)
    return text.strip()[:1800]


def ai_review(sig, board=""):
    """AI writes commentary from real numbers. Never invents prices."""
    if not sig:
        return None
    pair = sig.get("pair") or ""
    blob = (
        "نماد %s سمت %s امتیاز %s قیمت %s ورود %s حدضرر %s حدسود %s ستاپ %s دلیل %s\nتایم‌فریم‌ها:\n%s"
        % (
            pair,
            sig.get("side"),
            sig.get("score"),
            sig.get("price"),
            sig.get("entry"),
            sig.get("sl"),
            sig.get("tp"),
            sig.get("setup") or sig.get("reason") or "",
            sig.get("reason") or "",
            board.replace("<b>", "").replace("</b>", ""),
        )
    )
    raw = llm_ask(
        [],
        "از روی این داده واقعی ۴ خط فارسی مربی ICT بنویس. عدد جدید نساز. "
        "اگر NO SIGNAL یا امتیاز زیر ۴ است بگو وارد نشو. در غیر این صورت ورود/SL/TP را تکرار کن.\n"
        + blob[:1500],
    )
    return clean_ai(raw) if raw else None


def ai_confirm(sig, rows):
    """ICT: CONFIRM or REJECT only. Never widen TP to H4/D1."""
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return sig
    sig = dict(sig)
    pair = sig.get("pair")
    price = sig.get("price")
    if pair in PAIRS and price is not None:
        fixed, why = validate_geometry(sig, price, pair)
        if not fixed:
            sig["side"] = "NO SIGNAL"
            sig["reason"] = why or u"حد ضرر/حد سود نامعتبر"
            sig["score"] = 0
            sig["ai_verdict"] = "REJECT"
            sig["ai_block"] = True
            return sig
        sig = fixed
    rr = 0
    if sig.get("risk_pips"):
        rr = (sig.get("reward_pips") or 0) / float(sig["risk_pips"])
    d1 = ((sig.get("htf") or {}).get("d1") or {}).get("bias")
    h4 = ((sig.get("htf") or {}).get("h4") or {}).get("bias")
    against = (sig["side"] == "BUY" and d1 == "BEAR") or (
        sig["side"] == "SELL" and d1 == "BULL"
    )
    h4_against = (sig["side"] == "BUY" and h4 == "BEAR") or (
        sig["side"] == "SELL" and h4 == "BULL"
    )
    weak = (
        against
        or (sig.get("score") or 0) < 4
        or rr < 1.2
        or rr > 2.15
        or (not sig.get("inside_fvg"))
        or (not sig.get("disp"))
    )
    if weak:
        sig["ai_verdict"] = "REJECT"
        sig["ai_block"] = True
        sig["ai_note"] = u"فیلتر ICT: امتیاز/جهت/هدف ضعیف — وارد نشو"
        return sig
    cache_key = "%s|%s|%s|%s" % (
        sig.get("pair"),
        sig.get("side"),
        sig.get("entry"),
        sig.get("sl"),
    )
    hit = _ai_confirm_cache.get(cache_key)
    if hit and time.time() - hit[0] < 1800:
        sig.update(hit[1])
        return sig
    htf = sig.get("htf") or {}
    prompt = (
        "ICT. VERIFY only. Do NOT invent or change prices. "
        "CONFIRM only if Judas+MSS+FVG, not chased, HTF aligned, SL beyond wick, "
        "TP is nearby in-session IRL, R:R 1.0-2.0. Otherwise REJECT.\n"
        "Line1 only: CONFIRM or REJECT\n"
        "Line2 Persian max 16 words.\n"
        "LIVE=%s ENTRY=%s SL=%s TP=%s SIDE=%s pair=%s score=%s rr=%.2f "
        "1H=%s/%s H4=%s D1=%s kz=%s insideFVG=%s mss=%s ote=%s"
        % (
            fmt_px(pair, sig.get("price") or 0),
            fmt_px(pair, sig.get("entry") or 0),
            fmt_px(pair, sig.get("sl") or 0),
            fmt_px(pair, sig.get("tp") or 0),
            sig.get("side"),
            pair,
            sig.get("score"),
            rr,
            htf.get("bias") or "-",
            htf.get("pd") or "-",
            h4 or "-",
            d1 or "-",
            sig.get("killzone") or "-",
            sig.get("inside_fvg"),
            sig.get("mss"),
            sig.get("ote"),
        )
    )
    raw = ""
    try:
        raw = gemini_ask([], prompt) or ""
    except Exception:
        raw = ""
    if not str(raw).strip():
        try:
            raw = llm_ask([], prompt) or ""
        except Exception:
            raw = ""
    first = ""
    note = ""
    extra = {}
    if str(raw).strip():
        ls = [x.strip() for x in str(raw).strip().splitlines() if x.strip()]
        first = (ls[0] if ls else "").upper()
        note = " ".join(ls[1:])[:220] if len(ls) > 1 else ""
    if first.startswith("REJECT"):
        extra = {
            "ai_verdict": "REJECT",
            "ai_block": True,
            "ai_note": note or u"ستاپ ضعیف",
        }
        sig.update(extra)
    elif first.startswith("CONFIRM"):
        extra = {"ai_verdict": "CONFIRM", "ai_block": False, "ai_note": note}
        fixed, why = validate_geometry(sig, price, pair)
        if not fixed:
            extra = {
                "ai_verdict": "REJECT",
                "ai_block": True,
                "ai_note": why or u"هندسه نامعتبر",
            }
            sig["side"] = "NO SIGNAL"
            sig["reason"] = why or u"AI: هندسه نامعتبر"
            sig["score"] = 0
            sig.update(extra)
        else:
            sig = fixed
            sig.update(extra)
    else:
        extra = {
            "ai_verdict": "PENDING",
            "ai_block": False,
            "ai_note": u"AI لحظه‌ای در دسترس نبود — فیلتر ICT رد نکرد",
        }
        sig.update(extra)
    snap = {
        "ai_verdict": sig.get("ai_verdict"),
        "ai_block": sig.get("ai_block"),
        "ai_note": sig.get("ai_note"),
        "tp": sig.get("tp"),
        "reward_pips": sig.get("reward_pips"),
        "entry": sig.get("entry"),
        "sl": sig.get("sl"),
        "side": sig.get("side"),
        "reason": sig.get("reason"),
        "score": sig.get("score"),
        "warn": sig.get("warn"),
    }
    _ai_confirm_cache[cache_key] = (time.time(), snap)
    return sig



def detect_pair(text):
    t = (text or "").replace(u"ي", u"ی").lower()
    if any(w in t for w in (u"طلا", "gold", "xau")):
        return "XAUUSD"
    if any(w in t for w in (u"یورو", "euro", "eur")):
        return "EURUSD"
    if any(w in t for w in (u"پوند", "pound", "gbp", u"پون")):
        return "GBPUSD"
    try:
        if looks_like_crypto_query(text) or any(k in t for k in _CRYPTO_FA):
            hit = ensure_crypto_pair(text)
            if hit:
                return hit
            for key, pair in _CRYPTO_FA.items():
                if key in t and len(str(key)) >= 3:
                    got = ensure_crypto_pair(pair)
                    if got:
                        return got
    except Exception:
        pass
    return None


def want_live_signal(text):
    t = (text or "").replace(u"ي", u"ی").lower()
    if u"سیگنال" in t and any(k in t for k in (u"بده", u"الان", u"بگیر", u"نشون", u"چی", u"کجاست")):
        return True
    if u"ورود بده" in t or u"تحلیل کن" in t:
        return True
    if (u"بخرم" in t or u"بفروشم" in t) and u"آموزش" not in t and u"یاد" not in t:
        return True
    return False


def local_brain(text):
    t = (text or "").strip()
    low = t.replace(u"ي", u"ی").lower()
    now = int(time.time())
    kz = in_killzone(now) or u"خارج از کیل‌زون"
    sb = u"بله ⚡" if in_silver_bullet(now) else u"نه"
    pair = detect_pair(t)
    if any(w in low for w in (u"سلام", "hello", "hi", u"خوبی", u"درود", u"هی ")):
        return (
            u"سلام. مربی TZ FXام.\n"
            u"%s\n"
            u"کیل‌زون: %s · SB: %s\n"
            u"یورو، پوند، طلا یا اسم کوین را بپرس."
            % (fx_open_line(now), kz, sb)
        )
    if any(w in low for w in (u"آموزش", u"یاد", "ict", "fvg", u"سوئیپ", "ote")):
        return (
            u"ICT: نقدینگی → سوئیپ → جابجایی/FVG → ورود داخل FVG، "
            u"حد ضرر پشت سوئیپ، حد سود نقدینگی مخالف.\n"
            u"امتیاز زیر ۴ را معامله نکن. درس کامل دکمه 🎓."
        )
    lines = [u"🕒 %s" % tehran_fmt(), u"🌍 کیل‌زون: %s · SB: %s" % (kz, sb)]
    targets = [pair] if pair else list(FX_PAIRS) + list(CRYPTO_CORE[:6])
    for p in targets:
        if p not in PAIRS:
            try:
                ensure_crypto_pair(p)
            except Exception:
                pass
        rows = _ohlc_cache.get(p + "|15m") or []
        if not rows:
            lines.append(u"%s داده بازار نرسید." % p)
            continue
        px = fmt_px(p, rows[-1]["c"])
        sig = None
        try:
            sig = build_signal(rows, p)
        except Exception:
            sig = None
        if not sig:
            meta = PAIRS.get(p) or {}
            lines.append(u"%s %s  قیمت %s  · ستاپ ناقص" % (meta.get("emoji") or "", p, px))
            continue
        side = sig.get("side") or "NO SIGNAL"
        sc = sig.get("score") or 0
        if side in ("BUY", "SELL"):
            lines.append(
                u"%s %s %s  قیمت %s  امتیاز %s/6\nورود %s  SL %s  TP %s"
                % (
                    PAIRS[p]["emoji"],
                    p,
                    side,
                    px,
                    sc,
                    fmt_px(p, sig.get("entry") or 0),
                    fmt_px(p, sig.get("sl") or 0),
                    fmt_px(p, sig.get("tp") or 0),
                )
            )
            if sc < 4:
                lines.append(u"ضعیف است — وارد نشو.")
        else:
            lines.append(
                u"%s %s  قیمت %s  · صبر: %s"
                % (PAIRS[p]["emoji"], p, px, sig.get("reason") or "ستاپ نیست")
            )
    lines.append(u"آموزشی است · عدد الکی نیست.")
    return u"\n".join(lines)


def ai_chat(token, user_id, chat_id, text, short=False, reply_to=None, speak=False):
    import requests

    try:
        _ai_chat_inner(token, user_id, chat_id, text, short, reply_to, speak=speak)
    except Exception:
        log("ai_chat crash " + traceback.format_exc())
        try:
            send_message(
                token,
                chat_id,
                local_brain(text),
                kb_after(),
                parse_mode=None,
                reply_to=reply_to,
            )
        except Exception:
            send_message(token, chat_id, u"مربی الان شلوغه. از دکمه‌ها سیگنال بگیر.", kb_main(user_id))


def _ai_chat_inner(token, user_id, chat_id, text, short=False, reply_to=None, speak=False):
    import requests

    rec = load_user_mem(user_id)
    pair = detect_pair(text)
    if want_live_signal(text):
        if pair:
            mem_touch(user_id, pair=pair)
            deliver_one(token, chat_id, pair, reply_to=reply_to, user_id=user_id)
            return
        fav = rec.get("pair")
        if fav in PAIRS:
            deliver_one(token, chat_id, fav, reply_to=reply_to, user_id=user_id)
            return
        deliver_all(token, chat_id, reply_to=reply_to)
        return
    try:
        requests.post(
            tg_api(token) + "/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
            timeout=6,
        )
    except Exception:
        pass
    rec = load_user_mem(user_id or chat_id)
    key = str(user_id or chat_id)
    if (not is_owner(user_id)) and over_hour("aih:%s" % key, 40):
        send_message(
            token,
            chat_id,
            local_brain(text) + u"\n\nاین ساعت سهم چت پر شد — سیگنال از دکمه‌ها آزاد است.",
            kb_after(),
            parse_mode=None,
            reply_to=reply_to,
        )
        return
    q = text if not short else (text + u"\n(جواب حداکثر ۵ خط، خودمونی)")
    ans, rec = coach_reply(user_id or chat_id, q, topic=rec.get("topic"), strong=not short)
    if speak:
        rec["voice"] = True
        save_user_mem(user_id or chat_id, rec)
    wedu = get_wait(user_id)
    markup = kb_after()
    if (wedu.get("kind") or "") == "edu_chat":
        lk = wedu.get("lesson") or rec.get("topic") or ""
        if lk in EDU:
            markup = kb_lesson(lk)
        elif str(lk).startswith("l") and str(lk)[1:].isdigit():
            markup = kb_edu_level(str(lk)[1:])
        else:
            markup = kb_edu()
    mode = "HTML" if (u"<b>" in ans or u"<code>" in ans) else None
    ok = send_message(token, chat_id, ans, markup, parse_mode=mode, reply_to=reply_to)
    if not ok:
        ok = send_message(token, chat_id, strip_html(ans)[:3500], markup, parse_mode=None, reply_to=reply_to)
    if not ok:
        log("ai_chat send fail uid=%s chat=%s" % (user_id, chat_id))
    try:
        speak_text(token, chat_id, strip_html(ans)[:450], markup=markup, caption="")
    except Exception:
        log("speak " + traceback.format_exc())
    log("ai_chat uid=%s n=%s send=%s" % (user_id, len(ans or ""), bool(ok)))


def apply_admin_setting(token, chat_id, kind, text):
    text = (text or "").strip()
    if kind == "card":
        digits = "".join(ch for ch in text if ch.isdigit())
        if len(digits) < 12:
            send_message(token, chat_id, u"شماره کارت نامعتبر. دوباره بفرست.", kb_admin_pay())
            return False
        d = load_pay()
        d["card"] = digits
        save_pay(d)
        send_message(
            token,
            chat_id,
            u"✅ کارت ثبت شد:\n<code>%s</code>" % card_pretty(digits),
            kb_admin_pay(),
        )
        return True
    if kind == "holder":
        if len(text) < 2:
            send_message(token, chat_id, u"نام را کامل بفرست.", kb_admin_pay())
            return False
        d = load_pay()
        d["holder"] = text[:80]
        save_pay(d)
        send_message(token, chat_id, u"✅ به نام: <b>%s</b>" % text[:80], kb_admin_pay())
        return True
    if kind.startswith("amt_") or kind.startswith("day_") or kind.startswith("ttl_"):
        pid = kind.split("_", 1)[1]
        plans = load_plans()
        if pid not in plans:
            send_message(token, chat_id, u"پلن پیدا نشد.", kb_admin_pay())
            return False
        if kind.startswith("amt_"):
            digits = "".join(ch for ch in text if ch.isdigit())
            if not digits:
                send_message(token, chat_id, u"مبلغ را به تومان، فقط عدد بفرست.", kb_admin_pay())
                return False
            plans[pid]["amount"] = int(digits)
            save_plans(plans)
            send_message(
                token,
                chat_id,
                u"✅ مبلغ %s: %s" % (plans[pid].get("title"), fa_money(digits)),
                kb_admin_pay(),
            )
            return True
        if kind.startswith("day_"):
            digits = "".join(ch for ch in text if ch.isdigit())
            if not digits or int(digits) < 1:
                send_message(token, chat_id, u"تعداد روز را عدد بفرست.", kb_admin_pay())
                return False
            plans[pid]["days"] = int(digits)
            save_plans(plans)
            send_message(
                token,
                chat_id,
                u"✅ مدت %s: %s روز" % (plans[pid].get("title"), fa_num(digits)),
                kb_admin_pay(),
            )
            return True
        plans[pid]["title"] = text[:40]
        save_plans(plans)
        send_message(token, chat_id, u"✅ عنوان: %s" % text[:40], kb_admin_pay())
        return True
    return False


def approve_receipt(token, uid, pid):
    p = load_plans().get(pid) or {"days": 30, "title": pid}
    days = int(p.get("days") or 30)
    until = grant_sub(uid, days, pid)
    unban_vip(token, uid)
    send_message(
        token,
        uid,
        u"✅ پرداختت تایید شد.\nاشتراک <b>%s</b> تا %s فعال است.\nکانال VIP: %s"
        % (p.get("title") or pid, tehran_fmt(until), PRO_URL),
        kb_main(uid),
    )
    send_message(
        token,
        OWNER_ID,
        u"✅ %s فعال شد تا %s" % (uid, tehran_fmt(until)),
        kb_admin(),
    )
    rcps = load_rcps()
    rcps.pop(str(uid), None)
    save_rcps(rcps)
    pop_wait(uid)


def reject_receipt(token, uid):
    send_message(
        token,
        uid,
        u"❌ رسید تایید نشد. اگر واریز کردی دوباره عکس واضح بفرست یا به ادمین پیام بده.",
        kb_pay(),
    )
    send_message(token, OWNER_ID, u"رد شد %s" % uid, kb_admin())
    rcps = load_rcps()
    rcps.pop(str(uid), None)
    save_rcps(rcps)
    pop_wait(uid)


def handle_receipt_photo(token, user_id, chat_id, msg):
    photos = msg.get("photo") or []
    doc = msg.get("document") or {}
    file_id = None
    if photos:
        file_id = photos[-1].get("file_id")
    elif str(doc.get("mime_type") or "").startswith("image/"):
        file_id = doc.get("file_id")
    if not file_id:
        return False
    w = get_wait(user_id)
    if (w.get("kind") or "") != "receipt":
        return False
    pid = w.get("pid") or "m1"
    p = load_plans().get(pid) or {}
    from_user = msg.get("from") or {}
    name = " ".join(
        [
            from_user.get("first_name") or "",
            from_user.get("last_name") or "",
        ]
    ).strip()
    uname = from_user.get("username") or "-"
    cap = (
        u"📥 <b>رسید پرداخت</b>\n"
        u"────────────\n"
        u"کاربر: %s\n"
        u"آیدی: <code>%s</code>\n"
        u"یوزرنیم: @%s\n"
        u"پلن: <b>%s</b> · %s روز · %s\n"
        u"زمان: %s"
        % (
            name or "-",
            user_id,
            uname,
            p.get("title") or pid,
            fa_num(p.get("days") or 0),
            fa_money(p.get("amount") or 0),
            tehran_fmt(),
        )
    )
    kb = {
        "inline_keyboard": [
            [
                btn(u"✅ تایید", "okp_%s_%s" % (user_id, pid), style="success"),
                btn(u"❌ رد", "nop_%s" % user_id, style="danger"),
            ]
        ]
    }
    send_photo_id(token, OWNER_ID, file_id, cap, kb)
    rcps = load_rcps()
    rcps[str(user_id)] = {
        "pid": pid,
        "file_id": file_id,
        "ts": time.time(),
        "name": name,
    }
    save_rcps(rcps)
    send_message(
        token,
        chat_id,
        u"رسید رفت برای بررسی.\nبعد از تایید، اشتراک خودکار فعال می‌شود.",
        kb_main(user_id),
    )
    return True


def handle_start_payload(token, user_id, chat_id, payload):
    payload = (payload or "").strip().lower()
    if payload in ("app", "mini", "web"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_start(), kb_main(user_id))
        return
    if payload in ("learn", "edu"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, edu_intro(), kb_edu())
        return
    if payload in ("sub", "vip", "pay"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_paywall(user_id), kb_pay())
        return
    if payload in ("wr", "win", "winrate"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, wr_text(), kb_wr())
        return
    if payload in ("support", "sup", "helpdesk"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        start_support(token, user_id, chat_id)
        return
    if not gate(token, user_id, chat_id):
        return
    if payload in ("signal", "all", "sig"):
        deliver_all(token, chat_id)
        return
    if payload in ("crypto", "btc", "btcusdt"):
        deliver_one(token, chat_id, "BTCUSDT")
        return
    if payload in ("eth", "ethusdt"):
        deliver_one(token, chat_id, "ETHUSDT")
        return
    if payload in ("sol", "solusdt"):
        deliver_one(token, chat_id, "SOLUSDT")
        return
    if payload in ("desk", "radar"):
        send_message(token, chat_id, txt_desk_intro(), kb_desk())
        return
    if payload in ("eur", "eurusd"):
        deliver_one(token, chat_id, "EURUSD")
        return
    if payload in ("gbp", "gbpusd"):
        deliver_one(token, chat_id, "GBPUSD")
        return
    if payload in ("gold", "xau", "xauusd"):
        deliver_one(token, chat_id, "XAUUSD")
        return
    if payload in ("brief", "summary"):
        briefing(token, chat_id)
        return
    if payload in ("trade", "trd", "info"):
        start_trade_wizard(token, user_id, chat_id)
        return
    if payload.startswith("tr_") or payload.startswith("trade_"):
        p = payload.split("_", 1)[-1].upper()
        if p in ("XAU", "GOLD"):
            p = "XAUUSD"
        if p in PAIRS:
            start_trade_wizard(token, user_id, chat_id, p)
            return
        start_trade_wizard(token, user_id, chat_id)
        return
    send_message(token, chat_id, txt_start(), kb_main(user_id))


def handle_user(token, user_id, chat_id, cmd, payload=""):
    cmd = (cmd or "").lower()
    if cmd in ("/admin", "admin") and is_owner(user_id):
        send_message(token, chat_id, admin_stats_text(), kb_admin())
        return
    if cmd in ("/live", "live"):
        if not gate(token, user_id, chat_id):
            return
        send_message(token, chat_id, live_positions_text(chat_id), kb_after())
        return
    if cmd in ("/wr", "/winrate", "wr", "winrate") or cmd == u"وینریت" or cmd == u"وین‌ریت":
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, wr_text(), kb_wr())
        return
    if cmd in ("/watch", "watch"):
        if not gate(token, user_id, chat_id):
            return
        pl = (payload or "").strip().lower()
        if pl in ("off", "stop", "0"):
            watch_off(user_id)
            send_message(token, chat_id, u"👀 خبررسان خاموش شد.", kb_after())
            return
        watch_add(user_id, "ALL")
        send_message(
            token,
            chat_id,
            u"👀 خبررسان روشن شد. ستاپ کامل ICT را همین‌جا می‌فرستم.",
            kb_after(),
        )
        return
    if cmd in ("/me", "me", u"اشتراک"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(
            token,
            chat_id,
            txt_me(user_id),
            kb_main(user_id) if is_pro(user_id) else kb_pay(),
        )
        return
    if cmd in ("/support", "support") or cmd == u"پشتیبانی":
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        start_support(token, user_id, chat_id)
        return
    if cmd in ("/forget", "forget", u"فراموشی"):
        wipe_user_mem(user_id)
        send_message(
            token,
            chat_id,
            u"🧹 حافظه مربی مخصوص تو پاک شد.\nاز این به بعد از صفر می‌شناسیمت — مال بقیه دست نمی‌خورد.",
            kb_after(),
        )
        return
    if cmd in ("/trade", "trade") or cmd == u"معامله":
        if not gate(token, user_id, chat_id):
            return
        start_trade_wizard(token, user_id, chat_id)
        return
    if cmd in ("/debug",) and is_owner(user_id):
        try:
            tail = open(LOG_FILE).read()[-2500:]
        except Exception:
            tail = "-"
        send_message(
            token,
            chat_id,
            "v=%s\n%s" % (BOT_VERSION, (tail or "-")[-1800:]),
            kb_admin(),
            parse_mode=None,
        )
        return
    if cmd in ("/connect", "connect") or cmd == u"اتصال":
        if not is_owner(user_id):
            send_message(token, chat_id, u"اتصال صرافی/بروکر فقط برای مالک است.", kb_after())
            return
        try:
            send_message(token, chat_id, txt_connect(), kb_connect())
        except Exception:
            log("connect cmd " + traceback.format_exc())
            send_message(token, chat_id, u"اتصال", kb_connect(), parse_mode=None)
        return
    if cmd in ("/paper", "paper") or cmd == u"پیپر":
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        if not (is_owner(user_id) or is_pro(user_id)):
            send_message(token, chat_id, txt_paywall(user_id), kb_pay())
            return
        send_message(token, chat_id, paper_status_text(user_id), kb_paper(user_id))
        return
    if cmd in ("/crypto", "crypto") or cmd == u"کریپتو":
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_crypto_intro(), kb_crypto())
        return
    if cmd in ("/desk", "desk") or cmd == u"میز":
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_desk_intro(), kb_desk())
        return
    if cmd in ("/radar", "radar"):
        if not gate(token, user_id, chat_id):
            return
        send_message(token, chat_id, radar_card(FX_PAIRS), kb_desk())
        return
    if cmd in ("/session", "session"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, session_card_text(), kb_desk())
        return
    if cmd in ("/bias", "bias"):
        if not gate(token, user_id, chat_id):
            return
        send_message(token, chat_id, bias_card_text(), kb_desk())
        return
    if cmd in ("/journal", "journal"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, journal_card_text(user_id), kb_desk())
        return
    if cmd in ("/pulse", "pulse"):
        if not gate(token, user_id, chat_id):
            return
        send_message(token, chat_id, pulse_text(), kb_desk())
        return
    if cmd in ("/grant",) and is_owner(user_id):
        parts = (payload or "").split()
        if len(parts) >= 2:
            try:
                uid, days = int(parts[0]), int(parts[1])
                until = grant_sub(uid, days, "admin")
                try:
                    http().post(
                        tg_api(token) + "/unbanChatMember",
                        json={
                            "chat_id": PRO_CHANNEL_ID,
                            "user_id": uid,
                            "only_if_banned": True,
                        },
                        timeout=8,
                    )
                except Exception:
                    pass
                send_message(
                    token,
                    chat_id,
                    "✅ %s تا %s تهران" % (uid, tehran_fmt(until)),
                    kb_admin(),
                )
                send_message(
                    token,
                    uid,
                    "✅ اشتراک %s روزه فعال شد. کانال VIP: %s" % (days, PRO_URL),
                    kb_main(uid),
                )
            except Exception:
                send_message(token, chat_id, "فرمت: /grant آیدی روز", kb_admin())
        else:
            send_message(token, chat_id, "فرمت: /grant آیدی روز", kb_admin())
        return
    if cmd in ("/revoke",) and is_owner(user_id):
        try:
            uid = int((payload or "").split()[0])
            revoke_sub(uid)
            send_message(token, chat_id, "لغو شد %s" % uid, kb_admin())
        except Exception:
            send_message(token, chat_id, "فرمت: /revoke آیدی", kb_admin())
        return
    if cmd in ("/say",) and is_owner(user_id):
        text = payload or ""
        n = 0
        for k in list(load_users().keys())[:400]:
            try:
                if send_message(token, int(k), text, kb_main(int(k))):
                    n += 1
            except Exception:
                pass
        send_message(token, chat_id, "ارسال شد به %s نفر" % n, kb_admin())
        return
    if cmd in ("/card",) and is_owner(user_id):
        if payload:
            pop_wait(user_id)
            apply_admin_setting(token, chat_id, "card", payload)
        else:
            set_wait(user_id, "card")
            send_message(token, chat_id, u"شماره کارت را بفرست.", kb_admin_pay())
        return
    if cmd in ("/holder",) and is_owner(user_id):
        if payload:
            pop_wait(user_id)
            apply_admin_setting(token, chat_id, "holder", payload)
        else:
            set_wait(user_id, "holder")
            send_message(token, chat_id, u"نام صاحب کارت را بفرست.", kb_admin_pay())
        return
    if cmd in ("/price",) and is_owner(user_id):
        parts = (payload or "").split()
        if len(parts) >= 2:
            apply_admin_setting(token, chat_id, "amt_" + parts[0], parts[1])
        else:
            send_message(token, chat_id, u"فرمت: /price m1 900000", kb_admin_pay())
        return
    if cmd in ("/days",) and is_owner(user_id):
        parts = (payload or "").split()
        if len(parts) >= 2:
            apply_admin_setting(token, chat_id, "day_" + parts[0], parts[1])
        else:
            send_message(token, chat_id, u"فرمت: /days m1 30", kb_admin_pay())
        return
    if cmd in ("/title",) and is_owner(user_id):
        parts = (payload or "").split(None, 1)
        if len(parts) >= 2:
            apply_admin_setting(token, chat_id, "ttl_" + parts[0], parts[1])
        else:
            send_message(token, chat_id, u"فرمت: /title m1 سی روزه", kb_admin_pay())
        return
    if cmd in ("/start", "start"):
        w0 = get_wait(user_id)
        if (w0.get("kind") or "") in ("edu_chat", "support", "sup_reply"):
            pop_wait(user_id)
        if payload:
            handle_start_payload(token, user_id, chat_id, payload)
            return
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_start(), kb_main(user_id))
        if not is_pro(user_id):
            send_message(token, chat_id, txt_paywall(user_id), kb_pay())
        return
    if cmd in ("/tools", "tools", u"ابزار"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, tz_head(T("head.tools")) + T("txt.tools") + u"\n" + tz_foot(), kb_tools())
        return
    if cmd in ("/donate", "donate", u"حمایت", "/supporttz"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(
            token,
            chat_id,
            tz_head(T("head.donate")) + T("txt.donate") + u"\n" + tz_foot(),
            kb_main(user_id),
        )
        return
    if cmd in ("/lang", "lang", u"زبان", "/language", "language"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        cur = get_lang(user_id)
        nxt = "en" if cur != "en" else "fa"
        set_lang(user_id, nxt)
        use_lang(user_id)
        send_message(token, chat_id, T("txt.lang_set_en") if nxt == "en" else T("txt.lang_set_fa"), kb_main(user_id))
        return
    if cmd in ("/help", "help", "راهنما"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_help(), kb_main(user_id))
        return
    if cmd in ("/learn", "آموزش", "edu"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, edu_intro(), kb_edu())
        return
    if cmd in ("/signal", "signal", "سیگنال"):
        if not gate(token, user_id, chat_id):
            return
        deliver_all(token, chat_id)
        return
    if cmd in ("/brief", "خلاصه", "بازار"):
        if not gate(token, user_id, chat_id):
            return
        briefing(token, chat_id)
        return
    if cmd in ("/chat", "چت"):
        if not gate(token, user_id, chat_id):
            return
        send_message(
            token,
            chat_id,
            "💬 هرچی بپرسی جواب می‌دم — ICT، سیگنال، روانشناسی ترید، مدیریت سرمایه.\nهمین‌جا بنویس.",
            kb_after(),
        )
        return
    if not gate(token, user_id, chat_id):
        return
    send_message(token, chat_id, "از دکمه‌ها استفاده کن 👇", kb_main(user_id))


def save_group(chat):
    try:
        if (chat or {}).get("type") not in ("group", "supergroup"):
            return
        with open(GROUP_FILE, "w") as f:
            json.dump({"id": chat.get("id"), "title": chat.get("title")}, f)
    except Exception:
        pass


def handle_group(token, msg):
    chat = msg.get("chat") or {}
    chat_id = chat.get("id")
    save_group(chat)
    # Channel posts auto-forwarded into discussion — never reply to those
    if msg.get("is_automatic_forward"):
        return
    if (msg.get("sender_chat") or {}).get("type") == "channel":
        return
    text = (msg.get("text") or "").strip()
    if msg.get("new_chat_members"):
        send_message(
            token,
            chat_id,
            "👋 خوش اومدی به <b>TZ FX</b>\nسیگنال کامل داخل ربات با اشتراک است.",
            kb_open_bot("signal"),
        )
        return
    if not text:
        return
    low = text.lower()
    mentioned = BOT_USER.lower() in low
    ask = any(
        k in low
        for k in ("سیگنال", "/signal", "/start", "آموزش", "ربات", "حد ضرر", "حد سود")
    )
    reply_from = ((msg.get("reply_to_message") or {}).get("from") or {}).get("username") or ""
    uid = (msg.get("from") or {}).get("id")
    mid = msg.get("message_id")
    talk = mentioned or (reply_from.lower() == BOT_USER.lower())
    if talk and not text.startswith("/"):
        ai_chat(token, uid, chat_id, text, short=True, reply_to=mid)
        return
    if mentioned or text.startswith("/") or ask:
        send_message(
            token,
            chat_id,
            "💬 سوالت را گرفتم.\nجزئیات سیگنال و آموزش داخل <b>ربات خصوصی</b> است تا گروه شلوغ نشود.",
            kb_open_bot("signal"),
            reply_to=mid,
        )



def load_sup():
    d = _jload(SUP_FILE, {"map": {}, "inbox": [], "open": {}})
    if not isinstance(d, dict):
        d = {}
    d.setdefault("map", {})
    d.setdefault("inbox", [])
    d.setdefault("open", {})
    return d


def save_sup(d):
    _jsave(SUP_FILE, d)


def kb_support_user():
    return {
        "inline_keyboard": [
            [btn(u"🛑 بستن پشتیبانی", "sup_off")],
            [btn(u"🏠 منو", "home", style="primary")],
        ]
    }


def kb_support_owner(uid):
    return {
        "inline_keyboard": [
            [
                btn(u"✉️ پاسخ", "sr_%s" % uid, style="success"),
                btn(u"✅ بستن", "sx_%s" % uid),
            ]
        ]
    }


def start_support(token, user_id, chat_id):
    set_wait(user_id, "support")
    ui_desk_off()
    rec = load_user_mem(user_id)
    name = rec.get("name") or u"رفیق"
    send_message(
        token,
        chat_id,
        tz_head(u"🛟 پشتیبانی")
        + u"سلام %s، پیامت مستقیم می‌رسد به پشتیبانی TZ FX.\n"
        u"متن، عکس یا ویس بفرست.\nبرگشت: /start"
        % name,
        kb_support_user(),
    )


def _sup_map(mid, uid):
    if not mid or not uid:
        return
    d = load_sup()
    mp = d.get("map") or {}
    mp[str(mid)] = int(uid)
    if len(mp) > 400:
        keys = list(mp.keys())[-300:]
        mp = dict((k, mp[k]) for k in keys)
    d["map"] = mp
    save_sup(d)


def _sup_log(uid, text, kind="text"):
    d = load_sup()
    d["open"][str(uid)] = True
    box = list(d.get("inbox") or [])
    box.append(
        {
            "uid": int(uid),
            "ts": time.time(),
            "kind": kind,
            "text": (text or "")[:400],
            "status": "open",
        }
    )
    d["inbox"] = box[-80:]
    save_sup(d)


def tg_copy(token, to_chat, from_chat, mid):
    try:
        r = http().post(
            tg_api(token) + "/copyMessage",
            json={
                "chat_id": to_chat,
                "from_chat_id": from_chat,
                "message_id": int(mid),
            },
            timeout=12,
        )
        js = r.json() or {}
        if js.get("ok"):
            return (js.get("result") or {}).get("message_id")
    except Exception:
        log("copy " + traceback.format_exc())
    return None


def relay_support(token, user_id, chat_id, msg):
    rec = load_user_mem(user_id)
    name = rec.get("name") or ((msg.get("from") or {}).get("first_name") or u"کاربر")
    flag = u"VIP" if is_pro(user_id) else u"رایگان"
    raw = (msg.get("text") or msg.get("caption") or "").strip()
    head = (
        u"🛟 <b>پشتیبانی</b>\n"
        u"از: %s\n"
        u"آیدی: <code>%s</code> · %s\n"
        u"%s تهران"
        % (name, user_id, flag, tehran_fmt())
    )
    if raw:
        head += u"\n\n" + strip_html(raw)[:1600]
    mid_h = send_message(token, OWNER_ID, head, kb_support_owner(user_id))
    if mid_h and mid_h is not True:
        _sup_map(mid_h, user_id)
    src_mid = msg.get("message_id")
    if src_mid:
        cmid = tg_copy(token, OWNER_ID, chat_id, src_mid)
        if cmid:
            _sup_map(cmid, user_id)
    kind = "text"
    if msg.get("photo"):
        kind = "photo"
    elif msg.get("voice") or msg.get("audio"):
        kind = "voice"
    _sup_log(user_id, raw, kind)
    send_message(
        token,
        chat_id,
        u"✅ رسید. پشتیبانی جواب می‌دهد همین‌جا.",
        kb_support_user(),
    )


def deliver_support_reply(token, uid, msg, text=""):
    uid = int(uid)
    src_mid = msg.get("message_id")
    chat_id = (msg.get("chat") or {}).get("id")
    ok = False
    if src_mid and chat_id:
        cmid = tg_copy(token, uid, chat_id, src_mid)
        ok = bool(cmid)
    if not ok:
        body = u"🛟 <b>پاسخ پشتیبانی</b>\n" + strip_html(text or u"")[:1800]
        ok = bool(send_message(token, uid, body, kb_support_user()))
    if ok:
        send_message(token, OWNER_ID, u"✅ جواب برای <code>%s</code> ارسال شد." % uid, kb_admin())
        d = load_sup()
        d["open"][str(uid)] = True
        save_sup(d)
    else:
        send_message(token, OWNER_ID, u"ارسال به %s نشد." % uid, kb_admin())
    return ok


def handle_owner_support_out(token, user_id, chat_id, msg, text=""):
    if not is_owner(user_id):
        return False
    wk = get_wait(user_id).get("kind") or ""
    if wk in ("card", "holder") or wk.startswith("amt_") or wk.startswith("day_") or wk.startswith("ttl_"):
        return False
    rt = msg.get("reply_to_message") or {}
    rmid = rt.get("message_id")
    d = load_sup()
    tid = None
    if rmid:
        tid = (d.get("map") or {}).get(str(rmid))
    if not tid and wk == "sup_reply":
        try:
            tid = int(get_wait(user_id).get("uid") or 0)
        except Exception:
            tid = 0
    if not tid:
        return False
    deliver_support_reply(token, int(tid), msg, text)
    return True


def admin_support_inbox(token, chat_id):
    d = load_sup()
    box = list(d.get("inbox") or [])
    box.reverse()
    lines = [u"🛟 <b>صندوق پشتیبانی</b>"]
    if not box:
        lines.append(u"خالی است.")
    for it in box[:18]:
        st = u"باز" if (d.get("open") or {}).get(str(it.get("uid"))) else u"—"
        lines.append(
            u"<code>%s</code> · %s · %s\n%s"
            % (
                it.get("uid"),
                tehran_fmt(it.get("ts")),
                st,
                strip_html(it.get("text") or it.get("kind") or "")[:80],
            )
        )
    send_message(token, chat_id, "\n".join(lines), kb_admin())


def handle_message(token, msg):
    chat = msg.get("chat") or {}
    ctype = chat.get("type") or ""
    if msg.get("successful_payment"):
        handle_payment(token, msg)
        return
    if ctype in ("group", "supergroup"):
        handle_group(token, msg)
        return
    chat_id = chat.get("id")
    user_id = (msg.get("from") or {}).get("id")
    if not chat_id or not user_id:
        log("msg drop no-id type=%s" % ctype)
        return
    if ctype == "private":
        try:
            http().post(
                tg_api(token) + "/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"},
                timeout=4,
            )
        except Exception:
            pass
    try:
        use_lang(user_id, msg.get("from"))
    except Exception:
        pass
    try:
        nm = (msg.get("from") or {}).get("first_name") or ""
        mem_touch(user_id, name=nm)
    except Exception:
        pass
    if ctype == "private":
        raw_txt = (msg.get("text") or "")
        if raw_txt.startswith("/"):
            delete_message(token, chat_id, msg.get("message_id"))
        try:
            rec = load_user_mem(user_id)
            ui_desk(chat_id, rec.get("desk_mid"))
        except Exception:
            ui_desk(chat_id, None)
    npe = 0
    try:
        npe = harvest_pe(msg)
    except Exception:
        npe = 0
    text = (msg.get("text") or "").strip()
    try:
        _wk = ""
        try:
            _wk = (get_wait(user_id).get("kind") or "")
        except Exception:
            _wk = ""
        _safe_t = "-" if str(_wk).startswith("exch_") else (text or "")[:80]
        log(
            "msg type=%s uid=%s voice=%s photo=%s t=%s"
            % (
                ctype,
                user_id,
                bool(msg.get("voice") or msg.get("audio")),
                bool(msg.get("photo")),
                _safe_t,
            )
        )
    except Exception:
        pass
    ents_pe = [e for e in (msg.get("entities") or []) if e.get("type") == "custom_emoji"]
    if ents_pe:
        try:
            send_pe_echo(token, chat_id, msg)
        except Exception:
            log("pe echo call " + traceback.format_exc())
        letters = sum(1 for c in text if c.isalnum())
        if letters < 3 and not text.startswith("/"):
            return
    want_voice = False
    if msg.get("photo") or (
        (msg.get("document") or {}).get("mime_type") or ""
    ).startswith("image/"):
        if handle_receipt_photo(token, user_id, chat_id, msg):
            return
        if get_wait(user_id).get("kind") == "receipt":
            send_message(token, chat_id, u"عکس نرسید. دوباره عکس رسید را بفرست.", kb_pay())
            return
    wsup = get_wait(user_id)
    raw_sup = (msg.get("text") or msg.get("caption") or "").strip()
    if wsup.get("kind") == "support":
        if raw_sup.startswith("/"):
            pass
        elif (
            msg.get("photo")
            or msg.get("voice")
            or msg.get("audio")
            or msg.get("document")
            or raw_sup
        ):
            relay_support(token, user_id, chat_id, msg)
            return
    if is_owner(user_id) and handle_owner_support_out(token, user_id, chat_id, msg, raw_sup):
        return
    if (msg.get("voice") or msg.get("audio")) and not text:
        if get_wait(user_id).get("kind") == "receipt":
            send_message(token, chat_id, u"برای رسید عکس بفرست، نه ویس.", kb_pay())
            return
        text = ingest_voice(token, user_id, chat_id, msg) or ""
        if not text:
            return
        want_voice = True
        try:
            mem_touch(user_id, voice=True)
        except Exception:
            pass
    if is_owner(user_id):
        ch = msg.get("forward_from_chat")
        if not ch:
            fo = msg.get("forward_origin") or {}
            if fo.get("type") == "channel":
                ch = fo.get("chat")
        if ch and ch.get("type") == "channel":
            if bind_crypto_channel(ch):
                send_message(
                    token,
                    chat_id,
                    u"✅ کانال کریپتو ثبت شد: <b>%s</b>\n<code>%s</code>"
                    % (ch.get("title") or "", ch.get("id")),
                    kb_crypto(),
                )
                return
    if not text:
        return
    parts = text.split()
    raw = parts[0].split("@")[0]
    cmd = raw.lower()
    payload = " ".join(parts[1:]) if len(parts) > 1 else ""
    mid = msg.get("message_id")
    w = get_wait(user_id)
    if w and not text.startswith("/") and is_owner(user_id):
        kind = w.get("kind") or ""
        if kind in ("card", "holder") or kind.startswith("amt_") or kind.startswith("day_") or kind.startswith("ttl_"):
            pop_wait(user_id)
            apply_admin_setting(token, chat_id, kind, text)
            return
    if w.get("kind") == "trade" and not text.startswith("/"):
        handle_trade_text(token, user_id, chat_id, text)
        return
    if w.get("kind") == "edu_chat" and not text.startswith("/"):
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        ai_chat(token, user_id, chat_id, text, reply_to=mid, speak=want_voice)
        return
    if w.get("kind") == "receipt" and not text.startswith("/"):
        send_message(
            token,
            chat_id,
            u"برای این پلن باید <b>عکس رسید</b> بفرستی، نه متن.",
            kb_pay(),
        )
        return
    if handle_exch_wait(token, user_id, chat_id, text, mid):
        return
    if (get_wait(user_id).get("kind") or "") == "exch_livearm" and not text.startswith("/"):
        if is_owner(user_id) and (text or "").strip() == "LIVE":
            pop_wait(user_id)
            lx = _live_mod()
            cfg = lx.load_cfg()
            cfg["demo"] = False
            lx.save_cfg(cfg)
            send_message(token, chat_id, u"حالت واقعی روشن شد. حد ضرر اجباری.", kb_connect())
        else:
            pop_wait(user_id)
            send_message(token, chat_id, u"دمو ماند.", kb_connect())
        return
    if w.get("kind") == "crypto_find" and not text.startswith("/"):
        pop_wait(user_id)
        handle_crypto_query(token, user_id, chat_id, text, reply_to=mid)
        return
    if (not text.startswith("/")) and looks_like_crypto_query(text):
        handle_crypto_query(token, user_id, chat_id, text, reply_to=mid)
        return
    if cmd == "/start":
        handle_user(token, user_id, chat_id, "/start", payload)
        return
    if is_owner(user_id) and (
        cmd == "/pe"
        or "addemoji/" in (text or "").lower()
        or (text or "").lower().startswith("https://t.me/addemoji")
    ):
        name = payload or text
        n = 0
        if "addemoji" in (name or "").lower():
            n = ingest_pe_pack(token, name)
        send_message(
            token,
            chat_id,
            u"🎨 ایموجی پریمیوم ذخیره‌شده: <b>%s</b>\n"
            u"پک جدید: %s تا.\n"
            u"یک پیام با ایموجی پریمیوم بفرست، یا لینک t.me/addemoji/... را بده."
            % (len(_pe_map), n),
            kb_admin(),
        )
        return
    low = text.strip().lower()
    if text.startswith("/"):
        handle_user(token, user_id, chat_id, cmd, payload)
        return
    if low in (u"سیگنال", u"آموزش", u"خلاصه", u"بازار", u"راهنما", "help", u"چت", u"معامله", u"وینریت", u"وین‌ریت", u"پشتیبانی"):
        handle_user(token, user_id, chat_id, low)
        return
    if not gate(token, user_id, chat_id, need_pro=False):
        return
    ai_chat(token, user_id, chat_id, text, reply_to=mid, speak=want_voice)


def handle_callback(token, cq):
    user_id = (cq.get("from") or {}).get("id")
    msg = cq.get("message") or {}
    chat = msg.get("chat") or {}
    chat_id = chat.get("id")
    data = cq.get("data") or ""
    cq_id = cq.get("id")
    try:
        use_lang(user_id, cq.get("from"))
    except Exception:
        pass
    if (chat.get("type") or "") == "private":
        ui_desk(chat_id, msg.get("message_id"))
    try:
        log("cb uid=%s data=%s ctype=%s" % (user_id, (data or "")[:40], chat.get("type")))
    except Exception:
        pass
    # Old channel buttons must never reply inside the channel
    if chat.get("type") == "channel":
        start = "signal"
        if data == "sig_EURUSD":
            start = "eur"
        elif data == "sig_GBPUSD":
            start = "gbp"
        elif data == "sig_XAUUSD":
            start = "gold"
        elif data == "edu_menu" or (data or "").startswith("edu"):
            start = "learn"
        elif data == "brief":
            start = "brief"
        elif data in ("trade_info",) or (data or "").startswith("trd_"):
            start = "trade"
        elif data == "support" or (data or "").startswith("sr_") or (data or "").startswith("sx_"):
            start = "support"
        answer_callback(token, cq_id, url=BOT_URL + "?start=" + start)
        return

    if data == "check_join":
        if in_channel(token, user_id):
            answer_callback(token, cq_id, "عضو شدی ✅")
            send_message(token, chat_id, txt_start(), kb_main(user_id))
            if not is_pro(user_id):
                send_message(token, chat_id, txt_paywall(user_id), kb_pay())
        else:
            answer_callback(token, cq_id, "هنوز عضو نیستی")
            send_message(token, chat_id, txt_join(), kb_join())
        return

    if data.startswith("okp_") and is_owner(user_id):
        parts = data.split("_")
        if len(parts) >= 3:
            try:
                uid = int(parts[1])
            except Exception:
                uid = 0
            pid = parts[2]
            answer_callback(token, cq_id, u"تایید شد")
            if uid:
                approve_receipt(token, uid, pid)
        else:
            answer_callback(token, cq_id)
        return
    if data.startswith("nop_") and is_owner(user_id):
        try:
            uid = int(data.split("_", 1)[1])
        except Exception:
            uid = 0
        answer_callback(token, cq_id, u"رد شد")
        if uid:
            reject_receipt(token, uid)
        return

    if data == "donate":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(
            token,
            chat_id,
            tz_head(T("head.donate")) + T("txt.donate") + u"\n" + tz_foot(),
            kb_main(user_id),
        )
        return
    if data == "support":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        start_support(token, user_id, chat_id)
        return
    if data == "sup_off":
        answer_callback(token, cq_id, u"بسته شد")
        pop_wait(user_id)
        send_message(token, chat_id, u"پشتیبانی بسته شد. هر وقت خواستی دوباره دکمه را بزن.", kb_main(user_id))
        return
    if data.startswith("sr_") and is_owner(user_id):
        answer_callback(token, cq_id)
        try:
            uid = int(data.split("_", 1)[1])
        except Exception:
            uid = 0
        if uid:
            set_wait(user_id, "sup_reply", {"uid": uid})
            send_message(
                token,
                chat_id,
                u"جواب برای <code>%s</code> را بنویس، عکس یا ویس بفرست.\nریپلای همین پیام هم کافی است."
                % uid,
                kb_admin(),
            )
        return
    if data.startswith("sx_") and is_owner(user_id):
        answer_callback(token, cq_id, u"بسته شد")
        try:
            uid = int(data.split("_", 1)[1])
        except Exception:
            uid = 0
        d = load_sup()
        if uid:
            d["open"][str(uid)] = False
            save_sup(d)
            try:
                send_message(token, uid, u"این گفتگوی پشتیبانی بسته شد.", kb_main(uid))
            except Exception:
                pass
        send_message(token, chat_id, u"بسته شد.", kb_admin())
        return
    if data == "ad_sup" and is_owner(user_id):
        answer_callback(token, cq_id)
        admin_support_inbox(token, chat_id)
        return

    if data == "my_sub":
        answer_callback(token, cq_id)
        send_message(
            token,
            chat_id,
            txt_me(user_id),
            kb_main(user_id) if is_pro(user_id) else kb_pay(),
        )
        return

    if data == "sub_me" or data.startswith("buy_"):
        if not in_channel(token, user_id):
            answer_callback(token, cq_id, u"اول کانال رایگان را عضو شو")
            send_message(token, chat_id, txt_join(), kb_join())
            return
        if data == "sub_me":
            answer_callback(token, cq_id)
            send_message(token, chat_id, txt_paywall(user_id), kb_pay())
            return
        pid = data.split("_", 1)[1]
        answer_callback(token, cq_id)
        set_wait(user_id, "receipt", {"pid": pid})
        send_message(token, chat_id, txt_invoice(user_id, pid), kb_pay())
        return

    if data.startswith("ad_") and is_owner(user_id):
        answer_callback(token, cq_id)
        if data == "ad_stat":
            send_message(token, chat_id, admin_stats_text(), kb_admin())
        elif data == "ad_users":
            users = load_users()
            lines = ["👥 <b>آخرین کاربران</b>"]
            items = sorted(
                users.items(),
                key=lambda kv: (kv[1] or {}).get("seen") or 0,
                reverse=True,
            )[:25]
            for k, v in items:
                lines.append(
                    "<code>%s</code> · %s"
                    % (k, tehran_fmt((v or {}).get("seen")))
                )
            send_message(token, chat_id, "\n".join(lines), kb_admin())
        elif data == "ad_subs":
            subs = load_subs()
            now = time.time()
            lines = ["💎 <b>اشتراک‌ها</b>"]
            n = 0
            for k, v in sorted(subs.items(), key=lambda kv: -float((kv[1] or {}).get("until") or 0)):
                until = float((v or {}).get("until") or 0)
                if until <= now:
                    continue
                n += 1
                if n <= 30:
                    lines.append(
                        "<code>%s</code> تا %s · %s"
                        % (k, tehran_fmt(until), (v or {}).get("plan") or "")
                    )
            if n == 0:
                lines.append("فعالی نیست.")
            send_message(token, chat_id, "\n".join(lines), kb_admin())
        elif data == "ad_bc":
            send_message(
                token,
                chat_id,
                u"برای پیام همگانی بنویس:\n<code>/say متن</code>",
                kb_admin(),
            )
        elif data == "ad_pay":
            send_message(token, chat_id, admin_pay_text(), kb_admin_pay())
        elif data == "ad_rcp":
            rcps = load_rcps()
            if not rcps:
                send_message(token, chat_id, u"رسید بازی نیست.", kb_admin())
            else:
                lines = [u"📥 <b>رسیدهای باز</b>"]
                for k, v in list(rcps.items())[:20]:
                    lines.append(
                        u"<code>%s</code> · %s · %s"
                        % (
                            k,
                            (v or {}).get("pid") or "",
                            tehran_fmt((v or {}).get("ts")),
                        )
                    )
                send_message(token, chat_id, "\n".join(lines), kb_admin())
        elif data == "ad_setcard":
            set_wait(user_id, "card")
            send_message(token, chat_id, u"شماره کارت ۱۶ رقمی را بفرست.", kb_admin_pay())
        elif data == "ad_setholder":
            set_wait(user_id, "holder")
            send_message(token, chat_id, u"نام صاحب کارت را بفرست.", kb_admin_pay())
        elif data.startswith("ad_amt_"):
            pid = data[7:]
            set_wait(user_id, "amt_" + pid)
            send_message(
                token,
                chat_id,
                u"مبلغ پلن <code>%s</code> را به تومان، فقط عدد بفرست." % pid,
                kb_admin_pay(),
            )
        elif data.startswith("ad_day_"):
            pid = data[7:]
            set_wait(user_id, "day_" + pid)
            send_message(
                token,
                chat_id,
                u"مدت پلن <code>%s</code> چند روز باشد؟ عدد بفرست." % pid,
                kb_admin_pay(),
            )
        elif data.startswith("ad_ttl_"):
            pid = data[7:]
            set_wait(user_id, "ttl_" + pid)
            send_message(
                token,
                chat_id,
                u"عنوان پلن <code>%s</code> را بفرست." % pid,
                kb_admin_pay(),
            )
        return

    if data.startswith("edu") or data.startswith("eq_"):
        handle_edu_callback(token, user_id, chat_id, data, cq_id)
        return

    if data == "hear" or data.startswith("he_"):
        answer_callback(token, cq_id, u"دارم می‌خونم")
        if data == "hear":
            rec = load_user_mem(user_id)
            body = rec.get("last_ans") or ""
            if not body:
                send_message(token, chat_id, u"هنوز جوابی نیست که بخوانم. از مربی بپرس یا ویس بفرست.", kb_after())
                return
            try:
                ok = speak_text(token, chat_id, body, markup=kb_after(), caption="")
            except Exception:
                log("hear " + traceback.format_exc())
                ok = False
            if not ok:
                send_message(token, chat_id, strip_html(body)[:3500], kb_after(), parse_mode=None)
            return
        n = data[3:]
        key = "edu_" + n
        if key not in EDU:
            send_message(token, chat_id, u"درس پیدا نشد.", kb_edu())
            return
        cap = EDU_TITLE.get(key) or u"درس"
        kb = kb_lesson(key)
        raw = b""
        try:
            raw = load_edu_audio(key, fmt="ogg")
        except Exception:
            log("edu ogg " + traceback.format_exc())
        if raw and send_voice_note(token, chat_id, raw, caption=cap, markup=kb):
            return
        try:
            raw = load_edu_audio(key, fmt="mp3")
        except Exception:
            log("edu audio " + traceback.format_exc())
            raw = b""
        if raw and send_voice_note(token, chat_id, raw, caption=cap, markup=kb):
            return
        if raw and send_audio_mp3(token, chat_id, raw, caption=cap, markup=kb):
            return
        if raw:
            mime = "audio/ogg" if raw[:4] == b"OggS" else "audio/wav"
            name = "lesson.ogg" if mime == "audio/ogg" else "lesson.wav"
            if send_document_bytes(token, chat_id, raw, name, mime, caption=cap, markup=kb):
                return
        body = strip_html(EDU.get(key) or "")
        send_message(token, chat_id, body[:3500], kb, parse_mode=None)
        return

    if data == "lang_toggle":
        cur = get_lang(user_id)
        nxt = "en" if cur != "en" else "fa"
        set_lang(user_id, nxt)
        use_lang(user_id)
        answer_callback(token, cq_id, T("txt.lang_set_en") if nxt == "en" else T("txt.lang_set_fa"))
        send_message(token, chat_id, txt_start(), kb_main(user_id))
        return

    if data == "chat_ai":
        if not gate(token, user_id, chat_id, need_pro=False):
            answer_callback(token, cq_id, u"اول کانال را عضو شو")
            return
        answer_callback(token, cq_id)
        rec = load_user_mem(user_id)
        name = rec.get("name") or u"رفیق"
        fav = rec.get("pair") or u"یورو / پوند / طلا"
        topic = rec.get("topic") or "edu_0"
        set_wait(user_id, "edu_chat", {"lesson": topic})
        extra = u""
        if rec.get("summary") or rec.get("facts") or rec.get("notes"):
            extra = u"\nحرف‌های قبلی‌ات یادم هست — مال خودت است، با بقیه قاطی نمی‌شود."
        hello = (
            u"🎙️ سلام %s، مربی خودتم.\nنماد محبوب: <b>%s</b>%s\n\n"
            u"بنویس یا ویس فارسی بفرست — جواب متن و ویس است."
            % (name, fav, extra)
        )
        send_message(token, chat_id, hello, kb_after())
        try:
            speak_text(
                token,
                chat_id,
                u"سلام %s. مربی خودتی. فارسی بنویس یا ویس بفرست." % name,
                markup=kb_after(),
                caption="",
            )
        except Exception:
            log("coach hello speak " + traceback.format_exc())
        return

    if data == "home":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_start(), kb_main(user_id))
        return
    if data == "watch_on":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return
        watch_add(user_id, "ALL")
        answer_callback(token, cq_id, u"خبرت می‌کنم")
        send_message(
            token,
            chat_id,
            u"👀 فعال شد. هر وقت ستاپ ICT کامل شود همین‌جا خبرت می‌کنم.\nخاموش: /watch off",
            kb_after(),
        )
        return
    if data == "live_pos":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, u"اشتراک لازم است")
            return
        answer_callback(token, cq_id)
        send_message(token, chat_id, live_positions_text(chat_id), kb_after())
        return
    if data == "wr_menu":
        if not gate(token, user_id, chat_id, need_pro=False):
            answer_callback(token, cq_id)
            return
        answer_callback(token, cq_id)
        send_message(token, chat_id, wr_text(), kb_wr())
        return

    if data == "help":
        answer_callback(token, cq_id)
        if not gate(token, user_id, chat_id, need_pro=False):
            return
        send_message(token, chat_id, txt_help(), kb_main(user_id))
        return

    if data == "brief":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, "اشتراک لازم است")
            return
        answer_callback(token, cq_id, "خلاصه بازار...")
        briefing(token, chat_id)
        return

    if data == "risk_menu":
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, "اشتراک لازم است")
            return
        answer_callback(token, cq_id)
        send_message(
            token,
            chat_id,
            "💰 <b>حجم معامله با ۱٪ ریسک</b>\nحجم حساب را انتخاب کن:",
            kb_risk(),
        )
        return

    if data.startswith("risk_"):
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, "اشتراک لازم است")
            return
        try:
            bal = int(data.split("_")[1])
        except Exception:
            bal = 0
        answer_callback(token, cq_id)
        calc_risk(token, chat_id, bal)
        return

    if data in ("trade_info",) or data.startswith("trd_"):
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, "اشتراک لازم است")
            return
        answer_callback(token, cq_id)
        pair = None
        if data.startswith("trd_"):
            pair = data[4:]
            if pair not in PAIRS:
                pair = None
        start_trade_wizard(token, user_id, chat_id, pair)
        return

    if data.startswith("tb_") or data.startswith("ts_") or data.startswith("tk_") or data.startswith("tl_"):
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, "اشتراک لازم است")
            return
        answer_callback(token, cq_id)
        handle_trade_cb(token, user_id, chat_id, data)
        return

    if data.startswith("tf_"):
        if not in_channel(token, user_id):
            answer_callback(token, cq_id, "اول کانال را عضو شو")
            send_message(token, chat_id, txt_join(), kb_join())
            return
        rest = data[3:]
        if "_" not in rest:
            answer_callback(token, cq_id)
            return
        pair, code = rest.split("_", 1)
        if pair not in PAIRS:
            pair = ensure_crypto_pair(pair) or pair
        if pair not in PAIRS:
            answer_callback(token, cq_id)
            return
        answer_callback(token, cq_id, "تحلیل %s..." % code)
        deliver_one(token, chat_id, pair, tf=code)
        return

    if desk_handle_cb(token, user_id, chat_id, data, cq_id):
        return

    if data == "sig_ALL" or data.startswith("sig_"):
        if not gate(token, user_id, chat_id):
            answer_callback(token, cq_id, "اشتراک لازم است")
            return
        answer_callback(token, cq_id, "در حال تحلیل همه تایم‌فریم‌ها...")
        if data == "sig_ALL":
            deliver_all(token, chat_id)
        else:
            pair = data.split("_", 1)[1]
            if pair not in PAIRS:
                pair = ensure_crypto_pair(pair) or pair
            if pair in PAIRS:
                if is_crypto_pair(pair):
                    remember_crypto_watch(pair)
                deliver_one(token, chat_id, pair, tf="mtf")
        return

    answer_callback(token, cq_id)


def load_offset():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("offset")
    except Exception:
        return None


def save_offset(offset):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"offset": offset}, f)
    except Exception:
        pass


def load_posted():
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_posted(data):
    try:
        with open(POSTED_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def setup_id(sig):
    pair = sig["pair"]
    digits = PAIRS[pair]["digits"]
    fmt = "%." + str(digits) + "f"
    return "%s|%s|%s|%s" % (
        pair,
        sig["side"],
        fmt % float(sig.get("entry") or 0),
        fmt % float(sig.get("sl") or 0),
    )


def warm_cache():
    from concurrent.futures import ThreadPoolExecutor

    try:
        load_crypto_universe()
    except Exception:
        pass
    jobs = []
    for pair in list(FX_PAIRS) + list(CRYPTO_CORE):
        jobs.append((pair, "15m", "10d"))
        jobs.append((pair, "4h", "60d"))
        jobs.append((pair, "1d", "1y"))
    try:
        with ThreadPoolExecutor(max_workers=6) as ex:
            list(ex.map(lambda j: fetch_ohlc(*j), jobs))
    except Exception:
        pass


def _idea_id(sig):
    pair = sig.get("pair") or ""
    pip = (PAIRS.get(pair) or {}).get("pip") or 0.0001
    try:
        sl_q = int(round(float(sig.get("sl") or 0) / (pip * 5.0)))
    except Exception:
        sl_q = 0
    return "%s|%s|%s" % (pair, sig.get("side") or "", sl_q)


def _open_same(pair, side, chat_id):
    now = time.time()
    for t in load_trades():
        if t.get("status") != "open":
            continue
        if t.get("pair") != pair or t.get("side") != side:
            continue
        if str(t.get("chat_id")) != str(chat_id):
            continue
        try:
            age = now - float(t.get("ts") or 0)
        except Exception:
            age = 0
        if age < 2 * 3600:
            return True
    return False


def _ready_to_fire(sig):
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return False
    crypto = is_crypto_pair(sig.get("pair"))
    if (not crypto) and sig.get("ai_block"):
        return False
    sc = int(sig.get("score") or 0)
    if sc < (4 if crypto else 5):
        return False
    if not sig.get("inside_fvg"):
        return False
    if not sig.get("disp"):
        return False
    if (not crypto) and (not sig.get("aligned")):
        return False
    try:
        rr = float(sig.get("reward_pips") or 0) / float(sig.get("risk_pips") or 1)
    except Exception:
        rr = 0
    if crypto:
        if rr < 1.0 or rr > 2.6:
            return False
    elif rr < 1.2 or rr > 2.15:
        return False
    d1 = ((sig.get("htf") or {}).get("d1") or {}).get("bias")
    h4 = ((sig.get("htf") or {}).get("h4") or {}).get("bias")
    side = sig["side"]
    if (side == "BUY" and d1 == "BEAR") or (side == "SELL" and d1 == "BULL"):
        return False
    if (not crypto) and (
        (side == "BUY" and h4 == "BEAR") or (side == "SELL" and h4 == "BULL")
    ):
        return False
    tf = sig.get("tf") or "15m"
    kz = str(sig.get("killzone") or "")
    now_kz = in_killzone(int(time.time()))
    if crypto:
        now_kz = True
    if (not crypto) and tf in ("5m", "15m", "30m") and (u"خارج" in kz) and (not now_kz):
        return False
    pair = sig.get("pair")
    pip = (PAIRS.get(pair) or {}).get("pip") or 0.0001
    try:
        if abs(float(sig["entry"]) - float(sig["sl"])) < pip * 0.51:
            return False
    except Exception:
        return False
    return True


def post_to_channel(token, pair, sig, rows, force=False, dest="pro"):
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return False
    if dest == "crypto":
        if not crypto_channel_id():
            log("ch skip crypto no-id %s" % pair)
            return False
    else:
        if not market_is_open() and not force:
            return False
        if not force and not in_signal_window():
            log("ch skip %s %s night-window" % (dest, pair))
            return False
        if is_crypto_pair(pair):
            log("ch skip %s %s fx-desk" % (dest, pair))
            return False
    if not force and not _ready_to_fire(sig):
        log("ch skip %s %s not-ready sc=%s ai=%s" % (dest, pair, sig.get("score"), sig.get("ai_verdict")))
        return False
    if dest == "free" and (sig.get("score") or 0) < FREE_CHANNEL_SCORE and not force:
        log("ch skip %s %s free-weak" % (dest, pair))
        return False
    sc = sig.get("score") or 0
    min_sc = FREE_CHANNEL_SCORE if dest == "free" else MIN_CHANNEL_SCORE
    if dest == "crypto":
        min_sc = 4
    if dest == "free" and (not sig.get("aligned") or sig.get("warn")):
        if not force:
            log("ch skip %s %s not-aligned" % (dest, pair))
            return False
    if dest == "free" and sig.get("tf") == "5m" and sc < 6:
        log("ch skip %s %s 5m-weak" % (dest, pair))
        return False
    if (not force) and sc < min_sc:
        log("ch skip %s %s sc=%s<%s" % (dest, pair, sc, min_sc))
        return False
    if dest == "crypto":
        chat_id = crypto_channel_id()
    elif dest == "free":
        chat_id = CHANNEL_ID
    else:
        chat_id = PRO_CHANNEL_ID
    if (not force) and _open_same(pair, sig.get("side"), chat_id):
        log("ch skip %s %s open-same" % (dest, pair))
        return False
    posted = load_posted()
    now = time.time()
    key = pair + (":free" if dest == "free" else "")
    sid = _idea_id(sig)
    prev = posted.get(key)
    if isinstance(prev, dict):
        prev_id = prev.get("id")
        prev_ts = float(prev.get("ts") or 0)
        prev_side = prev.get("side")
    else:
        prev_id, prev_ts, prev_side = prev, 0, None
    if prev_id == sid and prev_ts and (now - prev_ts) < (3 * 3600):
        log("ch skip %s %s same-idea" % (dest, pair))
        return False
    wait = 2 * 3600 if dest == "free" else 40 * 60
    if (not force) and prev_ts and prev_side == sig.get("side") and (now - prev_ts) < wait:
        log("ch skip %s %s cooldown" % (dest, pair))
        return False
    text = format_signal(sig)
    msgid = send_chart(
        token, chat_id, rows, pair, sig, "15m", text, kb_open_bot("signal")
    )
    if not msgid:
        log("ch FAIL send %s %s %s" % (dest, pair, sig.get("side")))
        return False
    try:
        story = format_signal_story(sig)
        if story:
            send_message(token, chat_id, story, kb_open_bot("signal"), reply_to=msgid)
    except Exception:
        log("ch story " + traceback.format_exc())
    save_last(sig)
    register_trade(sig, chat_id, msgid, "channel")
    try:
        paper_on_signal(token, sig, pair)
    except Exception:
        log("paper signal " + traceback.format_exc())
    try:
        live_on_signal(token, sig, pair)
    except Exception:
        log("live signal " + traceback.format_exc())
    try:
        notify_watchers(token, sig)
    except Exception:
        log("watch ch " + traceback.format_exc())
    posted[key] = {"id": sid, "ts": now, "side": sig["side"]}
    save_posted(posted)
    log("channel %s posted %s %s sc=%s" % (dest, pair, sig["side"], sc))
    return True


def render_market_board(items):
    W, H = 1170, 1420
    bg = (224, 224, 228)
    paper = (255, 255, 255)
    ink = (29, 29, 31)
    muted = (142, 142, 147)
    goldb = (191, 149, 63)
    buf = bytearray([bg[0], bg[1], bg[2]] * (W * H))
    T = _chart_tools(W, H, buf)
    T["round_fill"](16, 16, W - 14, H - 12, (196, 196, 201), 16)
    T["round_fill"](10, 8, W - 18, H - 18, paper, 16)
    pw = T["text_w"]("TZ FX", 2) + 20
    T["round_fill"](24, 18, 24 + pw, 46, ink, 8)
    T["text"]("TZ FX", 34, 24, goldb, 2)
    T["text"]("HOURLY  4H BOARD", 24 + pw + 16, 24, ink, 2)
    clk = tehran_fmt(None, "latin")
    T["text"](clk, W - 28 - T["text_w"](clk, 1), 28, muted, 1)
    T["hline"](56, 22, W - 24, goldb, 1, 2)
    T["text"]("ICT  ·  LIVE PX ON 15M  ·  CANDLES 4H", 24, 62, muted, 1)

    ranked = sorted(items or [], key=lambda x: -int(x.get("pts") or 0))
    best_pair = ranked[0]["pair"] if ranked else None
    panel_h = 420
    top0 = 82
    for pi, it in enumerate((items or [])[:3]):
        y0 = top0 + pi * panel_h
        pair = it.get("pair") or ""
        rows = it.get("rows") or []
        sig = it.get("sig") or {}
        live = it.get("live")
        highlight = pair == best_pair
        box = (18, y0, W - 22, y0 + panel_h - 12)
        if highlight:
            T["round_fill"](box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2, (248, 246, 238), 14)
        _paint_price_panel(
            buf,
            W,
            H,
            rows,
            pair,
            sig=sig,
            box=box,
            label="4H",
            live_px=live,
            max_bars=36,
            show_levels=bool(sig.get("side") in ("BUY", "SELL")),
            show_ema=True,
            compact=True,
        )
        pass

    mark = "TZ FX"
    mw = T["text_w"](mark, 2) + 18
    T["round_fill"](W - 30 - mw, H - 42, W - 22, H - 20, ink, 7)
    T["text"](mark, W - 30 - mw + 9, H - 37, goldb, 2)
    T["text"]("EDU ONLY  ·  NOT FINANCIAL ADVICE", 24, H - 36, muted, 1)
    return _png(W, H, bytes(buf))


def market_is_open(ts=None):
    g = time.gmtime(ts or time.time())
    wd, hr = g.tm_wday, g.tm_hour
    if wd == 5:
        return False
    if wd == 6 and hr < 21:
        return False
    if wd == 4 and hr >= 21:
        return False
    return True


def in_signal_window(ts=None):
    """Signals only 08:30–20:30 Tehran. Block 20:30–08:30."""
    t = tehran_tuple(ts)
    mins = t.tm_hour * 60 + t.tm_min
    return 8 * 60 + 30 <= mins < 20 * 60 + 30


def watch_score(sig, rows):
    why = []
    pts = 0
    if not sig:
        return 0, [u"داده نیست"]
    side = sig.get("side") or ""
    htf = sig.get("htf") or {}
    sc = int(sig.get("score") or 0)
    pts += sc * 8
    if side == "BUY":
        pts += 18
        why.append(u"ستاپ خرید ICT")
    elif side == "SELL":
        pts += 18
        why.append(u"ستاپ فروش ICT")
    else:
        pts += 2
        why.append(u"ستاپ کامل نیست")
    if sig.get("aligned"):
        pts += 14
        why.append(u"هم‌راستا با پرمیوم/دیسکانت")
    if (side == "BUY" and htf.get("bias") == "BULL") or (
        side == "SELL" and htf.get("bias") == "BEAR"
    ):
        pts += 10
        why.append(u"۱ساعته هم‌جهت")
    h4 = (htf.get("h4") or {}).get("bias")
    if (side == "BUY" and h4 == "BULL") or (side == "SELL" and h4 == "BEAR"):
        pts += 10
        why.append(u"۴ساعته هم‌جهت")
    d1 = (htf.get("d1") or {}).get("bias")
    if (side == "BUY" and d1 == "BULL") or (side == "SELL" and d1 == "BEAR"):
        pts += 8
        why.append(u"روزانه هم‌جهت")
    elif (side == "BUY" and d1 == "BEAR") or (side == "SELL" and d1 == "BULL"):
        pts -= 12
        why.append(u"خلاف جهت روزانه")
    if in_killzone(int(time.time())):
        pts += 8
        why.append(u"داخل کیل‌زون")
    if in_silver_bullet(int(time.time())):
        pts += 6
        why.append(u"Silver Bullet")
    if sig.get("ai_verdict") == "CONFIRM":
        pts += 12
        why.append(u"تأیید جمنای")
    if sig.get("ai_verdict") == "REJECT" or sig.get("ai_block"):
        pts -= 25
        why.append(u"رد هوش مصنوعی")
    if sig.get("warn"):
        pts -= 6
    pair = sig.get("pair") or ""
    if rows and len(rows) > 16:
        atr = atr_val(rows)
        pip = (PAIRS.get(pair) or {}).get("pip") or 0.0001
        if atr:
            thin = pip * (8 if pair == "XAUUSD" else 4)
            fat = pip * (45 if pair == "XAUUSD" else 20)
            if atr < thin:
                pts -= 8
                why.append(u"نوسان خیلی کم")
            elif atr > fat:
                pts += 4
                why.append(u"نوسان کافی")
    return max(0, int(pts)), why


def format_hourly(items):
    kz = in_killzone(int(time.time())) or u"خارج از کیل‌زون"
    sb = u"فعال" if in_silver_bullet(int(time.time())) else u"خاموش"
    lines = [
        pe(u"✨") + u" <b>TZ FX</b>  ·  حال بازار این ساعت",
        pe(u"🕒") + u" %s تهران" % tehran_fmt(),
        u"────────────",
        pe(u"🌍") + u" کیل‌زون: <b>%s</b>" % kz,
        pe(u"⚡") + u" Silver Bullet: %s" % sb,
        u"",
    ]
    ranked = sorted(items or [], key=lambda x: -int(x.get("pts") or 0))
    for it in items or []:
        pair = it.get("pair")
        meta = PAIRS.get(pair) or {}
        sig = it.get("sig") or {}
        live = it.get("live")
        px = fmt_px(pair, live) if live is not None else "-"
        htf = sig.get("htf") or it.get("htf") or {}
        h4 = (htf.get("h4") or {}) if isinstance(htf.get("h4"), dict) else {}
        d1 = (htf.get("d1") or {}) if isinstance(htf.get("d1"), dict) else {}
        side = sig.get("side") or ""
        sc = int(sig.get("score") or 0)
        if side == "BUY":
            mark = u"🟢 <b>BUY</b>"
        elif side == "SELL":
            mark = u"🔴 <b>SELL</b>"
        else:
            mark = u"⏸ صبر"
        chg = it.get("chg1")
        if chg is None:
            chgs = ""
        else:
            chgs = u"  ·  ۱ساعت %s%.2f٪" % ("+" if chg >= 0 else "", chg)
        lines.append(
            u"%s <b>%s</b>  <code>%s</code>%s"
            % (meta.get("emoji") or "", pair, px, chgs)
        )
        lines.append(
            u"   %s  · ICT <b>%s/6</b>"
            % (mark, sc)
        )
        lines.append(
            u"   H1 <b>%s</b>/%s  ·  H4 <b>%s</b>  ·  D1 <b>%s</b>"
            % (
                htf.get("bias") or "-",
                htf.get("pd") or "-",
                h4.get("bias") or "-",
                d1.get("bias") or "-",
            )
        )
        if side in ("BUY", "SELL") and sig.get("entry") is not None:
            lines.append(
                u"   ورود <code>%s</code>  SL <code>%s</code>  TP <code>%s</code>"
                % (
                    fmt_px(pair, sig.get("entry")),
                    fmt_px(pair, sig.get("sl")) if sig.get("sl") is not None else "-",
                    fmt_px(pair, sig.get("tp")) if sig.get("tp") is not None else "-",
                )
            )
            reason = (sig.get("reason") or sig.get("setup") or "").strip()
            if reason:
                lines.append(u"   %s" % reason[:120])
        else:
            reason = (sig.get("reason") or u"ستاپ ICT کامل نیست").strip()
            lines.append(u"   %s" % reason[:120])
        lines.append("")
    best = ranked[0] if ranked else None
    if (
        best
        and int(best.get("pts") or 0) >= 28
        and (best.get("sig") or {}).get("side") in ("BUY", "SELL")
    ):
        meta = PAIRS.get(best["pair"]) or {}
        why = u"، ".join((best.get("why") or [])[:4]) or u"ساختار بهتر از بقیه"
        lines.append(
            u"🎯 <b>اولویت این ساعت: %s %s</b>"
            % (meta.get("emoji") or "", meta.get("name") or best["pair"])
        )
        lines.append(u"چرا: %s." % why)
        lines.append(u"تمرکز روی همین نماد — برد تضمینی نیست.")
    else:
        lines.append(u"🎯 این ساعت ستاپ تمیز ICT نیست.")
        lines.append(u"صبر کن. دنبال «حتماً یکی را بزن» نباش.")
    try:
        dail = daily_r_blob()
        tod = dail.get("today") or {}
        lines.append(
            u"📅 امروز  <b>%+.2fR</b>  ·  %s بسته‌شده"
            % (float(tod.get("r") or 0), tod.get("n") or 0)
        )
    except Exception:
        pass
    lines += [u"", u"⚖️ آموزشی است · مشاوره مالی نیست · درصد الکی نیست."]
    return u"\n".join(lines)


def hourly_channel(token):
    now = time.time()
    try:
        last = float(open(BRIEF_FILE).read().strip() or 0)
    except Exception:
        last = 0
    if now - last < 3600:
        return
    if not market_is_open(now):
        try:
            with open(BRIEF_FILE, "w") as f:
                f.write(str(now))
        except Exception:
            pass
        log("hourly skip market closed")
        return
    try:
        with open(BRIEF_FILE, "w") as f:
            f.write(str(now))
    except Exception:
        pass

    def one(pair):
        rows15 = []
        try:
            rows15 = fetch_ohlc(pair, "15m", "10d") or []
        except Exception:
            log("hourly ohlc " + pair + " " + traceback.format_exc())
            rows15 = []
        live = rows15[-1]["c"] if rows15 else None
        chg1 = None
        if live is not None and len(rows15) >= 5 and rows15[-5]["c"]:
            chg1 = (live - rows15[-5]["c"]) / rows15[-5]["c"] * 100.0
        sig = None
        try:
            sig = scan_signal(pair)
        except Exception:
            log("hourly scan " + pair + " " + traceback.format_exc())
            try:
                sig = build_signal(rows15, pair) if rows15 else None
            except Exception:
                sig = None
        if not sig:
            sig = {}
        if live is not None and not sig.get("price"):
            sig["price"] = live
        try:
            pts, why = watch_score(sig, rows15)
        except Exception:
            pts, why = 0, []
        return {
            "pair": pair,
            "live": live,
            "chg1": chg1,
            "sig": sig,
            "htf": sig.get("htf") or {},
            "pts": pts,
            "why": why,
        }

    items = []
    try:
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=3) as ex:
            items = list(ex.map(one, list(FX_PAIRS)))
    except Exception:
        log("hourly map " + traceback.format_exc())
        items = [one(p) for p in FX_PAIRS]
    try:
        text = format_hourly(items)
    except Exception:
        log("hourly fmt " + traceback.format_exc())
        text = u"TZ FX · حال بازار این ساعت\n%s تهران\nداده نرسید." % tehran_fmt()
    kb = kb_open_bot("brief")
    for dest, cid in (("free", CHANNEL_ID), ("pro", PRO_CHANNEL_ID)):
        ok = send_message(token, cid, text[:4000], kb)
        log("hourly posted %s ok=%s" % (dest, bool(ok)))


def channel_tick(token):
    now0 = time.time()
    try:
        last = float(open(TICK_FILE).read().strip() or 0)
    except Exception:
        last = 0
    if now0 - last < 120:
        return
    try:
        with open(TICK_FILE, "w") as f:
            f.write(str(now0))
    except Exception:
        pass
    beat_heartbeat()
    try:
        tick_alerts(token)
    except Exception:
        log("alerts " + traceback.format_exc())
    try:
        crypto_tick(token)
    except Exception:
        log("crypto_tick " + traceback.format_exc())
    if not market_is_open():
        log("ch tick fx-closed")
        return
    if not in_signal_window():
        log("ch tick night-window")
        return
    try:
        for pair in FX_PAIRS:
            sig = scan_signal(pair)
            if sig:
                sig = dict(sig)
            rows = (sig or {}).pop("_rows", None) if sig else None
            if not rows:
                rows = fetch_ohlc(pair)
            if not rows:
                log("ch skip %s no-ohlc" % pair)
                continue
            if not sig:
                sig = build_signal(rows, pair)
            side = (sig or {}).get("side")
            sc = (sig or {}).get("score")
            log(
                "ch scan %s %s sc=%s %s"
                % (
                    pair,
                    side,
                    sc,
                    ((sig or {}).get("reason") or (sig or {}).get("setup") or "")[:80],
                )
            )
            if side in ("BUY", "SELL"):
                log("ch tick %s %s sc=%s" % (pair, side, sc))
            if sig and sig.get("side") in ("BUY", "SELL"):
                try:
                    sig = ai_confirm(sig, rows)
                except Exception:
                    log("ai_confirm ch " + traceback.format_exc())
                log(
                    "ch after-ai %s %s sc=%s ai=%s"
                    % (
                        pair,
                        (sig or {}).get("side"),
                        (sig or {}).get("score"),
                        (sig or {}).get("ai_verdict"),
                    )
                )
            post_to_channel(token, pair, sig, rows, dest="pro")
            post_to_channel(token, pair, sig, rows, dest="free")
        try:
            hourly_channel(token)
        except Exception:
            log("hourly " + traceback.format_exc())
    except Exception:
        log("channel_tick error " + traceback.format_exc())


def dispatch_update(token, upd):
    mcm = upd.get("my_chat_member")
    if mcm:
        save_group(mcm.get("chat") or {})
        protect_pro(token, mcm)
        try:
            maybe_bind_crypto_member(token, mcm)
        except Exception:
            log("bind crypto " + traceback.format_exc())
        return False
    cp = upd.get("channel_post") or upd.get("edited_channel_post")
    if cp:
        try:
            bind_crypto_channel(cp.get("chat") or {})
        except Exception:
            pass
        return False
    cm = upd.get("chat_member")
    if cm:
        protect_pro(token, cm)
        return False
    pcq = upd.get("pre_checkout_query")
    if pcq:
        handle_pre_checkout(token, pcq)
        return True
    if upd.get("callback_query"):
        handle_callback(token, upd["callback_query"])
        return True
    msg = upd.get("message") or upd.get("edited_message")
    if msg:
        handle_message(token, msg)
        return True
    return False


def webhook_enabled():
    return os.path.isfile(WEBHOOK_FLAG)


def ensure_commands(token):
    try:
        age = 9e9
        if os.path.isfile(CMDS_FLAG):
            try:
                oldv = open(CMDS_FLAG).read().strip()
            except Exception:
                oldv = ""
            if oldv == BOT_VERSION:
                age = time.time() - os.path.getmtime(CMDS_FLAG)
                if age < 6 * 3600:
                    return
    except Exception:
        pass
    try:
        cmds_fa = [
                    {"command": "start", "description": "خانه"},
                    {"command": "signal", "description": "سیگنال"},
                    {"command": "crypto", "description": "کریپتو"},
                    {"command": "learn", "description": "آموزش"},
                    {"command": "wr", "description": "وین‌ریت"},
                    {"command": "lang", "description": "زبان / Language"},
                    {"command": "help", "description": "راهنما"},
        ]
        cmds_en = [
                    {"command": "start", "description": "Home"},
                    {"command": "signal", "description": "Signals"},
                    {"command": "crypto", "description": "Crypto"},
                    {"command": "learn", "description": "Learn"},
                    {"command": "wr", "description": "Win-rate"},
                    {"command": "lang", "description": "Language / زبان"},
                    {"command": "donate", "description": "Support"},
                    {"command": "help", "description": "Help"},
        ]
        http().post(
            tg_api(token) + "/setMyCommands",
            json={
                "commands": [
                    {"command": "start", "description": "خانه / Home"},
                    {"command": "signal", "description": "سیگنال / Signals"},
                    {"command": "crypto", "description": "کریپتو / Crypto"},
                    {"command": "connect", "description": "اتصال / Connect"},
                    {"command": "paper", "description": "پیپر / Paper"},
                    {"command": "learn", "description": "آموزش / Learn"},
                    {"command": "wr", "description": "وین‌ریت / Win-rate"},
                    {"command": "lang", "description": "زبان / Language"},
                    {"command": "donate", "description": "حمایت / Support"},
                    {"command": "help", "description": "راهنما / Help"},
                                ]
            },
            timeout=10,
        )
        with open(CMDS_FLAG, "w") as f:
            f.write(BOT_VERSION)
    except Exception:
        log("ensure_commands " + traceback.format_exc())


def ensure_public(token):
    ensure_commands(token)
    if os.path.isfile(PUBLIC_FLAG):
        return
    try:
        http().post(
            tg_api(token) + "/setMyName",
            json={"name": "TZ FX BOT"},
            timeout=10,
        )
        http().post(
            tg_api(token) + "/setMyShortDescription",
            json={
                "short_description": "TZ FX · ICT · یورو پوند طلا · آموزشی"
            },
            timeout=10,
        )
        http().post(
            tg_api(token) + "/setMyDescription",
            json={
                "description": (
                    "TZ FX — سیگنال ICT برای یورو، پوند و طلا.\n"
                    "مینی‌اپ، چارت، مربی متن و ویس، ۲۴ درس، وین‌ریت واقعی از حد سود/ضرر.\n"
                    "کانال رایگان @TZ_FX_CH · VIP خصوصی با اشتراک (کارت + رسید).\n"
                    "آموزشی است، مشاوره مالی نیست، سرمایه در خطر است. درصد الکی نمی‌گوییم."
                )
            },
            timeout=10,
        )
        with open(PUBLIC_FLAG, "w") as f:
            f.write("1")
        log("public profile set")
    except Exception:
        log("ensure_public " + traceback.format_exc())
        return
    if os.path.isfile(LAUNCH_FLAG):
        return
    try:
        text = (
            "🚀 <b>TZ FX BOT فعال شد</b>\n"
            "━━━━━━━━━━━━━━\n"
            "سیگنال زنده ICT برای:\n"
            "💶 یورو   💷 پوند   🥇 طلا\n\n"
            "داخل ربات:\n"
            "• ورود / حد ضرر / حد سود\n"
            "• دنبال کردن تا TP یا SL\n"
            "• آموزش از صفر\n"
            "• حجم با ۱٪ ریسک\n"
            "• چت با مربی\n\n"
            "کانال رایگان: ستاپ خیلی قویِ کم.\n"
            "کانال VIP و سیگنال کامل: با اشتراک.\n"
            "<i>آموزشی است · مشاوره مالی نیست · سرمایه در خطر است</i>"
        )
        msgid = send_message(token, CHANNEL_ID, text, kb_open_bot("signal"))
        if msgid:
            try:
                http().post(
                    tg_api(token) + "/pinChatMessage",
                    json={
                        "chat_id": CHANNEL_ID,
                        "message_id": int(msgid),
                        "disable_notification": False,
                    },
                    timeout=10,
                )
            except Exception:
                pass
            with open(LAUNCH_FLAG, "w") as f:
                f.write(str(msgid))
            log("launch posted")
    except Exception:
        log("launch " + traceback.format_exc())


def load_webhook_secret():
    try:
        with open(WEBHOOK_SECRET_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return ""


def process_once(timeout=0):
    global _bot_error, _last_poll
    try:
        ensure_requests()
        token = load_token()
        if not token:
            _bot_error = "no token"
            return
        try:
            load_pe_sets(token)
        except Exception:
            pass
        try:
            ensure_menu_button(token)
        except Exception:
            pass
        ensure_public(token)
        try:
            ensure_webhook(token)
        except Exception:
            log("ensure_webhook call " + traceback.format_exc())
        if webhook_enabled():
            maybe_fix_webhook(token)
            if webhook_enabled():
                beat_heartbeat()
                try:
                    nudge_crypto_owner(token)
                except Exception:
                    pass
                try:
                    monitor_trades(token)
                except NameError:
                    pass
                except Exception:
                    log("monitor error " + traceback.format_exc())
                try:
                    paper_monitor(token)
                except Exception:
                    log("paper mon " + traceback.format_exc())
                try:
                    channel_tick(token)
                except Exception:
                    log("channel_tick error " + traceback.format_exc())
                try:
                    warm_cache()
                except Exception:
                    pass
                return
        offset = load_offset()
        r = http().get(
            tg_api(token) + "/getUpdates",
            params={
                "timeout": timeout,
                "offset": offset,
                "allowed_updates": json.dumps(
                    [
                        "message",
                        "edited_message",
                        "callback_query",
                        "my_chat_member",
                        "chat_member",
                        "pre_checkout_query",
                    ]
                ),
            },
            timeout=timeout + 6,
        )
        payload = r.json()
        if not payload.get("ok"):
            _bot_error = str(payload)[:200]
            log("getUpdates fail " + _bot_error)
            desc = _bot_error.lower()
            if "conflict" in desc or "409" in desc:
                try:
                    http().post(
                        tg_api(token) + "/deleteWebhook",
                        json={"drop_pending_updates": False},
                        timeout=8,
                    )
                    log("deleted webhook after conflict")
                except Exception:
                    pass
            return
        _bot_error = None
        try:
            _last_poll = tehran_fmt(None, "%H:%M")
        except Exception:
            _last_poll = "-"
        try:
            hb = 0
            if os.path.isfile(HB_FILE):
                hb = float(open(HB_FILE).read().strip() or 0)
            if time.time() - hb > 600:
                with open(HB_FILE, "w") as f:
                    f.write(str(time.time()))
                log("alive")
        except Exception:
            pass
        n = len(payload.get("result") or [])
        if n:
            log("poll n=%s" % n)
        had_user = False
        for upd in payload.get("result", []):
            try:
                if dispatch_update(token, upd):
                    had_user = True
            except Exception:
                log("upd error " + traceback.format_exc())
                try:
                    msg = upd.get("message") or {}
                    chat = msg.get("chat") or {}
                    if chat.get("type") == "private" and chat.get("id"):
                        send_message(
                            token,
                            chat.get("id"),
                            u"یک لحظه گیر کرد — دوباره بفرست.",
                            kb_main(chat.get("id")),
                        )
                except Exception:
                    pass
            save_offset(upd["update_id"] + 1)
        try:
            monitor_trades(token)
        except Exception:
            log("monitor error " + traceback.format_exc())
        try:
            paper_monitor(token)
        except Exception:
            log("paper mon " + traceback.format_exc())
        try:
            channel_tick(token)
        except Exception:
            log("channel_tick error " + traceback.format_exc())
        if not had_user:
            warm_cache()
        try:
            _ohlc_disk_flush(force=True)
        except Exception:
            pass
    except Exception:
        _bot_error = traceback.format_exc()
        log("process_once error " + _bot_error)


def process_once_locked(timeout=0):
    lockf = open(LOCK_FILE, "a+")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (IOError, OSError):
        return
    try:
        process_once(timeout=timeout)
    finally:
        try:
            fcntl.flock(lockf, fcntl.LOCK_UN)
        except Exception:
            pass
        lockf.close()


def process_webhook(raw):
    try:
        log("webhook bytes=%s" % len(raw or b""))
        ensure_requests()
        token = load_token()
        if not token:
            log("webhook no token")
            return
        upd = json.loads(raw.decode("utf-8"))
        keys = [
            k
            for k in ("message", "callback_query", "my_chat_member", "edited_message")
            if upd.get(k)
        ]
        log("webhook " + (",".join(keys) or "empty"))
        global _last_poll, _bot_error
        try:
            _last_poll = tehran_fmt(None, "%H:%M")
            _bot_error = None
        except Exception:
            pass
        dispatch_update(token, upd)
    except Exception:
        log("webhook " + traceback.format_exc())


def _webhook_url():
    url = (WEBHOOK_URL or "").strip()
    if not url.startswith("https://"):
        return ""
    if url.endswith("index.cgi"):
        return url
    return url.rstrip("/") + "/"


def ensure_webhook(token):
    url = _webhook_url()
    if not url:
        return False
    try:
        r = http().get(tg_api(token) + "/getWebhookInfo", timeout=8)
        info = (r.json() or {}).get("result") or {}
        cur = (info.get("url") or "").strip()
        au = info.get("allowed_updates") or []
        need_au = [
            "message",
            "edited_message",
            "callback_query",
            "my_chat_member",
            "chat_member",
            "pre_checkout_query",
            "channel_post",
        ]
        if (
            cur.rstrip("/") == url.rstrip("/")
            and os.path.isfile(WEBHOOK_V_FILE)
            and ("channel_post" in au or not au)
        ):
            if not os.path.isfile(WEBHOOK_FLAG):
                with open(WEBHOOK_FLAG, "w") as f:
                    f.write("1")
            return True
        r2 = http().post(
            tg_api(token) + "/setWebhook",
            json={
                "url": url,
                "allowed_updates": [
                    "message",
                    "edited_message",
                    "callback_query",
                    "my_chat_member",
                    "chat_member",
                    "pre_checkout_query",
                    "channel_post",
                ],
                "drop_pending_updates": False,
                "max_connections": 8,
            },
            timeout=12,
        )
        js = r2.json() if r2.content else {}
        if js.get("ok"):
            with open(WEBHOOK_FLAG, "w") as f:
                f.write("1")
            try:
                with open(WEBHOOK_V_FILE, "w") as f:
                    f.write(BOT_VERSION)
            except Exception:
                pass
            log("webhook on v19")
            return True
        log("setWebhook fail " + str(js)[:200])
        return False
    except Exception:
        log("ensure_webhook " + traceback.format_exc())
        return False


def maybe_fix_webhook(token):
    try:
        r = http().get(tg_api(token) + "/getWebhookInfo", timeout=8)
        info = (r.json() or {}).get("result") or {}
        err = str(info.get("last_error_message") or "")
        if not info.get("url"):
            return
        bad = (
            "301",
            "302",
            "502",
            "503",
            "504",
            "timed out",
            "SSL",
            "Connection refused",
            "Wrong response",
        )
        if err and any(x in err for x in bad):
            http().post(
                tg_api(token) + "/deleteWebhook",
                json={"drop_pending_updates": False},
                timeout=8,
            )
            try:
                os.remove(WEBHOOK_FLAG)
            except Exception:
                pass
            log("webhook off because " + err[:160])
    except Exception:
        pass



def _qs_get(environ, name, default=""):
    raw = environ.get("QUERY_STRING") or ""
    for part in raw.split("&"):
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
        else:
            k, v = part, ""
        k = k.replace("+", " ")
        v = v.replace("+", " ")
        try:
            from urllib.parse import unquote
            k, v = unquote(k), unquote(v)
        except Exception:
            pass
        if k == name:
            return v
    return default


def admin_web(environ):
    key = (_qs_get(environ, "k") or "").strip()
    if not key or key != admin_key():
        return "403 Forbidden", "text/plain; charset=utf-8", b"need ?k="
    act = (_qs_get(environ, "act") or "").strip()
    uid = (_qs_get(environ, "uid") or "").strip()
    days = (_qs_get(environ, "days") or "30").strip()
    note = ""
    if act == "grant" and uid.isdigit():
        try:
            until = grant_sub(int(uid), int(days), "web")
            note = "granted %s until %s" % (uid, tehran_fmt(until))
        except Exception:
            note = "grant fail"
    elif act == "revoke" and uid.isdigit():
        revoke_sub(int(uid))
        note = "revoked %s" % uid
    users = load_users()
    subs = load_subs()
    now = time.time()
    active = []
    for k, v in sorted(
        subs.items(), key=lambda kv: -float((kv[1] or {}).get("until") or 0)
    ):
        until = float((v or {}).get("until") or 0)
        if until > now:
            active.append((k, until, (v or {}).get("plan") or ""))
    recent = sorted(
        users.items(),
        key=lambda kv: (kv[1] or {}).get("seen") or 0,
        reverse=True,
    )[:40]
    rows_sub = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (a[0], tehran_fmt(a[1]), a[2])
        for a in active[:80]
    ) or "<tr><td colspan=3>none</td></tr>"
    rows_u = "".join(
        "<tr><td>%s</td><td>%s</td></tr>"
        % (k, tehran_fmt((v or {}).get("seen")))
        for k, v in recent
    ) or "<tr><td colspan=2>none</td></tr>"
    html = (
        "<!doctype html><meta charset=utf-8><title>TZ FX admin</title>"
        "<style>body{font-family:-apple-system,sans-serif;max-width:720px;"
        "margin:24px auto;padding:0 16px;background:#f5f5f7;color:#1d1d1f}"
        "h1{font-size:22px}table{width:100%%;border-collapse:collapse;"
        "background:#fff;border-radius:12px;overflow:hidden}"
        "td,th{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;"
        "font-size:13px}form{margin:12px 0;padding:12px;background:#fff;"
        "border-radius:12px}input,button{padding:8px;margin:4px}"
        ".ok{color:#248a3d}</style>"
        "<h1>TZ FX admin</h1>"
        "<p class=ok>%s</p>"
        "<p>users %s · active subs %s</p>"
        "<form method=get>"
        "<input type=hidden name=k value=\"%s\">"
        "uid <input name=uid placeholder=telegram id>"
        "days <input name=days value=30 size=4>"
        "<button name=act value=grant>grant</button>"
        "<button name=act value=revoke>revoke</button>"
        "</form>"
        "<h2>active subs</h2><table><tr><th>uid</th><th>until Tehran</th>"
        "<th>plan</th></tr>%s</table>"
        "<h2>recent users</h2><table><tr><th>uid</th><th>seen</th></tr>%s</table>"
    ) % (
        note,
        len(users),
        len(active),
        key,
        rows_sub,
        rows_u,
    )
    return "200 OK", "text/html; charset=utf-8", html.encode("utf-8")



def ensure_menu_button(token):
    try:
        if os.path.isfile(MENU_FLAG) and (time.time() - os.path.getmtime(MENU_FLAG)) < 6 * 3600:
            return
    except Exception:
        pass
    try:
        http().post(
            tg_api(token) + "/setChatMenuButton",
            json={
                "menu_button": {
                    "type": "web_app",
                    "text": "TZ FX",
                    "web_app": {"url": APP_URL},
                }
            },
            timeout=10,
        )
        with open(MENU_FLAG, "w") as f:
            f.write("1")
        log("menu webapp set")
    except Exception:
        log("menu button " + traceback.format_exc())


def webapp_uid(init_data, token):
    if not init_data or not token:
        return None
    try:
        from urllib.parse import parse_qsl

        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        got = parsed.pop("hash", "")
        if not got:
            return None
        check = "\n".join("%s=%s" % (k, parsed[k]) for k in sorted(parsed))
        secret = hmac.new(b"WebAppData", token.encode("utf-8"), hashlib.sha256).digest()
        calc = hmac.new(secret, check.encode("utf-8"), hashlib.sha256).hexdigest()
        if calc != got:
            return None
        user = json.loads(parsed.get("user") or "{}")
        return int(user.get("id") or 0) or None
    except Exception:
        return None


def miniapp_wr_blob():
    raw = load_trades()
    rows = _unique_book([t for t in raw if int(t.get("gen") or 0) >= ENGINE_GEN])
    closed = [t for t in rows if t.get("status") in ("tp", "sl")]
    wins = [t for t in closed if t.get("status") == "tp"]
    loss = [t for t in closed if t.get("status") == "sl"]
    opens = [t for t in rows if t.get("status") == "open"]
    n = len(wins) + len(loss)
    pct = int(round(100.0 * len(wins) / n)) if n else 0
    avg = (sum(_r_of(t) for t in closed) / float(n)) if n else 0.0
    return {
        "n": n,
        "wins": len(wins),
        "loss": len(loss),
        "open": len(opens),
        "pct": pct,
        "avg_r": round(avg, 2),
    }


def _ema_last(rows, n, key="c"):
    if not rows or len(rows) < n:
        return None
    k = 2.0 / (n + 1.0)
    e = float(rows[0][key])
    for r in rows[1:]:
        e = float(r[key]) * k + e * (1.0 - k)
    return e


def _rsi14(rows):
    if not rows or len(rows) < 16:
        return None
    ag = 0.0
    al = 0.0
    for i in range(len(rows) - 14, len(rows)):
        d = float(rows[i]["c"]) - float(rows[i - 1]["c"])
        if d >= 0:
            ag += d
        else:
            al -= d
    ag /= 14.0
    al /= 14.0
    if al <= 1e-12:
        return 100.0
    return 100.0 - (100.0 / (1.0 + ag / al))


def miniapp_pack(pair, rows=None, htf=None):
    """Mini-app only. Extra confluence so beginners get more in-session ideas
    without changing the ICT channel engine."""
    meta = PAIRS.get(pair) or {}
    pip = meta.get("pip") or 0.0001
    out = {
        "pair": pair,
        "emoji": meta.get("emoji") or "",
        "name": meta.get("name") or pair,
        "side": "WAIT",
        "action": u"دست نزن",
        "color": "wait",
        "votes": 0,
        "need": 5,
        "why": u"هنوز چند نشانه با هم یکی نشده.",
        "steps": u"صبر کن. تعقیب نکن. حداکثر ۱٪.",
        "lights": [],
        "entry": None,
        "sl": None,
        "tp": None,
        "px": None,
        "score": 0,
        "rr": 0,
        "ict": False,
    }
    try:
        if not rows:
            rows = fetch_ohlc(pair, "15m", "10d") or []
    except Exception:
        rows = rows or []
    if not rows or len(rows) < 30:
        out["why"] = u"داده بازار کامل نیست — کمی بعد."
        return out
    price = float(rows[-1]["c"])
    out["px"] = fmt_px(pair, price)
    try:
        htf = htf or htf_context(pair, price) or {}
    except Exception:
        htf = htf or {}
    h1 = htf.get("bias") or "NEUTRAL"
    pd = htf.get("pd") or "-"
    h4 = (htf.get("h4") or {}).get("bias") or "NEUTRAL"
    d1 = (htf.get("d1") or {}).get("bias") or "NEUTRAL"
    ema20 = _ema_last(rows[-80:], 20)
    ema50 = _ema_last(rows[-80:], 50)
    rsi = _rsi14(rows)
    sh, sls = swing_points(rows, 2, 2)
    struct = "NEUTRAL"
    if sh and sls and len(sh) >= 2 and len(sls) >= 2:
        if rows[sh[-1]]["h"] > rows[sh[-2]]["h"] and rows[sls[-1]]["l"] >= rows[sls[-2]]["l"]:
            struct = "BULL"
        elif rows[sh[-1]]["h"] <= rows[sh[-2]]["h"] and rows[sls[-1]]["l"] < rows[sls[-2]]["l"]:
            struct = "BEAR"
    up_n = 0
    for r in rows[-8:]:
        if r["c"] >= r["o"]:
            up_n += 1
    mom = "BULL" if up_n >= 6 else ("BEAR" if up_n <= 2 else "NEUTRAL")
    kz = in_killzone(int(time.time()))
    ema12 = _ema_last(rows[-80:], 12)
    ema26 = _ema_last(rows[-80:], 26)
    win = rows[-32:]
    rng_hi = max(r["h"] for r in win)
    rng_lo = min(r["l"] for r in win)
    rng_mid = (rng_hi + rng_lo) / 2.0
    lights = []

    def add(ok, name, tip):
        lights.append({"ok": bool(ok), "name": name, "tip": tip})

    add(h4 == "BULL", u"روند ۴ساعته", u"۴ساعته بالا")
    add(h4 == "BEAR", u"روند ۴ساعته↓", u"۴ساعته پایین")
    add(h1 == "BULL", u"روند ۱ساعته", u"ساعتی با خرید")
    add(h1 == "BEAR", u"روند ۱ساعته↓", u"ساعتی با فروش")
    add(pd == "DISCOUNT", u"قیمت ارزان", u"زیر میانه")
    add(pd == "PREMIUM", u"قیمت گران", u"بالای میانه")
    add(ema20 and ema50 and price > ema20 > ema50, u"میانگین صعود", u"بالای میانگین")
    add(ema20 and ema50 and price < ema20 < ema50, u"میانگین نزول", u"زیر میانگین")
    add(ema12 and ema26 and ema12 > ema26, u"MACD صعود", u"میانگین سریع بالای کند")
    add(ema12 and ema26 and ema12 < ema26, u"MACD نزول", u"میانگین سریع زیر کند")
    add(struct == "BULL", u"ساختار صعود", u"کف و سقف بالاتر")
    add(struct == "BEAR", u"ساختار نزول", u"کف و سقف پایین‌تر")
    add(mom == "BULL", u"شتاب خرید", u"کندل‌های اخیر سبز")
    add(mom == "BEAR", u"شتاب فروش", u"کندل‌های اخیر قرمز")
    add(rsi is not None and rsi <= 40, u"RSI اشباع فروش", u"جا برای برگشت خرید")
    add(rsi is not None and rsi >= 60, u"RSI اشباع خرید", u"جا برای برگشت فروش")
    add(price >= rng_mid and h1 == "BULL", u"شکست سقف جلسه", u"قیمت بالای میانه جلسه")
    add(price <= rng_mid and h1 == "BEAR", u"شکست کف جلسه", u"قیمت زیر میانه جلسه")
    add(bool(kz), u"جلسه فعال", u"لندن/نیویورک")
    add(bool(in_silver_bullet(int(time.time()))), u"Silver Bullet", u"ساعت طلایی")

    BUY_N = (
        u"روند ۴ساعته", u"روند ۱ساعته", u"قیمت ارزان", u"میانگین صعود", u"MACD صعود",
        u"ساختار صعود", u"شتاب خرید", u"RSI اشباع فروش", u"شکست سقف جلسه",
    )
    SELL_N = (
        u"روند ۴ساعته↓", u"روند ۱ساعته↓", u"قیمت گران", u"میانگین نزول", u"MACD نزول",
        u"ساختار نزول", u"شتاب فروش", u"RSI اشباع خرید", u"شکست کف جلسه",
    )
    buy_pts = 0
    sell_pts = 0
    for L in lights:
        if not L["ok"]:
            continue
        n = L["name"]
        w = 2 if u"۴ساعته" in n else 1
        if n in BUY_N:
            buy_pts += w
        if n in SELL_N:
            sell_pts += w
    if kz:
        if buy_pts > sell_pts:
            buy_pts += 1
        elif sell_pts > buy_pts:
            sell_pts += 1
    if in_silver_bullet(int(time.time())):
        if buy_pts >= sell_pts:
            buy_pts += 1
        else:
            sell_pts += 1

    need = 4
    side = "WAIT"
    d1_note = ""
    if buy_pts >= need and buy_pts > sell_pts:
        side = "BUY"
    elif sell_pts >= need and sell_pts > buy_pts:
        side = "SELL"
    if side == "BUY" and d1 == "BEAR":
        if buy_pts < need + 2:
            side = "WAIT"
            d1_note = u"روزانه نزولی است — خرید را ول کن."
        else:
            d1_note = u"روزانه مخالف است؛ فقط اگر مطمئنی."
    if side == "SELL" and d1 == "BULL":
        if sell_pts < need + 2:
            side = "WAIT"
            d1_note = u"روزانه صعودی است — فروش را ول کن."
        else:
            d1_note = u"روزانه مخالف است؛ فقط اگر مطمئنی."

    atr = atr_val(rows) or pip * 12
    entry = snap_px(pair, price)
    sl = tp = None
    rr = 0
    min_px = pip * min_risk_pips(pair, "15m")
    max_px = pip * max_risk_pips(pair, "15m")
    buf = max(atr * 0.12, pip * (4 if pair == "XAUUSD" else 2))

    def _levels(side0):
        if side0 == "BUY":
            wick = rows[sls[-1]]["l"] if sls else min(r["l"] for r in rows[-16:])
            floor = min(r["l"] for r in rows[-16:])
            if wick >= entry:
                wick = floor
            sl0 = snap_px(pair, float(wick) - buf)
            if abs(entry - sl0) < min_px:
                sl0 = snap_px(pair, entry - min_px)
            if abs(entry - sl0) > max_px:
                sl0 = snap_px(pair, entry - max_px)
            if sl0 >= entry:
                return None, None, 0
            risk = abs(entry - sl0)
            tp0 = choose_tp("BUY", entry, sl0, rows, sh, sls, htf, pip, atr=atr, pair=pair)
            if tp0 is None or tp0 <= entry or abs(tp0 - entry) / risk < 1.0:
                tp0 = snap_px(pair, entry + risk * 1.4)
            rr0 = abs(tp0 - entry) / risk if risk else 0
            if rr0 < 1.0 or tp0 <= entry:
                return None, None, 0
            return sl0, tp0, rr0
        wick = rows[sh[-1]]["h"] if sh else max(r["h"] for r in rows[-16:])
        ceil = max(r["h"] for r in rows[-16:])
        if wick <= entry:
            wick = ceil
        sl0 = snap_px(pair, float(wick) + buf)
        if abs(entry - sl0) < min_px:
            sl0 = snap_px(pair, entry + min_px)
        if abs(entry - sl0) > max_px:
            sl0 = snap_px(pair, entry + max_px)
        if sl0 <= entry:
            return None, None, 0
        risk = abs(sl0 - entry)
        tp0 = choose_tp("SELL", entry, sl0, rows, sh, sls, htf, pip, atr=atr, pair=pair)
        if tp0 is None or tp0 >= entry or abs(entry - tp0) / risk < 1.0:
            tp0 = snap_px(pair, entry - risk * 1.4)
        rr0 = abs(entry - tp0) / risk if risk else 0
        if rr0 < 1.0 or tp0 >= entry:
            return None, None, 0
        return sl0, tp0, rr0

    if side in ("BUY", "SELL"):
        sl, tp, rr = _levels(side)
        if sl is None:
            side = "WAIT"
            d1_note = u"حد ضرر این ستاپ منطقی نشد — صبر کن."

    votes = max(buy_pts, sell_pts)
    if side == "BUY":
        action = u"بخر"
        color = "buy"
        why = u"چند روش با هم می‌گویند خرید (روند/میانگین/ساختار/جلسه)."
        if d1_note and u"مخالف" in d1_note:
            why = why + u" " + d1_note
        steps = u"۱) نزدیک همین قیمت بخر  ۲) حد ضرر را جابه‌جا نکن  ۳) حد سود را دست نزن  ۴) نرسید تعقیب نکن · حداکثر ۱٪."
    elif side == "SELL":
        action = u"بفروش"
        color = "sell"
        why = u"چند روش با هم می‌گویند فروش (روند/میانگین/ساختار/جلسه)."
        if d1_note and u"مخالف" in d1_note:
            why = why + u" " + d1_note
        steps = u"۱) نزدیک همین قیمت بفروش  ۲) حد ضرر را جابه‌جا نکن  ۳) حد سود را دست نزن  ۴) نرسید تعقیب نکن · حداکثر ۱٪."
    else:
        action = u"دست نزن"
        color = "wait"
        why = d1_note or u"نشانه‌ها یکی نیستند. مبتدی اینجا معامله نمی‌کند."
        steps = u"صبر کن. سیگنال بعدی را از همین صفحه ببین. حداکثر ۱٪ حساب."
        entry = sl = tp = None
        rr = 0

    out.update(
        {
            "side": side,
            "action": action,
            "color": color,
            "votes": int(votes),
            "buy_pts": int(buy_pts),
            "sell_pts": int(sell_pts),
            "need": need,
            "why": why,
            "steps": steps,
            "lights": lights,
            "entry": fmt_px(pair, entry) if entry is not None else None,
            "sl": fmt_px(pair, sl) if sl is not None else None,
            "tp": fmt_px(pair, tp) if tp is not None else None,
            "score": min(10, int(votes)),
            "rr": round(float(rr), 2),
            "h1": h1,
            "h4": h4,
            "d1": d1,
            "pd": pd,
            "rsi": None if rsi is None else round(rsi, 1),
            "kz": kz or u"خارج از کیل‌زون",
        }
    )
    return out


def miniapp_ict_blob(pair, sig=None):
    """ICT only."""
    meta = PAIRS.get(pair) or {}
    seq = [
        {"name": u"جهت تایم بالا", "ok": False},
        {"name": u"جاروی Judas", "ok": False},
        {"name": u"MSS", "ok": False},
        {"name": u"FVG", "ok": False},
        {"name": u"ورود در شکاف", "ok": False},
        {"name": u"OTE", "ok": False},
        {"name": u"کیل‌زون", "ok": False},
        {"name": u"پرمیوم/دیسکانت", "ok": False},
    ]
    out = {
        "pair": pair,
        "emoji": meta.get("emoji") or "",
        "name": meta.get("name") or pair,
        "model": u"ICT",
        "kind": "ict",
        "side": "WAIT",
        "action": u"صبر",
        "color": "wait",
        "why": u"مدل ICT هنوز کامل نشده — تعقیب نکن.",
        "steps": (
            u"۱) جهت تایم بالا  ۲) جاروی Judas از نقدینگی  "
            u"۳) MSS با جابجایی  ۴) ورود فقط داخل FVG/OTE  "
            u"۵) حد ضرر آن‌سوی ویک جارو  ۶) حد سود نقدینگی داخلی (IRL)."
        ),
        "seq": seq,
        "entry": None,
        "sl": None,
        "tp": None,
        "score": 0,
        "tf": "",
        "kz": in_killzone(int(time.time())) or u"خارج از کیل‌زون",
        "live": False,
        "setup": "",
    }
    if not sig:
        return out
    f = sig.get("forming") or {}
    kz_raw = sig.get("killzone")
    kz_ok = bool(kz_raw) and (u"خارج" not in str(kz_raw or ""))
    htf = sig.get("htf") or {}
    htf_bias = htf.get("bias") or ""
    live = sig.get("side") in ("BUY", "SELL")
    out["seq"] = [
        {"name": u"جهت تایم بالا", "ok": bool(htf_bias in ("BULL", "BEAR"))},
        {
            "name": u"جاروی Judas",
            "ok": bool(live or f.get("sweep") or sig.get("sweep_kind")),
        },
        {"name": u"MSS", "ok": bool(sig.get("mss") or f.get("mss"))},
        {
            "name": u"FVG",
            "ok": (sig.get("fvg_bot") is not None) or bool(f.get("fvg")),
        },
        {
            "name": u"ورود در شکاف",
            "ok": bool(sig.get("inside_fvg") or f.get("in_fvg")),
        },
        {"name": u"OTE", "ok": bool(sig.get("ote"))},
        {"name": u"کیل‌زون", "ok": bool(kz_ok or f.get("kz"))},
        {"name": u"پرمیوم/دیسکانت", "ok": bool(sig.get("aligned"))},
    ]
    out["score"] = int(sig.get("score") or 0)
    out["tf"] = sig.get("tf_label") or sig.get("tf") or ""
    if kz_raw:
        out["kz"] = kz_raw
    out["setup"] = sig.get("setup") or ""
    if live:
        side = sig.get("side")
        out["side"] = side
        out["live"] = True
        out["color"] = "buy" if side == "BUY" else "sell"
        out["action"] = u"بخر" if side == "BUY" else u"بفروش"
        why = sig.get("setup") or sig.get("reason") or u""
        if not why:
            why = u"ستاپ ICT کامل است. ورود فقط داخل شکاف؛ تعقیب نکن."
        out["why"] = why
        if sig.get("entry") is not None:
            out["entry"] = fmt_px(pair, sig["entry"])
        if sig.get("sl") is not None:
            out["sl"] = fmt_px(pair, sig["sl"])
        if sig.get("tp") is not None:
            out["tp"] = fmt_px(pair, sig["tp"])
    else:
        out["why"] = sig.get("reason") or out["why"]
    return out


def miniapp_lessons(uid=None):
    lang = get_lang(uid) if uid else "fa"
    out = []
    for k in EDU_ORDER:
        lv = "1"
        for a, ks in EDU_LEVELS.items():
            if k in ks:
                lv = a
                break
        title = EDU_TITLE.get(k, k)
        html = EDU.get(k) or ""
        if lang == "en" and _i18n_mod is not None:
            title = _i18n_mod.edu_title("en", k, title)
            html = _i18n_mod.edu_html("en", k, html)
        out.append(
            {
                "id": k,
                "n": _edu_n(k),
                "title": title,
                "level": lv,
                "html": html,
                "audio": "?app=audio&k=" + k + "&v=fa2",
            }
        )
    return out


def miniapp_chat(uid, text):
    if not uid or not is_pro(uid):
        return {"ok": False, "pay": True}
    text = (text or "").strip()[:1200]
    if not text:
        return {"ok": False, "err": T("txt.coach_empty")}
    if too_soon("appai:%s" % uid, 2):
        return {"ok": False, "err": T("txt.coach_wait")}
    if (not is_owner(uid)) and over_hour("aih:%s" % uid, 40):
        return {"ok": False, "err": u"سهم چت این ساعت پر شد"}
    try:
        rec0 = load_user_mem(uid)
        ans, rec = coach_reply(uid, text, topic=rec0.get("topic"))
    except Exception:
        log("app chat " + traceback.format_exc())
        ans = local_brain(text)
    if not ans:
        ans = u"الان مربی شلوغ است. کمی بعد دوباره بپرس."
    return {"ok": True, "ans": ans}


def miniapp_state(uid=None):
    pro = bool(uid and is_pro(uid))
    user = None
    if uid:
        user = {
            "id": uid,
            "pro": pro,
            "until": tehran_fmt(sub_until(uid)) if pro else "",
        }
    if uid:
        try:
            use_lang(uid)
        except Exception:
            pass
    lessons = miniapp_lessons(uid)
    base = {
        "ok": True,
        "lang": get_lang(uid) if uid else "fa",
        "time": tehran_fmt(),
        "kz": in_killzone(int(time.time())) or u"خارج از کیل‌زون",
        "kz_pct": 72 if in_killzone(int(time.time())) else 8,
        "sb": bool(in_silver_bullet(int(time.time()))),
        "pro": pro,
        "pay": not pro,
        "user": user,
        "lessons": lessons,
        "bot": BOT_URL,
        "vip": PRO_URL,
        "univ": 0,
        "fx": fx_open_line(),
    }
    try:
        base["univ"] = len((load_crypto_universe() or {}).get("syms") or {})
    except Exception:
        pass
    if not pro:
        base["pairs"] = [
            {"id": p, "name": m["name"], "emoji": m["emoji"], "locked": True}
            for p, m in PAIRS.items()
            if p in FX_PAIRS
        ]
        return base

    pairs = []
    px_map = {}
    icts = []
    for pair, meta in PAIRS.items():
        if pair not in FX_PAIRS:
            continue
        try:
            rows = fetch_ohlc(pair, "15m", "10d") or []
        except Exception:
            rows = []
        px = rows[-1]["c"] if rows else None
        if px is not None:
            px_map[pair] = px
        b = tf_bias(rows) if rows else {}
        chg = 0.0
        if len(rows) > 20 and rows[-20]["c"]:
            chg = (rows[-1]["c"] - rows[-20]["c"]) / rows[-20]["c"] * 100.0
        spark = []
        try:
            spark = [
                round(float(r["c"]), 5 if pair != "XAUUSD" else 2) for r in rows[-24:]
            ]
        except Exception:
            spark = []
        ict = {}
        try:
            htf = None
            try:
                htf = htf_context(pair, px or 0) if rows else None
            except Exception:
                htf = None
            sig15 = ict_2022(rows, pair, interval="15m", htf=htf) if rows else None
            ict = miniapp_ict_blob(pair, sig15)
        except Exception:
            log("app ict " + traceback.format_exc())
            ict = miniapp_ict_blob(pair, None)
        pairs.append(
            {
                "id": pair,
                "name": meta["name"],
                "emoji": meta["emoji"],
                "px": fmt_px(pair, px) if px is not None else "-",
                "bias": b.get("bias") or "-",
                "pd": b.get("pd") or "-",
                "chg": round(chg, 2),
                "spark": spark,
                "locked": False,
                "ict": {
                    "side": ict.get("side"),
                    "action": ict.get("action"),
                    "color": ict.get("color"),
                    "why": ict.get("why") or "",
                    "live": bool(ict.get("live")),
                    "score": ict.get("score") or 0,
                    "tf": ict.get("tf") or "",
                },
            }
        )
        icts.append(ict)
    best_ict = None
    live_i = [x for x in icts if x.get("side") in ("BUY", "SELL")]
    if live_i:
        live_i.sort(key=lambda x: -int(x.get("score") or 0))
        best_ict = live_i[0]
    base["pairs"] = pairs
    base["best_ict"] = {
        "pair": (best_ict or {}).get("pair"),
        "action": (best_ict or {}).get("action") or u"صبر",
        "side": (best_ict or {}).get("side") or "WAIT",
        "why": (best_ict or {}).get("why") or u"الان ستاپ ICT کامل نیست.",
        "live": bool(best_ict),
    }
    base["wr"] = miniapp_wr_blob()
    base["daily"] = daily_r_blob(px_map)
    return base



def miniapp_hot(limit=16):
    out = []
    n = 0
    try:
        n = len((load_crypto_universe() or {}).get("syms") or {})
    except Exception:
        n = 0
    seen = set()
    want = list(CRYPTO_CORE[:8])
    try:
        want += [x[1] for x in crypto_hot(24)]
    except Exception:
        pass
    for pair in want:
        if pair in seen:
            continue
        seen.add(pair)
        try:
            ensure_crypto_pair(pair)
        except Exception:
            continue
        if pair not in PAIRS:
            continue
        try:
            rows = _ohlc_cache.get(pair + "|15m") or fetch_ohlc(pair, "15m", "10d") or []
        except Exception:
            rows = []
        px = rows[-1]["c"] if rows else None
        chg = 0.0
        if len(rows) > 16 and rows[-16]["c"]:
            try:
                chg = (rows[-1]["c"] - rows[-16]["c"]) / rows[-16]["c"] * 100.0
            except Exception:
                chg = 0.0
        spark = []
        try:
            spark = [round(float(r["c"]), 6) for r in rows[-20:]]
        except Exception:
            spark = []
        ict = miniapp_ict_blob(pair, None)
        try:
            if rows:
                htf = htf_context(pair, px or 0) or {}
                sig = ict_2022(rows, pair, interval="15m", htf=htf)
                ict = miniapp_ict_blob(pair, sig)
        except Exception:
            pass
        meta = PAIRS.get(pair) or {}
        out.append(
            {
                "id": pair,
                "name": meta.get("name") or pair,
                "emoji": meta.get("emoji") or "",
                "px": fmt_px(pair, px) if px is not None else "-",
                "bias": "-",
                "pd": "-",
                "chg": round(chg, 2),
                "spark": spark,
                "ict": {
                    "side": ict.get("side"),
                    "action": ict.get("action"),
                    "color": ict.get("color"),
                    "why": ict.get("why") or "",
                    "score": ict.get("score") or 0,
                },
            }
        )
        if len(out) >= limit:
            break
    return {"ok": True, "pairs": out, "univ": n}


def miniapp_desk(uid=None):
    wr = miniapp_wr_blob()
    paper = {}
    try:
        if uid:
            _d, acc = paper_acc(uid, create=False)
            if acc:
                paper = {
                    "on": bool(acc.get("on")),
                    "bal": acc.get("bal"),
                    "wins": acc.get("wins"),
                    "loss": acc.get("loss"),
                }
    except Exception:
        paper = {}
    radar = []
    for pair in list(FX_PAIRS) + list(CRYPTO_CORE[:6]):
        try:
            rows = _ohlc_cache.get(pair + "|15m") or []
            if len(rows) < 24:
                continue
            htf = htf_context(pair, rows[-1]["c"]) or {}
            sig = ict_2022(rows, pair, interval="15m", htf=htf)
            side = (sig or {}).get("side")
            if side in ("BUY", "SELL"):
                radar.append(
                    {
                        "pair": pair,
                        "side": side,
                        "sc": (sig or {}).get("score") or 0,
                    }
                )
        except Exception:
            continue
    n = 0
    try:
        n = len((load_crypto_universe() or {}).get("syms") or {})
    except Exception:
        n = 0
    return {
        "ok": True,
        "fx": fx_open_line(),
        "kz": in_killzone(int(time.time())) or u"خارج",
        "sb": bool(in_silver_bullet(int(time.time()))),
        "news": news_window() or "",
        "wr": wr,
        "paper": paper,
        "radar": radar[:8],
        "univ": n,
        "next": next_session_line() if "next_session_line" in dir() else "",
    }


def miniapp_signal(pair):
    pair = (pair or "").upper().strip()
    if pair and not pair.endswith("USDT") and pair not in FX_PAIRS and pair != "XAUUSD":
        if len(pair) <= 12:
            pair = pair + "USDT"
    if pair not in PAIRS:
        try:
            ensure_crypto_pair(pair, probe=True)
        except Exception:
            pass
    if pair not in PAIRS:
        return {"ok": False}
    ict = miniapp_ict_blob(pair, None)
    try:
        sig = scan_signal(pair)
        ict = miniapp_ict_blob(pair, sig)
    except Exception:
        log("app scan " + traceback.format_exc())
    return {"ok": True, "pair": pair, "ict": ict}


def miniapp_html_bytes():
    try:
        with open(APP_FILE, "rb") as f:
            return f.read()
    except Exception:
        return (
            b"<!doctype html><meta charset=utf-8><title>TZ FX</title>"
            b"<body style='background:#05060c;color:#fff;font-family:sans-serif;padding:24px'>"
            b"TZ FX Mini App</body>"
        )


def _want_app(environ):
    uri = environ.get("REQUEST_URI") or ""
    pi = environ.get("PATH_INFO") or ""
    qs = environ.get("QUERY_STRING") or ""
    return (
        "app=1" in qs
        or "app=api" in qs
        or "app=audio" in qs
        or "/app" in pi
        or "/app" in uri
    )


def handle_miniapp(environ, start_response):
    method = (environ.get("REQUEST_METHOD") or "GET").upper()
    qs = environ.get("QUERY_STRING") or ""
    uri = (environ.get("REQUEST_URI") or "") + (environ.get("PATH_INFO") or "")
    if "app=audio" in qs:
        key = (_qs_get(environ, "k") or "").strip()
        raw = b""
        if key in ("coach", "say"):
            try:
                init = environ.get("HTTP_X_INIT_DATA") or _qs_get(environ, "init") or ""
                uid = webapp_uid(init, load_token())
            except Exception:
                uid = None
            if uid:
                rec = load_user_mem(uid)
                spoken = strip_html(rec.get("last_ans") or "")
                if spoken:
                    raw = tts_fa(spoken, fmt="ogg", quick=True)
        elif key in EDU:
            raw = load_edu_audio(key, build=False)
        if not raw:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"missing"]
        if raw[:4] == b"OggS":
            ctype = "audio/ogg"
        elif raw[:4] == b"RIFF":
            ctype = "audio/wav"
        elif raw[:4] == b"\x1aE\xdf\xa3":
            ctype = "audio/webm"
        else:
            ctype = "audio/mpeg"
        start_response(
            "200 OK",
            [
                ("Content-Type", ctype),
                ("Cache-Control", "no-store"),
                ("Content-Length", str(len(raw))),
                ("Access-Control-Allow-Origin", "*"),
            ],
        )
        return [raw]
    is_api = "app=api" in qs or "/api" in uri
    uid = None
    try:
        init = environ.get("HTTP_X_INIT_DATA") or _qs_get(environ, "init") or ""
        uid = webapp_uid(init, load_token())
    except Exception:
        uid = None
    pro = bool(uid and is_pro(uid))
    try:
        if uid:
            use_lang(uid)
    except Exception:
        pass
    payload = {}
    if method == "POST" and is_api:
        try:
            n = int(environ.get("CONTENT_LENGTH") or 0)
        except Exception:
            n = 0
        rawb = environ["wsgi.input"].read(n) if n else b"{}"
        try:
            payload = json.loads(rawb.decode("utf-8") or "{}")
        except Exception:
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
    if is_api:
        v = payload.get("v") or _qs_get(environ, "v") or "state"
        if v == "signal":
            if not pro:
                body = json.dumps({"ok": False, "pay": True}, ensure_ascii=False)
            else:
                pair = (payload.get("pair") or _qs_get(environ, "pair") or "XAUUSD").upper()
                body = json.dumps(miniapp_signal(pair), ensure_ascii=False)
        elif v == "chat":
            if not pro:
                body = json.dumps({"ok": False, "pay": True}, ensure_ascii=False)
            else:
                q = payload.get("q") or payload.get("text") or _qs_get(environ, "q") or ""
                body = json.dumps(miniapp_chat(uid, q), ensure_ascii=False)
        elif v == "lesson":
            key = payload.get("k") or _qs_get(environ, "k") or ""
            hit = None
            for it in miniapp_lessons(uid):
                if it["id"] == key:
                    hit = it
                    break
            body = json.dumps({"ok": bool(hit), "lesson": hit}, ensure_ascii=False)
        elif v == "hot":
            if not pro:
                body = json.dumps({"ok": False, "pay": True}, ensure_ascii=False)
            else:
                body = json.dumps(miniapp_hot(), ensure_ascii=False)
        elif v == "lang":
            code = (payload.get("lang") or _qs_get(environ, "lang") or "").lower()
            if uid and code in ("fa", "en"):
                set_lang(uid, code)
                use_lang(uid)
            body = json.dumps({"ok": True, "lang": get_lang(uid) if uid else "fa"}, ensure_ascii=False)
        elif v == "desk":
            if not pro:
                body = json.dumps({"ok": False, "pay": True}, ensure_ascii=False)
            else:
                body = json.dumps(miniapp_desk(uid), ensure_ascii=False)
        else:
            body = json.dumps(miniapp_state(uid), ensure_ascii=False)
        data = body.encode("utf-8")
        start_response(
            "200 OK",
            [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Cache-Control", "no-store"),
                ("Access-Control-Allow-Origin", "*"),
            ],
        )
        return [data]
    html = miniapp_html_bytes()
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Cache-Control", "no-store"),
        ],
    )
    return [html]


def application(environ, start_response):
    method = (environ.get("REQUEST_METHOD") or "GET").upper()
    qs = environ.get("QUERY_STRING") or ""
    if "app=bridge" in qs:
        return handle_bridge_http(environ, start_response)
    if "app=tick" in qs:
        try:
            process_once_locked(timeout=0)
        except Exception:
            log("tick fail " + traceback.format_exc().split("\n")[0][:120])
    if _want_app(environ):
        return handle_miniapp(environ, start_response)
    if method == "POST":
        try:
            n = int(environ.get("CONTENT_LENGTH") or 0)
        except Exception:
            n = 0
        raw = environ["wsgi.input"].read(n) if n else b""
        try:
            log("HTTP POST n=%s" % n)
        except Exception:
            pass
        process_webhook(raw)
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"ok"]
    if _qs_get(environ, "k"):
        status, ctype, body = admin_web(environ)
        start_response(status, [("Content-Type", ctype)])
        return [body]
    err = _bot_error
    if err:
        err = str(err).split("\n")[0][:80]
    poll = _last_poll
    try:
        if os.path.isfile(HB_FILE):
            hb = float(open(HB_FILE).read().strip() or 0)
            if hb:
                poll = tehran_fmt(hb, "%H:%M")
    except Exception:
        pass
    tick = "-"
    try:
        if os.path.isfile(TICK_FILE):
            tick = tehran_fmt(float(open(TICK_FILE).read().strip() or 0), "%H:%M")
    except Exception:
        pass
    body = "TZ FX online v=%s webhook=%s last=%s poll=%s tick=%s error=%s py=%s\n" % (
        BOT_VERSION,
        webhook_enabled(),
        _last_signal,
        poll,
        tick,
        err,
        sys.version.split()[0],
    )
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [body.encode("utf-8")]

if __name__ == "__main__":
    process_once_locked(timeout=0)
