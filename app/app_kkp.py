import sys 
sys.dont_write_bytecode = True 

from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_json import FlaskJSON

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager



app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = 'clients.loginClient'

json_kkp = FlaskJSON(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)