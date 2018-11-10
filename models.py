import uuid

import flask_sqlalchemy
import sqlalchemy.dialects.postgresql

db = flask_sqlalchemy.SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schema_type = db.Column(db.String(10))
    name = db.Column(db.String(255))
    image = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Text()))
    aggregate_rating = db.Column(db.Float)
    author = db.Column(db.String(255))
    date_published = db.Column(db.Date) # needs conversion from string?
    description = db.Column(db.Text())
    keywords = db.Column(db.Text())
    recipe_category = db.Column(db.Text())
    recipe_cuisine = db.Column(db.String(255))
    recipe_ingredient = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Text()))
    recipe_instructions = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Text()))
    recipe_yield = db.Column(db.String(255))
    total_time = db.Column(db.Interval()) # needs conversion from string?

    # Add columns data here.

def map_schema_to_db(**kwargs):
    """Generates soemthing that can be put in the db from a schema object"""
    vals = {"name": kwargs.get("name", None),
            "image": kwargs.get("image", []),
            "aggregate_ating": kwargs.get("aggregateRating", None),
            "author": kwargs.get("author", None),
            "description": kwargs.get("description", None),
            "keywords": kwargs.get("keywords", []),
            "recipe_category": kwargs.get("recipeCategory", None),
            "recipe_cuisine": kwargs.get("recipeCuisine", None),
            "recipe_ingredient": kwargs.get("recipeIngredient", []),
            "recipe_instructions": [x.get("text", "") for x in kwargs.get("recipeInstructions", [])],
            "recipe_yield": kwargs.get("recipeYield", None),
            "total_time": kwargs.get("totalTime", None),
            }
    return Recipe(**vals)

class User(db.Model):
    id = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    # Add column data here. The next 2 lines as example.
        # username = db.Column(db.String(80), unique=True, nullable=False)
        # email = db.Column(db.String(120), unique=True, nullable=False)

    pass
