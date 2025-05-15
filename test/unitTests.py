#assert what is in controllers.py
#python -m unittest unitTests.py
import unittest
from app import create_app, db
from app.config import TestConfig
from app.forms.login_form import LoginForm
from app.models import User, AssessmentType
# need to add 

class UnitTests(unittest.TestCase):
    def setUp(self):
        testApplication = create_app(TestConfig)
        self.app_ctx=testApplication.app_context()  
        self.app_ctx.push()
        db.create_all()
        return super().setUp()
    

    def test_database_user_model(self):
        #PLACEHOLDER: to update
        user = User(username='testuser', password_hash='password', email="test@gmail.com", study_field="test field")
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(username='testuser').first())


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
        return super().tearDown()