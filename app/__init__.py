from flask import Flask
from .config import Config
from .models import db
from flask_migrate import Migrate


application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)
with application.app_context():
    db.create_all()
migrate = Migrate(application, db)

import app.routes
