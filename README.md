<p align="center">
  <img src="docs/brand/logo.svg" width="72" height="72" alt="TZ FX"/>
</p>

<h1 align="center">TZ FX BOT</h1>

<p align="center">
  <strong>Telegram trading assistant and ICT 2022 market scanner.</strong><br/>
  WAIT is a first-class state. Stop loss is required. No fabricated performance.
</p>

<p align="center">
  <a href="https://t.me/TZ_FX_BOT"><img src="https://img.shields.io/badge/Telegram-TZ%20FX%20BOT-3D9B74?labelColor=0A0C0E" alt="Telegram bot"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-3D9B74?labelColor=0A0C0E" alt="MIT"/></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/Version-1.0.0-3D9B74?labelColor=0A0C0E" alt="1.0.0"/></a>
  <img src="https://img.shields.io/badge/Python-3.9+-3D9B74?labelColor=0A0C0E" alt="Python 3.9+"/>
</p>

<p align="center">
  <a href="https://t.me/TZ_FX_BOT">Open the bot</a>
  ·
  <a href="docs/fa.md">مستندات فارسی</a>
  ·
  <a href="https://github.com/E30TZ/tz-fx-bot">Source</a>
  ·
  <a href="https://t.me/E30TZ">EHSAN TZ</a>
</p>

<p align="center">
  <img src="docs/brand/og.png" alt="TZ FX BOT — Telegram trading assistant" width="720"/>
</p>

---

## Overview

TZ FX BOT is a Telegram bot and Mini App for scanning FX and USDT-spot crypto against **ICT Mentorship 2022**.

The engine does not invent a side. If the 2022 model is incomplete it returns **WAIT**. If it is complete it returns a setup **with a stop loss**.

Persian is the product default. English is a first-class UI and documentation language, stored in `i18n.py`, persisted per Telegram user.

This repository is the public tree. Secrets stay on the host.

