from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import recipes, substitutions

# Creates tables if they don't exist yet. For real migrations (renaming
# columns, etc.) we use Alembic instead — see backend/alembic/.
# Wrapped in try/except so importing this module doesn't crash in
# environments without a reachable database (e.g. CI, where tests use
# their own in-memory SQLite instead).
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: could not create tables at startup: {e}")

app = FastAPI(
    title="Recipe Remix API",
    description="Smart ingredient substitutions for dietary restrictions.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes.router)
app.include_router(substitutions.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
