from sqlalchemy.orm import Session

from app.schemas import RecipeData
from . import models

def create_recipe(db: Session, recipe_data: RecipeData):
    recipe = models.Recipe(**recipe_data.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def list_recipes(db: Session):
    return db.query(models.Recipe).all()