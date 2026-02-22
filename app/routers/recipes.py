from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import crud, schemas, models
from ..database import get_db
from ..scraper import fetch_and_parse_recipe

router = APIRouter(prefix="/recipes")

@router.post("/", response_model=schemas.RecipeOut, summary="Add a new recipe", description="Scrape a recipe from a URL and save it to the database. Returns the saved recipe if it already exists.")
def add_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    # look for existing recipe with same URL
    existing = db.query(models.Recipe).filter(models.Recipe.url == str(recipe.url)).first()
    if existing:
        return existing
    
    # scrape and normalize recipe data
    try:
        data = fetch_and_parse_recipe(str(recipe.url))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scrape failed: {e}")

    # save into database
    saved = crud.create_recipe(db, data)
    return saved

@router.get("/", response_model=list[schemas.RecipeOut], summary="List all recipes", description="Retrieve a paginated list of all recipes in the database.")
def list_recipes(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return db.query(models.Recipe).offset(skip).limit(limit).all()

@router.get("/search", response_model=list[schemas.RecipeOut], summary="Search recipes", description="Search recipes by title, ingredients, or maximum cooking time.")
def search_recipes(
    q: str | None = None,
    max_time: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe)

    if q:
        query = query.filter(
            or_(
                models.Recipe.title.ilike(f"%{q}%"),
                models.Recipe.ingredients.ilike(f"%{q}%")
            )
        )

    if max_time:
        query = query.filter(models.Recipe.total_time <= max_time)

    return query.all()

@router.get("/{recipe_id}", response_model=schemas.RecipeOut, summary="Get a recipe by ID", description="Retrieve a specific recipe by its ID.")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.patch("/{recipe_id}", response_model=schemas.RecipeOut, summary="Update a recipe", description="Update one or more fields of an existing recipe.")
def update_recipe(
    recipe_id: int,
    recipe_update: schemas.RecipeUpdate,
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_data = recipe_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(recipe, field, value)

    db.commit()
    db.refresh(recipe)

    return recipe

@router.delete("/{recipe_id}", status_code=204, summary="Delete a recipe", description="Delete a recipe from the database.")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()

    return None