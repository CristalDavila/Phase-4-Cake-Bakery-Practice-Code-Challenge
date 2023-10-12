from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask import Flask
from datetime import datetime


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here


class Cakes():
    __tablename__ = 'cakes_table'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

cb_cake_relationship = db.relationship('Cake_Bakeries', back_populates = 'cake_relationship')
    
    

class Cake_Bakeries():
    __tablename__ = 'cake_bakeries_table'

    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Integer, Nullable = False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    cake_id = db.Column(db.Integer, db.ForeignKey('cakes_table.id'))
    cake_relationship = db.relationship('Cake', back_populates='cb_cake_relationship')

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries_table.id'))
    bakery_relationship = db.relationship('Bakery', back_populates='cb_bakeries_relationship')




@validates('price')
def validate_price(self, key, price):
    if not 1 <= price >= 1000:
        raise ValueError("Invalid Price")
    return price


class Bakeries():
    __tablename__ = 'bakeries_table'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    cb_bakeries_relationship = db.relationship('Cake_Bakeries', back_populates='bakery_relationship')

