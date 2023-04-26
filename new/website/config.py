import os
from flask_login import current_user
from collections import defaultdict
from country_list import countries_for_language

class Config:

    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI =   os.environ['SQLALCHEMY_DATABASE_URI']
    CATEGORY_PRODUCT = ['Home', 'Auto', 'Tec', 'Hobby','Game', 'Sport']
    UPLOAD_FOLDER = 'website/static/images' 
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    CRYPTO_CURRENCY = ['BTC', 'ETH', 'XMR']
    COUNTRIES = dict(countries_for_language('en'))
    EMAIL_PYTHON = os.environ['EMAIL_PYTHON']
    EMAIL_PYTHON_PASS = os.environ['EMAIL_PYTHON_PASS']
    EMAIL_INFOSITE = os.environ['EMAIL_INFOSITE']
    EMAIL_INFOSITE_PYTHON_PASS = os.environ['EMAIL_INFOSITE_PYTHON_PASS']
    MEET_LINK = 'https://meet.google.com/twf-hbge-fju'