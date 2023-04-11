from flask import render_template, url_for, session, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from website import db, bcrypt
from website.models import User
from country_list import countries_for_language
import os

countries = dict(countries_for_language('en'))
 
users = Blueprint('users', __name__)

@users.route("/signin", methods=['GET', 'POST'])
def signin():
    country_list = countries
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        newuser = request.form.get('username_field')
        password = request.form.get('password_field')
        password_auth = request.form.get('password_auth')
        country_name = request.form.get('country')
        user_exist = User.query.filter_by(username=newuser).first()
        if user_exist:
            flash('Username already exists.', category='error')
        elif len(newuser) < 3:
            flash('Username must be greater than 3 character.', category='error')
        elif password != password_auth:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 3:
            flash('Password must be at least 3 characters.', category='error')
        else:
            
            user = User(username=newuser, country=country_name, photo_user='')
            user.set_password(password_auth)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            session['user_id'] = user.id
            session['CART'] = []
            
            folder = os.path.join( current_app.config["UPLOAD_FOLDER"], str(user.id))
            p_folder = folder + '/products_photo/'
            o_folder = folder + '/orders_file/'
            os.makedirs(folder)
            os.makedirs(p_folder)
            os.makedirs(o_folder)
            login_user(user)
            return redirect(url_for('main.home'))
        
    return render_template('signin.html', user=current_user , countries = country_list)

@users.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        name = request.form.get('username_log_field')
        password = request.form.get('password_log_field')
        user = User.query.filter_by(username=name).first()
            
        if user:
            
            if check_password_hash(user.password_hash, password):
                flash('Logged in successfully!', category='success')
                session['user_id'] = user.id
                session['CART'] = []
                login_user(user)
                
                return redirect(url_for('main.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Incorrect username, try again.', category='error')

    return render_template("login.html",  user=current_user)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

