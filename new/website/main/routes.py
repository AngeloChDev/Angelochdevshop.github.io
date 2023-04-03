from flask import render_template, request, Blueprint, redirect, current_app
from flask_login import login_user, current_user, logout_user, login_required
from .shop import list_order
from website.models import Product
import io 
import base64
from PIL import Image

main = Blueprint('main', __name__)

@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    try:
        print('try')
        products_list = Product.query.filter_by(seller=current_user).order_by(Product.date_posted.desc())
        for i in products_list:
            img = Image.open(current_app.config["UPLOAD_FOLDER"] + "/" + i.photo)
            data = io.BytesIO()
            img.save(data, 'JPEG')
            encode = base64.b64encode(data.getvalue())
            created = {'name': i.name, 'description': i.description, 'cost': i.price, 'photo':encode.decode('UTF-8') }
            print(type(encode))
    except:
        redirect(404)

    finally:
        print('finally')
    
    return render_template('home.html', user=current_user, user_products=products_list)

@main.route("/seller/<int: seller.id>", methods=['GET', 'POST'])
@login_required
def seller_view():
   return render_template('seller_view.html', user=current_user)
