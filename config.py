import os 

#Класс конфигурации
#В нем объявляем режим работы, строку подключения к базе данных и другие функции
class Configuration(object):
    # basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    	'postgresql+psycopg2://test_user:beta@https://kkpcourier.herokuapp.com/test'
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'Database/migrate')
    
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'