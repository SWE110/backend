import json

import flask
import dataset
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

    # Prepopulate local DB with sample recipes
    # Will load 4 recipes in DB every time server is started
    # Stacking up recipes in the DB every reload until manually deleted
    db = dataset.connect('sqlite:///recipe.db')
    recipes_table = db['recipes']
    models.db.create_all()

    with open('recipes.txt') as json_data:
        recipes = json.load(json_data)

    for r in recipes:
        # TODO Fix this barbarian stuff
        recipes_table.insert(dict(
            name=r['name'],
            # Need better format for ingredients to allow searching
            recipeIngredient=json.dumps(r['recipeIngredient']),
            recipeYield=r['recipeYield'],
            # Need to extract the steps. Keep steps broken up or merge them into one text file?
            # For now steps are nested
            recipeInstructions=json.dumps(r['recipeInstructions'])
        ))
    db.commit()

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
