# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask import request
import json
from flask import Response
from flask import jsonify

import mysql.connector
from mysql.connector import errorcode

# To be inserted in MSQL
key_mapping_list = {
    "sci-fi": ["The vampire diaries"],
    "supernatural": ["The vampire diaries"],
    "superhero": ["Supergirl", "The flash"],
    "fantasy": ["Lucifer", "Shadow and bone"],
    "science fiction": ["The 100"],
    "action": ["The umbrella academy", "Cobra kai", "Riverdale"],
    "animation": ["Tangled"],
    "Hero": ["The vampire diaries", "Lucifer", "Tangled"],
    "Heroine": ["Supergirl", "The 100", "Tangled"],
    "many": ["The vampire Diaries", "Cobra Kai", "riverdale", "The flash", "Shadow and Bone"],
    "show": ["The vampire diaries", "Supergirl", "The flash", "Lucifer", "Riverdale", "The 100"],
    "movie": ["Tangled"],
    "more": ["The 100", "Lucifer", "Riverdale", "Flash", "supergirl", "the 100", "The vampire diaries"],
    "less": ["shadow and bone", "cobra kai"]
}

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

connection = ""
mycursor = ""


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def hello_world():
    return 'basic testing\n'


#
# Route to handle HTML request
@app.route('/inventory', methods=['POST'])
def my_inventory():
    list1 = []
    list2 = []
    list3 = []
    list4 = []

    # Handle movie_genre
    # get user input for movie_genre
    movie_genre = request.form.get("movie_genre")

    # Query MQL to get key value pair
    sql = "SELECT quantity FROM inventory WHERE name = \'{}\'".format(movie_genre)
    try:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            list1.append(x)
    except:
        pass

    # Handle movie character
    # get user input for movie_character
    movie_character = request.form.get("movie_character")
    # Query MQL to get key value pair
    sql = "SELECT quantity FROM inventory WHERE name = \'{}\'".format(movie_character)
    try:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            list2.append(x)
    except:
        pass

    # Handle movie type
    # get user input for movie_type
    movie_type = request.form.get("movie_type")
    # Query MQL to get key value pair
    sql = "SELECT quantity FROM inventory WHERE name = \'{}\'".format(movie_type)
    try:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            list3.append(x)
    except:
        pass

    # Handle movie len
    # get user input for movie_len
    movie_len = request.form.get("movie_len")
    # Query MQL to get key value pair
    sql = "SELECT quantity FROM inventory WHERE name = \'{}\'".format(movie_len)
    try:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            list4.append(x)
    except:
        pass

    js = [
        {movie_genre: list1},
        {movie_character: list2},
        {movie_type: list3},
        {movie_len: list4}
    ]
    return jsonify(results=js)


#
# Handle SQL Connection
def SqlConnection():
    try:
        # cnx = mysql.connector.connect(host='localhost',
        #                               user='root',
        #                               password='secret',
        #                               auth_plugin='mysql_native_password')
        #
        cnx = mysql.connector.connect(host='localhost',
                                      user='root',
                                      password='secret',
                                      database="mydatabase",
                                      auth_plugin='mysql_native_password')
    except mysql.connector.Error as err:
        print(err.errno)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("!!!Success making connection")
        mycursor = cnx.cursor()

        try:
            print("Create database")
            mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
            print("Create table")
            mycursor.execute("CREATE TABLE IF NOT EXISTS inventory (name VARCHAR(100), quantity VARCHAR(100));")

            # Insert default entries
            for key in key_mapping_list:
                str1 = ','.join(key_mapping_list[key])
                mycursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", (key, str1))
                print("Inserted", mycursor.rowcount, "row(s) of data.")

        except:

            print("failed to insert entry in table")
            pass

    return cnx, mycursor


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    connection, mycursor = SqlConnection()
    app.run()
