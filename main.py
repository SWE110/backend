import json
from flask import Flask, Response, jsonify, request
app = Flask(__name__)

@app.route("/recipe", methods=['GET'])
def get_recipes_top_10():
    """Gets the top 10 recipes."""
    if not is_authorized():
        return Response("{'not': 'happening'}", status=401, mimetype='application/json')

    recipes = []
    for _ in range(10):
        recipes.append(json.loads(sample_recipe))

    return jsonify(recipes)

@app.route("/recipe/<recipe_id>", methods=['GET'])
def get_recipe_by_id(recipe_id):
    """Gets one recipe by its recipe id."""
    if not is_authorized():
        return Response("{'not': 'happening'}", status=401, mimetype='application/json')

    db_response = get_recipe_from_db(recipe_id)

     # Do things

    return jsonify(json.loads(sample_recipe))

@app.route("/recipe", methods=["POST"])
def create_recipe():
    """Creates a recipe based on receieved parameters and adds it to the db."""
    if not is_authorized():
        return Response("{'not': 'happening'}", status=401, mimetype='application/json')

    add_recipe_to_db(full_content=json.loads(sample_recipe))

    return Response("Created", status=201, mimetype='application/json')

def get_recipe_from_db(recipe_id):
    """Gets a recipe from the db from the recipe id."""
    # calls from db module here
    return ""

def add_recipe_to_db(*args, **kwargs):
    """Adds a recipe to the db."""
    # calls from db module here
    if "full_content" in kwargs:
        # generate all fields as in kwargs["full_content"].
        # use this to just copy from scraped data already formatted in schema.
        pass
    else:
        # populate user settable fields from form and auto generate the rest.
        # e.g. no initial rating, no comments.
        pass
    return ""

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
    app.run(host='0.0.0.0', debug=True)
