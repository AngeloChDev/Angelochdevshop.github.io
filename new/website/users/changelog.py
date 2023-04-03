from flask import render_template, url_for, session, flash, redirect, request, Blueprint
from flask_login import  current_user, login_required
from website import db, bcrypt
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash

change_log = Blueprint('change_log', __name__)

@change_log.route('/changelog', methods=['GET', 'POST'])
@login_required
def changelog():

    user = current_user
    if request.method == 'POST':
        cng_name = request.form.get('cng_name_field')
        cng_pswd1 = request.form.get('cng_pswd1_field')
        cng_pswd2 = request.form.get('cng_pswd2_field')
        old_pswd = request.form.get('old_pswd_field')
        
        
        user_exist = User.query.filter_by(username=cng_name).first()
        if user_exist:
            flash('Username already exists.', category='error')
        elif len(cng_name) < 3:
            flash('Username must be greater than 3 character.', category='error')
        elif cng_pswd1 != cng_pswd2:
            flash('Passwords don\'t match.', category='error')
        elif len(cng_pswd2) < 3:
            flash('Password must be at least 3 characters.', category='error')
        elif not check_password_hash(user.password_hash, old_pswd):
            flash('Current password error', category='error')
        else:
            user.username = cng_name
            hashed_password = user.set_password(cng_pswd1)
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('main.home'))


    return render_template('changelog.html', user=current_user)