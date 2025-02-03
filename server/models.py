from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


# Now you can implement the relationships as shown in the ER Diagram:


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates = "restaurant",   cascade='all, delete-orphan', overlaps ='restaurants,pizzas' )
    pizzas = db.relationship("Pizza", secondary = "restaurant_pizzas", back_populates = "restaurants", overlaps = 'restaurant_pizzas')
    # add serialization rules
    serialize_rules = ('-pizzas.restaurants', '-restaurant_pizzas.restaurant' )
    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates = "pizza", cascade='all, delete-orphan', overlaps ='restaurants,pizzas')
    restaurants =  db.relationship("Restaurant", secondary = "restaurant_pizzas", back_populates = "pizzas", overlaps = 'restaurant_pizzas' )
    # add serialization rules
    serialize_only = ('id', 'ingredients' , 'name')
    serialize_rules = ("-restaurants.pizzas", '-restaurant_pizzas.pizza')
    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer,db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer,db.ForeignKey("restaurants.id"))
    # add relationships

    pizza = db.relationship("Pizza", back_populates = "restaurant_pizzas",  overlaps ='restaurants,pizzas')
    restaurant = db.relationship("Restaurant", back_populates = "restaurant_pizzas",  overlaps ='restaurants,pizzas')

    # add serialization rules
    serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')
    # add validation
    @validates("price")
    def price_val(self,key,price):
        if 1<= price <= 30:
            return price
        else:
            raise ValueError("Must be between 1 and 30")
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
