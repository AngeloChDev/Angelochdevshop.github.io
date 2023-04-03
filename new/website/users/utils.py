from flask import render_template, url_for, session, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from website import db, bcrypt
from website.models import User, Product
from flask import current_app
from werkzeug.utils import secure_filename
import os

utils = Blueprint('utils', __name__)



@utils.route('/createProducts', methods=['GET', 'POST'])
@login_required
def product():
    
    CATEGORY = current_app.config["CATEGORY_PRODUCT"]
    user = current_user
    if request.method == 'POST':
        name = request.form.get('product_name')
        description = request.form.get('product_description')
        price = request.form.get('product_price')
        category = request.form.get('product_category')
        photo = request.files['product_photo']
        mimetype = photo.mimetype
        photo_name = secure_filename(current_user.username + photo.filename)
        path = os.path.join( current_app.config["UPLOAD_FOLDER"], photo_name )
        photo.save(path)

        if not description or len(description) < 60:
            flash('Description required min 60 charatters', category='error')
        elif 3 > len(name) > 30:
            flash('Product name required min 3 and max 30 charatters', category='error')
        elif not price:
            flash('Product price required!', category='error')
        else:
            product = Product(name=name, description=description, price=price, photo=photo_name, photo_file= photo.read(), photo_mimetype=mimetype, category=category,user_id=current_user.id)
            
            db.session.add(product)
            db.session.commit()
        


    return  render_template('createProduct.html', user=current_user, product_category=CATEGORY)


