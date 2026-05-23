# Vusense Decision App

Browser app for the executive **Problem Discovery** (Gate 1) and **Decision Tree** (Gate 2) process. Self-hosted with Docker; data stays in `./data` (not committed to command-center).

## Quick start

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. From this folder (`decision-app/`):

   ```bash
   cp .env.example .env
   # Edit .env — set AUTH_USERNAME and AUTH_PASSWORD
   docker compose up -d
   ```

3. Open **http://localhost:8501** and sign in.
4. Use the sidebar: **EB-25** → **Problem Statement** → **RFC** → **Handoff** → **Context Card** → **Framework** → **Register** → **Export**.

Stop the app:

```bash
docker compose down
```

Your data remains in `./data/`.

## Optional: multi-user credentials

Copy `credentials.yaml.example` to `credentials.yaml`, set bcrypt password hashes, and restart. If `credentials.yaml` exists, it overrides `.env` auth.

## Local development (without Docker)

```bash
cd decision-app
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
set PYTHONPATH=.
streamlit run app/main.py
```

Run tests:

```bash
pytest
```

## Exports

Markdown files are written to `data/exports/{decision-id}/`. Download a ZIP from the **Export** page for Obsidian or board packs.

## Methodology

Process documentation lives in the parent repo: [../README.md](../README.md) and [../decision-framework/](../decision-framework/).
