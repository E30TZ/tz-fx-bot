# -*- coding: utf-8 -*-
"""TZ FX MT5 bridge — run on the Windows PC where MetaTrader 5 is logged in.
Works with ANY MT5 broker (Exness, Alpari, IC Markets, ...).

  pip install MetaTrader5 requests
  python tz_mt5_bridge.py https://ehsantz.pingbaz.space/bot/index.cgi YOUR_TOKEN

Log into a DEMO account in MT5 first. Always sends SL+TP.
"""
from __future__ import print_function

import json
import sys
import time

try:
    import requests
except ImportError:
    print("pip install requests")
    sys.exit(1)
try:
    import MetaTrader5 as mt5
except ImportError:
    print("Windows + MT5 + pip install MetaTrader5")
    sys.exit(1)

MAGIC = 202209
POLL = 8


def _url(base):
    base = (base or "").rstrip("/")
    if "app=bridge" not in base:
        sep = "&" if "?" in base else "?"
        base = base + sep + "app=bridge"
    return base


def _sym(pair):
    p = (pair or "").upper()
    alts = [p]
    if p == "XAUUSD":
        alts += ["GOLD", "XAUUSD.", "XAUUSDm"]
    if p.endswith("USDT"):
        return []
    for a in alts:
        info = mt5.symbol_info(a)
        if info:
            if not info.visible:
                mt5.symbol_select(a, True)
            return a
    return p


def _lots(symbol, entry, sl, equity, risk):
    info = mt5.symbol_info(symbol)
    if info is None:
        return 0.0
    dist = abs(float(entry) - float(sl))
    if dist <= 0:
        return 0.0
    tick_val = float(info.trade_tick_value or 0) or 1.0
    tick_sz = float(info.trade_tick_size or 0) or float(info.point or 0.0001)
    if tick_sz <= 0:
        tick_sz = 0.0001
    usd_per_lot = (dist / tick_sz) * tick_val
    if usd_per_lot <= 0:
        return float(info.volume_min or 0.01)
    raw = (float(equity) * float(risk)) / usd_per_lot
    step = float(info.volume_step or 0.01) or 0.01
    mn = float(info.volume_min or 0.01)
    mx = float(info.volume_max or 100)
    n = max(mn, min(mx, (int(raw / step) * step)))
    return float("%.2f" % n)


def _fill(symbol, side, lots, sl, tp):
    info = mt5.symbol_info(symbol)
    tick = mt5.symbol_info_tick(symbol)
    if info is None or tick is None:
        return False, "no tick"
    order_type = mt5.ORDER_TYPE_BUY if side == "BUY" else mt5.ORDER_TYPE_SELL
    price = tick.ask if side == "BUY" else tick.bid
    filling_opts = []
    filling = info.filling_mode
    for mode in (mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_RETURN):
        filling_opts.append(mode)
    last = "no fill"
    for mode in filling_opts:
        req = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lots),
            "type": order_type,
            "price": float(price),
            "sl": float(sl),
            "tp": float(tp),
            "deviation": 30,
            "magic": MAGIC,
            "comment": "TZFX",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mode,
        }
        res = mt5.order_send(req)
        if res and res.retcode == mt5.TRADE_RETCODE_DONE:
            return True, "ticket %s" % res.order
        last = "ret %s %s" % (
            getattr(res, "retcode", "?"),
            getattr(res, "comment", ""),
        )
    return False, last[:120]


def main():
    if len(sys.argv) < 3:
        print("usage: python tz_mt5_bridge.py BRIDGE_URL TOKEN")
        sys.exit(2)
    url = _url(sys.argv[1])
    token = sys.argv[2]
    if not mt5.initialize():
        print("MT5 initialize failed", mt5.last_error())
        sys.exit(1)
    acc = mt5.account_info()
    print("MT5", getattr(acc, "login", None), getattr(acc, "server", None), getattr(acc, "trade_mode", None))
    print("polling", url)
    while True:
        try:
            r = requests.get(url, params={"token": token}, timeout=20)
            data = r.json() if r.content else {}
        except Exception as e:
            print("poll", e)
            time.sleep(POLL)
            continue
        if not data.get("ok"):
            print("auth/bridge", data)
            time.sleep(POLL)
            continue
        equity = float(getattr(mt5.account_info(), "equity", 0) or 0) or 10000.0
        risk = float(data.get("risk") or 0.01)
        for o in data.get("orders") or []:
            oid = o.get("id")
            pair = o.get("pair")
            side = o.get("side")
            if side not in ("BUY", "SELL") or not o.get("sl"):
                requests.get(
                    url,
                    params={"token": token, "ack": oid, "status": "skip", "note": "no-sl"},
                    timeout=12,
                )
                continue
            symbol = _sym(pair)
            if not symbol:
                requests.get(
                    url,
                    params={"token": token, "ack": oid, "status": "skip", "note": "fx-only"},
                    timeout=12,
                )
                continue
            lots = _lots(symbol, o.get("entry"), o.get("sl"), equity, risk)
            if lots <= 0:
                requests.get(
                    url,
                    params={"token": token, "ack": oid, "status": "fail", "note": "lot=0"},
                    timeout=12,
                )
                continue
            ok, note = _fill(symbol, side, lots, o.get("sl"), o.get("tp"))
            print(oid, symbol, side, lots, ok, note)
            requests.get(
                url,
                params={
                    "token": token,
                    "ack": oid,
                    "status": "sent" if ok else "fail",
                    "note": note,
                },
                timeout=12,
            )
        time.sleep(POLL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            mt5.shutdown()
        except Exception:
            pass
