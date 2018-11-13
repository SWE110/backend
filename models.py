import uuid
import datetime

import flask_sqlalchemy
import sqlalchemy.dialects.postgresql

db = flask_sqlalchemy.SQLAlchemy()

class Recipe(db.Model):
    meal_id = db.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meal_name = db.Column(db.String(255))
    image = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Text()))
    aggregate_rating = db.Column(db.Float)
    author = db.Column(db.String(255))
    date_published = db.Column(db.Date, default=datetime.date.today)
    description = db.Column(db.Text())
    keywords = db.Column(db.Text())
    recipe_category = db.Column(db.Text())
    recipe_cuisine = db.Column(db.String(255))
    recipe_ingredient = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Text()))
    recipe_instructions = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Text()))
    recipe_yield = db.Column(db.String(255))
    total_time = db.Column(db.Interval())

    def map_db_to_dict(self):
        """Returns a dictionary representation of this object that can be jsonified."""
        return {"meal_id": self.meal_id.hex,
                "name": self.meal_name,
                "image": self.image,
                "aggregate_rating": self.aggregate_rating,
                "author": self.author,
                "date_published": self.date_published.isoformat(),
                "desciption": self.description,
                "keywords": self.keywords,
                "recipe_category": self.recipe_category,
                "recipe_cuisine": self.recipe_cuisine,
                "recipe_ingredient": self.recipe_ingredient,
                "recipe_instructions": self.recipe_instructions,
                "recipe_yield": self.recipe_yield,
                "total_time": self.total_time.total_seconds(),
                }

def map_schema_to_db(**kwargs):
    """Generates soemthing that can be put in the db from a schema object"""
    vals = {"meal_name": kwargs.get("name", None),
            "image": kwargs.get("image", []),
            "aggregate_rating": kwargs.get("aggregateRating", {}).get("ratingValue", None),
            "author": kwargs.get("author", {}).get("name", None),
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
    user_id = db.Column(db.String(255), primary_key=True, nullable=False)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_first_name = db.Column(db.String(255), nullable=False)
    user_last_name = db.Column(db.String(255), nullable=False)
    security_question = db.Column(db.Text(), nullable=False)
    security_answer = db.Column(db.Text(), nullable=False)

class Inventory(db.Model):
    inventory_id = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(255), db.ForeignKey("user.user_id"))
    user_ingredients = db.Column(db.Text())

class SavedRecipe(db.Model):
    saved_recipe_id = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(255), db.ForeignKey("user.user_id"))
    meal_id = db.Column(sqlalchemy.dialects.postgresql.UUID(), db.ForeignKey("recipe.meal_id"), default=uuid.uuid4)

class Comment(db.Model):
    comment_id = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(255), db.ForeignKey("user.user_id"))
    meal_id = db.Column(sqlalchemy.dialects.postgresql.UUID(), db.ForeignKey("recipe.meal_id"), default=uuid.uuid4)
    user_comment = db.Column(db.Text())

class Report(db.Model):
    report_id = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(255), db.ForeignKey("user.user_id"))
    meal_id = db.Column(sqlalchemy.dialects.postgresql.UUID(), db.ForeignKey("recipe.meal_id"), default=uuid.uuid4)
    user_report = db.Column(db.Text())
