from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

connection = psycopg2.connect(
    host='Localhost',
    port='5432',
    database='zooapp'
)

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

    flash("Animal added to your zoo")

    return redirect(url_for('Index'))

    

if __name__ == "__main__":
    app.run(debug=True)
