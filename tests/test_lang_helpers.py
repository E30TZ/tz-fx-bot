# -*- coding: utf-8 -*-
"""Import bot helpers without talking to Telegram."""
from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

# Bot pulls requests/network on some paths; helpers we need are pure.
import i18n  # noqa: E402


def test_blank_mem_has_lang():
    # Read source — do not execute CGI.
    src = open(os.path.join(HERE, "telegrambot_bot.py"), encoding="utf-8").read()
    assert '"lang": "fa"' in src
    assert "def use_lang(" in src
    assert "def set_lang(" in src
    assert "def T(" in src


def test_miniapp_dark():
    html = open(os.path.join(HERE, "miniapp.html"), encoding="utf-8").read()
    assert "#0b0d10" in html
    assert "langb" in html
    assert "I18N" in html
    assert "WAIT" in html or "wait" in html.lower()


if __name__ == "__main__":
    test_blank_mem_has_lang()
    test_miniapp_dark()
    print("helpers ok")
