import json
from flask import Flask, Response, jsonify, request
app = Flask(__name__)

@app.route("/recipe", methods=['GET'])
def get_recipes_top_10():
    if not is_authorized():
        return Response("{'not': 'happening'}", status=401, mimetype='application/json')
    
    recipes = []
    for _ in range(10):
        recipes.append(json.loads(sample_recipe))
    
    return jsonify(recipes)

@app.route("/recipe/<recipe_id>", methods=['GET'])
def get_recipe_by_id(recipe_id):
    if not is_authorized():
        return Response("{'not': 'happening'}", status=401, mimetype='application/json')

    db_response = get_recipe_from_db(recipe_id)
    
     # Do things
    
    return jsonify(json.loads(sample_recipe))

@app.route("/recipe", methods=["POST"])
def create_recipe():
    if not is_authorized():
        return Response("{'not': 'happening'}", status=401, mimetype='application/json')

    #Create recipe here
    
    return Response("Created", status=201, mimetype='application/json')


def get_recipe_from_db(recipe_id):
    return ""

def is_authorized():
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
