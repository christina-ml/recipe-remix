"""
Pydantic schemas — these define the shape of API requests/responses,
separate from the SQLAlchemy models that define the DB shape.
"""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class RecipeIngredient(BaseModel):
    name: str
    quantity: str


class RecipeBase(BaseModel):
    title: str
    description: str = ""
    ingredients: List[RecipeIngredient]
    steps: List[str]
    tags: List[str] = []


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SubstitutionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    original: str
    substitute: str
    ratio: str
    note: str
    satisfies: List[str]
    score: int = 0  # net votes, filled in by the API layer


class SubstitutionCreate(BaseModel):
    original: str
    substitute: str
    ratio: str = "1:1"
    note: str = ""
    satisfies: List[str] = []


class VoteCreate(BaseModel):
    value: int  # +1 or -1


class RemixRequest(BaseModel):
    """Request to remix a recipe for a given dietary restriction."""
    diet: str  # e.g. "vegan", "gluten_free", "dairy_free", "nut_free"


class RemixedIngredient(BaseModel):
    original: str
    quantity: str
    flagged: bool
    suggestion: Optional[SubstitutionOut] = None


class RemixResponse(BaseModel):
    recipe_id: int
    diet: str
    ingredients: List[RemixedIngredient]
