from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    # Add columns data here.

    pass

class User(db.Model):
    # Add column data here. The next 3 lines as example.
        # id = db.Column(db.Integer, primary_key=True)
        # username = db.Column(db.String(80), unique=True, nullable=False)
        # email = db.Column(db.String(120), unique=True, nullable=False)

    pass