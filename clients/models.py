from app_kkp import db
from datetime import datetime
import re


#Класс модели клиента в базе данных
#Соответствует диаграмме классов
class Client(db.Model):
	__tablename__ = 'client'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(140), unique = True)
	name = db.Column(db.String(140))
	surname = db.Column(db.String(140))
	patronymic = db.Column(db.String(140))
	password = db.Column(db.String(140))
	phoneNumber = db.Column(db.String(140))
	photoUrl = db.Column(db.String(140))
	orders = db.relationship('Order', backref = db.backref('client'))
	lastSeen = db.Column(db.DateTime)

	def __init__(self, name = None, surname = None, patronymic = None, phoneNumber = None, photoUrl = None, email = None, password = None):
		super(Client, self).__init__(name = None, surname = None, patronymic = None, phoneNumber = None, \
			photoUrl = None, email = None, password = None)
		self.name = name
		self.surname = surname
		self.patronymic = patronymic
		self.phoneNumber = phoneNumber
		self.photoUrl = photoUrl
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id) #python 2
		except NameError:
			return str(self.id) #python 3

	def __repr__(self):
		return '<Id: {}. {} {} {}. Phone number: {}\n{}>'.format(self.id, self.surname, self.name, self.patronymic, self.phoneNumber, self.email)

#Класс модели заказа в базе данных
class Order(db.Model):
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key = True)
	typeId = db.Column(db.Integer, db.ForeignKey('orderType.id'))
	clientId = db.Column(db.Integer, db.ForeignKey('client.id'))
	courierId = db.Column(db.Integer, db.ForeignKey('courier.id'))
	statusId = db.Column(db.Integer, db.ForeignKey('orderStatus.id'))
	issuePointId = db.Column(db.Integer, db.ForeignKey('issuePoint.id'))
	numberOfAddresses = db.Column(db.Integer)
	informationAboutAddresses = db.Column(db.Text)
	dateOfCreation = db.Column(db.DateTime)
	description = db.Column(db.Text)
	photoUrl = db.Column(db.String(250))
	#dateOfCompletion = db.Column(db.DateTime)	
	cost = db.Column(db.Integer)

	operations = db.relationship('Operation', backref = db.backref('order'))

	def __init__(self, typeId = None, clientId = None, statusId = None, issuePointId = None, numberOfAddresses = None, \
		informationAboutAddresses = None, description = None, photoUrl = None, cost = None):
		
		super(Order, self).__init__(typeId = None, clientId = None, statusId = None, issuePointId = None, numberOfAddresses = None, \
		informationAboutAddresses = None, description = None, photoUrl = None, cost = None)

		self.typeId = typeId
		self.clientId = clientId
		#self.courierId = courierId
		self.statusId = statusId
		self.issuePointId = issuePointId
		self.numberOfAddresses = numberOfAddresses
		self.informationAboutAddresses = informationAboutAddresses
		#self.dateOfCreation = datetime.utcnow()
		self.description = description
		self.photoUrl = photoUrl
		#self.dateOfCompletion = dateOfCompletion
		self.cost = cost

	def is_active(self):
		return True

	def get_id(self):
		try:
			return unicode(self.id) #python 2
		except NameError:
			return str(self.id) #python 3

	def __repr__(self):
		return '<{}. {}>'.format(self.id, self.description)

