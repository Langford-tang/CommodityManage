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
        name = fake.name()
        contact = fake.phone_number()
        rank=1
        username = name.split(" ")[0]+"123"
        salesman = Salesman(name=name, contact=contact, rank=1, username=username)
        salesman.set_password('123')
        db.session.add(salesman)
    # add repository： 5
    for i in range(5):
        repository = Repository(address=fake.address())
        db.session.add(repository)

    commodityCategory = [
        {'id': 1, 'category': 'DailyUse'},
        {'id': 2, 'category': 'Entertainment'},
        {'id': 3, 'category': 'Electronic'},
        {'id': 4, 'category': 'Cloth'},
        {'id': 5, 'category': 'Food'},
        {'id': 6, 'category': 'Drinks'},
        {'id': 7, 'category': 'Furniture'}
    ]
    for c in commodityCategory:
        cate = CommodityCategory(id=c['id'], category=c['category'])
        db.session.add(cate)

    # add commodity: 10
    commodities = [
        {'name': 'pen', 'category': 1, 'supplierID': 1, 'price': 2.34},
        {'name': 'book', 'category': 2, 'supplierID': 1, 'price': 13.46},
        {'name': 'cellphone', 'category': 3, 'supplierID': 3, 'price': 122.47},
        {'name': 'jeans', 'category': 4, 'supplierID': 5, 'price': 34.76},
        {'name': 'cake', 'category': 5, 'supplierID': 2, 'price': 44.34},
        {'name': 'apple', 'category': 5, 'supplierID': 4, 'price': 37.86},
        {'name': 'wine', 'category': 6, 'supplierID': 4, 'price': 137.5},
        {'name': 'sofa', 'category': 7, 'supplierID': 2, 'price': 182.6},
        {'name': 'desk', 'category': 7, 'supplierID': 3, 'price': 182.4},
        {'name': 'chair', 'category': 7, 'supplierID': 1, 'price': 43.5},
    ]
    for c in commodities:
        commondity = Commondity(name=c['name'], categoryID=c['category'], supplierID=c['supplierID'], price=c['price'])
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
    for i in range(30):
        commodityID = random.choice(range(10))
        time = fake.date_time_this_year()
        repositoryID = random.choice(range(5))
        salesmanID = random.choice(range(30))
        commodityNumber = random.choice(range(100,200))
        
        enterRepo = EnterRepository(commodityID=commodityID, salesmanID=salesmanID, repositoryID=repositoryID,
                                    commodityNumber=commodityNumber, time=time)
        db.session.add(enterRepo)

    # out repository
    for i in range(30):
        commodityID = random.choice(range(10))
        time = fake.date_time_this_year()
        repositoryID = random.choice(range(5))
        salesmanID = random.choice(range(30))
        commodityNumber = random.choice(range(100,200))
        
        outRepo = OutRepository(commodityID=commodityID, salesmanID=salesmanID, repositoryID=repositoryID,
                                    commodityNumber=commodityNumber, time=time)
        db.session.add(outRepo)

    # switch repository
    for i in range(30):
        commodityID = random.choice(range(10))
        time = fake.date_time_this_year()
        outRepositoryID = random.choice(range(5))
        enterRepositoryID = random.choice(range(5))
        while (enterRepositoryID==outRepositoryID):
            outRepositoryID = random.choice(range(5))

        salesmanID = random.choice(range(30))
        commodityNumber = random.choice(range(100,200))
        
        switchRepo = SwitchRepository(commodityID=commodityID, salesmanID=salesmanID, 
                                    outRepositoryID=outRepositoryID, enterRepositoryID=enterRepositoryID,
                                    commodityNumber=commodityNumber, time=time)
        db.session.add(switchRepo)

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
