import json

import flask
import flask_restful
from flask import g
import models
import resources
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cap@104.248.220.214/RecipeDB'
api = flask_restful.Api(app)
models.DB.init_app(app)

@app.before_first_request
def startup():
    """Startup Code"""
    test_set_up()

def test_set_up():
    """Inititialize some mock data for testing."""
    models.DB.create_all()

api.add_resource(resources.RecipeList, "/recipe")
api.add_resource(resources.Recipe, "/recipe/<recipe_id>")
api.add_resource(resources.Search, "/search")
api.add_resource(resources.CreateUser, "/user/create")
api.add_resource(resources.TestAuth, "/testauth")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)
