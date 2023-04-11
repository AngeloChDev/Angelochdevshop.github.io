from flask import render_template, request, Blueprint, redirect, current_app, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import Product, User, Bio, Contact, Order
import io 
import base64
from PIL import Image
import os
from collections import defaultdict

main = Blueprint('main', __name__)
tot =[]

shopping_list = []
list_order = []
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
   products_list = Product.query.filter_by(seller=current_user).order_by(Product.date_posted.desc())
   result = defaultdict(lambda: {'product': int(), 'quantity': 0, })
   o=[]
   try:
      if session['CART']:
         for i in session['CART']:
            key = '{}'.format(i["product"])
            result[key]["product"] = i["product"]
            result[key]["quantity"] += i["quantity"]
            orders= list(result.values())

      if len(orders)>0:
         for i in orders:
            d = i['product']
            product = Product.query.filter_by(id=d).first()
            obj= {'product':product,'quantity':i['quantity'], 'file':None}
            o.append(obj)
   except:
      flash('Some error was wrong, try to relog in to the account', category='error')
      redirect(url_for('shopPage.shop'))
   finally:
      cart = []
      if request.method == 'POST':
         ord_id = request.form.getlist('order_id')
         ord_qnt = request.form.get('order_qnt')
         ord_address = request.form.get('order_address')
         ord_email = request.form.get('order_email_field')
         ord_tel = request.form.get('order_tel')
         ord_pin = request.form.get('order_pin')
         ord_wallet = request.form.get('order_wallet')
         
         for i in ord_id:
            selected = Product.query.filter_by(id=int(i)).first()
            
            if selected.require_file:
               myfile = request.files[f'file-{i}']
               name = myfile.filename
               user_folder =  current_app.config["UPLOAD_FOLDER"] + '/' + str(current_user.id) + '/'+ 'orders_file' +'/'
               path = os.path.join(user_folder, name )
               if not name:
                  flash('For this product are required some file media', category="error")
                  break
               myfile.save(path)
               order = Order(product_id=selected.id, user_id=current_user.id,address=ord_address, email=ord_email,tel=ord_tel,pin=ord_pin,wallet=ord_wallet,quantity=ord_qnt, files=name)
            else:
               order = Order(product_id=selected.id, user_id=current_user.id,address=ord_address, email=ord_email,tel=ord_tel,pin=ord_pin,wallet=ord_wallet,quantity=ord_qnt)
            db.session.add(order)  
            db.session.commit()
         session['CART'] = []
         o = []
         orders = []
         flash('register', category='success')
      
      return render_template('home.html',user=current_user,user_products=products_list,ord=o)

   return render_template('home.html', user=current_user, user_products=products_list)

@main.route("/seller/<seller_id>", methods=['GET', 'POST'])
@login_required
def seller_view(seller_id):

   seller = User.query.filter_by(id=seller_id).first()
   products_seller = Product.query.filter_by(seller=seller).order_by(Product.date_posted.desc())
   bio = Bio.query.filter_by(author=seller).first()
   contact_seller = Contact.query.filter_by(user_contact=seller).first()
   if request.method == 'POST':
      if 'buyNowSellerView' in request.form:
         qnt = request.form.get('qnt')
         code = request.form.get('code')

         if not qnt:
            flash('No product selected', category="error")
         else:
            selected = {'product': int(code), 'quantity': int(qnt)}
            session['CART'].append(selected)
            flash('Product added to cart', category="success")
         return redirect(url_for('main.home'))
            
            
   return render_template('seller_view.html', user=current_user, seller=seller, seller_prod=products_seller, bio=bio,contact=contact_seller)

@main.route("/product/<id>", methods=['GET', 'POST'])
@login_required
def product_view(id):
   product = Product.query.filter_by(id=id).first()
   seller = product.seller
   if request.method == 'POST':
      if 'form_name' in request.form :
         name = request.form.get('input_fieldName')
         if name:
            product.name = name
            db.session.commit()
            flash('Product name changed', category="success")
         else:
            flash('Error, product name can not be empty', category='error')
      elif 'form_description' in request.form :
         description = request.form.get('input_fieldDescription')
         if description:
            product.description = description
            db.session.commit()
            flash('Product description changed', category="success")
         else:
            flash('Error, product description is empty', category='error')
      elif 'form_price' in request.form :
         price = request.form.get('input_fieldPrice')
         if price:
            product.price = price
            db.session.commit()
            flash('Product price changed', category="success")
         else:
            flash('Error, product price can not be empty', category='error')
      elif 'buyNowSellerView' in request.form:
         qnt = request.form.get('p_qnt')
         code = request.form.get('p_code')

         if not qnt:
            flash('No product selected', category="error")
         else:
            selected = {'product': int(code), 'quantity': int(qnt)}
            session['CART'].append(selected)
            flash('Product added to cart', category="success")
      else:
         redirect(404)
   return render_template('product_view.html', user=current_user, prod = product, seller=seller)

@main.route("/product/<id>/delete", methods=['GET','POST'])
@login_required
def product_delete(id):
   Product.query.filter_by(id=id).delete()
   db.session.commit()
   
   return redirect(url_for('main.home'))


