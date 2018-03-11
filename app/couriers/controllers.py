from flask import render_template, Blueprint, request, flash, session, redirect, g, json, url_for
from flask_json import JsonError, json_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import check_password_hash, generate_password_hash

from app_kkp import app, db, lm, json_kkp

from clients.models import Order, OrderType, OrderStatus, Courier, CourierType, PersonalInformation, DocumentsPhoto, Operation

from datetime import datetime



couriers_blu = Blueprint('couriers', __name__, url_prefix = '/couriers')


@lm.user_loader
def load_courier(id):
	return Courier.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.lastSeen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@couriers_blu.route('/')
def getCouriers():
	couriers = Courier.query.order_by(Courier.id).all()
	ids = []

	for courier in couriers:
		ids.append(courier.id)

	return json_response(courierId = ids)

@couriers_blu.route('/singUpCourier', methods = ['GET', 'POST'])
def singUpCourier():
	data = request.get_json(force = True)

	try:
		courier = Courier(name = data['name'], surname = data['surname'], \
			patronymic = data['patronymic'], phoneNumber = data['phoneNumber'],\
			photoUrl = data['photoUrl'], email = data['email'], \
			password = generate_password_hash(data['password']), \
			courierTypeId = data['courierTypeId'], personalInformationId = data['personalInformationId'], \
			documentsPhotoId = data['documentsPhotoId'], courierBalance = data['courierBalance'])

		db.session.add(courier)
		db.session.commit()

		session['remember_me'] = True
	except:
		raise JsonError(description = 'Error register')
	return json_response(response = 'success')

@couriers_blu.route('/login', methods = ['GET', 'POST'])
def loginCourier():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('couriers.getCouriers'))

	data = request.get_json(force = True)

	try:
		courier = Courier.query.filter(Courier.email  ==  data['email']).first()

		if courier and check_password_hash(courier.password, data['password']):
			#session['remember_me'] = data['remember_me']

			remember_me = False
			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None)

			login_user(courier, remember = remember_me)
	except:
		raise JsonError(description = 'Error sing in')
	return json_response(response = 'success')

@couriers_blu.route('/logout', methods = ['GET', 'POST'])
def logOutCourier():
	logout_user()
	return redirect(url_for('couriers.getCourier'))

@couriers_blu.route('/<int:id>/profile')
@login_required
def getCourier(id):
	courier = Courier.query.filter(Courier.id  ==  id).first()

	return json_response(courierId = courier.id, courierEmail = courier.email, courierName = courier.name, \
		courierSurname = courier.surname, courierPatronymic = courier.patronymic, \
		courierPhoneNumber = courier.phoneNumber, courierTypeId = courier.courierTypeId, orders = courier.orders)

@couriers_blu.route('/<int:id>/profile/edit', methods = ['GET', 'POST'])
@login_required
def editProfile(id):
	data = request.get_json(force = True)
	try:
		g.user.name = data['name']
		g.user.surname =  data['surname']
		g.user.patronymic = data['patronymic']
		g.user.phoneNumber = data['phoneNumber']
		g.user.courierTypeId = data['courierTypeId']
		g.user.password = generate_password_hash(data['password'])
		db.session.add(g.user)
		db.session.commit()
	except:
		raise JsonError(description = 'Error to edit profile')
	return redirect(url_for('couriers.getCourier', id = g.user.id))
	
@couriers_blu.route('/<int:id>/profile/editPhoto', methods = ['GET', 'POST'])
def editProfilePhoto(id):
	pass

@couriers_blu.route('/<int:id>/orders', methods = ['GET'])
def getOrders(id):
	courier = Courier.query.filter(Courier.id  ==  id).first()
	courierOrders = courier.orders

	ordersId = []
	for order in courierOrders:
		ordersId.append(order.id)

	return json_response(orderId = ordersId)

couriers_blu.route('/<int:id>/orders/add', methods = ['GET', 'POST'])
def addOrder(id):
	data = request.get_json(force = True)
	courier = Courier.query.filter(Courier.id  ==  id).first()

	try:
		courier.orders.append(data['orderId'])

		db.session.add(courier)
		db.session.commit
	except:
		raise JsonError(description = 'Error add order')
	return json_response(description = 'success')

couriers_blu.route('/<int:id>/orders/<int:id_order>/editStatus', methods = ['POST'])
def editStatusOrder(id, id_order):
	data = request.get_json(force = True)
	order = Order.query.filter(Order.id  ==  id_order).first()

	try:
		order.statusId = data['orderStatusId']

		db.session.add(order)
		db.session.commit()
	except:
		raise JsonError(description = 'Error edit status order')
	return json_response(description = 'success')

couriers_blu.route('/<int:id>/operations', methods = ['GET'])
def getOperations(id):
	operations = Operation.query.order_by(Operation.courierId == id).all()

	operationsId = []
	for operation in operations:
		operationsId.append(operation.id)

	return json_response(operationId = operationsId)

couriers_blu.route('/<int:id>/operations/withdrawalOfFunds', methods = ['POST'])
def withdrawalOfFunds(id):
	pass