#!/usr/bin/env bash
# TZ FX BOT — VPS installer (Ubuntu 22.04 / 24.04)
# Does not print or invent secrets. Does not loosen ICT.
# Usage:
#   sudo bash scripts/install-vps.sh
#   sudo TZFX_DOMAIN=bot.example.com bash scripts/install-vps.sh
set -euo pipefail

REPO_URL="${TZFX_REPO:-https://github.com/e30tz/tz-fx-bot.git}"
APP_DIR="${TZFX_DIR:-/opt/tz-fx-bot}"
APP_USER="${TZFX_USER:-tzfx}"
BIND="${TZFX_BIND:-127.0.0.1:8080}"
DOMAIN="${TZFX_DOMAIN:-}"
SKIP_NGINX="${TZFX_SKIP_NGINX:-0}"
BRANCH="${TZFX_BRANCH:-main}"

if [[ ${EUID} -ne 0 ]]; then
  echo "run as root: sudo bash scripts/install-vps.sh" >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
  python3 python3-venv python3-pip git ca-certificates curl rsync \
  build-essential libssl-dev

if [[ -n "${DOMAIN}" && "${SKIP_NGINX}" != "1" ]]; then
  apt-get install -y --no-install-recommends nginx
fi

if ! id -u "${APP_USER}" >/dev/null 2>&1; then
  useradd --system --home "${APP_DIR}" --shell /usr/sbin/nologin "${APP_USER}"
fi

mkdir -p "${APP_DIR}"
SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -f "${SRC_DIR}/telegrambot_bot.py" ]]; then
  echo "install from local tree ${SRC_DIR}"
  if [[ "${SRC_DIR}" != "${APP_DIR}" ]]; then
    rsync -a --delete \
      --exclude '.git' \
      --exclude '.venv' \
      --exclude '__pycache__' \
      --exclude '.telegram_token' \
      --exclude '.gemini_key' \
      --exclude '.live.json' \
      --exclude '.env' \
      "${SRC_DIR}/" "${APP_DIR}/"
  fi
else
  echo "clone ${REPO_URL} (${BRANCH})"
  if [[ -d "${APP_DIR}/.git" ]]; then
    git -C "${APP_DIR}" fetch origin
    git -C "${APP_DIR}" checkout "${BRANCH}"
    git -C "${APP_DIR}" pull --ff-only origin "${BRANCH}"
  else
    git clone --branch "${BRANCH}" --depth 1 "${REPO_URL}" "${APP_DIR}"
  fi
fi

cd "${APP_DIR}"
ln -sfn telegrambot_bot.py bot.py

python3 -m venv "${APP_DIR}/.venv"
"${APP_DIR}/.venv/bin/pip" install --upgrade pip
"${APP_DIR}/.venv/bin/pip" install -r "${APP_DIR}/requirements-vps.txt"

install -d -m 700 -o "${APP_USER}" -g "${APP_USER}" "${APP_DIR}/.mem"
if [[ ! -f "${APP_DIR}/.telegram_token" ]]; then
  install -m 600 -o "${APP_USER}" -g "${APP_USER}" /dev/null "${APP_DIR}/.telegram_token"
  echo "created empty ${APP_DIR}/.telegram_token — put the bot token there, one line"
fi
if [[ -f "${APP_DIR}/.env.example" && ! -f "${APP_DIR}/.env" ]]; then
  install -m 600 -o "${APP_USER}" -g "${APP_USER}" "${APP_DIR}/.env.example" "${APP_DIR}/.env"
fi

chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}"
# keep venv + code readable by service user
chmod 750 "${APP_DIR}"

HOST="${BIND%:*}"
PORT="${BIND##*:}"

cat > /etc/systemd/system/tzfx.service <<EOF
[Unit]
Description=TZ FX BOT
After=network.target

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}
Environment=PYTHONUNBUFFERED=1
ExecStart=${APP_DIR}/.venv/bin/gunicorn --bind ${HOST}:${PORT} --workers 2 --threads 4 --timeout 120 wsgi:application
Restart=always
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/tzfx-tick.service <<EOF
[Unit]
Description=TZ FX BOT ICT tick

[Service]
Type=oneshot
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/.venv/bin/python ${APP_DIR}/scripts/tick.py
EOF

cat > /etc/systemd/system/tzfx-tick.timer <<EOF
[Unit]
Description=TZ FX BOT ICT tick every minute

[Timer]
OnBootSec=30s
OnUnitActiveSec=60s
AccuracySec=5s
Unit=tzfx-tick.service

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now tzfx.service tzfx-tick.timer

if [[ -n "${DOMAIN}" && "${SKIP_NGINX}" != "1" ]]; then
  cat > "/etc/nginx/sites-available/tzfx" <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN};
    client_max_body_size 20m;
    location / {
        proxy_pass http://${HOST}:${PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
    }
}
EOF
  ln -sfn /etc/nginx/sites-available/tzfx /etc/nginx/sites-enabled/tzfx
  nginx -t
  systemctl reload nginx
fi

echo
echo "TZ FX BOT installed"
echo "  dir:     ${APP_DIR}"
echo "  bind:    ${BIND}"
echo "  user:    ${APP_USER}"
echo "  health:  curl -sS http://${BIND}/"
echo
echo "Next:"
echo "  1) put Telegram token in ${APP_DIR}/.telegram_token (chmod 600)"
echo "  2) optional mentor key file ${APP_DIR}/.gemini_key"
echo "  3) set webhook to https://YOUR_DOMAIN/  (same path the bot WEBHOOK_URL uses)"
echo "  4) LIVE_MODE stays demo until you change it on purpose"
echo
echo "This script never prints tokens. Do not paste keys into the shell history."
