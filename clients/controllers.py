from flask import render_template, Blueprint, request, flash, session, redirect, g, json, url_for
from flask_json import JsonError, json_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import check_password_hash, generate_password_hash

from app_kkp import app, db, lm, json_kkp

from .models import Client, Order, OrderType, OrderStatus

from datetime import datetime


# Регистрируем основной url для клиента и объявляем его как переменную для дальнейшего использования
clients_blu = Blueprint('clients', __name__, url_prefix='/clients')


# Используется чтобы получения клиента
@lm.user_loader
def load_client(id):
    return Client.query.get(int(id))

# Проверка авторизован ли пользователь или нет


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.lastSeen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

# Получаем информацию о клиентах


@clients_blu.route('/')
def getClients():
    clients = Client.query.order_by(Client.id).all()
    ids = []

    for client in clients:
        ids.append(client.id)

    return json_response(clientId=ids)

# Метод для регистрации клиентов


@clients_blu.route('/signUpClient', methods=['GET', 'POST'])
def signUpClient():
    data = request.get_json(force=True)

    try:
        client = Client(name=data['clientName'], surname=data['clientSurname'],
                        patronymic=data['clientPatronymic'], phoneNumber=data['clientPhoneNumber'],
                        # photoUrl=data['photoUrl'],
                        email=data['clientEmail'],
                        password=generate_password_hash(data['clientPassword']))

        db.session.add(client)
        db.session.commit()

        session['remember_me'] = True
    except:
        raise JsonError(description='Error register')
    return json_response(response='success', clientId=client.id)

# Метод для авторизации клиента


@clients_blu.route('/login', methods=['GET', 'POST'])
def loginClient():
    if g.user is not None and g.user.is_authenticated:
        return json_response(response='user is authenticated')

    data = request.get_json(force=True)

    try:
        client = Client.query.filter(Client.email == data['clientEmail']).first()

        if client and check_password_hash(client.password, data['clientPassword']):
            #session['remember_me'] = data['remember_me']

            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)

            login_user(client, remember=remember_me)
        else:
            raise
    except:
        raise JsonError(description='Error sing in')
    return json_response(response='success', clientId=client.id)

# Метод для выхода из аккаунта


@clients_blu.route('/logout', methods=['GET', 'POST'])
def logOutClient():
    logout_user()
    return json_response(response='success')
    # return redirect(url_for('clients.getClients'))

# Получаем информацию о конкретном клиенте


@clients_blu.route('/<int:id>/profile', methods=['GET'])
# @login_required
def getClient(id):
    client = Client.query.filter(Client.id == id).first()

    return json_response(clientId=client.id, clientEmail=client.email, clientName=client.name,
                         clientSurname=client.surname, clientPatronymic=client.patronymic, clientPhoneNumber=client.phoneNumber) #,
                         #orders=client.orders)

# Метод для изменения информации о своем аккаунте


@clients_blu.route('/<int:id>/profile/editName', methods=['POST'])
# @login_required
def editProfileName(id):
    data = request.get_json(force=True)
    try:
        client = Client.query.filter(Client.id == id).update(
            {
            'name': data['clientName']
            })
        db.session.commit()
    except:
        raise JsonError(description='Error to edit name') 
    return json_response(response='success')
    # return redirect(url_for('clients.getClient', id=g.user.id))

@clients_blu.route('/<int:id>/profile/editSurname', methods=['POST'])
# @login_required
def editProfileSurname(id):
    data = request.get_json(force=True)
    try:
        client = Client.query.filter(Client.id == id).update(
            {
            'surname': data['clientSurname']
            })
        db.session.commit()
    except:
        raise JsonError(description='Error to edit surname') 
    return json_response(response='success')

@clients_blu.route('/<int:id>/profile/editPatronymic', methods=['POST'])
# @login_required
def editProfilePatronymic(id):
    data = request.get_json(force=True)
    try:
        client = Client.query.filter(Client.id == id).update(
            {
            'patronymic': data['clientPatronymic']
            })
        db.session.commit()
    except:
        raise JsonError(description='Error to edit patronymic') 
    return json_response(response='success')

