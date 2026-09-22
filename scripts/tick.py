# -*- coding: utf-8 -*-
"""Hourly/minute ICT tick — no outbound ping to the shared host."""
from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
sys.path.insert(0, HERE)

try:
    from bot import process_once_locked
except Exception:
    from telegrambot_bot import process_once_locked

if __name__ == "__main__":
    process_once_locked(timeout=0)
