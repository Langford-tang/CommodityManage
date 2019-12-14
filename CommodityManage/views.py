# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from sqlalchemy import func, event

from CommodityManage import app, db
from CommodityManage.models import *

@app.route('/', methods=['GET', 'POST'])
def myIndex():
    '''
    Index
    '''

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

        users = Salesman.query.all()
        print("User query susccess.")

        for user in users:
            if username == user.username and user.validate_password(password):
                print("User match.")
                login_user(user)
                session['user_type'] = 'salesman'
                session['user_id'] = user.id
                flash('Login success.')
                return redirect(url_for('stock_infor'))
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

    print(session['user_type'])
    print(session['user_id'])
    print(type(session['user_id']))

    queries = db.session().query(Stock.repositoryID, Commondity.name, CommodityCategory.category, Stock.number).\
        filter(Stock.commondityID==Commondity.id).\
        filter(Commondity.categoryID==CommodityCategory.id).all()
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
    commodities = db.session().query(Commondity.id, Commondity.name, Commondity.price,\
                                        Supplier.name.label('supplier_name'), CommodityCategory.category).\
        filter(Commondity.categoryID == CommodityCategory.id).\
        filter(Commondity.supplierID == Supplier.id).all()
    return render_template('commodity_infor.html', commodities=commodities)

@app.route('/commodity_category_infor.html', methods=['GET', 'POST'])
def commodity_category_infor():
    '''
    展示商品类别信息
    '''
    results = CommodityCategory.query.all()
    return render_template('commodity_category_infor.html', results=results)

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
            results = db.session().query(EnterRepository.commodityID, Commondity.name, CommodityCategory.category, func.sum(Stock.number).label('sum')).\
                            filter(EnterRepository.time.between(start_date, end_date)).\
                            filter(EnterRepository.commodityID==Commondity.id).\
                            filter(Commondity.categoryID==CommodityCategory.id).\
                            group_by(EnterRepository.commodityID).all()
        else:
            results = db.session().query(OutRepository.commodityID, Commondity.name, CommodityCategory.category, func.sum(Stock.number).label('sum')).\
                            filter(OutRepository.time.between(start_date, end_date)).\
                            filter(OutRepository.commodityID==Commondity.id).\
                            filter(Commondity.categoryID==CommodityCategory.id).\
                            group_by(OutRepository.commodityID).all()

    return render_template('commodity_static.html', results=results)

@app.route('/enter_repo.html', methods=['GET', 'POST'])
def enter_repo():
    '''
    入库业务
    '''
    if request.method == 'POST':
        commodityName = request.form['commodity']
        commodity = db.session().query(Commondity).\
            filter(Commondity.name==commodityName).first()
        if not commodity:
            '''商品名输入有误，重新填写'''
            print("invalid commodity name.")
            return redirect(url_for('enter_repo'))
        commodityID = commodity.id
        repositoryID = request.form['repository']
        num = request.form['num']
        user = db.session().query(Salesman).get(session['user_id'])
        time = datetime.now()

        enterRepository = EnterRepository(commodityID=commodityID, repositoryID=repositoryID,\
                                         salesmanID=user.id, commodityNumber=num, time=time)
        db.session.add(enterRepository)
        db.session.commit()
        print("商品入库成功！")

    results = db.session().query(EnterRepository.id, Commondity.name, CommodityCategory.category, EnterRepository.repositoryID,  
                                Salesman.id.label('salesmanID'), Salesman.name.label('salesmanName'), Supplier.name.label('supplierName'),
                                EnterRepository.commodityNumber, EnterRepository.time.label('date') ).\
                            filter(Commondity.id == EnterRepository.commodityID).\
                            filter(CommodityCategory.id == Commondity.categoryID).\
                            filter(Supplier.id == Commondity.supplierID).\
                            filter(Salesman.id == EnterRepository.salesmanID).all()
    return render_template('enter_repo.html', results=results)