#Класс модели курьера в базе данных
class Courier(db.Model):
	__tablename__ = 'courier'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(140), unique = True)
	name = db.Column(db.String(140))
	surname = db.Column(db.String(140))
	patronymic = db.Column(db.String(140))
	password = db.Column(db.String(140))
	phoneNumber = db.Column(db.String(140))
	photoUrl = db.Column(db.String(140))
	orders = db.relationship('Order', backref = db.backref('courier'))
	operations = db.relationship('Operation', backref = db.backref('courier'))
	courierBalance = db.Column(db.Integer)
	personalInformationId = db.Column(db.Integer, db.ForeignKey('personalInformation.id'))
	#db.relationship('PersonalInformation', uselist = False, backref = db.backref('courier'))
	documentsPhotoId = db.Column(db.Integer, db.ForeignKey('documentsPhoto.id'))
	#db.relationship('DocumentsPhoto', uselist = False, backref = db.backref('courier'))
	lastSeen = db.Column(db.DateTime)
	courierTypeId = db.Column(db.Integer, db.ForeignKey('courierType.id'))

	def __init__(self, name = None, surname = None, patronymic = None, phoneNumber = None, photoUrl = None, \
		email = None, password = None, courierTypeId = None, personalInformationId = None, \
		documentsPhotoId = None, courierBalance = None):

		super(Courier, self).__init__(name = None, surname = None, patronymic = None, phoneNumber = None, \
		photoUrl = None, email = None, password = None, courierTypeId = None, personalInformationId = None, \
		documentsPhotoId = None, courierBalance = None)

		self.name = name
		self.surname = surname
		self.patronymic = patronymic
		self.phoneNumber = phoneNumber
		self.photoUrl = photoUrl
		self.email = email
		self.password = password
		self.courierTypeId = courierTypeId
		self.personalInformationId = personalInformationId
		self.documentsPhotoId = documentsPhotoId
		self.courierBalance = courierBalance

	def __repr__(self):
		return '<Id: {}. {} {} {}. Phone number: {}\n{}. \n\nPersonalInformation: {}\nDocumentsPhotoId:{}\nBalance: {}>'.format(self.id, \
			self.surname, self.name, self.patronymic, self.phoneNumber, self.email, self.personalInformationId, \
			self.documentsPhotoId, self.courierBalance)

#Класс модели типа заказа в базе данных
class OrderType(db.Model):
	__tablename__ = 'orderType'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140), unique = True)
	orders = db.relationship('Order', uselist = False, backref = db.backref('orderType'))

	def __init__(self, name = None):
		super(OrderType, self).__init__(name = None)
		self.name = name

	def __repr__(self):
		return '<Id: {}. Name: {}>'.format(self.id, self.name)

#Класс модели статуса заказа в базе данных
class OrderStatus(db.Model):
	__tablename__ = 'orderStatus'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140), unique = True)
	orders = db.relationship('Order', uselist = False, backref = db.backref('orderStatus'))

	def __init__(self, name = None):
		super(OrderStatus, self).__init__(name = None)
		self.name = name

	def __repr__(self):
		return '<Id: {}. Name: {}>'.format(self.id, self.name)

#Класс модели пункта выдачи в базе данных
class IssuePoint(db.Model):
	__tablename__ = 'issuePoint'
	id = db.Column(db.Integer, primary_key = True)
	orders = db.relationship('Order', backref = db.backref('issuePoint'))
	destinationTypeId = db.Column(db.Integer, db.ForeignKey('destinationType.id'))
	orderNumber = db.Column(db.String)
	humanFIO = db.Column(db.String)
	description = db.Column(db.String)
	phoneNumber = db.Column(db.String)
	address = db.Column(db.String)

	def __init__(self, destinationTypeId = None, orderNumber = None, humanFIO = None, \
			description = None, phoneNumber = None, address = None):
		super(IssuePoint, self).__init__(destinationTypeId = None, orderNumber = None, humanFIO = None, \
			description = None, phoneNumber = None, address = None)
		self.destinationTypeId = destinationTypeId
		self.orderNumber = orderNumber
		self.humanFIO = humanFIO
		self.description = description
		self.phoneNumber = phoneNumber
		self.address = address

	def __repr__(self):
		return '<Id: {}. Description: {}>'.format(self.id, self.description)

