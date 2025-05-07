#Defines database schema using SQLAlchemy, will change if requirements says otherwise
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(64), unique=True, nullable=False, primary_key = True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class University(db.Model):
    __tablename__ = 'universities'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Faculty(db.Model):
    __tablename__ = 'faculties'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), unique=True, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False)


class Unit(db.Model):
    __tablename__ = 'units'
    id            = db.Column(db.Integer, primary_key=True)
    code          = db.Column(db.String(10), unique=True, nullable=False)
    title         = db.Column(db.String(150), nullable=False)
    faculty_id    = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    level         = db.Column(db.Integer, nullable=False)


class DiaryEntry(db.Model):
    __tablename__ = 'diary_entries'
    id                       = db.Column(db.Integer, primary_key=True)
    user_email               = db.Column(db.String(64), db.ForeignKey('users.email'), nullable=False)
    unit_id                  = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    semester                 = db.Column(db.Integer, nullable=False)
    year                     = db.Column(db.Integer, nullable=False)
    grade                    = db.Column(db.Float)
    overall_rating           = db.Column(db.Integer)
    difficulty_rating        = db.Column(db.Integer)
    coordinator_rating       = db.Column(db.Integer)
    workload_hours_per_week  = db.Column(db.Integer)
    __table_args__ = (
        db.UniqueConstraint('user_email','unit_id','semester', name='uix_user_unit_sem'),
    )


class AssessmentBreakdown(db.Model):
    __tablename__ = 'assessment_breakdowns'
    id         = db.Column(db.Integer, primary_key=True)
    entry_id   = db.Column(db.Integer, db.ForeignKey('diary_entries.id'), nullable=False)
    type       = db.Column(db.String(50), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)


class DiaryShare(db.Model):
    __tablename__ = 'diary_shares'
    id                = db.Column(db.Integer, primary_key=True)
    owner_email       = db.Column(db.String(64), db.ForeignKey('users.email'), nullable=False)
    recipient_email   = db.Column(db.String(64), db.ForeignKey('users.email'), nullable=False)
