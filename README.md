# TSS Music — Production Telegram Music & Video VC Platform

This repository is designed for the user's requested workflow: **GitHub Actions test → final publication → Railway deployment/control workflow → single Ubuntu VPS runtime**.

## Runtime architecture

The VPS is the actual playback host. Railway is not required for an active Voice Chat session. The VPS runs the bot, assistants, yt-dlp, FFmpeg, PyTgCalls, database, cache, monitoring and dashboard.

## Minimum requirements

- Ubuntu VPS
- Python 3.11+
- FFmpeg
- Telegram Bot token
- Telegram API ID/hash
- Owner numeric Telegram ID
- Assistant 1 session string
- Internet access
- Git

Assistants 2–6 and external providers are optional.

## GitHub first test

Push this repository to GitHub. The included workflow installs FFmpeg and Python dependencies, compiles every module, runs unit tests and performs import preflight. It does **not** require Telegram secrets, so repository tests are safe to run before production credentials are added.

## Local/VPS setup

```bash
sudo apt update
sudo apt install -y ffmpeg python3.11 python3.11-venv git
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python scripts/preflight.py
python bot.py
```

`ASSISTANT_1_SESSION` is mandatory. Sessions 2–6 can be empty.

## Commands

- `/play <query/url>` — audio-only playback request
- `/vdplay <query/url>` — video+audio playback request
- `/queue` — queue
- `/nowplaying` — current item
- `/stop` — stop and clear

## Dashboard

`http://SERVER:8080/` and `GET /health` are provided. For production, put HTTPS/reverse proxy and a proper Telegram Login configuration in front of the dashboard. Never expose `.env`.

## Important PyTgCalls integration note

PyTgCalls APIs have changed between releases. This project centralizes PyTgCalls media binding in `music/player.py` and assistant lifecycle in `assistants/worker.py`. The repository is structured so a library API change is isolated to those adapters rather than spread across the platform. The player supervisor already owns independent queues, locks, assistant selection and persistent state.

## Production hardening before public launch

1. Configure HTTPS and Telegram Login domain.
2. Set a strong firewall: SSH + HTTPS + required dashboard port only as needed.
3. Use SSH keys and fail2ban.
4. Run under systemd using `systemd/tss-music.service`.
5. Keep secrets only in `/opt/tss-music/.env` with restrictive permissions.
6. Configure automated database backups.
7. Set cache limits and preserve minimum free disk.
8. Validate your PyTgCalls/Kurigram versions against your VPS before opening the service publicly.

## Railway workflow

Railway should be used as the deployment/control pipeline if desired. The final active runtime should remain the single Ubuntu VPS. Do not make Railway a dependency for Voice Chat playback.

A practical deployment pattern is:

`GitHub → Railway build/deploy workflow → VPS deployment command/agent → /opt/tss-music → systemd restart`

Do not place bot tokens, API hashes or session strings in GitHub source files.

## VPS layout

```text
/opt/tss-music/
├── app files
├── data/
├── cache/audio/
├── cache/video/
├── cache/thumbnails/
├── cache/metadata/
├── temp/
├── logs/
├── backups/
└── sessions/
```

The cache is disposable. Persistent database/state is separate.
