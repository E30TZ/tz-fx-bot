# VPS install

Shared CGI on pingbaz stays the live desk until you migrate on purpose. This path is for a **new** Ubuntu VPS.

## One shot

On a clean Ubuntu 22.04 / 24.04 box:

```bash
sudo apt-get update
sudo apt-get install -y git
git clone https://github.com/e30tz/tz-fx-bot.git
cd tz-fx-bot
sudo bash scripts/install-vps.sh
```

With nginx on a domain:

```bash
sudo TZFX_DOMAIN=bot.example.com bash scripts/install-vps.sh
```

Then:

1. Put the bot token in `/opt/tz-fx-bot/.telegram_token` (mode `600`). Never commit it.
2. Point Telegram webhook at `https://bot.example.com/` (or your TLS terminator).
3. `curl -sS http://127.0.0.1:8080/` should print `TZ FX online v=1.0.0`.
4. Leave `LIVE_MODE=demo` until you intentionally go live.

## Layout

| | |
|---|---|
| Code | `/opt/tz-fx-bot` |
| WSGI | `wsgi.py` → `bot.py` symlink of `telegrambot_bot.py` |
| Process | `systemd` unit `tzfx.service` (gunicorn) |
| ICT tick | `tzfx-tick.timer` every minute (`scripts/tick.py`) |
| Secrets | `.telegram_token`, `.gemini_key`, `.live.json` — host only |

## What this does not do

- Does not copy keys from the shared host.
- Does not loosen ICT, WAIT, or stop-loss rules.
- Does not enable live exchange orders.
- Does not deploy to the current pingbaz CGI.

MT5 still runs on a Windows PC via `tz_mt5_bridge.py`. The VPS does not host MetaTrader.
