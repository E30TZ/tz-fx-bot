# Connect this workspace to GitHub

Repo: `e30tz/tz-fx-bot` · public · branch `main`

Do **not** paste a Personal Access Token into Telegram or this chat.

## What you do (once)

1. Open https://github.com/new  
   - Repository name: `tz-fx-bot`  
   - Owner: `e30tz`  
   - Public  
   - **Do not** add README, .gitignore, or LICENSE (they already exist here).

2. Add the **SSH public key** of this workspace:  
   GitHub → **Settings → SSH and GPG keys → New SSH key**  
   Title: `tz-fx-bot arena`  
   Key type: Authentication  
   Paste the `ssh-ed25519 … tz-fx-bot@arena` line from the agent.

3. Reply in the chat: `کلید اضافه شد`

The agent then runs:

```bash
cd /home/user/tz-fx-bot
git remote add origin git@github.com:e30tz/tz-fx-bot.git
git push -u origin main
git push origin v1.0.0
```

## Do not

- Paste `ghp_…` / `github_pat_…` into the chat.
- Force-push over an unrelated repo.
- Put `.telegram_token` or host passwords in GitHub.
