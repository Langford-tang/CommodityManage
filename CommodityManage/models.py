# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey, CheckConstraint

from CommodityManage import db


class User(db.Model, UserMixin):
    '''Admin user'''
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
 
# 业务相关 Entity
class Salesman(db.Model, UserMixin):
    __tablename__ = "Salesman"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    contact = db.Column(db.String(30), unique=True)
    rank = db.Column(db.Integer)
    repositoryID = db.Column(db.Integer, ForeignKey("Repository.id"))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

class Repository(db.Model):
    __tablename__ = "Repository"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120))

class Commondity(db.Model):
    __tablename__ = "Commodity"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    categoryID = db.Column(db.Integer, ForeignKey("CommodityCategory.id"))
    supplierID = db.Column(db.Integer, ForeignKey("Supplier.id"))
    price = db.Column(db.Float)

    CheckConstraint('price > 0')

class CommodityCategory(db.Model):
    __tablename__ = "CommodityCategory"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60))

class Supplier(db.Model):
    __tablename__ = "Supplier"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    address = db.Column(db.String(120), unique=True)
    contact = db.Column(db.String(30), unique=True)

class Stock(db.Model):
    __tablename__ = "Stock"
    commondityID = db.Column(db.Integer, primary_key=True)
    repositoryID = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)

    CheckConstraint('number > 0')

# 业务相关 Relation
class EnterRepository(db.Model):
    __tablename__ = "EnterRepository"
    id = db.Column(db.Integer, primary_key=True)
    commodityID = db.Column(db.Integer, ForeignKey("Commodity.id"))
    repositoryID = db.Column(db.Integer, ForeignKey("Repository.id"))
    salesmanID = db.Column(db.Integer, ForeignKey("Salesman.id"))
    commodityNumber = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    CheckConstraint('commodityNumber > 0')

class OutRepository(db.Model):
    __tablename__ = "OutRepository"
    id = db.Column(db.Integer, primary_key=True)
    commodityID = db.Column(db.Integer, ForeignKey("Commodity.id"))
    repositoryID = db.Column(db.Integer, ForeignKey("Repository.id"))
    salesmanID = db.Column(db.Integer, ForeignKey("Salesman.id"))
    commodityNumber = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    CheckConstraint('commodityNumber > 0')

class SwitchRepository(db.Model):
    __tablename__ = "SwitchRepository"
    id = db.Column(db.Integer, primary_key=True)
    commodityID = db.Column(db.Integer, ForeignKey("Commodity.id"))
    outRepositoryID = db.Column(db.Integer, ForeignKey("Repository.id"))
    enterRepositoryID = db.Column(db.Integer, ForeignKey("Repository.id"))
    salesmanID = db.Column(db.Integer, ForeignKey("Salesman.id"))
    commodityNumber = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    CheckConstraint('commodityNumber > 0')
