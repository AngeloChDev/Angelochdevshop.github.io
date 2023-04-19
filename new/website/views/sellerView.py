from flask import render_template, request, Blueprint, redirect, current_app, url_for, flash, session, jsonify, make_response
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.models import Product, User, Bio, Contact, Order

sellerView = Blueprint('sellerView', __name__)

@sellerView.route("/seller/<seller_name>", methods=['GET', 'POST'])
@login_required
def seller_view(seller_name):

   seller = User.query.filter_by(username=seller_name).first()
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
            selected = {'product': code, 'quantity': int(qnt)}
            session['CART'].append(selected)
            flash('Product added to cart', category="success")
         return redirect(url_for('main.home'))
            
            
   return render_template('seller_view.html', user=current_user, seller=seller, seller_prod=products_seller, bio=bio,contact=contact_seller)
  