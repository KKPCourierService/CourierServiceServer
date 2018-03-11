from flask import render_template, Blueprint, request, flash, session, redirect, g, json, url_for
from flask_json import JsonError, json_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import check_password_hash, generate_password_hash

from app_kkp import app, db, lm, json_kkp

from .models import Client, Order, OrderType, OrderStatus

from datetime import datetime



clients_blu = Blueprint('clients', __name__, url_prefix = '/clients')


@lm.user_loader
def load_client(id):
	return Client.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.lastSeen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@clients_blu.route('/')
def getClients():
	clients = Client.query.order_by(Client.id).all()
	ids = []

	for client in clients:
		ids.append(client.id)

	return json_response(clientId = ids)

@clients_blu.route('/singUpClient', methods = ['GET', 'POST'])
def singUpClient():
	data = request.get_json(force = True)

	try:
		client = Client(name = data['name'], surname = data['surname'], \
			patronymic = data['patronymic'], phoneNumber = data['phoneNumber'],\
			photoUrl = data['photoUrl'], email = data['email'], \
			password = generate_password_hash(data['password']))

		db.session.add(client)
		db.session.commit()

		session['remember_me'] = True
	except:
		raise JsonError(description = 'Error register')
	return json_response(response = 'success')

@clients_blu.route('/login', methods = ['GET', 'POST'])
def loginClient():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('clients.getClients'))

	data = request.get_json(force = True)

	try:
		client = Client.query.filter(Client.email  ==  data['email']).first()

		if client and check_password_hash(client.password, data['password']):
			#session['remember_me'] = data['remember_me']

			remember_me = False
			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None)

			login_user(client, remember = remember_me)
	except:
		raise JsonError(description = 'Error sing in')
	return json_response(response = 'success')

@clients_blu.route('/logout', methods = ['GET', 'POST'])
def logOutClient():
	logout_user()
	return redirect(url_for('clients.getClients'))

@clients_blu.route('/<int:id>/profile')
@login_required
def getClient(id):
	client = Client.query.filter(Client.id  ==  id).first()

	return json_response(clientId = client.id, clientEmail = client.email, clientName = client.name, \
		clientSurname = client.surname, clientPatronymic = client.patronymic, clientPhoneNumber = client.phoneNumber, \
		orders = client.orders)

@clients_blu.route('/<int:id>/profile/edit', methods = ['GET', 'POST'])
@login_required
def editProfile(id):
	data = request.get_json(force = True)
	try:
		g.user.name = data['name']
		g.user.surname =  data['surname']
		g.user.patronymic = data['patronymic']
		g.user.phoneNumber = data['phoneNumber']
		g.user.password = generate_password_hash(data['password'])
		db.session.add(g.user)
		db.session.commit()
	except:
		raise JsonError(description = 'Error to edit profile')
	return redirect(url_for('clients.getClient', id = g.user.id))
	
@clients_blu.route('/<int:id>/profile/editPhoto', methods = ['GET', 'POST'])
def editProfilePhoto(id):
	pass

@clients_blu.route('/<int:id>/orders', methods = ['GET'])
def getOrders(id):
	client = Client.query.filter(Client.id  ==  id).first()
	clientOrders = client.orders

	ordersId = []
	for order in clientOrders:
		ordersId.append(order.id)

	return json_response(orderId = ordersId)

@clients_blu.route('/<int:id>/orders/create', methods = ['GET', 'POST'])
def createOrder(id):
	data = request.get_json(force = True)

	try:
		order = Order(typeId = data['typeId'], clientId = id,	statusId = data['statusId'], issuePointId = None, \
			numberOfAddresses = data['numberOfAddresses'], informationAboutAddresses = data['informationAboutAddresses'], \
			description = data['description'], cost = data['cost'])

		db.session.add(order)
		db.session.commit()

	except:
		raise JsonError(description = 'Error to create order')
	return json_response(response = 'success')