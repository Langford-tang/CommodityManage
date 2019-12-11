# -*- coding: utf-8 -*-
import click
import random

from CommodityManage import app, db
from CommodityManage.models import *

from faker import Faker
fake = Faker()

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # add user
    user = User(username='longfei')
    user.set_password('112312')
    db.session.add(user)
    
    # add salesman: 30
    for i in range(29):
        salesman = Salesman(name=fake.name(), contact=fake.phone_number(), rank=1)
        db.session.add(salesman)
    salesman = Salesman(name=fake.name(), contact=fake.phone_number(), rank=2)
    db.session.add(salesman)
    # add repository： 5
    for i in range(5):
        repository = Repository(address=fake.address())
        db.session.add(repository)

    # add commodity: 10
    commodities = [
        {'name': 'pen', 'category': 'DailyUse', 'supplierID': 1, 'price': 2.34},
        {'name': 'book', 'category': 'Entertainment', 'supplierID': 1, 'price': 13.46},
        {'name': 'cellphone', 'category': 'Electronic', 'supplierID': 3, 'price': 122.47},
        {'name': 'jeans', 'category': 'Cloth', 'supplierID': 5, 'price': 34.76},
        {'name': 'cake', 'category': 'Food', 'supplierID': 2, 'price': 44.34},
        {'name': 'apple', 'category': 'Food', 'supplierID': 4, 'price': 37.86},
        {'name': 'wine', 'category': 'Drinks', 'supplierID': 4, 'price': 137.5},
        {'name': 'sofa', 'category': 'Furniture', 'supplierID': 2, 'price': 182.6},
        {'name': 'desk', 'category': 'Furniture', 'supplierID': 3, 'price': 182.4},
        {'name': 'chair', 'category': 'Furniture', 'supplierID': 1, 'price': 43.5},
    ]
    for c in commodities:
        commondity = Commondity(name=c['name'], category=c['category'], supplierID=c['supplierID'], price=c['price'])
        db.session.add(commondity)
    # add supplier: 10
    for i in range(10):
        supplier = Supplier(name=fake.company(), address=fake.address(), contact=fake.phone_number())
        db.session.add(supplier)
    # stock: 30
    for i in range(10):
        for j in range(5):
            stock = Stock(commondityID=i, repositoryID=j, number=random.choice(range(100,200)))
            db.session.add(stock)
    # enter repository
    # out repository
    # switch repository

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
