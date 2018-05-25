#!flask/bin/python
from app_kkp import db
from clients import models


db.create_all()
