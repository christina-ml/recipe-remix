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

## License

MIT — see [LICENSE](LICENSE).
