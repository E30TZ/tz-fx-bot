# Architecture

```
Telegram ──webhook──► bot_index.cgi / wsgi.py
                       └─ telegrambot_bot.application
                            ├─ callbacks / DMs
                            ├─ ICT scan (FX + USDT spot)
                            ├─ i18n.t(lang, key)
                            ├─ Mini App  miniapp.html + ?app=api
                            ├─ mentor
                            └─ live_exec (demo) ──queue──► tz_mt5_bridge
```

Language: `use_lang(uid)` reads `lang` from per-uid memory (`fa` default). Mini App `?app=api&v=lang`.

ICT: `ENGINE_GEN = 6`. Hourly FX scan has no chart. Signal charts are white 2560×1600, price + SL + TP only.

Host-only files: `.telegram_token`, mentor key, `.live.json`, `.edu_audio/`.
