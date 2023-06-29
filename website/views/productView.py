from flask import render_template, request, Blueprint, redirect, current_app, url_for, flash, session, jsonify, make_response
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import Product, User, Bio, Contact, Order

productView = Blueprint('productView', __name__)

@productView.route("/product/<id>", methods=['GET', 'POST'])
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
            selected = {'product': code, 'quantity': int(qnt)}
            session['CART'].append(selected)
            flash('Product added to cart', category="success")
      else:
         redirect(404)
   return render_template('product_view.html', user=current_user, prod = product, seller=seller)
  