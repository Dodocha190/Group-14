from flask import Flask
from .config import Config
from .models import db
from .routes import register_routes

application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)
register_routes(application)
