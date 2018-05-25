from flask import render_template, Blueprint, request, flash, session, redirect, g, json, url_for
from flask_json import JsonError, json_response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import check_password_hash, generate_password_hash

from app_kkp import app, db, lm, json_kkp

from clients.models import Manager, PersonalInformation, DocumentsPhoto

from datetime import datetime



managers_blu = Blueprint('managers', __name__, url_prefix = '/managers')


@lm.user_loader
def load_manager(id):
	return Manager.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.lastSeen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@managers_blu.route('/')
def getManagers():
	managers = Manager.query.order_by(Manager.id).all()
	ids = []

	for manager in managers:
		ids.append(manager.id)

	return json_response(managerId = ids)

@managers_blu.route('/singUpManager', methods = ['GET', 'POST'])
def singUpManager():
	data = request.get_json(force = True)

	try:
		manager = Manager(name = data['name'], surname = data['surname'], \
			patronymic = data['patronymic'], phoneNumber = data['phoneNumber'],\
			photoUrl = data['photoUrl'], email = data['email'], \
			password = generate_password_hash(data['password']))

		db.session.add(manager)
		db.session.commit()

		session['remember_me'] = True
	except:
		raise JsonError(description = 'Error register')
	return json_response(response = 'success')

@managers_blu.route('/login', methods = ['GET', 'POST'])
def loginManager():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('managers.getManagers'))

	data = request.get_json(force = True)

	try:
		manager = Manager.query.filter(Manager.email  ==  data['email']).first()

		if manager and check_password_hash(manager.password, data['password']):
			#session['remember_me'] = data['remember_me']

			remember_me = False
			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None)

			login_user(manager, remember = remember_me)
	except:
		raise JsonError(description = 'Error sing in')
	return json_response(response = 'success')

@managers_blu.route('/logout', methods = ['GET', 'POST'])
def logOutManager():
	logout_user()
	return redirect(url_for('managers.getManagers'))

@managers_blu.route('/<int:id>/profile')
@login_required
def getManager(id):
	manager = Manager.query.filter(Manager.id  ==  id).first()

	return json_response(managerId = manager.id, managerEmail = manager.email, managerName = manager.name, \
		managerSurname = manager.surname, managerPatronymic = manager.patronymic, managerPhoneNumber = manager.phoneNumber)

@managers_blu.route('/<int:id>/profile/edit', methods = ['GET', 'POST'])
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
	return redirect(url_for('managers.getManager', id = g.user.id))
	
@managers_blu.route('/<int:id>/profile/editPhoto', methods = ['GET', 'POST'])
def editProfilePhoto(id):
	pass