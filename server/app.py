#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Cakes, Bakeries, Cake_Bakeries

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

#GET /bakeries

@app.get('/bakeries')
def get_bakeries():
    bakeries = Cake_Bakeries.query.all()
    data = [bakeries.to_dict(only=('id', 'name', 'address'))for bakeries in bakeries]

    return make_response(
            jsonify(data),
            200)



#GET /bakeries/:id

@app.get('/bakeries/:<int:id>')
def get_bakery_by_id(id):
    bakeries = Cake_Bakeries.query.filter(Cake_Bakeries.id == id).first()
    
    if not bakeries:
        return make_response(
            jsonify({"error": "Bakery Not Found"}),
            404
        )
    return make_response(
        jsonify(bakeries.to_dict()),
        200
    )
#DELETE /bakeries/:id

@app.delete('/bakeries/<int:id>')
def delete_bakery(id):
    bakery = Cake_Bakeries.query.filter(Cake_Bakeries.id == id).first()

    if not bakery: 
        return make_response(
            jsonify({"error": "Bakery Not Found"}),
            404
        )
    db.session.delete(bakery)
    db.session.commit()

    return make_response(jsonify({}), 204)


#GET /cakes

@app.get('/cakes')
def get_all_cakes():
    cakes = Cakes.query.all()
    data = [cakes.to_dict(only=('id', 'name', 'description'))for cakes in cakes]

    return make_response(
        jsonify(data),
        200
    )

# POST /cake_bakery

@app.post('/cake_bakery')
def post_cake_bakery():
    data = request.get_json()
    print(data)

    try:
        new_bakery = Cake_Bakeries(
            price=data.get("price"),
            cake_id=data.get("cake_id"),
            bakery_id=data.get("bakery_id")
        )
        db.session.add(new_bakery)
        db.session.commit()

        return make_response(
            jsonify(new_bakery.to_dict(only=('price', 'cake', 'bakery'))), 
            201
        )
    except ValueError:
        return make_response(
            jsonify({"error": ["validation errors"]}),
            406
        )

if __name__ == '__main__':
    app.run(port=5555, debug=True)