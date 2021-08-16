from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

connection = psycopg2.connect(
    host='Localhost',
    port='5432',
    database='zooapp'
)
# jinja to index
@app.route('/')
def Index():
    # animals = ?
    # print(animals)
    # animals = Animal(animals_json)
    return render_template("index.html")

# @app.route('/api/animals')
# def getAnimals():
#     animals = request.data()
#     print( animals )


#class
class Animal:
    def __init__(self, json):
        self.id = json['id']
        self.species = json['species']
        self.age = json['age']
        self.age = json['gender']
        self.age = json['name']
        self.exhibits = json['exhibits_id']

# routes to db
#GET
@app.route('/api/animals', methods=['GET'])
def list_animals():
    #convert records to objects with RealDictCursor
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    #query text
    postgreSQL_select_Query = "SELECT * FROM animals;"
    #send it over
    cursor.execute(postgreSQL_select_Query)
    #select rows
    animals = cursor.fetchall()
    #response
    print( jsonify(animals) )
    return jsonify(animals)

#POST
@app.route('/api/animals', methods=['POST'])
def add():
    species = request.form['species']
    age = request.form['age']
    gender = request.form['gender']
    name = request.form['name']
    exhibits_id = request.form['exhibit']
    #SQL ALCHEMY STUFF:
    # animal_data = Animal(species, age, gender, name, exhibits_id)
    # db.session.add(animal_data)
    # db.session.commit()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        print(species, age, gender, name, exhibits_id)
        queryText = "INSERT INTO animals (species, age, gender, name, exhibits_id) VALUES ( %s, %s, %s, %s, %s );"
        cursor.execute(queryText, (species, age, gender, name, exhibits_id))
        #commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, 'Animal added')
        #response
        result = { 'status' : 'CREATED' }
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as err:
        print( 'Add animal failed on server', err )
        result = { 'status' : 'ERROR' }
        return jsonify( result ), 500
    finally:
        if(cursor):
            cursor.close()

    # flash("Animal added to your zoo")
    # OLD: return redirect(url_for('Index'))

#DELETE
@app.route( '/api/animals', methods=['DELETE'])
def remove_animal( id ):
    try:
        print( id )
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        queryText = 'DELETE FROM animals WHERE id = %s'
        cursor.execute(queryText, id)
        deleted_rows = cursor.rowcount
        print( deleted_rows, 'Animal removed' )
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.DatabaseError) as err:
        print( 'Remove animal failed on server', err )
    finally:
        if connection is not None:
            connection.close()



if __name__ == "__main__":
    app.run(debug=True)

