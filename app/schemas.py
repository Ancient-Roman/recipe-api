from pydantic import BaseModel, AnyHttpUrl
from typing import List, Optional

class RecipeCreate(BaseModel):
    url: AnyHttpUrl  # validate recipe URL

class RecipeData(BaseModel):
    url: str
    title: str
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    ingredients: List[str]
    instructions: List[str]
    dietary_restrictions: Optional[List[str]] = None

class RecipeOut(BaseModel):
    id: int
    url: str
    title: str
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    ingredients: List[str]
    instructions: List[str]
    dietary_restrictions: Optional[List[str]] = None

    class Config:
        from_attributes = True   # new name replacing orm_mode

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[List[str]] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    dietary_restrictions: Optional[List[str]] = None

    class Config:
        from_attributes = True