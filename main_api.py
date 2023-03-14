import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    
@app.route('/random', methods=["GET"])
def get_random_cafe():
    cafes = Cafe.query.all()
    random_cafe = random.choice(cafes)
    cafe_dict = random_cafe.__dict__
    del cafe_dict['_sa_instance_state']
    return jsonify(cafe=cafe_dict)

@app.route('/all', methods=["GET"])
def allCafes():
    cafes = Cafe.query.all()
    all_cafes = list()
    for cafe in cafes:
        cafe_dict = cafe.__dict__
        del cafe_dict['_sa_instance_state']
        all_cafes.append(cafe_dict)
    return jsonify(cafes=all_cafes)

@app.route('/search')
def search_cafe():
    query_location = request.args.get('loc')
    cafes = Cafe.query.filter_by(location=query_location).all()
    if cafes:
        all_cafes = list()
        for cafe in cafes:
            cafe_dict = cafe.__dict__
            del cafe_dict['_sa_instance_state']
            all_cafes.append(cafe_dict)
        return jsonify(cafes=all_cafes)
    else:
        return jsonify(cafes=f"no cafes in {query_location}")


@app.route('/add', methods=["POST"])
def post_new_cafe():
    new = Cafe(name=request.form.get('name'),
                map_url=request.form.get('map_url'),
                img_url=request.form.get('img_url'),
                location=request.form.get('loc'),
                has_sockets=bool(request.form.get('sockets')),
                has_toilet=bool(request.form.get('toilet')),
                has_wifi = bool(request.form.get('wifi')),
                can_take_calls=bool(request.form.get('calls')),
                seats=request.form.get('seats'),
                coffee_price = request.form.get('coffe_price')
                )
    db.session.add(new)
    db.session.commit()
    return jsonify(response={'success' : "New coffee place added"})


@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    print(cafe_id)
    new_price = request.args.get('new_price')
    print(new_price)
    cafe_place = Cafe.query.filter_by(id=cafe_id).first()
    print(cafe_place.name)
    if cafe_place:
        cafe_place.coffee_price = new_price
        db.session.commit()
        return jsonify({'succeess': f"Price was updated to {new_price}"})
    else:
        return jsonify({'not found':'no cafe found'})


@app.route('/delete/<int:coffee_id>', methods=["DELETE"])
def del_coffe(coffee_id):
    user_api_key = request.args.get('TopSecretAPIKey')
    if user_api_key=='123':
        coffe_to_delete = Cafe.query.filter_by(id=coffee_id).first()
        if coffe_to_delete:
            db.session.delete(coffe_to_delete)
            db.session.commit()
            return jsonify({'result':'cafe deleted'})
        else:
            return jsonify({'result':'cafe not found'})
    else:
        return jsonify({'result': 'wrong api key'})


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
