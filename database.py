import psycopg2
import json
from datetime import datetime

def connect():
    """ Connect to the PostgreSQL database server """
    connect.conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connect.conn = psycopg2.connect("host=104.248.220.214 dbname=RecipeDB user=postgres password=cap")

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
    sql = """INSERT INTO Recipes (
        recipeType,
        mealName,
        image,
        aggregateRating,
        author,
        datePublished,
        description,
        keywords,
        recipeCategory,
        recipeCuisine,
        recipeIngredient,
        recipeInstructions,
        recipeYield,
        totalTime
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    for insert in range(0, len(data)):
        recipeType = data[insert]['@type']
        mealName = data[insert]['name']
        image = data[insert]['image']
        try:
            aggregateRating = data[insert]['aggregateRating']['ratingValue']
        except:
            aggregateRating = None
        author = data[insert]['author']['name'].partition('\\')[0]
        dt = datetime.now()
        description = data[insert]['description']
        keywords = data[insert]['keywords'].replace(',', '').split()
        recipeCategory = data[insert]['recipeCategory']
        recipeCuisine = data[insert]['recipeCuisine']
        recipeIngredient = data[insert]['recipeIngredient']
        recipeInstructions = data[insert]['recipeInstructions']
        recipeYield = data[insert]['recipeYield']
        totalTime = data[insert]['totalTime']

        instructionsList = []
        for i in range(0, len(recipeInstructions)):
            instructionsList.append(recipeInstructions[i].values()[0])

        connect.cur.execute(sql, (
                recipeType,
                mealName,
                image,
                aggregateRating,
                author,
                str(dt).partition(".")[0],
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
