# Recipe Remix 🍳

Got a recipe but can't eat one of the ingredients? Recipe Remix flags anything
that violates a dietary restriction (vegan, vegetarian, dairy-free,
gluten-free, nut-free) and suggests a community-voted substitution — with
notes on ratio and how it'll change the result.

Built as a learning project and an open-source repo for devs interested. Contributions welcome — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Stack

- **Backend**: Python3, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React (Vite), Tailwind CSS
- **Infra**: Docker Compose (for local Postgres), GitHub Actions (CI)

## Project structure

```
recipe-remix/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + router registration
│   │   ├── models.py          # SQLAlchemy ORM models
│   │   ├── schemas.py         # Pydantic request/response schemas
│   │   ├── crud.py            # DB access helpers
│   │   ├── substitutions.py   # The substitution/remix engine
│   │   ├── seed_data.py       # Sample recipes + substitutions
│   │   └── routers/
│   │       ├── recipes.py
│   │       └── substitutions.py
│   └── tests/
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/
└── docker-compose.yml          # Local Postgres
```

## Getting started

### 1. Start Postgres

```bash
docker compose up -d
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Load sample data (a few recipes + common substitutions)
python3 -m app.seed_data

# Run the API
uvicorn app.main:app --reload
```

The API is now running at `http://localhost:8000`. Interactive docs (Swagger)
are at `http://localhost:8000/docs` — useful for poking at endpoints before
the frontend is wired up.

### 3. Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

The app is now running at `http://localhost:5173`.

## Running tests

```bash
cd backend
pytest -v
```

Backend tests use an in-memory SQLite database, so you don't need Postgres
running just to run the test suite.

## How the substitution engine works

Each `Substitution` row says "ingredient A can become ingredient B, and this
swap satisfies these dietary tags" (see `backend/app/substitutions.py`).
Remixing a recipe means:

1. Check each ingredient against a denylist for the chosen diet (e.g. "milk"
   violates `dairy_free`).
2. For any flagged ingredient, look up known substitutions that satisfy that
   diet.
3. Sort by community vote score and return the best one.

This is intentionally simple for the MVP — see [CONTRIBUTING.md](CONTRIBUTING.md)
for ideas on how to extend it (flavor-profile matching, more diets, etc).

## Stopping and restarting the app

To stop everything: `Ctrl+C` in the terminals running `uvicorn` and `npm run dev`,
then `docker compose down` (no `-v` flag) to stop Postgres while keeping your data.

To start again: `docker compose up -d`, wait for `docker compose ps` to show
`healthy`, then start the backend (`uvicorn app.main:app --reload`) and frontend
(`npm run dev`) as usual. No need to reinstall dependencies or reseed the
database — those are one-time setup steps, not part of the regular start/stop
cycle.

**Why this order matters:**

- **Postgres needs a moment to become `healthy` before the backend can connect
  reliably.** Starting `uvicorn` too early can produce misleading connection
  errors that look like a config problem but are really just a timing issue.
- **`docker compose down` (without `-v`) stops the container but keeps its data
  volume**, so your recipes and substitutions survive a restart. Adding `-v`
  _deletes_ that volume — only do that intentionally, e.g. to reset the
  database to a clean state.
- **Dependencies and seed data only need to be (re)done once** — reinstalling
  or reseeding on every restart is unnecessary and, in the case of seeding,
  will just skip since the check in `seed_data.py` sees existing rows.

## Steps to Shut down (stop) & Restart the app

**Shut down:**

1. In the terminal running `uvicorn`, press `Ctrl+C`.
2. In the terminal running `npm run dev` (frontend), press `Ctrl+C`.
3. Stop Postgres:

bash

`cd ~/Desktop/projects-2026/recipe-remix
docker compose down`

(No `-v` this time — you want to _keep_ the data you seeded, not wipe it.)

**Start back up:**

1. Postgres:

bash

`docker compose up -d
docker compose ps        # confirm "healthy" before moving on`

1. Backend (new terminal):

bash

`cd ~/Desktop/projects-2026/recipe-remix/backend
source venv/bin/activate
uvicorn app.main:app --reload`

No need to re-run `pip install` or `python3 -m app.seed_data` this time — the venv and the database both already have what they need from before.

1. Frontend (another terminal):

bash

`cd ~/Desktop/projects-2026/recipe-remix/frontend
npm run dev`

1. Check `http://localhost:5173` — your seeded recipes (and anything you added, like the stir-fry) should still be there, since you didn't wipe the volume this time.

Christina’s note: In another terminal, you can also run:

`curl http://localhost:8000/health`
to see if it says `{"status":"ok"}%`

## Troubleshooting

**Postgres connection errors (e.g. "role does not exist"):** if you have another
Postgres instance already running locally on port 5432, it can conflict with
Docker's container. This project maps Docker's Postgres to port `5433` instead
(see `docker-compose.yml` and `.env.example`) to avoid that collision.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for setup notes, good first issue ideas, and PR guidelines.

## License

MIT — see [LICENSE](LICENSE).
