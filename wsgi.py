# -*- coding: utf-8 -*-
"""WSGI entry for VPS (gunicorn) and CGI wrappers.

Prefers bot.py (host layout) then telegrambot_bot.py (this repo).
"""
from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    from bot import application  # noqa: F401
except Exception:
    from telegrambot_bot import application  # noqa: F401
