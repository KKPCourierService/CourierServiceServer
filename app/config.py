import os 

class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test_user:beta@localhost/test'
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'Database/migrate')
    
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'