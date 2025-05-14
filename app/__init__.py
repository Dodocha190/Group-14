from flask import Flask
from .config import Config
from .models import db, User, AssessmentType
from flask_migrate import Migrate
from flask_login import LoginManager

application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)
migrate = Migrate(application, db)
login_manager = LoginManager()
login_manager.init_app(application)

import app.routes

@application.context_processor
def inject_user():
    from flask_login import current_user
    return dict(show_user_info=current_user.is_authenticated)

@application.before_request
def add_initial_assessment_types_before_first_request():
    with application.app_context():
        if db.session.query(AssessmentType).count() == 0:
            initial_types = ['Final Exam', 'Midsemester Exam', 'Individual Project', 'Group Project', 'Essay', 'Test/Quiz', 'Labs', 'Participation Marks', 'Other']
            for type_name in initial_types:
                if not db.session.query(AssessmentType).filter_by(name=type_name).first():
                    assessment_type = AssessmentType(name=type_name)
                    db.session.add(assessment_type)
            db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
