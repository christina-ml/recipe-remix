"""
SQLAlchemy models.

Schema overview:
- Recipe: a dish with ingredients (JSON list) and steps
- Ingredient: a normalized ingredient name, used by the substitution engine
- Substitution: a suggested swap from one ingredient to another, tagged by
  which dietary restrictions it satisfies (vegan, gluten_free, etc.)
- SubstitutionVote: community upvote/downvote on whether a substitution
  actually works well in practice
"""
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
    Float,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, default="")
    # Stored as a list of {"name": str, "quantity": str} objects.
    ingredients = Column(JSON, nullable=False)
    steps = Column(JSON, nullable=False)  # list of strings
    tags = Column(JSON, default=list)  # e.g. ["dessert", "quick"]
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)


class Substitution(Base):
    __tablename__ = "substitutions"

    id = Column(Integer, primary_key=True, index=True)
    original_ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    substitute_ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    ratio = Column(String(50), default="1:1")  # e.g. "1:1", "3/4 cup per 1 cup"
    note = Column(Text, default="")  # e.g. "expect a denser, moister texture"
    # Which restrictions this swap satisfies, e.g. ["vegan", "dairy_free"]
    satisfies = Column(JSON, default=list)

    original = relationship("Ingredient", foreign_keys=[original_ingredient_id])
    substitute = relationship("Ingredient", foreign_keys=[substitute_ingredient_id])


class SubstitutionVote(Base):
    __tablename__ = "substitution_votes"

    id = Column(Integer, primary_key=True, index=True)
    substitution_id = Column(Integer, ForeignKey("substitutions.id"), nullable=False)
    value = Column(Integer, nullable=False)  # +1 or -1
    created_at = Column(DateTime(timezone=True), server_default=func.now())
