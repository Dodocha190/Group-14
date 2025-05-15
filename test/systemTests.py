#assert what is in controllers.py
#python -m unittest unitTests.py
import unittest
from app import create_app, db
from app.config import TestConfig
from app.forms.login_form import LoginForm
from app.models import User, AssessmentType
# need to add 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import multiprocessing
import time
from werkzeug.security import generate_password_hash
import platform

localHost = "http://127.0.0.1:5000/"

def run_test_server(app):
    app.run(debug=False, use_reloader=False) 

class SystemTests(unittest.TestCase):


    def setUp(self):
        self.testApplication = create_app(TestConfig)
        self.app_ctx = self.testApplication.app_context()
        self.app_ctx.push()
        db.create_all()
        self.add_user(email="rhiannah@gmail.com", password="abc123")

        if platform.system() == 'Darwin':
            try:
                multiprocessing.set_start_method('fork')
            except RuntimeError:
                pass

        self.server_process = multiprocessing.Process(target=run_test_server, args=(self.testApplication,), daemon=True)
        self.server_process.start()
        time.sleep(1)  # Give the server a moment to start

        self.driver = webdriver.Chrome()
        return super().setUp()

    def add_user(self, email, password, username="testuser", study_field="test field"):
        # Generate password hash from plain text password
        password_hash = generate_password_hash(password, method='pbkdf2')
        
        # Create user with hashed password
        user = User(
            username=username,
            password_hash=password_hash,  # Use the generated hash, not plain text
            email=email,
            study_field=study_field
        )
        
        # Add to session and commit
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        created_user = User.query.filter_by(email=email).first()
        if not created_user:
            print(f"WARNING: Failed to create user {username} with email {email}")
        else:
            print(f"Successfully created user: {created_user.username} ({created_user.email})")
            
        return user

    def test_login_workflow(self):
        # First create a user in the database
        test_email = "rhiannah@gmail.com"
        test_password = "abc123"
        
        # Make sure user doesn't already exist
        existing_user = User.query.filter_by(email=test_email).first()
        if not existing_user:
            print(f"Creating user {test_email} for login test")
            self.add_user(test_email, test_password, "dog", "dog field")
            uers= User.query.filter_by(email=test_email).first()
            print(f"User created: {uers}")
        
        # Verify user exists in database
        user = User.query.filter_by(email=test_email).first()
        self.assertIsNotNone(user, "User was not created in database")
        
        # Now try to login
        self.driver.get(localHost + "login")
        
        username_field = self.driver.find_element(By.ID, "email")
        password_field = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "submit-button")
        
        username_field.send_keys(test_email)
        password_field.send_keys(test_password)
        
        # Scroll to the submit button to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        time.sleep(1)  # Give the page time to scroll
        
        # Try clicking with JavaScript if regular click fails
        try:
            submit_button.click()
        except Exception as e:
            print(f"Regular click failed: {e}")
            self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Wait for redirect to dashboard
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_changes(localHost + "login")
        )
        
        self.assertEqual(self.driver.current_url, localHost + "dashboard")
    
    def test_signup_page(self):
        self.driver.get(localHost + "signup")
        self.add_user(email="test@gmail.com", password="abc123")
        # Fill out the signup form
        email = self.driver.find_element(By.ID, "email")
        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        study_field = self.driver.find_element(By.ID, "study-field")
        submit_button = self.driver.find_element(By.ID, "submit-button")
        
        email.send_keys("dog@gmail.com")
        username.send_keys("dog")
        password.send_keys("abc123")
        study_field.send_keys("dog field")
        # Scroll to the submit button to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        time.sleep(1)  # Give the page time to scroll
        
        # Try clicking with JavaScript if regular click fails
        try:
            submit_button.click()
        except Exception as e:
            print(f"Regular click failed: {e}")
            self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Wait for redirect to login page
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_changes(localHost + "signup")
        )
        
        self.assertEqual(self.driver.current_url, localHost + "login")
    



    def tearDown(self):
        self.driver.quit()
        self.server_process.terminate()
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
        return super().tearDown()