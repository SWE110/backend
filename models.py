import flask_sqlalchemy
import sqlalchemy.dialects.postgresql

db = flask_sqlalchemy.SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True)
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

    pass

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add column data here. The next 2 lines as example.
        # username = db.Column(db.String(80), unique=True, nullable=False)
        # email = db.Column(db.String(120), unique=True, nullable=False)

    pass
