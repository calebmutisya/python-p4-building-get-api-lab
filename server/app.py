#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list=[]
    for bakery in Bakery.query.all():
        bakery_dict={
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at,
            "baked_goods": []
        }

        for baked_good in BakedGood.query.filter_by(bakery_id=bakery.id).all():
            baked_good_dict={
                "id": baked_good.id,
                "name": baked_good.name,
                "price": baked_good.price,
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
                "bakery_id": baked_good.bakery_id
            }
            bakery_dict["baked_goods"].append(baked_good_dict)

        bakeries_list.append(bakery_dict)

    response= make_response(
        jsonify(bakeries_list),
        200
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery= Bakery.query.filter(Bakery.id == id).first()
    if bakery:
        bakery_dict={
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at,
            "baked_goods": []
        }

        for baked_good in BakedGood.query.filter_by(bakery_id=bakery.id).all():
            baked_good_dict = {
                "id": baked_good.id,
                "name": baked_good.name,
                "price": baked_good.price,
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
                "bakery_id": baked_good.bakery_id
            }
            bakery_dict["baked_goods"].append(baked_good_dict)

        response = make_response(
            jsonify(bakery_dict), 200
        )

    else:
        response = make_response(jsonify({"error": "Bakery not found"}), 404)

    
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods= BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list= []
    for baked_good in baked_goods:
        bakery= Bakery.query.get(baked_good.bakery_id)

        if bakery:
            baked_good_dict = {
                "id": baked_good.id,
                "name": baked_good.name,
                "price": baked_good.price,
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
                "bakery_id": baked_good.bakery_id,
                "bakery": {
                    "id": bakery.id,
                    "name": bakery.name,
                    "created_at": bakery.created_at,
                    "updated_at": bakery.updated_at
                }
            }
            baked_goods_list.append(baked_good_dict)
    
    response= make_response(jsonify(baked_goods_list),200)

    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive= BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()

    if most_expensive:
        bakery= Bakery.query.get(most_expensive.bakery_id)

        most_expensive_dict = {
            "id": most_expensive.id,
            "name": most_expensive.name,
            "price": most_expensive.price,
            "created_at": most_expensive.created_at,
            "updated_at": most_expensive.updated_at,
            "bakery_id": most_expensive.bakery_id,
            "bakery": {
                "id": bakery.id,
                "name": bakery.name,
                "created_at": bakery.created_at,
                "updated_at": bakery.updated_at
            }
        }
        response= make_response(jsonify(most_expensive_dict), 200)
    else:
        response = make_response(jsonify({"error": "No baked goods found"}), 404)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
