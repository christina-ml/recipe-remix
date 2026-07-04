from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.substitutions import best_substitution_for, ingredient_violates_diet

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=List[schemas.Recipe])
def list_recipes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_recipes(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Recipe, status_code=201)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)


@router.get("/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    if not crud.delete_recipe(db, recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")


@router.post("/{recipe_id}/remix", response_model=schemas.RemixResponse)
def remix_recipe(recipe_id: int, remix: schemas.RemixRequest, db: Session = Depends(get_db)):
    """
    Walk a recipe's ingredients and, for anything that violates the
    requested diet, attach the best-known substitution (if one exists).
    """
    recipe = crud.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    remixed_ingredients = []
    for ing in recipe.ingredients:
        name = ing["name"]
        flagged = ingredient_violates_diet(name, remix.diet)
        suggestion = None
        if flagged:
            sub = best_substitution_for(db, name, remix.diet)
            if sub:
                suggestion = crud.to_substitution_out(db, sub)
        remixed_ingredients.append(
            schemas.RemixedIngredient(
                original=name,
                quantity=ing["quantity"],
                flagged=flagged,
                suggestion=suggestion,
            )
        )

    return schemas.RemixResponse(
        recipe_id=recipe.id, diet=remix.diet, ingredients=remixed_ingredients
    )
