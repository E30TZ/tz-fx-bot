# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 1.x | Yes |

## Report a vulnerability

Telegram [@E30TZ](https://t.me/E30TZ).

Do **not** open a public GitHub issue for a live bot token, API key, host password, or user receipt.

Include the class of secret, where you saw it, and whether it is in git history. Do not paste the value. There is no bounty.

## This repository must never contain

- Telegram bot tokens
- Mentor / speech API keys (host file, never git)
- Host FTP or panel passwords
- Exchange API keys (`.live.json`)
- User memory, receipts, paper books
- A filled `.env`

Use `.env.example` only. Public donation addresses in README are not secrets.

## Runtime rules

- Connect keys: host file + `deleteMessage`. Never log a key.
- `LIVE_MODE=demo` must not call live crypto `/order`.
- Mini App `initData` is HMAC-checked before uid is trusted.
- Rotate every credential if you fork this. `@TZ_FX_BOT` is not yours.
