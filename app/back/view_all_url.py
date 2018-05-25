'''@app.route('/clients')
def clients_get():
	return render_template('clients.html')

@app.route('/clients/registrationNewClient')
def clients_registrationNewClient():
	pass

@app.route('/clients/<IdClient>/login')
def clients_login(IdClient):
	pass

@app.route('/clients/<IdClient>/logOut')
def clients_logOut(IdClient):
	pass

@app.route('/clients/<IdClient>/profile')
def clients_profile(IdClient):
	pass

@app.route('/clients/<IdClient>/profile/edit')
def clients_profile_edit(IdClient):
	pass

@app.route('/clients/<IdClient>/profile/editPhoto')
def clients_profile_editPhoto(IdClient):
	pass

@app.route('/clients/<IdClient>/orders')
def clients_orders(IdClient):
	pass

@app.route('/clients/<IdClient>/orders/create')
def clients_orders_create(IdClient):
	pass

@app.route('/couriers')
def couriers_get():
	return render_template('couriers.html')

@app.route('/couriers/registrationNewCouriers')
def couriers_registrationNewCouriers():
	pass

@app.route('/couriers/<IdCourier>/login')
def couriers_login(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/logOut')
def couriers_logOut(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/profile')
def couriers_profile(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/profile/edit')
def couriers_profile_edit(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/profile/editPhoto')
def couriers_profile_editPhoto(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/orders')
def couriers_orders(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/orders/create')
def couriers_orders_create(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/orders/add')
def couriers_orders_add(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/orders/<IdOrder>/editStatus')
def couriers_orders_editStatus(IdCourier, IdOrder):
	pass

@app.route('/couriers/<IdCourier>/operations')
def couriers_operations(IdCourier):
	pass

@app.route('/couriers/<IdCourier>/operations/withdrawalOfFunds')
def couriers_operations_withdrawalOfFunds(IdCourier):
	pass

@app.route('/managers')
def managers_get():
	return render_template('managers.html')

@app.route('/managers/<IdManager>/registrationNewManager')
def managers_registrationNewManager(IdManager):
	pass

@app.route('/managers/<IdManager>/login')
def managers_login(IdManager):
	pass

@app.route('/managers/<IdManager>/logOut')
def managers_logOut(IdManager):
	pass

@app.route('/managers/<IdManager>/profile')
def managers_profile(IdManager):
	pass

@app.route('/managers/<IdManager>/profile/edit')
def managers_profile_edit(IdManager):
	pass

@app.route('/orders')
def orders():
	return render_template('orders.html')

@app.route('/orders/free')
def orders_free():
	pass

@app.route('/operations/<IdOperation>')
def operations(IdOperation):
	pass'''