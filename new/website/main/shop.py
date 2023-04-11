from flask import render_template, request, Blueprint, redirect, url_for, current_app, flash,session
from flask_login import current_user
from website.models import Product, User
from country_list import countries_for_language
from collections import defaultdict

countries = dict(countries_for_language('en'))

shopPage = Blueprint('shopPage', __name__)

list_order = []
tot =[]
ord_tot= []
result = defaultdict(lambda: {'product': int(), 'quantity': 0, })

@shopPage.route("/", methods=['GET', 'POST'])
@shopPage.route("/shop", methods=['GET', 'POST'])
def shop():

    countr = countries
    CATEGORY = current_app.config["CATEGORY_PRODUCT"]
    row = Product.query.all()
    if request.method == 'POST':
        if 'filter' in request.form:
            country_selected = request.form.get('country_value')
            category_selected = request.form.get('category_value')
            filter_product = []
            if category_selected or country_selected:
                filter_category = Product.query.filter_by(category=category_selected).all()
                filter_user =  User.query.filter_by(country=country_selected).all()

                for i in filter_category:
                    filter_product.append(i)

                for i in filter_user:
                    p = i.products
                    for i in p:
                        filter_product.append(i)
            else:
                flash('No filters selected.', category='error')
                
            return render_template('shop.html', prod= filter_product, user=current_user, country=countr, category=CATEGORY)
        elif 'buy_now' in request.form:
            qnt = request.form.get('qnt')
            code = request.form.get('code')

            if not qnt:
                flash('No product selected', category="error")
            else:
                selected = {'product': int(code), 'quantity': int(qnt)}
                session['CART'].append(selected)
                flash('Product added to cart', category="success")
                pass
                
        else:
            redirect(404)
    

    return render_template('shop.html', prod=row, user=current_user, country=countr, category=CATEGORY)


