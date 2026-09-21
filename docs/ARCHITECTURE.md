# Architecture

```
Telegram ──webhook──► bot_index.cgi ──► telegrambot_bot.application
                                           ├─ handle_callback / handle_message
                                           ├─ ICT scan (FX + USDT spot)
                                           ├─ i18n.t(lang, key)
                                           ├─ Mini App  (miniapp.html + ?app=api)
                                           ├─ mentor (Gemini text + TTS)
                                           └─ live_exec (demo gate) ──queue──► tz_mt5_bridge
```

## Language

`use_lang(uid)` loads `lang` from per-uid memory (`fa` default). `T(key)` reads `i18n.py`. Mini App `?app=api&v=lang`.

## ICT

Hourly FX scan does **not** attach a chart. `/start` signal charts stay. Chart payload is price + SL + TP on a white 2560×1600 canvas. Engine generation counter is `ENGINE_GEN = 6`.

## Files the host needs

| File | Role |
|---|---|
| `.telegram_token` | Bot token (not in git) |
| Gemini key file | Mentor + TTS (not in git) |
| `.live.json` | Venue keys (not in git) |
| `.edu_audio/` | Persian lesson ogg (not in git) |
