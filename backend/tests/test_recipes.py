"""
Basic API tests using an in-memory SQLite DB so CI doesn't need Postgres
running. This is a deliberate trade-off for test speed/simplicity — if you
add a feature that relies on Postgres-specific behavior, mention it in
your PR so we can adjust.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def sample_recipe_payload():
    return {
        "title": "Test Pancakes",
        "description": "for testing",
        "ingredients": [
            {"name": "flour", "quantity": "1 cup"},
            {"name": "milk", "quantity": "1 cup"},
            {"name": "butter", "quantity": "2 tbsp"},
        ],
        "steps": ["mix", "cook"],
        "tags": ["breakfast"],
    }


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_and_get_recipe(client):
    resp = client.post("/recipes/", json=sample_recipe_payload())
    assert resp.status_code == 201
    recipe_id = resp.json()["id"]

    resp = client.get(f"/recipes/{recipe_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Test Pancakes"


def test_get_missing_recipe_404s(client):
    resp = client.get("/recipes/9999")
    assert resp.status_code == 404


def test_remix_flags_dairy_and_suggests_substitution(client):
    create_resp = client.post("/recipes/", json=sample_recipe_payload())
    recipe_id = create_resp.json()["id"]

    client.post(
        "/substitutions/",
        json={
            "original": "milk",
            "substitute": "oat milk",
            "ratio": "1:1",
            "note": "neutral flavor",
            "satisfies": ["vegan", "dairy_free"],
        },
    )

    resp = client.post(f"/recipes/{recipe_id}/remix", json={"diet": "dairy_free"})
    assert resp.status_code == 200
    body = resp.json()

    milk_entry = next(i for i in body["ingredients"] if i["original"] == "milk")
    assert milk_entry["flagged"] is True
    assert milk_entry["suggestion"]["substitute"] == "oat milk"

    flour_entry = next(i for i in body["ingredients"] if i["original"] == "flour")
    assert flour_entry["flagged"] is False


def test_voting_changes_substitution_score(client):
    resp = client.post(
        "/substitutions/",
        json={"original": "honey", "substitute": "maple syrup", "satisfies": ["vegan"]},
    )
    sub_id = resp.json()["id"]

    client.post(f"/substitutions/{sub_id}/vote", json={"value": 1})
    resp = client.post(f"/substitutions/{sub_id}/vote", json={"value": 1})
    assert resp.json()["score"] == 2

    resp = client.post(f"/substitutions/{sub_id}/vote", json={"value": -1})
    assert resp.json()["score"] == 1
