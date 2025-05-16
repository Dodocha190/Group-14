#fill db with examples for testing, do not merge
from app import create_app, db
from app.config import DeploymentConfig
from app.models import User, University, Unit, DiaryEntry, Faculty, AssessmentType, UnitAssessmentType, DiaryShare
from werkzeug.security import generate_password_hash

#users
def populate_data_base():
    user1=User(
                email="user1@student.uwa.edu.au",
                username="User Name 1",
                password_hash=generate_password_hash("password", method='pbkdf2'),
                study_field="Computer Science")
    user2=User(
                email="user2@student.uwa.edu.au",
                username="User Name 2",
                password_hash=generate_password_hash("password", method='pbkdf2'),
                study_field="English")
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    #universities
    uni1=University(
                    name="University of Western Australia")

    uni2=University(
                    name="Another University")
    db.session.add(uni1)
    db.session.add(uni2)
    db.session.commit()
    #faculties
    faculty1=Faculty(
                    name="Philosophy",
                    university_id=uni1.id)
    faculty2=Faculty(
                    name="Computer Science",
                    university_id=uni1.id)
    faculty3=Faculty(
                    name="Statistics",
                    university_id=uni1.id)
    faculty4=Faculty(
                    name="Faculty",
                    university_id=uni2.id)
    db.session.add_all([faculty1, faculty2, faculty3, faculty4])    
    db.session.commit()
    #units
    unit1=Unit(code="PHIL2001",
                title="Bioethics",
                faculty_id=faculty1.name,
                level=3,
                university_id=uni1.name)
    unit2=Unit(code="CITS3401",
                title="Data Warehousing",
                faculty_id=faculty2.name,
                level=3,
                university_id=uni1.name)
    unit3=Unit(code="CITS3403",
                title="Agile Web Development",
                faculty_id=faculty2.name,
                level=3,
                university_id=uni1.name)
    unit4=Unit(code="STAT2402",
                title="Analysis of Observations",
                faculty_id=faculty3.name,
                level=2,
                university_id=uni1.name)
    unit5=Unit(code="CODE01",
                title="A unit at another uni",
                faculty_id=faculty4.name,
                level=1,
                university_id=uni2.name)
    db.session.add_all([unit1, unit2, unit3, unit4, unit5])
    db.session.commit()
    #assessment types
    assessment_type1=AssessmentType(name="Final Exam")
    assessment_type2=AssessmentType(name="Midsemester Exam")

    db.session.add_all([assessment_type1, assessment_type2])
    db.session.commit()
    #unit assessment types
    unit_assessment_type1=UnitAssessmentType(unit_id=unit1.id,
                                            assessment_type_id=assessment_type1.id)
    unit_assessment_type2=UnitAssessmentType(unit_id=unit1.id,
                                            assessment_type_id=assessment_type2.id)
    unit_assessment_type3=UnitAssessmentType(unit_id=unit2.id,
                                            assessment_type_id=assessment_type1.id)
    db.session.add_all([unit_assessment_type1, unit_assessment_type2, unit_assessment_type3])
    db.session.commit()
    #diary entries
    entry1=DiaryEntry(user_id=user1.id, #review of same unit by diff user to check results unit summary
                unit_id=unit1.id,
                semester=1,
                year=2025,
                grade=70,
                overall_rating=5,
                difficulty_rating=3,
                coordinator_rating=5,
                workload_hours_per_week=10,
                optional_comments="cool unit")

    entry2=DiaryEntry(user_id=user2.id, #review of same unit by diff user to check results unit summary
                unit_id=unit1.id,
                semester=1,
                year=2025,
                grade=60,
                overall_rating=4,
                difficulty_rating=4,
                coordinator_rating=4,
                workload_hours_per_week=10)
    entry3=DiaryEntry(user_id=user1.id, 
                unit_id=unit2.id,
                semester=1,
                year=2025,
                grade=65,
                overall_rating=5,
                difficulty_rating=5,
                coordinator_rating=5,
                workload_hours_per_week=10,
                optional_comments="challenging")
    entry4=DiaryEntry(user_id=user2.id, 
                unit_id=unit2.id, #second cits unit
                semester=1,
                year=2025,
                grade=80, #should result in cits being highest wam area
                overall_rating=5,
                difficulty_rating=4,
                coordinator_rating=5,
                workload_hours_per_week=8,
                optional_comments="great")
    entry5=DiaryEntry(user_id=user1.id, 
                unit_id=unit3.id,
                semester=2,
                year=2024,
                grade=69,
                overall_rating=3,
                difficulty_rating=3,
                coordinator_rating=3,
                workload_hours_per_week=8)
    db.session.add_all([entry1, entry2, entry3, entry4, entry5])
    db.session.commit()
#search phil2001 to see if a unit with 2 reviews summarised
#look at user1 diary for user summary
if __name__ == "__main__":
    application = create_app(DeploymentConfig)
    with application.app_context():
        db.create_all()
        populate_data_base()