import sys 
sys.dont_write_bytecode = True 

from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_json import FlaskJSON

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


#Объявление переменной для запуска сервера
app = Flask(__name__)
app.config.from_object(Configuration)

#Объявление переменной базы данных
db = SQLAlchemy(app)

#Объявление переменной для работы с аунтификацией
lm = LoginManager(app)
lm.login_view = 'clients.loginClient'

json_kkp = FlaskJSON(app)


#Объявление переменной миграции для переноса данных из старой версии базы в новую
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)