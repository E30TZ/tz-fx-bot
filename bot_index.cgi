#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import signal

ROOT = os.environ.get("TZFX_ROOT") or os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ.setdefault("PYTHONPATH", ROOT)

for sig in (getattr(signal, "SIGHUP", None), getattr(signal, "SIGPIPE", None)):
    if sig is not None:
        try:
            signal.signal(sig, signal.SIG_IGN)
        except Exception:
            pass

method = (os.environ.get("REQUEST_METHOD") or "GET").upper()
if method == "POST":
    try:
        n = int(os.environ.get("CONTENT_LENGTH") or 0)
    except Exception:
        n = 0
    raw = sys.stdin.buffer.read(n) if n else b""
    sys.stdout.write("Status: 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nok\r\n")
    sys.stdout.flush()
    try:
        from bot import process_webhook

        process_webhook(raw)
    except Exception:
        try:
            from bot import log
            import traceback

            log("cgi post " + traceback.format_exc())
        except Exception:
            pass
    sys.exit(0)

from wsgiref.handlers import CGIHandler

try:
    from bot import application
except Exception:
    from telegrambot_bot import application

CGIHandler().run(application)
