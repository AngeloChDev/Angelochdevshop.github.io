from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from website.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    Migrate(app, db)
    db.init_app(app)
   
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from website.users.auth import auth
    from website.views.home import main
    from website.views.shop import shopPage
    from website.users.changelog import change_log
    from website.users.utils import utils
    from website.views.sellerView import sellerView
    from website.views.productView import productView
    from website.views.homeInfo import homeInfo
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(shopPage)
    app.register_blueprint(change_log)
    app.register_blueprint(utils)
    app.register_blueprint(sellerView)
    app.register_blueprint(productView)
    app.register_blueprint(homeInfo)

    from .models import User

    with app.app_context():
        db.create_all()
        

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

