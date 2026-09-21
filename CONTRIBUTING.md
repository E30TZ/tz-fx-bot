# Contributing

## فارسی

قبل از PR:

1. استراتژی فقط ICT است.
2. مدل ناقص = **صبر / WAIT**. `sig3` را شل نکن.
3. وین‌ریت الکی، اسکرین سود، ستاره جعلی نگذار.
4. رشته UI در `i18n.py` (FA و EN)، نه وسط هندلر.
5. پیش‌فرض فارسی بماند.
6. راز commit نکن.
7. قابلیت کارکننده را برای «تمیزی» حذف نکن.

---

## English

PRs that loosen ICT, invent win-rate, or drop working features will be closed.

```bash
python3 -m pip install -r requirements.txt
python3 tests/test_i18n.py
python3 tests/test_repo.py
python3 tests/test_donations.py
python3 tests/test_lang_helpers.py
python3 -m py_compile telegrambot_bot.py i18n.py live_exec.py tz_mt5_bridge.py chart_pro.py wsgi.py
```

No Telegram token is required for these tests.

| Do | Don't |
|---|---|
| Strings in `i18n.py` | One-language hardcode |
| WAIT as a real state | Force BUY/SELL under score 3 |
| SL on every live side | Naked market orders |
| `lang` per uid | Global language flag |
| Demo-gate `live_exec` | Live `/order` in demo |
| Isolated mentor memory | Shared chat log |

Contact: [@E30TZ](https://t.me/E30TZ)
