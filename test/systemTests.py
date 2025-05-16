#assert what is in controllers.py
#python -m unittest unitTests.py
import unittest
from app import create_app, db
from app.config import TestConfig
from app.forms.login_form import LoginForm
from app.models import User, AssessmentType, Unit, DiaryEntry, Faculty, University, DiaryShare
# need to add 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.populate_initial_data()

        #Forking on MacOS 
        if platform.system() == 'Darwin':
            try:
                multiprocessing.set_start_method('fork')
            except RuntimeError:
                pass

        self.server_process = multiprocessing.Process(target=run_test_server, args=(self.testApplication,), daemon=True)
        self.server_process.start()
        time.sleep(1)  
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        return super().setUp()

    def populate_initial_data(self):
        #Test user for login functionality
        user1= self.add_user(email="rhiannah@gmail.com", password="abc123", username="test1", study_field="test field 1")
        
        # Data for share review test 
        self.user1_email = "user1@example.com"
        self.user2_email = "user2@example.com"
        self.user1= self.add_user(email=self.user1_email, password="password", username="user1", study_field="Test Field 1")
        self.user2= self.add_user(email=self.user2_email, password="tester2", username="user2", study_field="Test Field 2")
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        # Create a diary entry for user1 to share
        university = University(name="Test University")
        db.session.add(university)
        db.session.commit()
        faculty = Faculty(name="Test Faculty", university_id=university.id)
        db.session.add(faculty)
        db.session.commit()
        self.unit = Unit(code="TEST101", title="Test Unit", faculty_id=faculty.id, level=1, university_id=university.id)  
        db.session.add(self.unit)
        db.session.commit()
        self.diary_entry = DiaryEntry(user_id=self.user1.id, unit_id=self.unit.id, semester=1, year=2024, grade=80, overall_rating=5, difficulty_rating=3, coordinator_rating=4, workload_hours_per_week=10, optional_comments="Good unit")
        db.session.add(self.diary_entry)
        db.session.commit()

    def share_review(owner_id, recipient_id):
        new_share = DiaryShare(owner_id=current_user.id, recipient_id=recipient.id)
        db.session.add(new_share)
        db.session.commit()

    def add_user(self, email, password, username="testuser", study_field="test field"):
        # Generate password hash from plain text password
        password_hash = generate_password_hash(password, method='pbkdf2')
        
        # Create user with hashed password
        user = User(
            username=username,
            password_hash=password_hash,  
            email=email,
            study_field=study_field
        )
        

        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        created_user = User.query.filter_by(email=email).first()
        if not created_user:
            print(f"WARNING: Failed to create user {username} with email {email}")
        else:
            print(f"Successfully created user: {created_user.username} ({created_user.email})")
            
        return user

    def login_user(self, email, password):
        self.driver.get(localHost + "login")
        username_field = self.driver.find_element(By.ID, "email")
        password_field = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "submit-button")
        username_field.send_keys(email)
        password_field.send_keys(password)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        time.sleep(1) 
        submit_button.click()
        WebDriverWait(self.driver, 5).until(EC.url_changes(localHost + "login"))

    def test_share_diary_workflow(self):
        # 1. Navigate to the shared diaries page
        self.login_user(self.user1_email, "password")
        self.driver.get(localHost + "shared-diaries")
        time.sleep(5)

        # 2. Fill in the share form
        share_diary_form_button = self.driver.find_element(By.ID, "share_diary_form")
        share_diary_form_button.click()  

        # 3. Wait for the modal to appear and fill in the recipient's email
        modal = WebDriverWait(self.driver, 15).until(
        EC.visibility_of_element_located((By.ID, "shareDiaryModal"))
        )

        recipient_email_field = self.driver.find_element(By.ID, "recipient_email")
        recipient_email_field.send_keys(self.user2_email)

        share_button = self.driver.find_element(By.ID, "share_diary_button") 
        share_button.click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))

        logout_button = self.driver.find_element(By.ID, "logout") 
        logout_button.click()


        # 6. Log in user2 (the recipient)
        self.login_user(self.user2_email, "tester2")

        # 7. Navigate to the shared diaries page for user2
        self.driver.get(localHost + "shared-diaries")

        # 8. Determine if the shared diary entry is visible
        diary_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'shared-diary')) 
        )
        diary_link.click()

        # 9. Assert that user2 is on the diary page and sees the entry
        WebDriverWait(self.driver, 5).until(
            EC.url_contains(localHost + "unit_diary" + "/" + str(self.user1.id))
        )
        time.sleep(5)
        self.assertIn("TEST101", self.driver.page_source, "Diary entry content not found") 

    def test_login_workflow(self):
        # First create a user in the database
        test_email = "rhiannah@gmail.com"
        test_password = "abc123"
        
        # Make sure user doesn't already exist
        existing_user = User.query.filter_by(email=test_email).first()
        if not existing_user:
            print(f"Creating user {test_email} for login test")
            self.add_user(test_email, test_password, "dog", "dog field")
            user= User.query.filter_by(email=test_email).first()
            print(f"User created: {user.email}")
        
        # Verify user exists in database
        user = User.query.filter_by(email=test_email).first()
        self.assertIsNotNone(user, "User was not created in database")
        
        # Now try to login
        self.login_user(test_email, test_password) 
        
        self.assertEqual(self.driver.current_url, localHost + "unit_diary/" + str(user.id))
    
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
        
        try:
            submit_button.click()
        except Exception as e:
            print(f"Regular click failed: {e}")
            self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Wait for redirect to login page
        WebDriverWait(self.driver, 10).until(
            EC.url_changes(localHost + "signup")
        )
        
        self.assertEqual(self.driver.current_url, localHost + "login")
    
    def test_add_unit(self):
        self.login_user(self.user1_email, "password")
        self.driver.get(localHost + "add_unit")
        university_field = self.driver.find_element(By.ID, "add_uni")
        faculty_field = self.driver.find_element(By.ID, "add_faculty")
        unit_code = self.driver.find_element(By.ID, "add_code")
        unit_name = self.driver.find_element(By.ID, "add_unit_name")
        unit_level = self.driver.find_element(By.ID, "add_unit_level")
        submit_button = self.driver.find_element(By.ID, "add_submit")

        university_field.send_keys("Test University")
        faculty_field.send_keys("Test Faculty")
        unit_code.send_keys("TEST102")
        unit_name.send_keys("Test Unit 2")
        unit_level.send_keys("1")

        # Scroll to the submit button to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)

        #Wait for the page to scroll
        time.sleep(1)

        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.url_changes(localHost + "add_unit")
        )

        self.assertEqual(self.driver.current_url, localHost + "search_results")

        search_bar = self.driver.find_element(By.ID, "unitNameInput")
        search_bar.send_keys("TEST102")
        self.assertIn("TEST102", self.driver.page_source, "Unit not found in search results")


    def test_add_review_to_database(self):

        self.login_user(self.user2_email, "tester2")
        unit = Unit.query.filter_by(code="TEST101").first()

        if Unit.query.filter_by(code="TEST101").first() is None:
            print(Unit.query.all())
            print("Unit does not exist in the database.")
            return

        # Check if the user has already submitted a review for this unit
        if DiaryEntry.query.filter_by(user_id=self.user2.id, unit_id=self.unit.id).first():
            print("Diary entry already exists for this user and unit.")
            return

        self.driver.get(localHost + "submit_review" + "/" + str(unit.id))

        semester_field = self.driver.find_element(By.ID, "rev_semester")
        unit_year = self.driver.find_element(By.ID, "rev_year")
        unit_coord_rating_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='rev_unit_coord_rating'][value='4']")
        difficulty_rating_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='rev_difficulty'][value='3']")
        hours_field = self.driver.find_element(By.ID, "rev_hours")
        assessment_fields = self.driver.find_elements(By.CSS_SELECTOR, "#rev_assessments input[type='checkbox']") 
        grade_field = self.driver.find_element(By.ID, "rev_grade")
        avg_hours_field = self.driver.find_element(By.ID, "rev_avg_hours")
        rating_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='rev_rating'][value='4']")
        comments_field = self.driver.find_element(By.ID, "rev_comments")
        submit_button = self.driver.find_element(By.ID, "rev_submit")

        semester_field.send_keys("1")
        unit_year.send_keys("2024")

        #Scroll to the unit coordinator rating to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", unit_coord_rating_field)
        time.sleep(2)  # Give the page time to scroll
        unit_coord_rating_field.click()
        difficulty_rating_field.click()

        # Scroll to the hours field to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hours_field)
        time.sleep(1)  # Give the page time to scroll
        hours_field.send_keys("10")
        if assessment_fields:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", assessment_fields[0])
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(assessment_fields[0]))
            assessment_fields[0].click()

        # Scroll to the grade field to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", grade_field)
        time.sleep(1)
        grade_field.send_keys("80")
        avg_hours_field.send_keys("5")
        # Scroll to the rating field to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rating_field)
        time.sleep(1)
        rating_field.click()
        comments_field.send_keys("Good unit")
        # Scroll to the submit button to make it visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        #Wait for the page to scroll
        time.sleep(1)
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_changes(localHost + "submit_review" + "/" + str(unit.id))
        )
        self.assertEqual(self.driver.current_url, localHost + "unit_diary/" + str(self.user2.id))



    def tearDown(self):
        self.driver.quit()
        self.server_process.terminate()
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
        return super().tearDown()