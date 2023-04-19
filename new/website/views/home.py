from flask import render_template, request, Blueprint, redirect, current_app, url_for, flash, session, jsonify, make_response
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import Product, User, Bio, Contact, Order
import io 
import base64
from PIL import Image
import os
from collections import defaultdict
import json
import simplejson
import requests
import time
import random


main = Blueprint('main', __name__)
                                                         ### HOME PAGE
##########################################################################################

@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
   try:
      products_list = Product.query.filter_by(user_id=current_user.id).all()
      buyed = Order.query.filter_by(user_id=current_user.id).all()
      selled = Order.query.filter_by(seller_id=current_user.id).all()
      result = defaultdict(lambda: {'product': '', 'quantity': 0, })
      sum_ord = []
     
     
      if len(session['CART']) > 0:
         for i in session['CART']:
            
            key = '{}'.format(i["product"])
            result[key]["product"] = i["product"]
            result[key]["quantity"] += i["quantity"]
            sum_ord = list(result.values())
      else:
         print('session cart empty')
      cart = []
      if len(sum_ord) > 0:
         for o in sum_ord:
            product = Product.query.filter_by(id=o["product"]).first()
            s = product.seller
            
            cart.append({
               'order_id': ''.join(random.choice('qwertzuiopasdfghjklyxcvbnm1234567890') for i in range(30)),
               'quantity':o['quantity'],
               'buyer':current_user.id,
               'product': {
                  'product_id':product.id,
                  'product_name':product.name,
                  'product_price':product.price,
                  'product_require_file':product.require_file
                  },
               'seller':{
                  'seller_id':s.id,
                  'seller_username':s.username,
                  #'seller_wallet':s.contact.wallet 
                  }
               }
            )
            
         else:
            print('Some error wrong loading product data')
      else:
         print('Cart empty')
      session['BOX'] = cart
   except:
      pass
   finally:

      if request.method == 'POST':
         ord_address = request.form.get('order_address')
         ord_email = request.form.get('order_email_field')
         ord_tel = request.form.get('order_tel')
         ord_pin = request.form.get('order_pin')
         ord_wallet = request.form.get('order_wallet')
         
         for i in session['BOX']:
            p_id = i['product']['product_id']
            s = i['seller']['seller_id']
            if i['product']['product_require_file']:
               myfile = request.files[f'file-{p_id}']
               name = myfile.filename
               user_folder =  current_app.config["UPLOAD_FOLDER"] + '/' + str(current_user.id) + '/'+ 'orders_file' +'/'
               path = os.path.join(user_folder, name )
               if not name:
                  flash('For this product are required some file media', category="error")
                  break
               myfile.save(path)
               order = Order(product_id=p_id, pin=i['order_id'], user_id=current_user.id,seller_id=s,address=ord_address, email=ord_email,tel=ord_tel,wallet=ord_wallet,quantity=i['quantity'], files=name)
            else:
               order = Order(product_id=p_id, pin=i['order_id'], user_id=current_user.id,seller_id=s,address=ord_address, email=ord_email,tel=ord_tel,wallet=ord_wallet,quantity=i['quantity'])
            db.session.add(order)  
            db.session.commit()
         session['CART'] = []
         session['BOX'] = []
         cart = []

         flash('Order registered successfully', category='success')

         
   return render_template('home.html',user=current_user,user_products=products_list,cart=session['BOX'],buyed=buyed)
                                                    ####### PRODUCT DELETE
############################################################################
@main.route("/product/<p_id>/delete", methods=['GET','POST'])
@login_required
def product_delete(p_id):
   if request.method == 'GET':
      
      prodeuct_to_delete = Product.query.filter_by(id=p_id).first()
      
      prodeuct_to_delete.DELETED = 1
      db.session.commit()
      flash('Product deleted', category="success")
   else:
      flash('some error wrong deleted this product', category="error")
   
   return redirect(url_for('main.home'))
                                                      ##### SELLED
#######################################################################