@app.route('/out_repo.html', methods=['GET', 'POST'])
def out_repo():
    '''
    出库业务
    '''
    if request.method == 'POST':
        commodityName = request.form['commodity']
        commodity = db.session().query(Commondity).\
            filter(Commondity.name==commodityName).first()
        if not commodity:
            '''商品名输入有误，重新填写'''
            print("invalid commodity name.")
            return redirect(url_for('enter_repo'))
        commodityID = commodity.id
        repositoryID = request.form['repository']
        num = int(request.form['num'])
        user = db.session().query(Salesman).get(session['user_id'])
        time = datetime.now()

        # check stock num > 0 
        check_num = db.session.query(Stock).filter(Stock.commondityID==commodityID).\
                                filter(Stock.repositoryID==repositoryID).first().number
        if check_num-num<0:
            print("volite >0 constraint")
            flash("库存数量小于销售数量")
            return redirect(url_for('enter_repo'))

        outRepository = OutRepository(commodityID=commodityID, repositoryID=repositoryID,\
                                         salesmanID=user.id, commodityNumber=num, time=time)
        db.session.add(outRepository)
        db.session.commit()
        print("商品出库成功！")

    results = db.session().query(OutRepository.id, Commondity.name, CommodityCategory.category, OutRepository.repositoryID,  
                                Salesman.id.label('salesmanID'), Salesman.name.label('salesmanName'),
                                OutRepository.commodityNumber, OutRepository.time.label('date') ).\
                            filter(Commondity.id == OutRepository.commodityID).\
                            filter(CommodityCategory.id == Commondity.categoryID).\
                            filter(Salesman.id == OutRepository.salesmanID).all()
    return render_template('out_repo.html', results=results)

@app.route('/switch_repo.html', methods=['GET', 'POST'])
def switch_repo():
    '''
    转仓业务
    '''
    if request.method == 'POST':
        commodityName = request.form['commodity']
        commodity = db.session().query(Commondity).\
            filter(Commondity.name==commodityName).first()
        if not commodity:
            '''商品名输入有误，重新填写'''
            print("invalid commodity name.")
            return redirect(url_for('enter_repo'))
        commodityID = commodity.id
        fromRepositoryID = request.form['switch_from_repository']
        toRepositoryID = request.form['switch_to_repository']
        num = request.form['num']
        user = db.session().query(Salesman).get(session['user_id'])
        time = datetime.now()

        # check stock num > 0 
        check_num = db.session.query(Stock).filter(Stock.commondityID==commodityID).\
                                filter(Stock.outRepositoryID==fromRepositoryID).first().number
        if check_num-num<0:
            print("volite >0 constraint")
            flash("库存数量小于销售数量")
            return redirect(url_for('switch_repo'))

        switchRepository = SwitchRepository(commodityID=commodityID, outRepositoryID=fromRepositoryID,\
                                            enterRepositoryID = toRepositoryID, salesmanID=user.id,\
                                            commodityNumber=num, time=time)
        db.session.add(switchRepository)
        db.session.commit()
        print("商品转仓成功！")

    results = db.session().query(SwitchRepository.id, Commondity.name, CommodityCategory.category, 
                                SwitchRepository.enterRepositoryID, SwitchRepository.outRepositoryID,  
                                Salesman.id.label('salesmanID'), Salesman.name.label('salesmanName'),
                                SwitchRepository.commodityNumber, SwitchRepository.time.label('date') ).\
                            filter(Commondity.id == SwitchRepository.commodityID).\
                            filter(CommodityCategory.id == Commondity.categoryID).\
                            filter(Salesman.id == SwitchRepository.salesmanID).all()
    return render_template('switch_repo.html', results=results)

@event.listens_for(EnterRepository, 'after_insert')
def after_EnterRepo_intert(mapper, connection, target):
    '''入库之后更新库存表'''
    commodityID = target.commodityID
    repositoryID = target.repositoryID
    commodityNumber = int(target.commodityNumber)

    db.session.query(Stock).filter(Stock.commondityID==commodityID).\
                            filter(Stock.repositoryID==repositoryID).\
                            update({"number": (Stock.number + commodityNumber)})
    # db.session.commit()
    print("库存表根据入库表已更新")

@event.listens_for(OutRepository, 'after_insert')
def after_OutRepository_intert(mapper, connection, target):
    '''出库之后更新库存表'''
    commodityID = target.commodityID
    repositoryID = target.repositoryID
    commodityNumber = int(target.commodityNumber)

    db.session.query(Stock).filter(Stock.commondityID==commodityID).\
                            filter(Stock.repositoryID==repositoryID).\
                            update({"number": (Stock.number - commodityNumber)})
    print("库存表根据出库表已更新")

@event.listens_for(SwitchRepository, 'after_insert')
def after_SwitchRepository_intert(mapper, connection, target):
    '''转仓之后更新库存表'''
    commodityID = target.commodityID
    outRepositoryID = target.outRepositoryID
    enterRepositoryID = target.enterRepositoryID
    commodityNumber = int(target.commodityNumber)

    db.session.query(Stock).filter(Stock.commondityID==commodityID).\
                            filter(Stock.repositoryID==enterRepositoryID).\
                            update({"number": (Stock.number + commodityNumber)})
    db.session.query(Stock).filter(Stock.commondityID==commodityID).\
                            filter(Stock.repositoryID==outRepositoryID).\
                            update({"number": (Stock.number - commodityNumber)})
    # db.session.commit()
    print("库存表根据转仓表已更新")