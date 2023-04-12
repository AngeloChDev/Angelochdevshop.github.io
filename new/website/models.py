from datetime import datetime
from flask_login import UserMixin
from . import db
from sqlalchemy import JSON


from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    country = db.Column(db.String(30), nullable= True)
    products = db.relationship('Product', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy= True)
    bio = db.relationship('Bio', backref='author', lazy=True)
    contact = db.relationship('Contact', backref='user_contact', lazy=True)
    photo_user =db.Column(JSON)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    obj_seller = db.Column(db.Integer,  nullable= False)
    address = db.Column(db.String(100),nullable=True)
    email = db.Column(db.String(50),nullable=True)
    tel = db.Column(db.String(30), nullable=True)
    pin = db.Column(db.String(20),nullable=False)
    wallet = db.Column(db.String(80), nullable=False)
    files = db.Column(db.String,nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=True)
    name = db.Column(db.String(20),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(JSON, nullable=True)
    category = db.Column(db.String(20), nullable = False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    require_file = db.Column(db.Boolean(), nullable=False, default=False)
    order_id = db.relationship('Order', backref='product', lazy=True)
    

class Bio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    email = db.Column(db.String, nullable=True)
    number = db.Column(db.String, nullable=True)
    wallet = db.Column(JSON, nullable=True)
    social_link = db.Column(db.String, nullable=True)
    social_name = db.Column(db.String, nullable=True)
    social2_link = db.Column(db.String, nullable=True)
    social2_name = db.Column(db.String, nullable=True)