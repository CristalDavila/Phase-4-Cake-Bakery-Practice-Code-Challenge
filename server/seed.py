from random import choice as rc, randint
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Cake, CakeBakery, Bakery

with app.app_context():
    fake = Faker()

def create_cakes():
    cakes = []
    for _ in range(10):  
        c = Cake(
            name=fake.name(),
            description=fake.sentence(),
        )
        cakes.append(c)
    return cakes

def create_bakeries():
    bakeries = []
    for _ in range(10):
        b = Bakery(
            name=fake.name(),
            address=fake.address(),
        )
        bakeries.append(b)
    return bakeries

def create_cake_bakeries():
    cake_bakeries = []
    for _ in range(10):
        cake_bakeries.append(CakeBakery(
            price=randint(1, 100),
            cake_id=randint(1, 10),
            bakery_id=randint(1, 10),
        ))
    return cake_bakeries

if __name__ == '__main__':
    with app.app_context():
        Cake.query.delete()
        Bakery.query.delete()
        CakeBakery.query.delete()
        cakes = create_cakes()
        bakeries = create_bakeries()
        cakebakeries = create_cake_bakeries()

        db.session.add_all(cakes)
        db.session.add_all(cakebakeries)
        db.session.add_all(bakeries)
        db.session.commit()
