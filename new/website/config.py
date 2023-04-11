import os
from flask_login import current_user

class Config:

    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI =   os.environ['SQLALCHEMY_DATABASE_URI']
    CATEGORY_PRODUCT = ['home', 'auto', 'tec', 'hobby','fiori']
    UPLOAD_FOLDER = 'website/static/images' 
    ALLOWED_EXTENSIONS = [ 'png', 'jpg', 'jpeg']

