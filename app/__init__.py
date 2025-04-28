from flask import Flask
from .config import Config
from .models import db


application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)

import app.routes
# register_routes(application)