Live instance (shared CGI): [@TZ_FX_BOT](https://t.me/TZ_FX_BOT) · free channel [@TZ_FX_CH](https://t.me/TZ_FX_CH)

---

## Core features

| | |
|---|---|
| Scanner | EURUSD, GBPUSD, XAUUSD + USDT-spot crypto. Tehran clock. |
| ICT 2022 | Killzone, sweep, displacement, FVG, OTE, PD array. Score 0–6. |
| WAIT | Incomplete geometry is a published state, not a silent failure. |
| Mini App | Dark desk: Forex, Crypto, Desk, Learn, Mentor. |
| Mentor | Isolated per-uid memory. Voice in, text + voice out. |
| Education | 26 lessons, five levels, through API / broker connect. |
| Paper | Separate book. Not the channel win-rate. |
| Connect | CEX REST + MT5 bridge queue. `LIVE_MODE=demo` until you change it. |
| Language | `/lang`, home switcher, Mini App chip. |

---

## How it works

```
Telegram  ──webhook──►  WSGI / CGI
                         ├─ ICT scan
                         ├─ i18n.t(lang, key)
                         ├─ Mini App API
                         ├─ mentor
                         └─ live_exec (demo) ──► MT5 bridge
```

Hourly FX scan does not attach a chart. `/start` signal charts stay, and they draw **price + SL + TP only**.

Channel FX window 20:30–08:30 Tehran is silent. In-bot DM is 24/7 and still WAIT when there is no model.

---

## Trading engine

Locked to ICT Mentorship 2022.

1. HTF draw → Judas sweep → MSS with displacement → enter inside FVG/OTE → SL beyond the wick.
2. Live side requires score ≥ 3. Below that: **WAIT**.
3. No stop loss → no live side.
4. No invented prices. No chase. No “multi-setup” mashup.
5. Closed book only. No fabricated win-rate.
6. Saturday FX is closed. Crypto is USDT spot, beta.
7. Risk cap 1%. Educational disclaimer on the desk.

Do not loosen this in a pull request.

---

## Telegram

Commands: `/start` `/signal` `/crypto` `/learn` `/wr` `/lang` `/help` `/donate`

Owner extras: `/connect` `/paper` `/admin`

Paywall: join [@TZ_FX_CH](https://t.me/TZ_FX_CH), then card + receipt. Owner confirms VIP ([invite](https://t.me/+uWnJTwhqC_FhMmM8)). Crypto beta: [invite](https://t.me/+8hM_fEp9y7Y0ZmQ8).

---

## Mini App

Five tabs, dark desk, FA/EN chip. InitData is HMAC-checked before a uid is trusted. WAIT is a badge, not a missing screen.

---

## Education

Twenty-six lessons. Levels: beginner → ICT foundation → advanced → execution → API & connect. Copy lives in `i18n.py`. Lesson audio on the host is Persian; English users still get English text.

---

## Paper trading

Paper is practice. It is not the channel book and must not be quoted as a marketing win-rate. Demo must not send live crypto `/order`.

---

## Integrations

| | |
|---|---|
| Binance, Bybit, OKX, Bitget, … | `live_exec.py`, demo-gated |
| MetaTrader 5 | `tz_mt5_bridge.py` on the Windows PC that runs MT5 |
| Telegram | Bot API, webhook |

Keys: host file + `deleteMessage`. Never log a key.

---

## Screenshots

Interface previews with demonstration data. Not a live book. Not performance claims.

<p>
<img src="docs/screenshots/desk.jpg" alt="Desk — WAIT on EUR, GBP, gold" width="240"/>
<img src="docs/screenshots/wait.jpg" alt="ICT WAIT, score 2/6" width="240"/>
<img src="docs/screenshots/mentor.jpg" alt="Mentor explaining FVG" width="240"/>
</p>

| | |
|---|---|
| Desk | FX radar with WAIT as the default honest state |
| Signal | Incomplete 2022 model — do not chase |
| Mentor | Product Q&A, isolated to the Telegram user |

---

## Architecture

| File | Role |
|---|---|
| `telegrambot_bot.py` | Bot, webhook, Mini App API, ICT, mentor, paywall |
| `i18n.py` | FA / EN catalog + 26 English lessons |
| `miniapp.html` | Mini App |
| `live_exec.py` | Demo-gated CEX + MT5 queue |
| `tz_mt5_bridge.py` | Windows poller |
| `chart_pro.py` | White charts: price, SL, TP |
| `wsgi.py` | Gunicorn / CGI entry |
| `scripts/install-vps.sh` | Ubuntu installer |

---

## Installation

### Shared CGI

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
# token → .telegram_token  (file, not the shell history)
python3 -c "import telegrambot_bot as b; print(b.BOT_VERSION)"
python3 tests/test_i18n.py && python3 tests/test_repo.py
```

Point the webhook at the CGI path. Keep tokens off git.

### Ubuntu VPS

```bash
git clone https://github.com/E30TZ/tz-fx-bot.git
cd tz-fx-bot
sudo bash scripts/install-vps.sh
```

See [docs/VPS.md](docs/VPS.md). Token: `/opt/tz-fx-bot/.telegram_token`. Leave `LIVE_MODE=demo` until you change it.

---

## Configuration

| Host file | Purpose |
|---|---|
| `.telegram_token` | Bot token |
| Mentor key file | Mentor / speech |
| `.live.json` | Exchange keys |
| `.edu_audio/` | Persian lesson voice |

Copy [`.env.example`](.env.example). Never commit real values.

---

## Security

Read [SECURITY.md](SECURITY.md).

Report issues to [@E30TZ](https://t.me/E30TZ), not as a public GitHub issue, if a live token or receipt is involved.

---

## Support TZ FX

### حمایت از TZ FX

اگر TZ FX برای شما مفید بوده، می‌توانید با ارسال دونیت از توسعه و نگهداری پروژه حمایت کنید.

If TZ FX has been useful to you, you can support continued development with a donation.

Donation only — not an investment, not a deposit, not a managed account. No return.

⚠️ Always select the exact network shown. Sending assets through the wrong network may result in permanent loss.

⚠️ هنگام انتقال، شبکه را دقیقاً مطابق شبکه نمایش‌داده‌شده انتخاب کنید. انتقال روی شبکه اشتباه ممکن است باعث از دست رفتن دارایی شود.

<table>
<tr>
<td valign="top" width="50%">

**TRX — TRON**

<img src="docs/donations/trx-tron.png" width="112" alt="QR TRX TRON"/>

```
TF4TbyEu1eC1sYTW1oviBbmPKT1KkxViba
```

</td>
<td valign="top" width="50%">

**TON — TON**

<img src="docs/donations/ton-ton.png" width="112" alt="QR TON"/>

```
UQDKUFjOEWXcyjOE459jWbniQRtdNYN1taRRn1XhdA8KKiqT
```

</td>
</tr>
<tr>
<td valign="top" width="50%">

**USDT — TRC20**

<img src="docs/donations/usdt-trc20.png" width="112" alt="QR USDT TRC20"/>

```
TF4TbyEu1eC1sYTW1oviBbmPKT1KkxViba
```

Not ERC-20 / BEP20 / TON.

</td>
<td valign="top" width="50%">

**USDT — BEP20**

<img src="docs/donations/usdt-bep20.png" width="112" alt="QR USDT BEP20"/>

```
0x258380877EC849e04082C4A6795d01432c3F4B7B
```

Not TRC20 / ERC-20 / TON.

</td>
</tr>
</table>

No other wallets. QR payloads were encoded from these addresses and decoded back before commit.

---

## Custom development

[EHSAN TZ](https://github.com/E30TZ) · Telegram [@E30TZ](https://t.me/E30TZ)

Scoped engineering — not a clone of TZ FX signals:

- Custom Telegram bots
- Web applications
- APIs
- Automation systems
- Software products

---

## Roadmap

Not a date promise. Not a return promise.

- Remaining Persian lesson audio on the host (`edu_19`, `edu_20`, `edu_23`, `edu_24`, `edu_26`)
- English lesson audio when quota allows

Out of scope: loosening ICT, fake win-rate, guaranteed profit.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). ICT lock, required SL, and WAIT are not negotiable in a drive-by PR.

---

## Disclaimer

Educational software. Not financial advice. Not a broker.

Markets can wipe a deposit. TZ FX does not guarantee profit, does not manage your money, and does not treat a donation as a stake.

حد ضرر اجباری است. حداکثر ۱٪. سود تضمینی نیست.

---

## License

[MIT](LICENSE) © 2026 EHSAN TZ
