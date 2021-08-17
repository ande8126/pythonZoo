from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

connection = psycopg2.connect(
    host='Localhost',
    port='5432',
    database='zooapp2'
)
# jinja to index
@app.route('/')
def Index():
    return render_template("index.html")


# routes to db
#GET
@app.route('/api/animals', methods=['GET'])
def list_animals():
    #convert records to objects with RealDictCursor
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    #query text
    queryText = "SELECT animals.id, animals.species, animals.age, animals.gender, animals.name, exhibits.name AS exhibit, animals.on_display FROM animals JOIN exhibits ON exhibits.id = animals.exhibits_id;"
    #send it over
    cursor.execute(queryText)
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

#DELETE
@app.route( '/api/animals/<id>', methods=['DELETE'])
def remove_animal( id ):
    try:
        print( id )
        cursor = connection.cursor()
        queryText = f'DELETE FROM animals WHERE id = {id}'
        cursor.execute(queryText)
        deleted_rows = cursor.rowcount
        print( deleted_rows, 'Animal removed' ) 
        cursor.close()
        result = { 'status' : 'DELETED' }
        return jsonify(result), 200 
    except(Exception, psycopg2.DatabaseError) as err:
        print( 'Remove animal failed on server', err )
    finally:
        if(cursor):
            cursor.close()

#PUT
@app.route( '/api/animals/<id>', methods=['PUT'])
def update_exhibit( id ):
    try:
        animal_id = id
        cursor = connection.cursor()
        queryText = f'UPDATE animals SET on_display = false WHERE id={animal_id}'
        cursor.execute(queryText)
        print( 'animal moved', queryText, id )
        connection.commit()
        count = cursor.rowcount
        cursor.close()
        print( count, 'update worked' )
        result = { 'status' : 'UPDATED' }
        return jsonify(result), 200
    except(Exception, psycopg2.DatabaseError) as err:
        print( 'PUT animal failed on server', err )
    finally:
        if(cursor):
            cursor.close()

if __name__ == "__main__":
    app.run(debug=True)

