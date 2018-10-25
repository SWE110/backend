import itertools

import flask
import flask_restful
import dataset

class RecipeList(flask_restful.Resource):
    def get(self):
        """Gets the top 10 recipes."""
        if not is_authorized():
            return {'not': 'happening'}, 401

        # Can we persist the db handle? Tried to persist in Flask.g didn't seem to
        # work but could be user error
        db = dataset.connect('sqlite:///recipe.db')
        recipes_table = db['recipes']
        all_results = recipes_table.all()
        # Get 10
        results_list = [r for r in itertools.islice(all_results, 10)]
        return results_list

    def post(self):
        """Creates a recipe based on receieved parameters and adds it to the db."""
        if not is_authorized():
            return {'not': 'happening'}, 401
        if not flask.request.is_json:
            flask_restful.abort(400, message="Not formatted as json.")
        print("Creating recipe")
        incoming_recipe = flask.request.get_json()

        # For now assumes full_content
        recipe_created = add_recipe_to_db(full_content=incoming_recipe)
        if not recipe_created:
            flask_restful.abort(500, message="Create failed.")

        return flask.Response("Created", status=201, mimetype='application/json')

class Recipe(flask_restful.Resource):
    def get(self, recipe_id):
        """Gets one recipe by its recipe id."""
        if not is_authorized():
            return {'not': 'happening'}, 401

        db = dataset.connect('sqlite:///recipe.db')
        recipes_table = db['recipes']

        one_result_in_list = recipes_table.find(id=recipe_id)
        result = [r for r in itertools.islice(one_result_in_list, 1)][0]
        print(result)
        return result

# temp stuff to check if working

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