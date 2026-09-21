# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIR = {
    ".git",
    ".github",
    "__pycache__",
    ".pytest_cache",
    "docs",
    "tests",
}

SECRET_RES = [
    re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),  # telegram bot token
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"\bAQ\.[A-Za-z0-9_\-]{20,}\b"),  # Gemini
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
]


def _files():
    out = []
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR and not d.startswith(".")]
        for fn in files:
            if fn.startswith("."):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, HERE)
            if fn.endswith((".png", ".jpg", ".ogg", ".wav", ".zip")):
                continue
            out.append(path)
    return out


def test_no_secret_files():
    banned = {
        ".telegram_token",
        ".gemini_key",
        ".host_ftp",
        ".host_new",
        ".env",
        ".live.json",
        ".paper.json",
    }
    names = set(os.listdir(HERE))
    for b in banned:
        assert b not in names, b


def test_no_secret_payloads():
    hits = []
    for path in _files():
        try:
            text = open(path, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for rx in SECRET_RES:
            if rx.search(text):
                hits.append(os.path.relpath(path, HERE))
                break
    assert hits == [], hits


def test_bot_version():
    s = open(os.path.join(HERE, "telegrambot_bot.py"), encoding="utf-8").read()
    assert 'BOT_VERSION = "1.0.0"' in s
    assert "import i18n" in s
    assert "lang_toggle" in s
    assert 'T("btn.hear")' in s or "btn.hear" in s


def test_ict_lock():
    s = open(os.path.join(HERE, "telegrambot_bot.py"), encoding="utf-8").read()
    assert "ICT" in s
    assert "WAIT" in s or "صبر" in s


if __name__ == "__main__":
    for fn in (test_no_secret_files, test_no_secret_payloads, test_bot_version, test_ict_lock):
        fn()
        print("ok", fn.__name__)
    print("repo ok")
