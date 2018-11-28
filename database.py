import psycopg2
import json
from datetime import datetime
from datetime import timedelta

def connect():
    """ Connect to the PostgreSQL database server """
    connect.conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connect.conn = psycopg2.connect("host=104.248.220.214 dbname=RecipeDB user=postgres password=cap")
        # connect.conn = psycopg2.connect("host=localhost dbname=videomode user=postgres")

        # create a cursor
        connect.cur = connect.conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        connect.cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = connect.cur.fetchone()
        print(db_version)
    except:
        print 'Cannot connect to Database'

def disconnect():
    try:
        print "Closing connection to the PostgreSQL database..."
        connect.cur.close()
        print "Connection closed!"
    except:
        print 'Cannot disconnect from Database'

#data has to be exactly like recipes.txt on gitlab (as of Oct 24, 2018 3:57am)
def insertRecipes(data):
    connect()
    sql = """INSERT INTO Recipe (
        meal_name,
        image,
        aggregate_rating,
        author,
        description,
        keywords,
        recipe_category,
        recipe_cuisine,
        recipe_ingredient,
        recipe_instructions,
        recipe_yield,
        total_time
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    for insert in range(0, len(data)):
        # recipeType = data[insert]['@type']
        mealName = data[insert]['name']
        image = data[insert]['image']
        try:
            aggregateRating = data[insert]['aggregateRating']['ratingValue']
        except:
            aggregateRating = None
        try:
            author = data[insert]['author']['name'].partition('\\')[0]
        except:
            author = None
        dt = datetime.now()
        try:
            description = data[insert]['description']
        except:
            description = None
        try:
            keywords = data[insert]['keywords'].replace(',', '').split()
        except:
            keywords = None
        try:
            recipeCategory = data[insert]['recipeCategory']
        except:
            recipeCategory = None
        try:
            recipeCuisine = data[insert]['recipeCuisine']
        except:
            recipeCuisine = None
        try:
            recipeIngredient = data[insert]['recipeIngredient']
        except:
            recipeIngredient = None
        try:
            recipeInstructions = data[insert]['recipeInstructions']
        except:
            recipeInstructions = None
        try:
            recipeYield = data[insert]['recipeYield']
        except:
            recipeYield = None
        try:
            total = data[insert]['totalTime']
            hours = int(total[2:4])
            minutes = int(total[5:7])
            totalTime = timedelta(hours=hours, minutes=minutes)
        except:
            totalTime = None

        instructionsList = []
        for i in range(0, len(recipeInstructions)):
            instructionsList.append(recipeInstructions[i].values()[0])

        connect.cur.execute(sql, (
                mealName,
                image,
                aggregateRating,
                author,
                description,
                keywords,
                recipeCategory,
                recipeCuisine,
                recipeIngredient,
                instructionsList,
                recipeYield,
                totalTime
            )
        )
        connect.conn.commit()
    disconnect()

with open('recipes.txt') as json_data:
    recipes = json.load(json_data)

insertRecipes(recipes)