#Класс модели пунтка назначения в базе данных
class DestinationType(db.Model):
	__tablename__ = 'destinationType'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140), unique = True)
	issuePoint = db.relationship('IssuePoint', uselist = False, backref = db.backref('destinationType'))

	def __init__(self, name = None):
		super(DestinationType, self).__init__(name = None)
		self.name = name

	def __repr__(self):
		return '<Id: {}. Name: {}>'.format(self.id, self.name)

#Класс модели денежных операций в базе данных
class Operation(db.Model):
	__tablename__ = 'operation'
	id = db.Column(db.Integer, primary_key = True)
	operationTypeId = db.Column(db.Integer, db.ForeignKey('operationType.id'))
	operationStatusId = db.Column(db.Integer, db.ForeignKey('operationStatus.id'))
	courierId = db.Column(db.Integer, db.ForeignKey('courier.id'))
	date = db.Column(db.DateTime)
	orderId = db.Column(db.Integer, db.ForeignKey('order.id'))
	
	def __init__(self, operationTypeId = None, operationStatusId = None, courierId = None, orderId = None):
		super(Operation, self).__init__(operationTypeId = None, operationStatusId = None, courierId = None, \
			orderId = None)
		self.operationTypeId = operationTypeId
		self.operationStatusId = operationStatusId
		self.courierId = courierId
		self.orderId = orderId

	def __repr__(self):
		return '<Id: {}. Type- {}, Status- {}>'.format(self.id, self.operationTypeId, self.operationStatusId)

#Класс модели типа операций в базе данных
class OperationType(db.Model):
	__tablename__ = 'operationType'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140), unique = True)
	issuePoint = db.relationship('Operation', uselist = False, backref = db.backref('operationType'))

	def __init__(self, name = None):
		super(OperationType, self).__init__(name = None)
		self.name = name

	def __repr__(self):
		return '<Id: {}. Name: {}>'.format(self.id, self.name)	

#Класс модели статуса операций в базе данных
class OperationStatus(db.Model):
	__tablename__ = 'operationStatus'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140), unique = True)
	issuePoint = db.relationship('Operation', uselist = False, backref = db.backref('operationStatus'))

	def __init__(self, name = None):
		super(OperationStatus, self).__init__(name = None)
		self.name = name

	def __repr__(self):
		return '<Id: {}. Name: {}>'.format(self.id, self.name)	 

#Класс модели типа курьера в базе данных
class CourierType(db.Model):
	__tablename__ = 'courierType'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140), unique = True)
	courier = db.relationship('Courier', uselist = False, backref = db.backref('courierType'))

	def __init__(self, name = None):
		super(CourierType, self).__init__(name = None)
		self.name = name

	def __repr__(self):
		return '<Id: {}. Name: {}>'.format(self.id, self.name)

#Класс модели персональной информации в базе данных
class PersonalInformation(db.Model):
	__tablename__ = 'personalInformation'
	id = db.Column(db.Integer, primary_key = True)
	passportNumber = db.Column(db.String, unique = True)
	passportSeries = db.Column(db.String, unique = True)
	issuedByPasport = db.Column(db.String)
	dateOfIssueOfPasport = db.Column(db.String)
	dateOfBirth = db.Column(db.DateTime)
	placeOfRegistration = db.Column(db.String)
	SNILSNumber = db.Column(db.String, unique = True)
	INNNumber = db.Column(db.String, unique = True)
	actualAddressOfResidence = db.Column(db.String)
	#courierId = db.Column(db.Integer, db.ForeignKey('courier.id'))
	#managerId = db.Column(db.Integer, db.ForeignKey('manager.id'))

	courier = db.relationship('Courier', uselist = False, backref = db.backref('personalInformation'))
	manager = db.relationship('Manager', uselist = False, backref = db.backref('personalInformation'))

	def __init__(self, passportNumber = None, passportSeries = None, issuedByPasport = None, dateOfIssueOfPasport = None, \
		placeOfRegistration = None, SNILSNumber = None, INNNumber = None, actualAddressOfResidence = None):

		super(PersonalInformation, self).__init__(passportNumber = None, passportSeries = None, issuedByPasport = None, \
			dateOfIssueOfPasport = None, placeOfRegistration = None, SNILSNumber = None, INNNumber = None, \
			actualAddressOfResidence = None)

		self.passportNumber = passportNumber
		self.passportSeries = passportSeries
		self.issuedByPasport = issuedByPasport
		self.dateOfIssueOfPasport = dateOfIssueOfPasport
		self.placeOfRegistration = placeOfRegistration
		self.SNILSNumber = SNILSNumber
		self.INNNumber = INNNumber
		self.actualAddressOfResidence = actualAddressOfResidence

	def __repr__(self):
		return '<Id {}.\nPasport: Series-{}, Number-{}, dateOfIssueOfPasport-{}.>'.format(self.id, self.passportSeries,\
			self.passportNumber, self.dateOfIssueOfPasport)

