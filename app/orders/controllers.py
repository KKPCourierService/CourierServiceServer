from flask import render_template, Blueprint, request, flash, session, redirect, g, json, url_for
from flask_json import JsonError, json_response
from flask_login import login_required

from app_kkp import app, db, lm, json_kkp

from clients.models import Order, Client, OrderType, OrderStatus, IssuePoint

from datetime import datetime



orders_blu = Blueprint('orders', __name__, url_prefix = '/orders')


@orders_blu.route('/')
def getOrders():
	orders = Order.query.order_by(Order.dateOfCreation).all()

	ordersId = []
	for order in orders:
		ordersId.append(order.id)

	return json_response(orderId = ordersId)

@orders_blu.route('/<int:id>')
@login_required
def getOrder(id):
	order = Order.query.filter(Order.id  ==  id).first()
	issue = order.issuePoint
	dictionary_issue = []
	if issue is not None:
		for i in issue:
			dict_issue = {}
			issuePoint = IssuePoint.query.filter(IssuePoint.id == i).first()
			dict_issue['destinationType'] = issuePoint.destinationTypeId
			dict_issue['issuePointOrderNumber'] = issuePoint.orderNumber
			dict_issue['issuePointHumanFIO'] = issuePoint.humanFIO
			dict_issue['issuePointDescription'] = issuePoint.description
			dict_issue['issuePointPhoneNumber'] = issuePoint.phoneNumber
			dict_issue['issuePointAddress'] = issuePoint.address
			dictionary.append(dict_issue)

	#issuePoint = IssuePoint.query.filter(IssuePoint.id == order.issuePointId).first()
	#client = Client.query.filter(Client.id == order.clientId).first()
	#orderType = OrderType.query.filter(OrderType.id == order.typeId).first()
	#orderStatus = OrderType.query.filter(OrderType.id == order.statusId).first()

	return json_response(orderTypeId = order.typeId, clientId = order.clientId, courierId = order.courierId, \
		orderStatusId = order.statusId, orderNumberOfAddresses = order.numberOfAddresses, \
		orderInformationAboutAddresses = dictionary_issue, orderDescription = order.description, \
		orderPhoto = order.photoUrl, orderCost = order.cost)

@orders_blu.route('/free')
def getFreeOrders():
	orders = Order.query.order_by(Order.statusId == 5).all()

	ordersId = []
	for order in orders:
		ordersId.append(order.id)

	return json_response(orderId = ordersId)