from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import Required, EqualTo, Email
from clients.models import OrderType, OrderStatus


class CreateOrder(Form):
	typeId = SelectField('typeId', coerce = int)
	#clientId = TextField('clientId', [Required()])
	statusId = SelectField('statusId', coerce = int)
	numberOfAddresses = IntegerField('numberOfAddresses', [Required()])
	informationAboutAddresses = TextField('informationAboutAddresses', [Required()])
	#dateOfCreation = TextField('dateOfCreation', [Required()])
	description = TextField('description', )
	#photoUrl = TextField('photoUrl') 


	#dateOfCompletion = TextField('dateOfCompletion')
	cost = IntegerField('cost', [Required()])
		