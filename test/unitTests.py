import unittest
from app import create_app, db
from app.routes import login
from app.config import TestConfig
from app.forms.login_form import LoginForm
from app.forms.unit_review import AddUnitForm
from app.models import User, AssessmentType, Unit, DiaryEntry, Faculty, University, UnitAssessmentType
import random
from app.controllers import get_avg_rating_for_unit, get_optional_comments_for_unit, avg_rating_for_unit_coord, get_difficulty_rating_avg_for_unit, get_overall_rating_count_for_unit, get_assessment_types_for_unit
from werkzeug.security import generate_password_hash

class UnitTests(unittest.TestCase):
    def setUp(self):
        testApplication = create_app(TestConfig)
        self.app_ctx=testApplication.app_context()  
        self.app_ctx.push()
        self.client = testApplication.test_client(use_cookies=True)
        db.create_all()
        self.populate_initial_data()
        return super().setUp()

    def populate_initial_data(self):    

        # Create class variables for the tests
        self.university = University(name="Test University")
        db.session.add(self.university)
        db.session.commit()
        self.faculty = Faculty(name="Test Faculty", university_id=self.university.id)
        db.session.add(self.faculty)
        db.session.commit()
        self.unit = Unit(code="TEST101", title="Test Unit", faculty_id=self.faculty.id, level=1, university_id=self.university.id) 
        db.session.add(self.unit)
        db.session.commit()

        #Populate the database with assessment types
        exam = AssessmentType(name="Exam")
        project = AssessmentType(name="Project")
        db.session.add_all([exam, project])
        db.session.commit()

    def test_get_avg_rating_for_unit_no_entries(self):
        """Test the function when there are no diary entries for the unit."""
        non_existent_id=-1
        avg_rating = get_avg_rating_for_unit(non_existent_id)
        self.assertIsNone(avg_rating)

    def test_get_avg_rating_for_unit_multiple_entries(self):
        """Test the function with multiple diary entries."""
        unit = Unit(code="CITS1002", title="Test Unit 2", faculty_id=self.faculty.id, level=1, university_id=self.university.id)
        db.session.add(unit)
        db.session.commit()
        entry1 = DiaryEntry(user_id=5, unit_id=unit.id, overall_rating=2, semester=1, year=2024)
        entry2 = DiaryEntry(user_id=6, unit_id=unit.id, overall_rating=3, semester=1, year=2024)
        entry3 = DiaryEntry(user_id=7, unit_id=unit.id, overall_rating=5, semester=1, year=2024)
        entry4 = DiaryEntry(user_id=8, unit_id=unit.id, overall_rating=2, semester=1, year=2024)   
        db.session.add_all([entry1, entry2, entry3, entry4])
        db.session.commit()

        avg_rating = get_avg_rating_for_unit(unit.id)
        self.assertEqual(avg_rating, 3.0) 

    def test_get_overall_rating_count_for_unit_no_entries(self):
        """Test the function when there are no diary entries for the unit."""
        non_existent_id = -1
        rating_counts = get_overall_rating_count_for_unit(non_existent_id)
        expected_counts = {"Amazing": 0, "Great": 0, "Okay": 0, "Bad": 0, "Poor": 0}
        self.assertEqual(rating_counts, expected_counts)

    
    def test_get_overall_rating_for_unit_mixed_entries(self):
        """Test with a mix of all rating values."""
        unit = Unit(code="CITS1003", title="Test Unit 3", faculty_id=self.faculty.id, level=1, university_id=self.university.id)
        db.session.add(unit)
        db.session.commit()
        entries = [
            DiaryEntry(user_id=10 , unit_id=unit.id, overall_rating=5, semester=1, year=2024),
            DiaryEntry(user_id=11, unit_id=unit.id, overall_rating=4, semester=1, year=2024),
            DiaryEntry(user_id=12, unit_id=unit.id, overall_rating=3, semester=1, year=2024),
            DiaryEntry(user_id=13, unit_id=unit.id, overall_rating=2, semester=1, year=2024),
        ]
        db.session.add_all(entries)
        db.session.commit()
        expected_result = {
            "Amazing": 1,
            "Great": 1,
            "Okay": 1,
            "Bad": 1,
            "Poor": 0,
        }
        self.assertEqual(get_overall_rating_count_for_unit(unit.id), expected_result)

    def test_get_assessment_types_for_unit_no_assessments(self):
        """Test the function when the unit has no associated assessment types."""
        assessment_types = get_assessment_types_for_unit(self.unit.id)
        self.assertEqual(assessment_types, [])

    def test_get_assessment_types_for_unit_single_assessment(self):
        """Test the function when the unit has a single associated assessment type."""
        exam=db.session.query(AssessmentType).first().id
        association = UnitAssessmentType(
        unit_id=self.unit.id,
        assessment_type_id=exam
        )
        db.session.add(association)
        db.session.commit()
        
        assessment_types = get_assessment_types_for_unit(self.unit.id)
        self.assertEqual(len(assessment_types), 1)
        self.assertEqual(assessment_types[0].name, "Exam")

    def test_get_assessment_types_for_unit_multiple_assessments(self):
        """Test the function when the unit has multiple associated assessment types."""
        assessment_types= db.session.query(AssessmentType).all()
        for assessment in assessment_types:
            association = UnitAssessmentType(
            unit_id=self.unit.id,
            assessment_type_id=assessment.id
            )
            db.session.add(association)
        db.session.commit()
        
        assessment_types = get_assessment_types_for_unit(self.unit.id)
        self.assertEqual(len(assessment_types), 2)
        self.assertIn("Exam", [at.name for at in assessment_types])
        self.assertIn("Project", [at.name for at in assessment_types])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
        return super().tearDown()