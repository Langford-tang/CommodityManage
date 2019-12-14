# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from CommodityManage import app, db
from CommodityManage.models import *

@app.route('/', methods=['GET', 'POST'])
def myIndex():
    '''
    Index
    '''
    # movies = Movie.query.all()
    # return render_template('myIndex.html', movies=movies)
    return render_template('myIndex.html')

@app.route('/salesmanEntry.html', methods=['GET', 'POST'])
def salesmanEntry():
    '''
    salesman 登录界面
    '''
    if request.method == 'POST':
        print('method POST.')

        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            print("Invalid input.")
            flash('Invalid input.')
            return redirect(url_for('salesmanEntry'))

        users = User.query.all()
        print("User query susccess.")

        for user in users:
            if username == user.username and user.validate_password(password):
                print("User match.")
                login_user(user)
                flash('Login success.')
                return redirect(url_for('salesman'))
        print("User not match.")
        flash('Invalid username or password.')
        return redirect(url_for('salesmanEntry'))

    return render_template('salesmanEntry.html')

@app.route('/adminEntry.html', methods=['GET', 'POST'])
def adminEntry():
    '''
    admin 登录界面
    '''
    if request.method == 'POST':
        print('method POST.')

        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            print("Invalid input.")
            flash('Invalid input.')
            return redirect(url_for('adminEntry'))

        users = User.query.all()
        print("User query susccess.")

        for user in users:
            if username == user.username and user.validate_password(password):
                print("User match.")
                login_user(user)
                flash('Login success.')
                return redirect(url_for('repository_infor'))
        print("User not match.")
        flash('Invalid username or password.')
        return redirect(url_for('adminEntry'))

    return render_template('adminEntry.html')

@app.route('/salesman.html', methods=['GET', 'POST'])
def salesman():
    '''
    salesman 查看界面
    '''
    queries = db.session().query(Stock.repositoryID, Commondity.name, Stock.number). \
        filter(Stock.commondityID == Commondity.id).all()
    return render_template('salesman.html', queries=queries)

@app.route('/stock_infor.html', methods=['GET', 'POST'])
def stock_infor():
    '''
    展示库存信息
    '''
    queries = db.session().query(Stock.repositoryID, Commondity.name, Stock.number).\
        filter(Stock.commondityID==Commondity.id).all()
    return render_template('stock_infor.html', queries = queries)

@app.route('/repository_infor.html', methods=['GET', 'POST'])
def repository_infor():
    '''
    展示仓库信息
    '''
    repositories = Repository.query.all()
    return render_template('repository_infor.html', repositories=repositories)

@app.route('/supplier_infor.html', methods=['GET', 'POST'])
def supplier_infor():
    '''
    展示供货商信息
    '''
    suppliers = Supplier.query.all()
    return render_template('supplier_infor.html', suppliers=suppliers)

@app.route('/salesman_infor.html', methods=['GET', 'POST'])
def salesman_infor():
    '''
    展示业务员信息
    '''
    salesmen = Salesman.query.all()
    return render_template('salesman_infor.html', salesmen=salesmen)

@app.route('/commodity_infor.html', methods=['GET', 'POST'])
def commodity_infor():
    '''
    展示商品信息
    '''
    commodities = Commondity.query.all()
    return render_template('commodity_infor.html', commodities=commodities)

@app.route('/commodity_static.html', methods=['GET', 'POST'])
def commodity_static():
    '''
    商品统计信息
    '''
    if request.method == 'POST':
        print('Method POST')

        option_state = request.form['state']
        commodity_name = request.form['commodity_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        print(option_state)
        print(commodity_name)
        print(start_date)
        print(end_date)

    statics = Commondity.query.all()
    return render_template('commodity_static.html', statics=statics)