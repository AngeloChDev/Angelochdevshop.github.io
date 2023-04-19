import os
from flask_login import current_user
from collections import defaultdict

class Config:

    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI =   os.environ['SQLALCHEMY_DATABASE_URI']
    CATEGORY_PRODUCT = ['home', 'auto', 'tec', 'hobby','fiori']
    UPLOAD_FOLDER = 'website/static/images' 
    ALLOWED_EXTENSIONS = [ 'png', 'jpg', 'jpeg']
    DEFAULT_ORD = {'order_id':'',
        'quantity':0,
        'buyer':0,
        'product': {
            'product_id':'',
            'product_name': '',
            'product_price':0,
            'product_require_file':''
            },
        'seller':{'seller_id':0,
            'seller_username':'',
            'seller_wallet':''
            }
        }
