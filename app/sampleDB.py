#fill db with examples for testing, do not merge
from app import application, db
from app.models import User, University, Unit, DiaryEntry, Faculty, AssessmentType, UnitAssessmentType, DiaryShare
from werkzeug.security import generate_password_hash

#users
user1=User(id=1,
            email="user1@student.uwa.edu.au",
            username="User Name 1",
            password_hash=generate_password_hash("password", method='pbkdf2'),
            study_field="Computer Science")
user2=User(id=2,
            email="user2@student.uwa.edu.au",
            username="User Name 2",
            password_hash=generate_password_hash("password", method='pbkdf2'),
            study_field="English")

#universities
uni1=University(id=1,
                name="University of Western Australia")
uni2=University(id=2,
                name="Another University")

#faculties
faculty1=Faculty(id=1,
                 name="Philosophy",
                 university_id=1)
faculty2=Faculty(id=2,
                 name="Computer Science",
                 university_id=1)
faculty3=Faculty(id=3,
                 name="Statistics",
                 university_id=1)
faculty4=Faculty(id=4,
                 name="Faculty",
                 university_id=2)

#units
unit1=Unit(code="PHIL2001",
            title="Bioethics",
            faculty_id="1",
            level=3,
            university_id="1")
unit2=Unit(code="CITS3401",
            title="Data Warehousing",
            faculty_id="2",
            level=3,
            university_id="1")
unit3=Unit(code="CITS3403",
            title="Agile Web Development",
            faculty_id="2",
            level=3,
            university_id="1")
unit4=Unit(code="STAT2402",
            title="Analysis of Observations",
            faculty_id="3",
            level=2,
            university_id="1")
unit5=Unit(code="CODE01",
            title="A unit at another uni",
            faculty_id="4",
            level=1,
            university_id="2") #to test uni filtering

#diary entries
entry1=DiaryEntry(user_id=1, 
            unit_id="PHIL2001",
            semester=1,
            year=2025,
            grade=70,
            overall_rating=5,
            difficulty_rating=3,
            coordinator_rating=5,
            workload_hours_per_week=10,
            optional_comments="cool unit")
entry2=DiaryEntry(user_id=2, #review of same unit by diff user to check results unit summary
            unit_id="PHIL2001",
            semester=1,
            year=2025,
            grade=60,
            overall_rating=4,
            difficulty_rating=4,
            coordinator_rating=4,
            workload_hours_per_week=10)
entry3=DiaryEntry(user_id=1, 
            unit_id="CITS3401",
            semester=1,
            year=2025,
            grade=65,
            overall_rating=5,
            difficulty_rating=5,
            coordinator_rating=5,
            workload_hours_per_week=10,
            optional_comments="challenging")
entry4=DiaryEntry(user_id=1, 
            unit_id="CITS3403", #second cits unit
            semester=1,
            year=2025,
            grade=80, #should result in cits being highest wam area
            overall_rating=5,
            difficulty_rating=4,
            coordinator_rating=5,
            workload_hours_per_week=8,
            optional_comments="great")
entry5=DiaryEntry(user_id=1, 
            unit_id="STAT2402",
            semester=2,
            year=2024,
            grade=69,
            overall_rating=3,
            difficulty_rating=3,
            coordinator_rating=3,
            workload_hours_per_week=8)
#search phil2001 to see if a unit with 2 reviews summarised
#look at user1 diary for user summary

with application.app_context():
    db.session.add_all([user1, user2,
                        uni1, uni2,
                        faculty1, faculty2, faculty3, faculty4,
                        unit1, unit2, unit3, unit4, unit5,
                        entry1,entry2,entry3,entry4,entry5])
    db.session.commit()