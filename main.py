import json
import itertools

import flask
import dataset

import models

app = flask.Flask(__name__)
models.db.init_app

@app.before_first_request
def startup():
    """Startup Code"""

    # Prepopulate local DB with sample recipes
    # Will load 4 recipes in DB every time server is started
    # Stacking up recipes in the DB every reload until manually deleted
    db = dataset.connect('sqlite:///recipe.db')
    recipes_table = db['recipes']

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

@app.route("/recipe", methods=['GET'])
def get_recipes_top_10():
    """Gets the top 10 recipes."""
    if not is_authorized():
        return flask.Response("{'not': 'happening'}", status=401, mimetype='application/json')

    # Can we persist the db handle? Tried to persist in Flask.g didn't seem to
    # work but could be user error
    db = dataset.connect('sqlite:///recipe.db')
    recipes_table = db['recipes']
    all_results = recipes_table.all()
    # Get 10
    results_list = [r for r in itertools.islice(all_results, 10)]
    return flask.jsonify(results_list)

@app.route("/recipe/<recipe_id>", methods=['GET'])
def get_recipe_by_id(recipe_id):
    """Gets one recipe by its recipe id."""
    if not is_authorized():
        return flask.Response("{'not': 'happening'}", status=401, mimetype='application/json')

    db = dataset.connect('sqlite:///recipe.db')
    recipes_table = db['recipes']

    one_result_in_list = recipes_table.find(id=recipe_id)
    result = [r for r in itertools.islice(one_result_in_list, 1)][0]
    print(result)
    return flask.jsonify(result)

@app.route("/recipe", methods=["POST"])
def create_recipe():
    """Creates a recipe based on receieved parameters and adds it to the db."""
    if not is_authorized():
        return flask.Response("{'not': 'happening'}", status=401, mimetype='application/json')
    if not flask.request.is_json:
        flask.abort(400)
    print("Creating recipe")
    incoming_recipe = flask.request.get_json()

    # For now assumes full_content
    recipe_created = add_recipe_to_db(full_content=incoming_recipe)
    if not recipe_created:
        flask.abort(500)

    return flask.Response("Created", status=201, mimetype='application/json')

def add_recipe_to_db(*args, **kwargs):
    """Adds a recipe to the db."""

    print('Adding recipe to db')
    db = dataset.connect('sqlite:///recipe.db')
    recipes_table = db['recipes']

    if "full_content" in kwargs:
        # generate all fields as in kwargs["full_content"].
        # use this to just copy from scraped data already formatted in schema.
        r = kwargs["full_content"]

        # I'm unsure of recipes_table.insert return value
        db_result = recipes_table.insert(dict(
            name=r['name'],
            recipeIngredient=json.dumps(r['recipeIngredient']),
            recipeYield=r['recipeYield'],
            recipeInstructions=json.dumps(r['recipeInstructions']),
        ))

        # db_result is 1 following successful insert but I don't know what it returns on fail
        # Assuming makes an ass out of you and me
        return True
    else:
        # populate user settable fields from form and auto generate the rest.
        # e.g. no initial rating, no comments.
        pass

def is_authorized():
    """Checks if the user is authorized."""
    return True

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
