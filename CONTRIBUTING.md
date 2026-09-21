# Contributing

## فارسی

پول و ICT شوخی نیست. قبل از PR:

1. استراتژی فقط **ICT Mentorship 2022** است. ستاپ جدید نساز.
2. اگر مدل کامل نیست خروجی باید **صبر / WAIT** بماند. `sig3` را شل نکن.
3. وین‌ریت الکی، اسکرین‌شات سود، ستاره جعلی نگذار.
4. رشته‌های UI را در `i18n.py` بگذار، نه کپی وسط `telegrambot_bot.py`.
5. زبان پیش‌فرض فارسی است. انگلیسی را هم سطح اول بنویس.
6. راز (توکن، کلید، FTP) commit نکن.
7. قابلیت کارکننده را حذف نکن تا «تمیز» شود.

---

## English

This is a live trading-desk bot. PRs that loosen ICT, invent WR%, or drop working features will be closed.

### Setup

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest tests/ -q
python3 -m py_compile telegrambot_bot.py i18n.py live_exec.py tz_mt5_bridge.py chart_pro.py
```

You do not need a Telegram token to run unit tests.

### Rules

| Do | Don't |
|---|---|
| Add strings to `i18n.py` (FA + EN) | Hardcode UI in one language |
| Keep WAIT as a real state | Force BUY/SELL when score < 3 |
| Keep SL on every live side | “Market order, no stop” |
| Persist `lang` per uid | Global language flag |
| Demo-gate live_exec | Hit exchange `/order` in demo |
| Isolated per-uid mentor memory | Shared chat log |

### PR checklist

- [ ] `pytest tests/ -q` passes
- [ ] No secrets in the diff
- [ ] FA default still works
- [ ] EN is written English, not pasted MT
- [ ] Mini App still dark, 5 tabs, ICT-only
- [ ] Charts still show price + SL/TP only

### Code style

- Bot API via `requests`, no aiogram.
- CGI-safe: no background threads that the host will kill.
- Commands in English slashes; button labels from `T("…")`.

### Contact

Developer: [@E30TZ](https://t.me/E30TZ)