#Класс модели фото документов в базе данных
class DocumentsPhoto(db.Model):
	__tablename__ = 'documentsPhoto'
	id = db.Column(db.Integer, primary_key = True)
	pasportMainPagePhotoURL = db.Column(db.String, unique = True)
	pasportRegistrationPagePhotoURL = db.Column(db.String, unique = True)
	SNILSPhotoURL = db.Column(db.String, unique = True)
	INNPhotoUrl = db.Column(db.String, unique = True)
	#courierId = db.Column(db.Integer, db.ForeignKey('courier.id'))
	#managerId = db.Column(db.Integer, db.ForeignKey('manager.id'))

	courier = db.relationship('Courier', uselist = False, backref = db.backref('documentsPhoto'))
	manager = db.relationship('Manager', uselist = False, backref = db.backref('documentsPhoto'))

	def __init__(self, pasportMainPagePhotoURL = None, pasportRegistrationPagePhotoURL = None, SNILSPhotoURL = None, INNPhotoUrl = None):

		super(DocumentsPhoto, self).__init__(pasportMainPagePhotoURL = None, pasportRegistrationPagePhotoURL = None, \
			SNILSPhotoURL = None, INNPhotoUrl = None)

		self.pasportMainPagePhotoURL = pasportMainPagePhotoURL
		self.pasportRegistrationPagePhotoURL = pasportRegistrationPagePhotoURL
		self.SNILSPhotoURL = SNILSPhotoURL
		self.INNPhotoUrl = INNPhotoUrl

	def __repr__(self):
		return '<Id {}.\nPhoto pasport: main-{}, \nregistration-{}>'.format(self.id, self.pasportMainPagePhotoURL,\
			self.pasportRegistrationPagePhotoURL)

#Класс модели менеджера в базе данных
class Manager(db.Model):
	__tablename__ = 'manager'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(140), unique = True)
	name = db.Column(db.String(140))
	surname = db.Column(db.String(140))
	patronymic = db.Column(db.String(140))
	password = db.Column(db.String(140))
	phoneNumber = db.Column(db.String(140))
	photoUrl = db.Column(db.String(140))
	personalInformationId = db.Column(db.Integer, db.ForeignKey('personalInformation.id'))
	documentsPhotoId = db.Column(db.Integer, db.ForeignKey('documentsPhoto.id'))
	lastSeen = db.Column(db.DateTime)

	def __init__(self, name = None, surname = None, patronymic = None, phoneNumber = None, photoUrl = None, email = None, password = None):
		super(Manager, self).__init__(name = None, surname = None, patronymic = None, phoneNumber = None, \
			photoUrl = None, email = None, password = None)
		self.name = name
		self.surname = surname
		self.patronymic = patronymic
		self.phoneNumber = phoneNumber
		self.photoUrl = photoUrl
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id) #python 2
		except NameError:
			return str(self.id) #python 3

	def __repr__(self):
		return '<Id: {}.\nManager\n{} {} {}. Phone number: {}\n{}>'.format(self.id, self.surname, self.name, self.patronymic, self.phoneNumber, self.email)
