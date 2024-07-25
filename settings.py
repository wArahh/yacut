import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


BASE_URL = os.getenv('BASE_URL', 'http://localhost/')
ACCEPTED_SYMBOLS = string.ascii_letters + string.digits