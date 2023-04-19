from flask import render_template, request, Blueprint, redirect, current_app, url_for, flash, session, jsonify, make_response
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import Product, User, Bio, Contact, Order

homeInfo = Blueprint('homeInfo', __name__)

@homeInfo.route('/home/selled', methods=['GET', 'POST'])
@login_required
def infoSelled():
   selled = Order.query.filter_by(seller_id=current_user.id).all()

   return render_template('infoSelled.html', user=current_user,cart=session['BOX'],selled=selled)



@homeInfo.route('/home/buyed', methods=['GET', 'POST'])
@login_required
def infoBuyed():

   buyed = Order.query.filter_by(user_id=current_user.id).all()
   
   return render_template('infoBuyed.html', user=current_user,buyed=buyed,cart=session['BOX'])


@homeInfo.route('/home/product', methods=['GET', 'POST'])
@login_required
def infoProduct():
   
   product = Product.query.filter_by(user_id=current_user.id).all()
   return render_template('infoProduct.html', user=current_user,user_products=product,cart=session['BOX'])