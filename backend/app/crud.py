"""Database access helpers, kept separate from route handlers so the
routers stay thin and the logic here stays easy to unit test."""
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas


def get_recipes(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Recipe).offset(skip).limit(limit).all()


def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=[ing.model_dump() for ing in recipe.ingredients],
        steps=recipe.steps,
        tags=recipe.tags,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, recipe_id: int) -> bool:
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        return False
    db.delete(db_recipe)
    db.commit()
    return True


def get_or_create_ingredient(db: Session, name: str) -> models.Ingredient:
    name = name.strip().lower()
    ingredient = (
        db.query(models.Ingredient)
        .filter(func.lower(models.Ingredient.name) == name)
        .first()
    )
    if ingredient:
        return ingredient
    ingredient = models.Ingredient(name=name)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


def create_substitution(db: Session, sub: schemas.SubstitutionCreate) -> models.Substitution:
    original = get_or_create_ingredient(db, sub.original)
    substitute = get_or_create_ingredient(db, sub.substitute)
    db_sub = models.Substitution(
        original_ingredient_id=original.id,
        substitute_ingredient_id=substitute.id,
        ratio=sub.ratio,
        note=sub.note,
        satisfies=sub.satisfies,
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub


def substitution_score(db: Session, substitution_id: int) -> int:
    votes = (
        db.query(func.coalesce(func.sum(models.SubstitutionVote.value), 0))
        .filter(models.SubstitutionVote.substitution_id == substitution_id)
        .scalar()
    )
    return votes or 0


def to_substitution_out(db: Session, sub: models.Substitution) -> schemas.SubstitutionOut:
    return schemas.SubstitutionOut(
        id=sub.id,
        original=sub.original.name,
        substitute=sub.substitute.name,
        ratio=sub.ratio,
        note=sub.note,
        satisfies=sub.satisfies or [],
        score=substitution_score(db, sub.id),
    )


def cast_vote(db: Session, substitution_id: int, value: int) -> models.SubstitutionVote:
    vote = models.SubstitutionVote(substitution_id=substitution_id, value=value)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote
