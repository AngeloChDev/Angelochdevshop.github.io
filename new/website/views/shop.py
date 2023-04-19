from flask import render_template, request, Blueprint, redirect, url_for, current_app, flash,session
from flask_login import current_user
from website.models import Product, User
from country_list import countries_for_language
from collections import defaultdict
import random

countries = dict(countries_for_language('en'))

shopPage = Blueprint('shopPage', __name__)

@shopPage.route("/", methods=['GET', 'POST'])
@shopPage.route("/shop", methods=['GET', 'POST'])
def shop():
    row = list()
    default_ord = current_app.config['DEFAULT_ORD']
    countr = countries
    result = defaultdict(lambda: {'product': '', 'quantity': 0, })
    CATEGORY = current_app.config["CATEGORY_PRODUCT"]
    try:
        row = Product.query.filter_by(DELETED=False).all()
        
    
    except:
        pass
    finally:
        if request.method == 'POST':
            if 'filter' in request.form:
                country_selected = request.form.get('country_value')
                category_selected = request.form.get('category_value')
                filter_product = []
                if category_selected or country_selected:
                    filter_category = Product.query.filter_by(DELETED=False,category=category_selected).all()
                    filter_user =  User.query.filter_by(DELETED=False,country=country_selected).all()

                    for i in filter_category:
                        filter_product.append(i)

                    for i in filter_user:
                        p = i.products
                        for i in p:
                            filter_product.append(i)
                    row = filter_product
                else:
                    flash('No filters selected.', category='error')
                    
                return render_template('shop.html', prod= filter_product, user=current_user, country=countr, category=CATEGORY)
            elif 'buy_now' in request.form:
                qnt = request.form.get('qnt')
                code = request.form.get('code')
                if not qnt:
                    flash('No product selected', category="error")
                else:
                    
                    result['product'] = code
                    result['quantity'] = int(qnt)
                    session['CART'].append(result)
                    flash('Product added to cart', category="success")
                    
                    
            else:
                redirect(404)
    

    return render_template('shop.html', prod=row, user=current_user, country=countr, category=CATEGORY)


