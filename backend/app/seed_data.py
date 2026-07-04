"""
Populates the database with a handful of recipes and common substitutions,
so the app has something to look at immediately after setup.

Run with:  python -m app.seed_data
"""
from app.database import Base, SessionLocal, engine
from app import crud, schemas

SUBSTITUTIONS = [
    dict(original="butter", substitute="applesauce", ratio="1:1",
         note="Works well in baked goods; expect a denser, moister crumb.",
         satisfies=["vegan", "dairy_free"]),
    dict(original="butter", substitute="coconut oil", ratio="1:1",
         note="Good for frying and baking; adds a faint coconut flavor.",
         satisfies=["vegan", "dairy_free"]),
    dict(original="milk", substitute="oat milk", ratio="1:1",
         note="Neutral flavor, works in almost everything.",
         satisfies=["vegan", "dairy_free", "nut_free"]),
    dict(original="egg", substitute="flax egg (1 tbsp flaxseed + 3 tbsp water)", ratio="1:1",
         note="Best in baked goods where eggs are a binder, not the star.",
         satisfies=["vegan"]),
    dict(original="flour", substitute="almond flour", ratio="1:1",
         note="Denser result; good for cookies, less ideal for bread.",
         satisfies=["gluten_free"]),
    dict(original="flour", substitute="oat flour", ratio="1:1.25",
         note="Mild flavor, slightly more absorbent than wheat flour.",
         satisfies=["gluten_free"]),
    dict(original="honey", substitute="maple syrup", ratio="1:1",
         note="Slightly less sweet, subtly different flavor.",
         satisfies=["vegan"]),
    dict(original="cheese", substitute="nutritional yeast", ratio="1/4 cup per 1 cup",
         note="Adds a savory, cheesy flavor; won't melt like real cheese.",
         satisfies=["vegan", "dairy_free"]),
    dict(original="peanut butter", substitute="sunflower seed butter", ratio="1:1",
         note="Similar texture, nut-free.",
         satisfies=["nut_free"]),
]

RECIPES = [
    dict(
        title="Classic Chocolate Chip Cookies",
        description="Chewy in the middle, crisp at the edges.",
        ingredients=[
            {"name": "flour", "quantity": "2 1/4 cups"},
            {"name": "butter", "quantity": "1 cup"},
            {"name": "egg", "quantity": "2"},
            {"name": "chocolate chips", "quantity": "2 cups"},
            {"name": "honey", "quantity": "1/4 cup"},
        ],
        steps=[
            "Cream butter and honey together.",
            "Beat in eggs one at a time.",
            "Mix in flour until just combined.",
            "Fold in chocolate chips.",
            "Bake at 375°F for 10-12 minutes.",
        ],
        tags=["dessert", "baking"],
    ),
    dict(
        title="Weeknight Pancakes",
        description="Fluffy pancakes with pantry staples.",
        ingredients=[
            {"name": "flour", "quantity": "1 1/2 cups"},
            {"name": "milk", "quantity": "1 1/4 cups"},
            {"name": "egg", "quantity": "1"},
            {"name": "butter", "quantity": "3 tbsp, melted"},
            {"name": "honey", "quantity": "2 tbsp"},
        ],
        steps=[
            "Whisk dry ingredients together.",
            "Whisk in milk, egg, melted butter, and honey.",
            "Cook 1/4 cup portions on a hot griddle until bubbles form, then flip.",
        ],
        tags=["breakfast", "quick"],
    ),
    dict(
        title="Creamy Mac and Cheese",
        description="Stovetop, no baking required.",
        ingredients=[
            {"name": "pasta", "quantity": "1 lb"},
            {"name": "cheese", "quantity": "2 cups, shredded"},
            {"name": "milk", "quantity": "1 cup"},
            {"name": "butter", "quantity": "2 tbsp"},
            {"name": "flour", "quantity": "2 tbsp"},
        ],
        steps=[
            "Cook pasta until al dente.",
            "Melt butter, whisk in flour to make a roux.",
            "Slowly whisk in milk until thickened.",
            "Stir in cheese until melted, then toss with pasta.",
        ],
        tags=["dinner", "comfort food"],
    ),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(crud.models.Recipe).count() == 0:
            for r in RECIPES:
                db.add(crud.models.Recipe(**r))
            db.commit()
            print(f"Seeded {len(RECIPES)} recipes.")
        else:
            print("Recipes already present, skipping recipe seed.")

        if db.query(crud.models.Substitution).count() == 0:
            for s in SUBSTITUTIONS:
                crud.create_substitution(db, schemas.SubstitutionCreate(**s))
            print(f"Seeded {len(SUBSTITUTIONS)} substitutions.")
        else:
            print("Substitutions already present, skipping substitution seed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
