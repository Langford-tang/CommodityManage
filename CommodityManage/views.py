# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from sqlalchemy import func

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
    return render_template('salesman.html')

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
    results=[]
    if request.method == 'POST':
        print('Method POST')

        # 获得统计信息选项
        option_state = request.form['state']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        # start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        # end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        # 查询指定时间段内所有商品的入库信息
        if option_state == "enter":
            results = db.session().query(EnterRepository.commodityID, Commondity.name, Commondity.category, func.sum(Stock.number).label('sum')).\
                            filter(EnterRepository.time.between(start_date, end_date)).\
                            filter(EnterRepository.commodityID==Commondity.id).\
                            group_by(EnterRepository.commodityID).all()
        else:
            results = db.session().query(OutRepository.commodityID, Commondity.name, Commondity.category, func.sum(Stock.number).label('sum')).\
                            filter(OutRepository.time.between(start_date, end_date)).\
                            filter(OutRepository.commodityID==Commondity.id).\
                            group_by(OutRepository.commodityID).all()

    return render_template('commodity_static.html', results=results)