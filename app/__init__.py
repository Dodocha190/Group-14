from flask import Flask
from .config import Config
from .routes import main
from .models import db, User
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' #redirect if not logged in

    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
