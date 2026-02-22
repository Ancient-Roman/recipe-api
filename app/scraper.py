# scraper.py - fetches and parses recipe data from URLs using recipe-scrapers library
# type: ignore

import requests
from recipe_scrapers import scrape_me

from app.schemas import RecipeData

def fetch_and_parse_recipe(url: str) -> RecipeData:
    # fetch HTML
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()

    # extract structured recipe info
    scraper = scrape_me(url)

    return RecipeData(
        url=url,
        title=safe_call(scraper, "title"), 
        ingredients=safe_call(scraper, "ingredients", []),
        instructions=safe_call(scraper, "instructions", "").split("\n"),  # split into steps
        total_time=safe_call(scraper, "total_time"),
        prep_time=safe_call(scraper, "prep_time"),
        cook_time=safe_call(scraper, "cook_time"),
        dietary_restrictions=safe_call(scraper, "dietary_restrictions", [])
    )

# helper to call scraper methods safely, returning None if not implemented or fails
def safe_call(scraper, method_name, default=None):
    method = getattr(scraper, method_name, None)
    if callable(method):
        try:
            return method()
        except Exception:
            return default
    return default