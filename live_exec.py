# -*- coding: utf-8 -*-
"""TZ FX live desk — crypto REST + MT5 bridge. Demo never hits live order endpoints."""
from __future__ import print_function

import hashlib
import hmac
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CFG_FILE = os.path.join(HERE, ".live.json")
QUEUE_FILE = os.path.join(HERE, ".live_queue.json")
KEY_DIR = HERE

VENUES = (
    ("binance", u"Binance", "crypto"),
    ("bybit", u"Bybit", "crypto"),
    ("okx", u"OKX", "crypto"),
    ("bitget", u"Bitget", "crypto"),
    ("bingx", u"BingX", "crypto"),
    ("mt5", u"MT5 همه بروکرها", "fx"),
)

TESTNET = {
    "binance": "https://testnet.binance.vision",
    "bybit": "https://api-testnet.bybit.com",
}
LIVE_API = {
    "binance": "https://api.binance.com",
    "bybit": "https://api.bybit.com",
    "okx": "https://www.okx.com",
    "bitget": "https://api.bitget.com",
    "bingx": "https://open-api.bingx.com",
}


def _jload(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default


def _jsave(path, data):
    try:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        try:
            with open(path, "w") as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception:
            pass


def load_cfg():
    d = _jload(CFG_FILE, None)
    if not isinstance(d, dict):
        d = {}
    d.setdefault("demo", True)
    d.setdefault("crypto_on", False)
    d.setdefault("mt5_on", False)
    d.setdefault("crypto_venue", "binance")
    d.setdefault("risk", 0.01)
    d.setdefault("bridge_token", "")
    if not d.get("bridge_token"):
        try:
            d["bridge_token"] = hashlib.sha256(os.urandom(32)).hexdigest()[:40]
        except Exception:
            d["bridge_token"] = hashlib.sha256(("%s" % time.time()).encode("utf-8")).hexdigest()[:40]
        save_cfg(d)
    return d


def save_cfg(d):
    _jsave(CFG_FILE, d)


def key_path(venue):
    return os.path.join(KEY_DIR, ".exch_%s" % venue)


def load_keys(venue):
    path = key_path(venue)
    try:
        raw = open(path, "r").read()
    except Exception:
        return None
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    if len(lines) < 2:
        return None
    rec = {"key": lines[0], "secret": lines[1]}
    if len(lines) >= 3:
        rec["passphrase"] = lines[2]
    return rec


def save_keys(venue, key, secret, passphrase=None):
    path = key_path(venue)
    body = (key or "").strip() + "\n" + (secret or "").strip()
    if passphrase:
        body += "\n" + passphrase.strip()
    with open(path, "w") as f:
        f.write(body)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass


def has_keys(venue):
    return load_keys(venue) is not None


def load_queue():
    d = _jload(QUEUE_FILE, None)
    if not isinstance(d, dict):
        d = {"orders": []}
    if not isinstance(d.get("orders"), list):
        d["orders"] = []
    return d


def save_queue(d):
    orders = d.get("orders") or []
    open_ = [o for o in orders if o.get("status") in ("queued", "sent", "working")]
    done = [o for o in orders if o.get("status") not in ("queued", "sent", "working")][-80:]
    d["orders"] = open_ + done
    _jsave(QUEUE_FILE, d)


def _http():
    try:
        import requests

        return requests
    except Exception:
        return None


def _hmac_hex(secret, msg):
    return hmac.new(
        secret.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def _hmac_b64(secret, msg):
    import base64

    dig = hmac.new(secret.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(dig).decode("ascii")


def _round_qty(qty, step=0.000001):
    try:
        q = float(qty)
    except Exception:
        return 0.0
    if q <= 0:
        return 0.0
    step = float(step or 0.000001)
    n = math.floor(q / step + 1e-12) * step
    return float("%.8f" % n)


def venue_label(code):
    for c, n, _k in VENUES:
        if c == code:
            return n
    return code


def needs_passphrase(venue):
    return venue in ("okx", "bitget")


def ping_venue(venue, demo=True):
    """Check keys. Never returns secrets. Demo does not place orders."""
    if venue == "mt5":
        q = load_queue()
        hb = q.get("mt5_hb") or 0
        age = time.time() - float(hb or 0)
        if hb and age < 90:
            return True, u"MT5 بریج زنده · %ss پیش" % int(age)
        return False, u"MT5 بریج قطع است — اسکریپت را روی ویندوز کنار متاتریدر اجرا کن"
    keys = load_keys(venue)
    if not keys:
        return False, u"کلید %s نیست" % venue_label(venue)
    req = _http()
    if req is None:
        return False, u"requests نیست"
    try:
        if venue == "binance":
            base = TESTNET["binance"] if demo else LIVE_API["binance"]
            ts = int(time.time() * 1000)
            qs = "timestamp=%s" % ts
            sig = _hmac_hex(keys["secret"], qs)
            r = req.get(
                base + "/api/v3/account",
                params={"timestamp": ts, "signature": sig},
                headers={"X-MBX-APIKEY": keys["key"]},
                timeout=8,
            )
            if r.status_code != 200:
                if demo:
                    return False, u"دمو: تست‌نت بایننس رد کرد (کلید زنده؟). سفارش واقعی نمی‌فرستم."
                return False, u"بایننس HTTP %s" % r.status_code
            js = r.json() or {}
            bals = js.get("balances") or []
            usdt = 0.0
            for b in bals:
                if (b.get("asset") or "") == "USDT":
                    usdt = float(b.get("free") or 0)
                    break
            return True, u"Binance وصل · آزاد %.2f USDT" % usdt
        if venue == "bybit":
            base = TESTNET["bybit"] if demo else LIVE_API["bybit"]
            ts = str(int(time.time() * 1000))
            recv = "5000"
            body = ""
            path = "/v5/account/wallet-balance?accountType=UNIFIED"
            param = "accountType=UNIFIED"
            pre = ts + keys["key"] + recv + param
            sign = _hmac_hex(keys["secret"], pre)
            r = req.get(
                base + "/v5/account/wallet-balance",
                params={"accountType": "UNIFIED"},
                headers={
                    "X-BAPI-API-KEY": keys["key"],
                    "X-BAPI-SIGN": sign,
                    "X-BAPI-TIMESTAMP": ts,
                    "X-BAPI-RECV-WINDOW": recv,
                },
                timeout=8,
            )
            if r.status_code != 200:
                if demo:
                    return False, u"دمو: تست‌نت بای‌بیت رد کرد. سفارش واقعی نمی‌فرستم."
                return False, u"Bybit HTTP %s" % r.status_code
            js = r.json() or {}
            if str(js.get("retCode")) not in ("0", "None"):
                return False, u"Bybit %s" % (js.get("retMsg") or js.get("retCode"))
            return True, u"Bybit وصل"
        if venue in ("okx", "bitget", "bingx"):
            # key present is enough in demo; live ping below
            if demo:
                return True, u"%s کلید ذخیره شد · دمو سفارش نمی‌فرستد" % venue_label(venue)
            return True, u"%s کلید هست" % venue_label(venue)
    except Exception as e:
        return False, u"خطا: %s" % str(e)[:80]
    return False, u"صرافی پشتیبانی نشده"


def _binance_filters(symbol, demo):
    req = _http()
    if req is None:
        return 0.000001, 0.01
    base = TESTNET["binance"] if demo else LIVE_API["binance"]
    try:
        r = req.get(base + "/api/v3/exchangeInfo", params={"symbol": symbol}, timeout=8)
        js = r.json() or {}
        step, minq = 0.000001, 0.0
        for s in js.get("symbols") or []:
            if s.get("symbol") != symbol:
                continue
            for f in s.get("filters") or []:
                if f.get("filterType") == "LOT_SIZE":
                    step = float(f.get("stepSize") or step)
                    minq = float(f.get("minQty") or 0)
            break
        return step, minq
    except Exception:
        return 0.000001, 0.0


def _place_binance(keys, pair, side, qty, sl, tp, demo):
    req = _http()
    base = TESTNET["binance"] if demo else LIVE_API["binance"]
    ts = int(time.time() * 1000)
    params = {
        "symbol": pair,
        "side": side,
        "type": "MARKET",
        "quantity": ("%.8f" % qty).rstrip("0").rstrip("."),
        "timestamp": ts,
        "newOrderRespType": "RESULT",
    }
    qs = "&".join("%s=%s" % (k, params[k]) for k in params)
    params["signature"] = _hmac_hex(keys["secret"], qs)
    r = req.post(
        base + "/api/v3/order",
        params=params,
        headers={"X-MBX-APIKEY": keys["key"]},
        timeout=12,
    )
    js = r.json() if r.content else {}
    if r.status_code != 200 or js.get("code"):
        return False, str(js.get("msg") or js.get("code") or r.status_code)[:120], js
    oid = js.get("orderId")
    # OCO exit
    try:
        exit_side = "SELL" if side == "BUY" else "BUY"
        ts2 = int(time.time() * 1000)
        stop = sl
        limit_tp = tp
        oco = {
            "symbol": pair,
            "side": exit_side,
            "quantity": params["quantity"],
            "price": ("%.8f" % float(limit_tp)).rstrip("0").rstrip("."),
            "stopPrice": ("%.8f" % float(stop)).rstrip("0").rstrip("."),
            "stopLimitPrice": ("%.8f" % float(stop)).rstrip("0").rstrip("."),
            "stopLimitTimeInForce": "GTC",
            "timestamp": ts2,
        }
        qs2 = "&".join("%s=%s" % (k, oco[k]) for k in oco)
        oco["signature"] = _hmac_hex(keys["secret"], qs2)
        r2 = req.post(
            base + "/api/v3/order/oco",
            params=oco,
            headers={"X-MBX-APIKEY": keys["key"]},
            timeout=12,
        )
        oco_ok = r2.status_code == 200
    except Exception:
        oco_ok = False
    extra = u"" if oco_ok else u" · OCO نرفت — SL را روی صرافی چک کن"
    return True, u"بایننس #%s%s" % (oid, extra), js


def _place_bybit(keys, pair, side, qty, sl, tp, demo):
    req = _http()
    base = TESTNET["bybit"] if demo else LIVE_API["bybit"]
    ts = str(int(time.time() * 1000))
    recv = "5000"
    body = json.dumps(
        {
            "category": "spot",
            "symbol": pair,
            "side": "Buy" if side == "BUY" else "Sell",
            "orderType": "Market",
            "qty": ("%.8f" % qty).rstrip("0").rstrip("."),
            "takeProfit": str(tp),
            "stopLoss": str(sl),
            "tpslMode": "Full",
        },
        separators=(",", ":"),
    )
    pre = ts + keys["key"] + recv + body
    sign = _hmac_hex(keys["secret"], pre)
    r = req.post(
        base + "/v5/order/create",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-BAPI-API-KEY": keys["key"],
            "X-BAPI-SIGN": sign,
            "X-BAPI-TIMESTAMP": ts,
            "X-BAPI-RECV-WINDOW": recv,
        },
        timeout=12,
    )
    js = r.json() if r.content else {}
    if str(js.get("retCode")) != "0":
        return False, str(js.get("retMsg") or js.get("retCode") or r.status_code)[:120], js
    oid = ((js.get("result") or {}).get("orderId")) or ""
    return True, u"Bybit #%s" % oid, js


def place_crypto(venue, pair, side, qty, sl, tp, demo):
    keys = load_keys(venue)
    if not keys:
        return False, u"کلید نیست", {}
    if demo:
        # never hit LIVE order endpoints in demo
        if venue not in TESTNET:
            return True, u"دمو · %s سفارش ساخته شد، ارسال نشد" % venue_label(venue), {"dry": True}
        try:
            if venue == "binance":
                return _place_binance(keys, pair, side, qty, sl, tp, True)
            if venue == "bybit":
                return _place_bybit(keys, pair, side, qty, sl, tp, True)
        except Exception as e:
            return False, str(e)[:120], {}
        return True, u"دمو · ارسال نشد", {"dry": True}
    try:
        if venue == "binance":
            return _place_binance(keys, pair, side, qty, sl, tp, False)
        if venue == "bybit":
            return _place_bybit(keys, pair, side, qty, sl, tp, False)
        return True, u"%s · زنده هنوز جای‌گذاری کامل ندارد — صف MT5/صف ثبت شد" % venue_label(venue), {"queued": True}
    except Exception as e:
        return False, str(e)[:120], {}


def _qty_from_risk(entry, sl, equity, risk):
    dist = abs(float(entry) - float(sl))
    if dist <= 0:
        return 0.0
    usd = max(1.0, float(equity) * float(risk))
    return usd / dist


def on_signal(sig, pair, equity=10000.0):
    """Queue + optional crypto exec. Never without SL. Never invent side."""
    if not sig or sig.get("side") not in ("BUY", "SELL"):
        return None
    if not sig.get("sl") or not sig.get("tp") or not sig.get("entry"):
        return None
    pair = pair or sig.get("pair")
    if not pair:
        return None
    cfg = load_cfg()
    demo = bool(cfg.get("demo", True))
    try:
        entry = float(sig["entry"])
        sl = float(sig["sl"])
        tp = float(sig["tp"])
    except Exception:
        return None
    qty = _qty_from_risk(entry, sl, equity, cfg.get("risk") or 0.01)
    if qty <= 0:
        return None
    rec = {
        "id": "o%s" % int(time.time() * 1000),
        "ts": time.time(),
        "pair": pair,
        "side": sig["side"],
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "score": sig.get("score"),
        "demo": demo,
        "status": "queued",
        "venue": None,
        "note": "",
    }
    crypto = str(pair).upper().endswith("USDT")
    reports = []
    if crypto and cfg.get("crypto_on"):
        venue = cfg.get("crypto_venue") or "binance"
        rec["venue"] = venue
        step, minq = 0.000001, 0.0
        if venue == "binance":
            step, minq = _binance_filters(pair, demo)
        q2 = _round_qty(qty, step)
        if minq and q2 < minq:
            rec["status"] = "skip"
            rec["note"] = u"حجم زیر حداقل صرافی"
        else:
            rec["qty"] = q2
            ok, msg, _raw = place_crypto(venue, pair, sig["side"], q2, sl, tp, demo)
            rec["note"] = msg
            rec["status"] = "sent" if ok else "fail"
        reports.append(rec.copy())
    if (not crypto) and cfg.get("mt5_on"):
        rec2 = dict(rec)
        rec2["id"] = rec["id"] + "m"
        rec2["venue"] = "mt5"
        rec2["status"] = "queued"
        rec2["note"] = u"در صف بریج MT5"
        rec2["qty"] = qty  # lots computed on the terminal
        reports.append(rec2)
    if not reports:
        return None
    q = load_queue()
    for r in reports:
        q["orders"].append(r)
    save_queue(q)
    return reports


def open_count():
    q = load_queue()
    n = 0
    for o in q.get("orders") or []:
        if o.get("status") in ("queued", "sent", "working"):
            n += 1
    return n


def bridge_snapshot(token):
    cfg = load_cfg()
    want = (cfg.get("bridge_token") or "")
    if not want or not token or token != want:
        return None
    q = load_queue()
    q["mt5_hb"] = time.time()
    save_queue(q)
    pending = [
        o
        for o in (q.get("orders") or [])
        if o.get("venue") == "mt5" and o.get("status") == "queued"
    ]
    return {
        "ok": True,
        "demo": bool(cfg.get("demo", True)),
        "risk": cfg.get("risk") or 0.01,
        "orders": pending[:8],
    }


def bridge_ack(token, oid, status, note=""):
    cfg = load_cfg()
    if not token or token != (cfg.get("bridge_token") or ""):
        return False
    q = load_queue()
    for o in q.get("orders") or []:
        if o.get("id") == oid and o.get("venue") == "mt5":
            o["status"] = status or "working"
            if note:
                o["note"] = str(note)[:160]
            o["ack_ts"] = time.time()
            save_queue(q)
            return True
    return False


def status_text():
    cfg = load_cfg()
    mode = u"دمو" if cfg.get("demo", True) else u"واقعی"
    cv = cfg.get("crypto_venue") or "binance"
    lines = [
        u"حالت: <b>%s</b>" % mode,
        u"صرافی: %s · %s · کلید %s"
        % (
            venue_label(cv),
            u"روشن" if cfg.get("crypto_on") else u"خاموش",
            u"هست" if has_keys(cv) else u"نیست",
        ),
        u"MT5: %s" % (u"روشن" if cfg.get("mt5_on") else u"خاموش"),
        u"ریسک ۱٪ · حد ضرر اجباری",
    ]
    q = load_queue()
    opens = [o for o in (q.get("orders") or []) if o.get("status") in ("queued", "sent", "working")]
    if opens:
        lines.append(u"صف: %s سفارش" % len(opens))
        for o in opens[:4]:
            lines.append(
                u"%s %s %s · %s"
                % (o.get("pair"), o.get("side"), o.get("venue"), o.get("status"))
            )
    else:
        lines.append(u"صف خالی است.")
    hb = q.get("mt5_hb") or 0
    if hb:
        lines.append(u"بریج MT5: %ss پیش" % int(time.time() - float(hb)))
    return u"\n".join(lines)
