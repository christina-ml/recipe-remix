"""
The substitution engine.

This is intentionally rule-based rather than ML-based for the MVP: each
Substitution row says "ingredient A can become ingredient B, and that
swap satisfies these dietary tags." Remixing a recipe means walking its
ingredient list and, for any ingredient that violates the requested diet,
looking up the best-voted substitution that satisfies it.

This module is a great place for contributors to extend later — e.g.
weighting substitutions by flavor-profile similarity instead of just
vote count.
"""
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models

# Ingredients considered incompatible with each diet tag. This is a simple
# denylist for the MVP; a "good first issue" is expanding this list or
# moving it into the database so it's community-editable.
DIET_DENYLIST = {
    "vegan": {
        "butter", "milk", "egg", "eggs", "honey", "cheese", "cream",
        "yogurt", "beef", "chicken", "pork", "fish", "gelatin",
    },
    "vegetarian": {"beef", "chicken", "pork", "fish", "bacon", "gelatin"},
    "dairy_free": {"butter", "milk", "cheese", "cream", "yogurt"},
    "gluten_free": {"flour", "wheat flour", "breadcrumbs", "soy sauce", "pasta"},
    "nut_free": {"almonds", "peanuts", "walnuts", "cashews", "almond milk", "peanut butter"},
}


def ingredient_violates_diet(ingredient_name: str, diet: str) -> bool:
    denylist = DIET_DENYLIST.get(diet, set())
    return ingredient_name.strip().lower() in denylist


def best_substitution_for(
    db: Session, ingredient_name: str, diet: str
) -> Optional[models.Substitution]:
    """
    Find the highest-voted substitution for `ingredient_name` that
    satisfies `diet`. Returns None if no known substitution exists.
    """
    ingredient = (
        db.query(models.Ingredient)
        .filter(func.lower(models.Ingredient.name) == ingredient_name.strip().lower())
        .first()
    )
    if not ingredient:
        return None

    candidates = (
        db.query(models.Substitution)
        .filter(models.Substitution.original_ingredient_id == ingredient.id)
        .all()
    )
    matching = [c for c in candidates if diet in (c.satisfies or [])]
    if not matching:
        return None

    def score(sub: models.Substitution) -> int:
        votes = (
            db.query(func.coalesce(func.sum(models.SubstitutionVote.value), 0))
            .filter(models.SubstitutionVote.substitution_id == sub.id)
            .scalar()
        )
        return votes or 0

    matching.sort(key=score, reverse=True)
    return matching[0]
