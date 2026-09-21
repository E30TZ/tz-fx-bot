<p align="center">
  <img src="docs/brand/logo.svg" width="96" height="96" alt="TZ FX"/>
</p>

<h1 align="center">TZ FX BOT</h1>

<p align="center">
  <b>ICT Mentorship 2022</b> · Persian default · English first-class<br/>
  WAIT is a real state · Stop loss required · No fake win-rate
</p>

<p align="center">
  <a href="https://t.me/TZ_FX_BOT">@TZ_FX_BOT</a> ·
  <a href="https://t.me/TZ_FX_CH">@TZ_FX_CH</a> ·
  <a href="https://t.me/E30TZ">@E30TZ</a>
</p>

<p align="center">
  <img src="docs/brand/og.png" alt="TZ FX — ICT Mentorship 2022" width="640"/>
</p>

---

**فارسی.** ربات و مینی‌اپ معامله با مدل ICT Mentorship 2022. زبان پیش‌فرض فارسی است؛ انگلیسی هم سطح اول است. اگر مدل کامل نباشد خروجی **صبر / WAIT** است. حد ضرر اجباری است. درصد برد ساختگی چاپ نمی‌شود. آموزش است، مشاوره مالی نیست، سود تضمینی ندارد.

**English.** Telegram bot + dark Mini App. The engine prints a full ICT 2022 setup **with SL**, or it prints **WAIT**. It does not invent BUY/SELL, chase price, or fabricate performance.

| | |
|---|---|
| Bot | [@TZ_FX_BOT](https://t.me/TZ_FX_BOT) |
| Free channel | [@TZ_FX_CH](https://t.me/TZ_FX_CH) |
| VIP | [invite](https://t.me/+uWnJTwhqC_FhMmM8) |
| Crypto beta | [invite](https://t.me/+8hM_fEp9y7Y0ZmQ8) |
| Developer | [@E30TZ](https://t.me/E30TZ) |
| Release | `v1.0.0` · branch `main` |

---

## Overview

TZ FX is a CGI Telegram bot (Bot API, no aiogram) and a Telegram Mini App.

- **Strategy lock:** ICT Mentorship 2022 only.
- **Language:** `fa` default, `en` first-class, persisted per Telegram user in `i18n.py`.
- **Desk:** FX (EURUSD, GBPUSD, XAUUSD) + USDT-spot crypto. Tehran time.
- **Mentor:** voice in, voice+text out, memory isolated per uid.
- **Paper + connect:** demo-gated. Live exchange `/order` is off until you change that on purpose.
- **Paywall:** join the free channel, then card + receipt. Owner confirms VIP.

This repository is the public tree. Host secrets stay on the host.

---

## Features

| Area | What you get |
|---|---|
| Signals | ICT 2022 geometry or WAIT. SL on every live side. |
| Language | `/lang`, home switcher, Mini App chip. Written EN, not raw MT. |
| Mini App | Dark 5 tabs: Forex, Crypto, Desk, Learn, Mentor. |
| Mentor | Gemini. Per-uid memory. Hear button after a signal. |
| Education | 26 lessons, text + voice. Level 5 is API / connect. |
| Paper | Isolated book. Crypto 9W/17L is **not** the channel WR. |
| Connect | CEX REST + MT5 bridge queue. `LIVE_MODE=demo`. |
| Channel | 20:30–08:30 Tehran silent. In-bot DM 24/7, still WAIT when empty. |

---

## Screenshots

UI chrome only. Not performance claims. No win-rate, no P&L.

<p>
<img src="docs/screenshots/miniapp-desk.png" alt="Mini App desk" width="280"/>
<img src="docs/screenshots/signal-wait.png" alt="ICT WAIT" width="220"/>
<img src="docs/screenshots/mentor.png" alt="Mentor" width="220"/>
</p>

---

## Architecture

```
Telegram ──webhook──► bot_index.cgi ──► telegrambot_bot.application
                                         ├─ callbacks / DMs
                                         ├─ ICT scan (FX + USDT spot)
                                         ├─ i18n.t(lang, key)
                                         ├─ Mini App  miniapp.html + ?app=api
                                         ├─ mentor (Gemini text + TTS)
                                         └─ live_exec (demo) ──queue──► tz_mt5_bridge
```

| File | Role |
|---|---|
| `telegrambot_bot.py` | Bot, webhook, Mini App API, ICT, mentor, paywall |
| `i18n.py` | FA/EN catalog + 26 EN lessons |
| `miniapp.html` | Dark Mini App |
| `live_exec.py` | Demo-gated CEX + MT5 queue |
| `tz_mt5_bridge.py` | Windows poller beside MetaTrader 5 |
| `chart_pro.py` | White high-res charts: price + SL/TP only |

Webhook path: `https://ehsantz.pingbaz.space/bot/index.cgi`  
Passenger off. CGI. No `secret_token` on the webhook.

---

## ICT Engine

Locked to **ICT Mentorship 2022**.

1. Killzone, draw on liquidity, displacement, FVG, OTE, PD array.
2. Score 0–6. A live side needs 3+.
3. Incomplete model → **WAIT**. Do not chase.
4. Every live side has a stop loss.
5. No invented prices. No SMC mashup. No “multi-setup”.
6. Hourly FX scan does not attach a chart. `/start` charts stay.
7. Chart canvas: white, 2560×1600, price + SL + TP only.
8. Closed book only. `ENGINE_GEN = 6`. No fake %.
9. Saturday FX is closed. Crypto is USDT spot.
10. Risk cap 1%. Educational disclaimer on the desk.

Do not loosen this in a PR.

---

## AI Mentor

- Isolated memory per Telegram uid. No shared chat log.
- Voice message in → voice + text out.
- System prompt follows the user language (`ai.sys` in `i18n.py`).
- Lesson *audio* on the host is Persian (Charon). English users still get EN text.
- `/forget` clears that user’s mentor memory.

---

## Mini App

Dark trading desk. Five tabs: **Forex · Crypto · Desk · Learn · Mentor**.

- ICT cards with WAIT as a first-class badge.
- Language chip FA/EN (`?app=api&v=lang`).
- Lessons and mentor require the same paywall as the bot for signals; education listing stays open.
- InitData HMAC before uid is trusted.

---

## Education

26 lessons, five levels: beginner → ICT foundation → advanced → execution → API & connect.

Strings live in `i18n.py` (`EDU_*` FA in the bot, `EDU_EN` / `EDU_TITLE_EN` / `EDU_SPEAK_EN` for English). Do not duplicate lesson HTML inside random handlers.

---

## Paper Trading

Paper is a separate book. It is not the channel win-rate.

Crypto paper currently reads **9 wins / 17 losses** on the host book. That number is not a marketing WR and must not be copy-pasted as “the bot wins 9/17 of channel signals”.

Mode: `both_paper` then 1% risk. Demo must not send live crypto `/order`.

---

## Integrations

| Venue | Notes |
|---|---|
| Binance, Bybit, OKX, Bitget, … | REST via `live_exec.py`, demo-gated |
| MetaTrader 5 | Windows bridge `tz_mt5_bridge.py`, any MT5 broker |
| Telegram | Bot API 9.4 `style`, webhook CGI |
| Gemini | Mentor + TTS. Key on the host, never in git |

Keys: host file + `deleteMessage`. Never `log()` a key.

---

## Installation

Python 3.6+ on a CGI host. `requests` is the only required extra.

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
# put the bot token in .telegram_token — file, not the shell history
python3 -c "import telegrambot_bot as b; print(b.BOT_VERSION)"
python3 tests/test_i18n.py && python3 tests/test_repo.py
```

### CGI

1. Copy `telegrambot_bot.py`, `i18n.py`, `miniapp.html`, `live_exec.py`, `chart_pro.py` next to `bot_index.cgi`.
2. Point the webhook at `…/bot/index.cgi`.
3. Keep `.telegram_token` and the Gemini key **off** this repo.

You do not need a VPS. Passenger stays off.

---

## Configuration

See [`.env.example`](.env.example). Real values belong in host files:

| File (host only) | Purpose |
|---|---|
| `.telegram_token` | Bot token |
| Gemini key file | Mentor / TTS |
| `.live.json` | Exchange keys |
| `.edu_audio/` | Persian lesson voice |

`LIVE_MODE=demo` until you intentionally go live.

---

## Security

Read [SECURITY.md](SECURITY.md).

Never commit tokens, Gemini keys, host FTP, exchange keys, user memory, or receipts.

If a key leaked in chat, rotate it. Do not paste it into an issue.

---

## Roadmap

Honest queue. Not a promise of dates or returns.

- Publish verified donation wallets (network + address from the maintainer).
- Remaining lesson voice clips on the host (`edu_19`, `edu_20`, `edu_23`, `edu_24`, `edu_26`).
- English lesson audio, same Charon pipeline, when quota allows.
- GitHub public remote once credentials exist.

Out of scope: loosening ICT, fake WR, guaranteed profit.

---

## Support TZ FX

**💚 Support TZ FX**

If TZ FX BOT is useful to you and you'd like to support its development, you can support the project through cryptocurrency.

اگر TZ FX BOT برای شما مفید بوده و دوست دارید از توسعه پروژه حمایت کنید، می‌توانید از طریق ارز دیجیتال از پروژه حمایت کنید.

This is a **donation**. It is not an investment, not a deposit, not a managed account. There is no return, no profit share, and no “earn by sending funds”.

| Asset | Network | Address |
|---|---|---|
| — | — | *Not published yet* |

No sample address. No placeholder QR. Do not send coins until [@E30TZ](https://t.me/E30TZ) publishes a network and address in this table.

Maintainer: when you have the wallet, send **asset + network + address** (example: `USDT — TRC20` + address). Each wallet is listed on its own row.

---

## Custom Development

Need a desk like this built for your desk — not a clone of TZ FX’s signals?

[@E30TZ](https://t.me/E30TZ) takes scoped work:

- Custom Telegram bots
- AI automation
- Telegram Mini Apps
- Trading systems
- API integrations
- Web applications

Serious briefs only. No signal-selling pitches.

---

## Disclaimer

Educational software. Not financial advice. Not a broker.

Markets can wipe a deposit. TZ FX does not guarantee profit, does not manage your money, and does not treat a donation as a stake.

حد ضرر اجباری است. حداکثر ۱٪. سود تضمینی نیست.

---

## License

[MIT](LICENSE) © 2026 E30TZ