@clients_blu.route('/<int:id>/profile/editPhoneNumber', methods=['POST'])
# @login_required
def editProfilePhoneNumber(id):
    data = request.get_json(force=True)
    try:
        client = Client.query.filter(Client.id == id).update(
            {
            'phoneNumber': data['clientPhoneNumber']
            })
        db.session.commit()
    except:
        raise JsonError(description='Error to edit phone number') 
    return json_response(response='success')

@clients_blu.route('/<int:id>/profile/editPassword', methods=['POST'])
# @login_required
def editProfilePassword(id):
    data = request.get_json(force=True)
    try:
        client = Client.query.filter(Client.id == id).update(
            {
            'password': data['clientPassword']
            })
        db.session.commit()
    except:
        raise JsonError(description='Error to edit password') 
    return json_response(response='success')


@clients_blu.route('/<int:id>/profile/editPhoto', methods=['POST'])
def editProfilePhoto(id):
    pass

# Метод для полечения информации о всех заказах


@clients_blu.route('/<int:id>/orders', methods=['GET'])
def getOrders(id):
    client = Client.query.filter(Client.id == id).first()
    clientOrders = client.orders

    ordersId = []
    for order in clientOrders:
        ordersId.append(order.id)

    return json_response(orderId=ordersId)

# Метод для создания заказа


@clients_blu.route('/<int:id>/orders/create', methods=['GET', 'POST'])
def createOrder(id):
    data = request.get_json(force=True)

    try:
        order = Order(typeId=data['orderTypeId'], clientId=id, 
                      statusId=data['orderStatusId'],
         			  issuePointId=None,
                      numberOfAddresses=data['orderNumberOfAddresses'],
                      informationAboutAddresses=data['orderInformationAboutAddresses'],
                      description=data['orderDescription'], cost=data['orderCost'])

        db.session.add(order)
        db.session.commit()

    except:
        raise JsonError(description='Error to create order')
    return json_response(response='success', orderId=order.id)

@clients_blu.route('/admin/createType', methods=['POST'])
def createOrderType():
    data = request.get_json(force=True)

    try:
        orderType = OrderType(name=data['name'])

        db.session.add(orderType)
        db.session.commit()

    except:
        raise JsonError(description='Error to create order type')
    return json_response(response='success')

@clients_blu.route('/admin/createStatus', methods=['POST'])
def createOrderStatus():
    data = request.get_json(force=True)

    try:
        orderStatus = OrderStatus(name=data['name'])

        db.session.add(orderStatus)
        db.session.commit()

    except:
        raise JsonError(description='Error to create order status')
    return json_response(response='success')

@clients_blu.route('/admin/orderType', methods=['GET'])
def getOrderTypes():
    orderTypes = OrderType.query.order_by(OrderType.id).all()
    ids = []

    for orderType in orderTypes:
        ids.append(orderType.id)

    return json_response(orderTypeId=ids)

@clients_blu.route('/admin/orderStatus', methods=['GET'])
def getOrderStatuses():
    orderStatuses = OrderStatus.query.order_by(OrderStatus.id).all()
    ids = []

    for orderStatus in orderStatuses:
        ids.append(orderStatus.id)

    return json_response(orderStatusId=ids)

@clients_blu.route('/admin/orderType/<int:id>', methods=['GET'])
# @login_required
def getOrderType(id):
    orderType = OrderType.query.filter(OrderType.id == id).first()

    return json_response(typeId=orderType.id, typeName=orderType.name)

@clients_blu.route('/admin/orderStatus/<int:id>', methods=['GET'])
# @login_required
def getOrderStatus(id):
    orderStatus = OrderStatus.query.filter(OrderStatus.id == id).first()

    return json_response(statusId=orderStatus.id, statusName=orderStatus.name)