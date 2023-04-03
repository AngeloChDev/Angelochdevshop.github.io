from .models import Product, User

p = Product.query.all()
print(p)
