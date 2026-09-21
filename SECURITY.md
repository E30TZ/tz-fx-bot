# Security Policy

## Supported versions

| Version | Support |
|---|---|
| 1.x | Active |

## Report a vulnerability

Telegram the developer: [@E30TZ](https://t.me/E30TZ)

Do **not** open a public GitHub issue for a live token, Gemini key, host password, or user receipt.

Include:

- what is exposed (bot token, API key, host panel, user PII)
- where you found it (file, log, Mini App response)
- whether it is already in git history

You will get a reply when the key is rotated. Do not expect a bounty.

## What this repo must never contain

- Telegram bot tokens (`123456:ABC…`)
- Gemini / Google API keys
- Host FTP or cPanel passwords (`.host_ftp`, `.host_new`)
- Exchange API keys (`.live.json`)
- User memory, receipts, paper books
- `.env` with real values

Use `.env.example` only.

## Runtime rules already in the bot

- Connect keys: host file + `deleteMessage`. Never `log()` a key.
- `LIVE_MODE=demo` must not call live crypto `/order`.
- Mini App initData is HMAC-checked before uid is trusted.
- CGI webhook has no `secret_token` because Passenger is off — keep the script path unguessable and the host TLS valid.

## If you fork this

Rotate **every** credential. The public bot `@TZ_FX_BOT` is not yours.
