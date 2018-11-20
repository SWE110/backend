import uuid
import datetime

import flask_sqlalchemy
import sqlalchemy.dialects.postgresql

NAMESPACE_SEARCH = uuid.UUID("0cedf00c175348f4bc102ff7e4ffae5c")

DB = flask_sqlalchemy.SQLAlchemy()

class Recipe(DB.Model):
    meal_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meal_name = DB.Column(DB.String(255))
    image = DB.Column(sqlalchemy.dialects.postgresql.ARRAY(DB.Text()))
    aggregate_rating = DB.Column(DB.Float)
    author = DB.Column(DB.String(255))
    date_published = DB.Column(DB.Date, default=datetime.date.today)
    description = DB.Column(DB.Text())
    keywords = DB.Column(DB.Text())
    recipe_category = DB.Column(DB.Text())
    recipe_cuisine = DB.Column(DB.String(255))
    recipe_ingredient = DB.Column(sqlalchemy.dialects.postgresql.ARRAY(DB.Text()))
    recipe_instructions = DB.Column(sqlalchemy.dialects.postgresql.ARRAY(DB.Text()))
    recipe_yield = DB.Column(DB.String(255))
    total_time = DB.Column(DB.Interval())

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

class User(DB.Model):
    user_id = DB.Column(DB.String(255), primary_key=True, nullable=False)
    user_email = DB.Column(DB.String(255), unique=True, nullable=False)
    user_password = DB.Column(DB.String(255), nullable=False)
    user_first_name = DB.Column(DB.String(255), nullable=False)
    user_last_name = DB.Column(DB.String(255), nullable=False)
    security_question = DB.Column(DB.Text(), nullable=False)
    security_answer = DB.Column(DB.Text(), nullable=False)

class Search(DB.Model):
    search_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False)
    search_params = DB.Column(DB.PickleType, nullable=False)
    # Update columns as needed to be more efficient. Right now search just stores the pickled dictionary of search options

class Inventory(DB.Model):
    inventory_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = DB.Column(DB.String(255), DB.ForeignKey("user.user_id"))
    user_ingredients = DB.Column(DB.Text())

class SavedRecipe(DB.Model):
    saved_recipe_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = DB.Column(DB.String(255), DB.ForeignKey("user.user_id"))
    meal_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(), DB.ForeignKey("recipe.meal_id"), default=uuid.uuid4)

class Comment(DB.Model):
    comment_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = DB.Column(DB.String(255), DB.ForeignKey("user.user_id"))
    meal_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(), DB.ForeignKey("recipe.meal_id"), default=uuid.uuid4)
    user_comment = DB.Column(DB.Text())

class Report(DB.Model):
    report_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True, default=uuid.uuid4)
    user_id = DB.Column(DB.String(255), DB.ForeignKey("user.user_id"))
    meal_id = DB.Column(sqlalchemy.dialects.postgresql.UUID(), DB.ForeignKey("recipe.meal_id"), default=uuid.uuid4)
    user_report = DB.Column(DB.Text())
