from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY DATABASE_URI'] = 'postgresql://patrickanderson@Localhost/zooapp'
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    species = db.Column(db.String(40))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    name = db.Column(db.String(40))
    exhibit_id = db.Column(db.Integer)

    def __init__(self, species, age, gender, name, exhibit_id):
        self.species = species
        self.age = age
        self.gender = gender
        self.name = name
        self.exhibit_id = exhibit_id



@app.route('/')
def Index():
    return render_template("index.html")

# routes to db
@app.route('/api/animals', methods=['POST'])
def insert():
    if request.method == 'POST':
        species = request.form['species']
        age = request.form['age']
        gender = request.form['gender']
        name = request.form['name']
        exhibits_id = request.form['exhibit']

        animal_data = Animal(species, age, gender, name, exhibits_id)
        db.session.add(animal_data)
        db.session.commit()

        return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
