from flask import Flask
from .config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

migrate = Migrate(application, db)

import app.routes

@application.context_processor
def inject_user():
    from flask_login import current_user
    return dict(show_user_info=current_user.is_authenticated)
