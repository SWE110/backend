import uuid

import flask
import flask_restful

import models

class RecipeList(flask_restful.Resource):
    def get(self):
        """Gets the top 10 recipes."""
        if not is_authorized():
            return {'not': 'happening'}, 401

        return [recipe.map_db_to_dict() for recipe in models.Recipe.query.all()[:10]]

    def post(self):
        """Creates a recipe based on receieved parameters and adds it to the db."""
        if not is_authorized():
            return {'not': 'happening'}, 401
        if not flask.request.is_json:
            flask_restful.abort(400, message="Not formatted as json.")
        print("Creating recipe")
        incoming_recipe = flask.request.get_json()

        # For now assumes full_content
        recipe_id = add_recipe_to_db(full_content=incoming_recipe)
        if not recipe_id:
            flask_restful.abort(500, message="Create failed.")

        return flask.Response(recipe_id, status=201, mimetype='application/json')

class Recipe(flask_restful.Resource):
    def get(self, recipe_id):
        """Gets one recipe by its recipe id."""
        if not is_authorized():
            return {'not': 'happening'}, 401

        return models.Recipe.query.filter_by(meal_id=recipe_id).first().map_db_to_dict()

    def delete(self, recipe_id):
        """Deletes one recipe by its recipe id."""
        if not is_authorized():
            return {'not': 'happening'}, 401

        delete_recipe_from_db(recipe_id)
        return flask.Response("Deleted", status=204, mimetype='application/json')

class Search(flask_restful.Resource):
    def get(self):
        """Returns recipes based on search id provided"""
        try:
            search_id = uuid.UUID(flask.request.args.get("id", ""))
        except ValueError:
            flask_restful.abort(400, message="Invalid search id.")

        search = models.Search.query.get(search_id)
        if not search:
            flask_restful.abort(400, message="Invalid search id.")

        return do_search(search.search_params)

    def post(self):
        """Creates a search object if it does not alreayd exist in the database"""
        if not flask.request.is_json:
            flask_restful.abort(400, message="Not formatted as json.")

        return do_search(flask.request.get_json())

        # search_id = uuid.uuid5(models.NAMESPACE_SEARCH, flask.request.data)
        # if models.Search.query.get(search_id) is None:
            # search_params = flask.request.get_json()
            # models.DB.session.add(models.Search(search_id=search_id, search_params=search_params))
            # models.DB.session.commit()
            # # maybe do some preprocessing that makes search easier

        # flask.redirect(flask.url_for(Search.get, id=search_id), code=307)

def add_recipe_to_db(**kwargs):
    """Adds a recipe to the db."""
    if "full_content" in kwargs:
        # generate all fields as in kwargs["full_content"].
        # use this to just copy from scraped data already formatted in schema.
        recipe = models.map_schema_to_db(**kwargs["full_content"])
        models.DB.session.add(recipe)
        models.DB.session.commit()

        return recipe.meal_id.hex
    else:
        # populate user settable fields from form and auto generate the rest.
        # e.g. no initial rating, no comments.
        return None

def delete_recipe_from_db(recipe_id):
    """Deletes a recipe from the db."""
    recipes = models.Recipe.query.filter_by(meal_id=recipe_id)
    for recipe in recipes:
        models.DB.session.delete(recipe)

    models.DB.session.commit()

def do_search(search_params):
    """Searches db based on parameters"""
    query_filters = []
    if "title" in search_params:
        query_filters.append(models.Recipe.meal_name.contains(search_params['title']))
    if "restrictive" in search_params:
        query_filters.append(models.Recipe.recipe_ingredient.contained_by(search_params['restrictive']))
    if "inclusive" in search_params:
        query_filters.append(models.Recipe.recipe_ingredient.overlap(search_params['inclusive']))
    if "rejective" in search_params:
        query_filters.append(~(models.Recipe.recipe_ingredient.overlap(search_params['rejective'])))

    recipes = models.Recipe.query.filter(*query_filters).all()
    return [r.map_db_to_dict() for r in recipes]

def is_authorized():
    """Checks if the user is authorized."""
    return True
