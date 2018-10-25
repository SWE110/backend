from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add columns data here.

    pass

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add column data here. The next 2 lines as example.
        # username = db.Column(db.String(80), unique=True, nullable=False)
        # email = db.Column(db.String(120), unique=True, nullable=False)

    pass
