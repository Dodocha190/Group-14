#fill db with examples for testing, do not merge
from .models import db, User, University, Unit, DiaryEntry, Faculty, AssessmentType, UnitAssessmentType, DiaryShare
from werkzeug.security import generate_password_hash, check_password_hash

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
            university_id="2")


db.session.add_all([user1, user2,
                    uni1, uni2,
                    faculty1, faculty2, faculty3, faculty4,
                    unit1, unit2, unit3, unit4, unit5,
                    ])
db.session.commit()