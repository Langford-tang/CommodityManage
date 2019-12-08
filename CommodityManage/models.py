# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from CommodityManage import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# 业务相关 Entity
class Salesman(db.Model):
    __tablename__ = "Salesman"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    contact = db.Column(db.String(30))
    rank = db.Column(db.Integer)

class Repository(db.Model):
    __tablename__ = "Repository"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120))

class Commondity(db.Model):
    __tablename__ = "Commodity"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    category = db.Column(db.String(60))
    supplierID = db.Column(db.Integer)
    price = db.Column(db.Float)

class Supplier(db.Model):
    __tablename__ = "Supplier"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    address = db.Column(db.String(120))
    contact = db.Column(db.String(30))

class Stock(db.Model):
    __tablename__ = "Stock"
    commondityID = db.Column(db.Integer, primary_key=True)
    repositoryID = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)

# 业务相关 Relation
class EnterRepository(db.Model):
    __tablename__ = "EnterRepository"
    id = db.Column(db.Integer, primary_key=True)
    commodityID = db.Column(db.Integer)
    repositoryID = db.Column(db.Integer)
    salesmanID = db.Column(db.Integer)
    commodityNumber = db.Column(db.Integer)
    time = db.Column(db.DateTime)

class OutRepository(db.Model):
    __tablename__ = "OutRepository"
    id = db.Column(db.Integer, primary_key=True)
    commodityID = db.Column(db.Integer)
    repositoryID = db.Column(db.Integer)
    salesmanID = db.Column(db.Integer)
    commodityNumber = db.Column(db.Integer)
    time = db.Column(db.DateTime)

class SwitchRepository(db.Model):
    __tablename__ = "SwitchRepository"
    id = db.Column(db.Integer, primary_key=True)
    commodityID = db.Column(db.Integer)
    outRepositoryID = db.Column(db.Integer)
    enterRepositoryID = db.Column(db.Integer)
    salesmanID = db.Column(db.Integer)
    commodityNumber = db.Column(db.Integer)
    time = db.Column(db.DateTime)
