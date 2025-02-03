#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        restaurants = []
        for r in Restaurant.query.all():
            r_json = {
                "address" :r.address,
                "id":r.id,
                "name": r.name
            }
            restaurants.append(r_json)
        return restaurants, 200
    

class RestaurantById(Resource):
    def get(self,id):
        restarurant = Restaurant.query.filter_by(id=id).first()
        if not restarurant:
            return {"error": "Restaurant not found"}, 404
        return restarurant.to_dict(), 200

    def delete(self, id):
         restarurant = Restaurant.query.filter_by(id=id).first()
         if not restarurant:
            return {"error": "Restaurant not found"}, 404
         db.session.delete(restarurant)
         db.session.commit()
         return {} , 204
    
class Pizzas(Resource):
    def get(self):
        pizzas = [p.to_dict() for p in Pizza.query.all()]
        return pizzas, 200
    
class Resturant_pizzas(Resource):
    def post(self):
        try:
            new_rp = RestaurantPizza(price = request.get_json()['price'],pizza_id = request.get_json()['pizza_id'],restaurant_id = request.get_json()['restaurant_id'])
            db.session.add(new_rp)
            db.session.commit()

            return new_rp.to_dict(), 201
        except:
            return {"errors": ["validation errors"]}, 400
    
api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(Resturant_pizzas, '/restaurant_pizzas')
if __name__ == "__main__":
    app.run(port=5555, debug=True)
