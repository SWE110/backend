import json

import flask
import flask_restful

import models
import resources

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cap@104.248.220.214/RecipeDB'
api = flask_restful.Api(app)
models.db.init_app(app)

@app.before_first_request
def startup():
    """Startup Code"""

    test_set_up()

def test_set_up():
    """Inititialize some mock data for testing."""
    models.db.create_all()

    with open('recipes.txt') as json_data:
        recipes = json.load(json_data)

    for r in recipes:
        resources.add_recipe_to_db(full_content=r)

api.add_resource(resources.RecipeList, "/recipe")
api.add_resource(resources.Recipe, "/recipe/<recipe_id>")

sample_recipe = """
 {
      "@context": "http://schema.org",
      "@type": "Recipe",
      "author": "Jake  Smith",
      "cookTime": "PT2H",
      "datePublished": "2015-05-18",
      "description": "Your recipe description goes here",
      "image": "http://www.example.com/images.jpg",
      "recipeIngredient": [
        "ingredient 1",
        "ingredient 2",
        "ingredient 3",
        "ingredient 4",
        "ingredient 5"
      ],
      "interactionStatistic": {
        "@type": "InteractionCounter",
        "interactionType": "http://schema.org/Comment",
        "userInteractionCount": "5"
      },
      "name": "Rand's Cookies",
      "nutrition": {
        "@type": "NutritionInformation",
        "calories": "1200 calories",
        "carbohydrateContent": "12 carbs",
        "proteinContent": "9 grams of protein",
        "fatContent": "9 grams fat"
      },
      "prepTime": "PT15M",
      "recipeInstructions": "This is the long part, etc.",
      "recipeYield": "12 cookies"
}
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6666)
