from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import Required, EqualTo, Email

#В данном файле представлены классы для форм регистрации,
#авторизации, изменения клиента и создания заказов
#В данной версии сервера, данный функционал не используетсяы

class LoginForm(Form):
	email = TextField('email', [Required(), Email()])
	password = PasswordField('password', [Required()])
	remember_me = BooleanField('remember_me', default = False)

class RegisterClientForm(Form):
	email = TextField('email', [Required(), Email()])
	name = TextField('name', [Required()])
	surname = TextField('surname', [Required()])
	patronymic = TextField('patronymic', [Required()])
	phoneNumber = TextField('phoneNumber', [Required()])
	#photoUrl = TextField('photoUrl', [Required()])

	password = PasswordField('password', [Required()])
	confirm = PasswordField('repeatPassword', [
		Required(),
		EqualTo('password', message='Passwords must match')])

class EditClientForm(Form):
	name = TextField('name', [Required()])
	surname = TextField('surname', [Required()])
	patronymic = TextField('patronymic', [Required()])
	phoneNumber = TextField('phoneNumber', [Required()])
	#photoUrl = TextField('photoUrl', [Required()])

	#password = PasswordField('password', [Required()])

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