from flask import render_template, url_for, session, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from website import db, bcrypt
from website.models import User, Product, Bio, Contact
from flask import current_app
from werkzeug.utils import secure_filename
import os

utils = Blueprint('utils', __name__)

wallet_list = []

@utils.route('/createProducts', methods=['GET', 'POST'])
@login_required
def product():
    check = False
    CATEGORY = current_app.config["CATEGORY_PRODUCT"]
    
    if request.method == 'POST':
        name = request.form.get('product_name')
        description = request.form.get('product_description')
        price = request.form.get('product_price')
        category = request.form.get('product_category')
        photo = request.files.getlist('product_photo')
        required = request.form.get('required_file')
        if 'required_file' in request.form:
            check = True
        else:
            check = False
        p=[]

        for i in photo:
            photo_name = secure_filename(str(current_user.id) +'product'+ i.filename)
            folder =  current_app.config["UPLOAD_FOLDER"] + '/' + str(current_user.id) + '/products_photo/'
            path = os.path.join(folder, photo_name )
            p.append(photo_name)
            i.save(path)

        if not description or len(description) < 2:
            flash('Description required min 60 charatters', category='error')
        elif not name or len(name) > 30:
            flash('Product name required min 3 and max 30 charatters', category='error')
        elif not price:
            flash('Product price required!', category='error')
        else:
            product = Product(name=name, description=description, price=price, photo=p, category=category,user_id=current_user.id,require_file=check)
            db.session.add(product)
            db.session.commit()
    
    return  render_template('createProduct.html', user=current_user, product_category=CATEGORY)

@utils.route('/WriteYourBio', methods=['GET', 'POST'])
@login_required
def bio():
    Bio_user = Bio.query.filter_by(author=current_user).first()
    if request.method == 'POST':
        bio = request.form.get('bio_in')
        if not bio:
            flash('text field empty', category='error')
        elif Bio_user:
            Bio_user.bio = bio
            return redirect(url_for('main.home'), 202)
        else:    
            user_bio = Bio(user_id=current_user.id, bio=bio)
            db.session.add(user_bio)
            db.session.commit()
            return redirect(url_for('main.home'), 202)

    return render_template('bio.html', user=current_user)

@utils.route('/AddContact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        wallet = request.form.get('wallet_field')
        s_link = request.form.get('social')
        s_name = request.form.get('social_name')
        s2_link = request.form.get('social2')
        s2_name = request.form.get('social2_name')
        wallet_list.append(wallet)
        user_contact = Contact(user_id=current_user.id, email=email,number=number,wallet=wallet_list,social_name=s_name,social_link=s_link, social2_name=s2_name,social2_link=s2_link)
        db.session.add(user_contact)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('contact.html', user= current_user)

@utils.route('/AddPhotoUser', methods=['GET', 'POST'])
@login_required
def photo_user():
    if request.method == 'POST':
        
        photo = request.files['photo_user']
        photo_name = secure_filename(str(current_user.id) + photo.filename)
        folder =  current_app.config["UPLOAD_FOLDER"] + '/' + str(current_user.id) + '/'
        path = os.path.join(folder, photo_name )
        
        photo.save(path)
        current_user.photo_user = photo_name
        db.session.commit()

    return render_template('photo_user.html', user= current_user)

