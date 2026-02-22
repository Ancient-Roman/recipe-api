from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String)
    cook_time = Column(Integer, nullable=True)
    prep_time = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=True)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    dietary_restrictions = Column(JSON, nullable=True)