from flask import render_template, url_for, session, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from website import db, bcrypt
from website.models import User, Product, Bio, Contact, Order
from flask import current_app
from werkzeug.utils import secure_filename
import os
import random
from bitcoinlib.wallets import Wallet
import bitcoin 
from email.message import EmailMessage
import ssl
import smtplib
import time


utils = Blueprint('utils', __name__)

@utils.route('/createProducts', methods=['GET', 'POST'])
@login_required
def product():
    check = False
    CATEGORY = current_app.config["CATEGORY_PRODUCT"]
    try:
        c = Contact.query.filter_by(user_id=current_user.id).first()

        if not current_user.authenticated and c:
            flash('Authenticate user and Register a wallet are required', category='success')
        else:
            pass
    except:
        pass
    finally:
        if request.method == 'POST':
            name = request.form.get('product_name')
            description = request.form.get('product_description')
            price = request.form.get('product_price')
            category = request.form.get('product_category')
            photo = request.files.getlist('product_photo')
            required = request.form.get('required_file')
            prod_pin = ''.join(random.choice(
                    'qwertzuiopasdfghjklyxcvbnm1234567890') for i in range(30))
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
                product = Product(name=name,id=prod_pin, description=description, price=price, photo=p, category=category,user_id=current_user.id,require_file=check)
                db.session.add(product)
                db.session.commit()
                flash('Product created successfully', category="success")
        
    
    return  render_template('createProduct.html', user=current_user, product_category=CATEGORY)

@utils.route('/WriteYourBio', methods=['GET', 'POST'])
@login_required
def bio():
    try:
        Bio_user = Bio.query.filter_by(author=current_user).first()
    except:
        flash('Some error was wrong saving your bio',category="error")
        redirect(404)
    finally:
        if request.method == 'POST':
            bio = request.form.get('bio_in')
            if not bio:
                flash('Text field empty', category='error')
            elif Bio_user:
                Bio_user.bio = bio
                flash('New bio added', category='success')
            else:    
                user_bio = Bio(user_id=current_user.id, bio=bio)
                db.session.add(user_bio)
                db.session.commit()
                flash('Bio Added', category='success')
            return redirect(url_for('main.home'))

    return render_template('bio.html', user=current_user)

@utils.route('/AddContact', methods=['GET', 'POST'])
@login_required
def contact():
    try:
        user_contact = Contact.query.filter_by(user_id=current_user.id).first()
        if user_contact:
            flash('You already have added some contact mode, if you insert some data only that will be update', category= 'success')
    except:
        flash('Some error was wrong adding new contact mode', category="error")
        redirect(404)
    finally:
        if request.method == 'POST':
            email = request.form.get('email')
            number = request.form.get('number')
            s_link = request.form.get('social')
            s_name = request.form.get('social_name')
            s2_link = request.form.get('social2')
            s2_name = request.form.get('social2_name')
            
            if user_contact:
                if email:
                    user_contact.email=email
                if number:
                    user_contact.number=number
                if s_name:
                    user_contact.social_name=s_name
                    user_contact.social_link=s_link
                if s2_name:
                    user_contact.social2_name=s2_name
                    user_contact.social2_link=s2_link
                db.session.commit()
            else:
                c = Contact(user_id=current_user.id,email=email,number=number,social_name=s_name,social_link=s_link, social2_name=s2_name,social2_link=s2_link)
                db.session.add(c)
                db.session.commit()
            flash('New contact mode added', category="success")
            return redirect(url_for('main.home'))
    return render_template('contact.html', user= current_user)

@utils.route('/AddPhotoUser', methods=['GET', 'POST'])
@login_required
def photo_user():
    try:
        if request.method == 'POST':
            
            photo = request.files['photo_user']
            photo_name = secure_filename(str(current_user.id) + photo.filename)
            folder =  current_app.config["UPLOAD_FOLDER"] + '/' + str(current_user.id) + '/'
            path = os.path.join(folder, photo_name )
            
            photo.save(path)
            current_user.photo_user = photo_name
            db.session.commit()
            flash('Photo user added successfully', category="success")
            return redirect(url_for('main.home'))
    except:
        flash('Some error was wrong uploading this file', category="error")
        redirect(url_for('main.home'))


    return render_template('photo_user.html', user= current_user)


@utils.route('/getWallet', methods=['GET', 'POST'])
@login_required
def getWallet():
    
    currency_list = current_app.config['CRYPTO_CURRENCY']
    try:
        c = Contact.query.filter_by(user_id = current_user.id).first()

        if c.wallet:
            flash('wallet already exist ', category="error")
        else:
            pass
    except:
        pass
    finally:
        if request.method == 'POST':
            if 'submitWallet' in request.form:
                currency_selected = request.form['currency_selector']
                return 'done'
            elif 'addOldWallet' in request.form:
                wallet_addr = request.form.get('wallet_field')
                currency = request.form.get('currency_field')

                wallet = {'wallet_addr':wallet_addr, 'currency':currency}
                c = Contact.query.filter_by(user_id = current_user.id).first()
                if c:
                    if c.wallet:
                        email_sender = current_app.config['EMAIL_PYTHON']
                        password = current_app.config['EMAIL_PYTHON_PASS']
                        email_reciver = current_app.config['EMAIL_INFOSITE']
                        subject = 'Change Wallet Request'
                        body = f'The user with id {current_user.id} want to cange him wallet address with the new {str(wallet)}'

                        em = EmailMessage()
                        em['From'] = email_sender
                        em['To'] = email_reciver
                        em['Subject'] = subject
                        em.set_content(body)
                        context = ssl.create_default_context()

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                            smtp.login(email_sender, password)
                            smtp.sendmail(email_sender, email_reciver, em.as_string())
                else:
                    contact = Contact(user_id=current_user.id,wallet=wallet)
                
                    db.session.add(contact)
                    db.session.commit()
                    flash('ok',category="success")
                    return redirect(url_for('main.home'))
            else: 
                flash('some error', category="error")
    return render_template('getWallet.html', user = current_user, currency=currency_list, c=c)


auth_pin = ''.join(random.choice('1234567890') for i in range(5))
@utils.route('/Authenticate', methods=['GET', 'POST'])
@login_required
def authenticate():
    global auth_pin
    if request.method == 'POST':
        user_email = request.form.get('authenticate_email')
        email_sender = current_app.config['EMAIL_INFOSITE']
        password = current_app.config['EMAIL_INFOSITE_PYTHON_PASS']
    
        if 'submit_authenticate_email' in request.form:
           
            subject = 'Authenticate User Code'
            body = f'Your security code is :{auth_pin}'

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = user_email
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, password)
                smtp.sendmail(email_sender, user_email, em.as_string())

            time.sleep(80) 
            pass

        elif 'submit_authenticate_code' in request.form:
            code = request.form['authenticate_code']

            if auth_pin == code: 
                link = current_app.config['MEET_LINK']
                flash('Security sistem passed successfully', category="success")
                subject = 'Authenticate user video-call link'
                body = f'Your link for partecipate at the video-call :{link}'

                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = user_email
                em['Subject'] = subject
                em.set_content(body)
                context = ssl.create_default_context()
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, password)
                    smtp.sendmail(email_sender, user_email, em.as_string())

            else:
                flash('Codes doesn t match', category="error")
        else:
            pass
    return render_template('authenticate.html', user = current_user)