# Defines database schema using SQLAlchemy, will change if requirements says otherwise
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    study_field = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Faculty(db.Model):
    __tablename__ = 'faculties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id', name='fk_faculties_universities_university_id'), nullable=False)


class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id', name='fk_units_faculties_faculty_id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id', name='fk_units_universities_university_id'), nullable=False)
    assessment_types = db.relationship('AssessmentType', secondary='unit_assessment_types', backref='units', lazy=True)

class AssessmentType(db.Model):
    __tablename__ = 'assessment_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class UnitAssessmentType(db.Model):
    __tablename__ = 'unit_assessment_types'
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', name='fk_unit_assessment_types_units_unit_id'), nullable=False)
    assessment_type_id = db.Column(db.Integer, db.ForeignKey('assessment_types.id', name='fk_unit_assessment_types_assessment_types_assessment_type_id'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('unit_id', 'assessment_type_id', name='uix_unit_assessment_type'),
    )
    
class DiaryEntry(db.Model):
    __tablename__ = 'diary_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_diary_entries_users_user_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', name='fk_diary_entries_units_unit_id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Float)
    overall_rating = db.Column(db.Integer)
    difficulty_rating = db.Column(db.Integer)
    coordinator_rating = db.Column(db.Integer)
    workload_hours_per_week = db.Column(db.Integer)
    optional_comments = db.Column(db.String(250), nullable=True)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'unit_id', 'semester', name='uix_user_unit_sem'),
    )


class DiaryShare(db.Model):
    __tablename__ = 'diary_shares'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_diary_shares_users_owner_id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_diary_shares_users_recipient_id'), nullable=False)
