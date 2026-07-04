from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import recipes, substitutions

# Creates tables if they don't exist yet. For real migrations (renaming
# columns, etc.) we use Alembic instead — see backend/alembic/.
Base.metadata.create_all(bind=engine)

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
