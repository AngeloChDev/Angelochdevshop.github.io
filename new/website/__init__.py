from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from website.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
   
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from website.users.routes import users
    from website.main.routes import main
    from website.main.shop import shopPage
    from website.users.changelog import change_log
    from website.users.utils import utils
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(shopPage)
    app.register_blueprint(change_log)
    app.register_blueprint(utils)

    from .models import User

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

