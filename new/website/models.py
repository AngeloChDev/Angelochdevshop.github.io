from datetime import datetime
from flask_login import UserMixin
from . import db

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    country = db.Column(db.String(30), nullable= True)
    products = db.relationship('Product', backref='seller', lazy=True)
    orders = db.relationship('Order', lazy= True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(20),unique=True,nullable=False)
    detail = db.Column(db.String(10),nullable=False)
    contact = db.Column(db.String(30))
    wallet = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(20),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(50))
    photo_file = db.Column(db.LargeBinary)
    photo_mimetype = db.Column(db.String)
    category = db.Column(db.String(20), nullable = False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
