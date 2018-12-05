import re
import uuid
import functools

import flask
from flask import g, current_app
import flask_restful
from flask_httpauth import HTTPBasicAuth

import models
import crawler

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = models.User.query.filter_by(user_id = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

class TestAuth(flask_restful.Resource):
    @auth.login_required
    def get(self):
        return "You are authorized!"

class CreateUser(flask_restful.Resource):
    ##### Passwords should be posted in some hash agreeable by both front and backend. Recommend md5, we aren't a bank.
    def post(self):
        if not flask.request.is_json:
            flask_restful.abort(400, message="Not formatted as json.")
       
        username = flask.request.json.get('username')
        email = flask.request.json.get('email')
        password = flask.request.json.get('password')
        firstname = flask.request.json.get('firstname')
        lastname = flask.request.json.get('lastname')
        question = flask.request.json.get('question')
        answer = flask.request.json.get('answer')

        if username is None or password is None or email is None or firstname is None or lastname is None or question is None or answer is None:
            flask_restful.abort(400, message="Must enter username, password, and email")
        if models.User.query.filter_by(user_id = username).first() is not None:
            flask_restful.abort(400, message="Username already exists")
        if models.User.query.filter_by(user_email = email).first() is not None:
            flask_restful.abort(400, message="User email already exists")
        newuser = models.User(user_id = username, user_email = email, user_password = password, user_first_name = firstname, user_last_name = lastname, security_question = question, security_answer = answer)
        models.DB.session.add(newuser)
        models.DB.session.commit()
    # returns http 200 on success

class RecipeList(flask_restful.Resource):
    def get(self):
        """Gets the top 10 recipes."""
        if not is_authorized():
            return {'not': 'happening'}, 401

        start = int(flask.request.args.get("start", "0"))
        count = int(flask.request.args.get("count", "20"))

        return [recipe.map_db_to_dict() for recipe in models.Recipe.query.slice(start, start + count).all()]

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

class Comment(flask_restful.Resource):
    def get(self, comment_id):
        """Gets one comment by its comment id."""
        return models.Comment.query.filter_by(comment_id=comment_id).first().get_dict()

    def delete(self, comment_id):
        """Deletes one comment by its comment id."""
        if not is_authorized():
            return {'not': 'happening'}, 401

        delete_comment_from_db(comment_id)
        return flask.Response("Deleted", status=204, mimetype='application/json')

class RecipeComment(flask_restful.Resource):
    def get(self, recipe_id):
        """Gets the comments for a recipe."""
        return [comment.get_dict() for comment in models.Comment.query.filter_by(meal_id=recipe_id).all()]

    @auth.login_required
    def post(self, recipe_id):
        """Posts a comment to a recipe."""
        if not flask.request.is_json:
            flask_restful.abort(400, message="Not formatted as json.")

        comment_data = flask.request.get_json()
        comment_data_validated = {"user_id": g.user.user_id,
                                  "meal_id": recipe_id,
                                  "user_comment": comment_data.get("text", "")
                                 }

        comment_id = add_comment_to_db(**comment_data_validated)
        if not comment_id:
            flask_restful.abort(500, message="Create failed.")

        return flask.Response(recipe_id, status=201, mimetype='application/json')

class Search(flask_restful.Resource):
    def options(self):
        pass
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

class Crawl(flask_restful.Resource):
    def post(self):
        """Starts a crawler"""
        if not flask.request.is_json:
            flask_restful.abort(400, message="Not formatted as json.")

        return do_crawl(flask.request.get_json())
        

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
    recipes = models.Recipe.query.filter_by(meal_id=recipe_id).all()
    for recipe in recipes:
        models.DB.session.delete(recipe)
        comments = models.Comment.query.filter_by(meal_id=recipe_id).all()
        for comment in comments:
            delete_comment_from_db(comment.comment_id)

    models.DB.session.commit()
    # TODO: try to make sure that commit only called when necessary... Maybe decorator?

def add_comment_to_db(**kwargs):
    """Adds a comment to the db."""
    comment = models.Comment(**kwargs)
    models.DB.session.add(comment)
    models.DB.session.commit()
    return comment.meal_id.hex

def delete_comment_from_db(comment_id):
    """Deletes a comment from the db."""
    comments = models.Comment.query.filter_by(comment_id=comment_id).all()
    for comment in comments:
        models.DB.session.delete(comment)

    models.DB.session.commit()

def do_search(search_params):
    """Searches db based on parameters"""
    order_options = {
                     "meal_id": models.Recipe.meal_id.asc(),
                     "aggregate_rating": -models.Recipe.aggregate_rating.asc(),
                     "total_time": models.Recipe.total_time.asc()
                    }
    regex_extract_params = re.compile("(\w+)\s*:\s*\"([^\"]+)\"")
    regex_extract_title_words = re.compile("(?:\A|\s+)([\d\w]+)(?=\s+|\Z)")
    regex_comma_split = re.compile("\s*,\s*")

    start = int(search_params.get("start", "0")) # move to get request when possible
    count = int(search_params.get("count", "20")) # move to get request when possible
    order = order_options.get(search_params.get("order", ""), models.Recipe.meal_id.asc())

    search_bar_params = dict(regex_extract_params.findall(search_params.get("title", "")))
    search_bar_title_words = " ".join(regex_extract_title_words.findall(search_params.get("title", "")))

    query_filters = []
    if search_bar_title_words:
        query_filters.append(models.DB.func.lower(models.Recipe.meal_name).contains(search_bar_title_words.lower()))
    if "yield" in search_bar_params:
        query_filters.append(models.Recipe.recipe_yield != None)
        query_filters.append(models.DB.func.lower(models.Recipe.recipe_yield).contains(search_bar_params["yield"]))
    # if "restrictive" in search_params:
        # # query_filters.append(models.Recipe.recipe_ingredient.all_().like(models.DB.any_(search_params['restrictive'])))
        # query_filters.append(models.db.func.bool_and(models.DB.func.unnest(models.Recipe.recipe_ingredient).like("%pizza%")))
    # if "inclusive" in search_params:
        # query_filters.append(models.Recipe.recipe_ingredient.overlap(search_params['inclusive']))
    # if "rejective" in search_params:
        # query_filters.append(~(models.Recipe.recipe_ingredient.overlap(search_params['rejective'])))r()))

    recipes = [recipe.map_db_to_dict() for recipe in models.Recipe.query.filter(*query_filters).order_by(order).all()]

    # TODO FIX THIS UNSCALABALE STUFF
    if "restrictive" in search_bar_params:
        ingredient_params = [param.lower() for param in regex_comma_split.split(search_bar_params["restrictive"])]
        recipes_temp = []
        for recipe in recipes:
            valid = True
            for ingredient in recipe["recipe_ingredient"]:
                valid &= functools.reduce((lambda x, y: x or y in ingredient.lower()), ingredient_params, False)
            if valid:
                recipes_temp.append(recipe)
        recipes = recipes_temp
    if "inclusive" in search_bar_params:
        ingredient_params = [param.lower() for param in regex_comma_split.split(search_bar_params["inclusive"])]
        recipes_temp = []
        for recipe in recipes:
            valid = False
            for ingredient in recipe["recipe_ingredient"]:
                valid |= functools.reduce((lambda x, y: x or y in ingredient.lower()), ingredient_params, False)
            if valid:
                recipes_temp.append(recipe)
        recipes = recipes_temp
    if "rejective" in search_bar_params:
        ingredient_params = [param.lower() for param in regex_comma_split.split(search_bar_params["rejective"])]
        recipes_temp = []
        for recipe in recipes:
            valid = False
            for ingredient in recipe["recipe_ingredient"]:
                valid |= functools.reduce((lambda x, y: x or y in ingredient.lower()), ingredient_params, False)
            if not valid:
                recipes_temp.append(recipe)
        recipes = recipes_temp

    if start >= len(recipes):
        return []
    elif start + count >= len(recipes):
        return recipes[start:]
    else:
        return recipes[start:start + count]

def do_crawl(crawler_params):
    """Starts and runs a crawler"""
    def crawler_callback(recipe, app):
        with app.app_context():
            add_recipe_to_db(full_content=recipe)
    crawler_params["recipe_callback"] = crawler_callback
    crawler_params["recipe_callback_args"] = (current_app._get_current_object(),)
    crawler_params["recipe_callback_kwargs"] = {}
    crawler.Crawler(**crawler_params)

def is_authorized():
    """Checks if the user is authorized."""
    return True
