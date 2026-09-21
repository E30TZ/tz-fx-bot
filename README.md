<p align="center">
  <img src="docs/brand/logo.svg" width="96" height="96" alt="TZ FX"/>
</p>

<h1 align="center">TZ FX BOT</h1>

<p align="center">
  <b>ICT Mentorship 2022</b> · Persian default · English first-class<br/>
  WAIT is a real state · Stop loss required · No fake win-rate
</p>

<p align="center">
  <a href="https://t.me/TZ_FX_BOT">@TZ_FX_BOT</a>
  ·
  <a href="https://t.me/TZ_FX_CH">@TZ_FX_CH</a>
  ·
  <a href="https://t.me/E30TZ">@E30TZ</a>
  ·
  EHSAN TZ
</p>

<p align="center">
  <img src="docs/brand/og.png" alt="TZ FX — ICT Mentorship 2022" width="640"/>
</p>

---

**فارسی.** دستیار معامله در تلگرام با مدل ICT Mentorship 2022. زبان پیش‌فرض فارسی است؛ انگلیسی هم سطح اول است. اگر مدل کامل نباشد خروجی **صبر / WAIT** است. حد ضرر اجباری است. درصد برد ساختگی چاپ نمی‌شود. آموزش است، مشاوره مالی نیست، سود تضمینی ندارد.

**English.** Telegram trading assistant + dark Mini App. The engine prints a full ICT 2022 setup **with SL**, or it prints **WAIT**. It does not invent BUY/SELL, chase price, or fabricate performance.

| | |
|---|---|
| Bot | [@TZ_FX_BOT](https://t.me/TZ_FX_BOT) |
| Free channel | [@TZ_FX_CH](https://t.me/TZ_FX_CH) |
| VIP | [invite](https://t.me/+uWnJTwhqC_FhMmM8) |
| Crypto beta | [invite](https://t.me/+8hM_fEp9y7Y0ZmQ8) |
| Developer | [@E30TZ](https://t.me/E30TZ) · [EHSAN TZ](https://github.com/E30TZ) |
| Release | `v1.0.0` · branch `main` |

---

## Project overview

TZ FX is a CGI Telegram bot (Bot API, no aiogram) and a Telegram Mini App.

- **Strategy lock:** ICT Mentorship 2022 only.
- **Language:** `fa` default, `en` first-class, persisted per Telegram user (`i18n.py`).
- **Desk:** FX (EURUSD, GBPUSD, XAUUSD) + USDT-spot crypto. Tehran time.
- **Mentor:** in-product Q&A, voice in / voice+text out, memory isolated per uid.
- **Paper + connect:** demo-gated. Live exchange `/order` stays off until you change that on purpose.
- **Paywall:** join the free channel, then card + receipt. Owner confirms VIP.

This repository is the public tree. Host secrets stay on the host.

---

## Features

| Area | What you get |
|---|---|
| Signals | ICT 2022 geometry or WAIT. SL on every live side. |
| Language | `/lang`, home switcher, Mini App chip. Written EN, not raw machine translation. |
| Mini App | Dark 5 tabs: Forex, Crypto, Desk, Learn, Mentor. |
| Mentor | In-bot mentor. Per-uid memory. Hear after a signal. |
| Education | 26 lessons, text + voice. Level 5 is API / connect. |
| Paper | Isolated book. Not the channel win-rate. |
| Connect | CEX REST + MT5 bridge queue. `LIVE_MODE=demo`. |
| Channel | 20:30–08:30 Tehran silent. In-bot DM 24/7, still WAIT when empty. |

### ICT engine

Locked to **ICT Mentorship 2022**.

1. Killzone, draw on liquidity, displacement, FVG, OTE, PD array.
2. Score 0–6. A live side needs 3+.
3. Incomplete model → **WAIT**. Do not chase.
4. Every live side has a stop loss.
5. No invented prices. No “multi-setup”.
6. Hourly FX scan does not attach a chart. `/start` charts stay.
7. Chart canvas: white, 2560×1600, price + SL + TP only.
8. Closed book only. No fake %.
9. Saturday FX is closed. Crypto is USDT spot.
10. Risk cap 1%. Educational disclaimer on the desk.

### Mentor

Product feature: isolated memory per Telegram uid, voice message in → voice + text out, `/forget` clears that user’s memory. System prompt follows the user language.

### Mini App

Dark trading desk. Tabs: **Forex · Crypto · Desk · Learn · Mentor**. WAIT is a first-class badge. FA/EN chip. InitData HMAC before uid is trusted.

### Education

26 lessons, five levels: beginner → ICT foundation → advanced → execution → API & connect. Strings live in `i18n.py`.

### Paper trading

Paper is a separate book. It is not the channel win-rate. Mode: paper first, then 1% risk. Demo must not send live crypto `/order`.

### Integrations

| Venue | Notes |
|---|---|
| Binance, Bybit, OKX, Bitget, … | REST via `live_exec.py`, demo-gated |
| MetaTrader 5 | Windows bridge `tz_mt5_bridge.py` |
| Telegram | Bot API, webhook CGI |

Keys: host file + `deleteMessage`. Never `log()` a key.

---

## Architecture

```
Telegram ──webhook──► bot_index.cgi ──► telegrambot_bot.application
                                         ├─ callbacks / DMs
                                         ├─ ICT scan (FX + USDT spot)
                                         ├─ i18n.t(lang, key)
                                         ├─ Mini App  miniapp.html + ?app=api
                                         ├─ mentor
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
Passenger off. CGI.

---

## Screenshots / Demo

UI chrome only. Not performance claims. No win-rate, no P&L.

<p>
<img src="docs/screenshots/miniapp-desk.png" alt="Mini App desk" width="280"/>
<img src="docs/screenshots/signal-wait.png" alt="ICT WAIT" width="220"/>
<img src="docs/screenshots/mentor.png" alt="Mentor" width="220"/>
</p>

Live bot: [@TZ_FX_BOT](https://t.me/TZ_FX_BOT)

---

## Installation

### CGI (current live desk)

Python 3.6+. `requests` is the only required extra.

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
# put the bot token in .telegram_token — file, not the shell history
python3 -c "import telegrambot_bot as b; print(b.BOT_VERSION)"
python3 tests/test_i18n.py && python3 tests/test_repo.py
```

1. Copy `telegrambot_bot.py`, `i18n.py`, `miniapp.html`, `live_exec.py`, `chart_pro.py` next to `bot_index.cgi`.
2. Point the webhook at `…/bot/index.cgi`.
3. Keep `.telegram_token` and mentor keys **off** this repo.

Passenger stays off on the shared host.

### VPS (Ubuntu)

For a dedicated box, not a migrate of the live CGI:

```bash
git clone https://github.com/e30tz/tz-fx-bot.git
cd tz-fx-bot
sudo bash scripts/install-vps.sh
```

Details: [docs/VPS.md](docs/VPS.md). Token stays in `/opt/tz-fx-bot/.telegram_token`. `LIVE_MODE=demo` until you change it.

---

## Configuration

See [`.env.example`](.env.example). Real values belong in host files:

| File (host only) | Purpose |
|---|---|
| `.telegram_token` | Bot token |
| Mentor key file | Mentor / speech |
| `.live.json` | Exchange keys |
| `.edu_audio/` | Persian lesson voice |

`LIVE_MODE=demo` until you intentionally go live.

---

## Security

Read [SECURITY.md](SECURITY.md).

Never commit tokens, API keys, host FTP, exchange keys, user memory, or receipts.

If a key leaked in chat, rotate it. Do not paste it into an issue.

---

## Support TZ FX

### حمایت از TZ FX

اگر TZ FX برای شما مفید بوده، می‌توانید با ارسال دونیت از توسعه و نگهداری پروژه حمایت کنید.

### Support TZ FX

If TZ FX has been useful to you, you can support the continued development and maintenance of the project with a donation.

This is a **donation**. Not an investment, not a deposit, not a managed account. No return, no profit share.

⚠️ **Always select the exact network shown above. Sending assets through the wrong network may result in permanent loss.**

⚠️ **هنگام انتقال، شبکه را دقیقاً مطابق شبکه نمایش‌داده‌شده انتخاب کنید. انتقال روی شبکه اشتباه ممکن است باعث از دست رفتن دارایی شود.**

Use the copy control on each address block in GitHub.

<table>
<tr>
<td width="50%" valign="top">

**TRX — TRON**

<img src="docs/donations/trx-tron.png" alt="QR TRX TRON" width="140"/>

```
TF4TbyEu1eC1sYTW1oviBbmPKT1KkxViba
```

Network: **TRON** · Asset: **TRX**

</td>
<td width="50%" valign="top">

**TON — TON**

<img src="docs/donations/ton-ton.png" alt="QR TON TON" width="140"/>

```
UQDKUFjOEWXcyjOE459jWbniQRtdNYN1taRRn1XhdA8KKiqT
```

Network: **TON** · Asset: **TON**

</td>
</tr>
<tr>
<td width="50%" valign="top">

**USDT — TRC20**

<img src="docs/donations/usdt-trc20.png" alt="QR USDT TRC20" width="140"/>

```
TF4TbyEu1eC1sYTW1oviBbmPKT1KkxViba
```

Network: **TRC20** · Asset: **USDT**  
Do not send this as ERC-20 / BEP20 / TON.

</td>
<td width="50%" valign="top">

**USDT — BEP20**

<img src="docs/donations/usdt-bep20.png" alt="QR USDT BEP20" width="140"/>

```
0x258380877EC849e04082C4A6795d01432c3F4B7B
```

Network: **BEP20** · Asset: **USDT**  
Do not send this as TRC20 / ERC-20 / TON.

</td>
</tr>
</table>

No other wallets. QR payloads were encoded from these four addresses and decoded back with OpenCV before commit.

---

## Custom Development

Scoped work via [@E30TZ](https://t.me/E30TZ):

- Custom Telegram bots
- Automation
- Telegram Mini Apps
- Trading systems
- API integrations
- Web applications

Serious briefs only. Not a clone of TZ FX signals.

---

## Roadmap

Honest queue. Not a promise of dates or returns.

- Remaining lesson voice clips on the host (`edu_19`, `edu_20`, `edu_23`, `edu_24`, `edu_26`).
- English lesson audio, same voice pipeline, when quota allows.

Out of scope: loosening ICT, fake WR, guaranteed profit.

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
