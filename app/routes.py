from app import application
from flask import render_template, redirect, url_for, flash, request
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm
from app.forms.unit_review import AddUnitForm
from app.forms.unit_review import ReviewForm
from .models import db, User, Unit, DiaryEntry, Faculty
import difflib
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func

@application.route('/')
def home():
    return render_template('intro.html')

@application.route('/unit-summary')
def unit_summary():
    return render_template('unit_summary.html')


@application.route('/dashboard') #temporary, somewhere to go to after successful login
def dashboard():
    units_taken = get_diary_entries_from_user(current_user.email)
    return render_template('unitdiary.html', show_user_info=True, user_email='current_user.email', units_taken=units_taken)

def get_diary_entries_from_user(user_email):
    """
    Fetches all diary entries associated with a given user email, including their units.
    """ 
    query = db.session.query(DiaryEntry, Unit).join(Unit, DiaryEntry.unit_id == Unit.id).order_by(DiaryEntry.year.desc(), DiaryEntry.semester.desc())
    results = query.filter(DiaryEntry.user_email == user_email).all()
    return results

def summarise_diary_entries(user_email):
    highest_wam_area = db.session.query(Unit.faculty_id, func.avg(DiaryEntry.grade)).join(DiaryEntry.unit_id == Unit.id).filter(DiaryEntry.user_email == user_email).group_by(Unit.faculty_id).order_by(func.avg(DiaryEntry.grade).desc()).first()
    percent_by_faculty = db.session.query(Unit.faculty_id, 100*func.count(Unit.faculty_id)/func.sum(func.count(Unit.faculty_id))).join(DiaryEntry.unit_id == Unit.id).filter(DiaryEntry.user_email == user_email).group_by(Unit.faculty_id)
    total_credits = db.session.query(6*func.count(DiaryEntry)).join(DiaryEntry.unit_id == Unit.id).filter(DiaryEntry.user_email == user_email, DiaryEntry.grade>=50)
    avg_difficulty = db.session.query(func.avg(DiaryEntry.difficulty_rating)).join(DiaryEntry.unit_id == Unit.id).filter(DiaryEntry.user_email == user_email)
    return highest_wam_area, percent_by_faculty, total_credits, avg_difficulty

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data, method='pbkdf2'),
            study_field=form.study_field.data
          )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))
    flash("Please fill in all fields.")
    return render_template('sign_up_page.html', form=form)

@application.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
            return redirect(url_for('dashboard'))  # Redirect if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user) 
            return redirect(url_for('dashboard')) 
        else:
            flash('Invalid email or password.')

    return render_template('login_page.html', form=form)
  
@application.route('/unit_diary')
def diary():
    return render_template('unitdiary.html')

@application.route('/submit_review', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        unit = Unit.query.filter_by(code=form.rev_code.data).first()
        if not unit:
            flash("Unit not found.")
            return redirect(url_for('add_unit'))
        dataEntry = DiaryEntry(
            user_email=current_user.email, 
            unit_id=unit.id,
            semester=form.rev_semester.data,
            year=form.rev_year.data,
            grade=form.rev_grade.data,
            overall_rating=form.rev_rating.data,
            difficulty_rating=form.rev_difficulty.data,
            coordinator_rating=form.rev_unit_coord_rating.data,
            workload_hours_per_week=form.rev_avg_hours.data
        )
        db.session.add(dataEntry)
        db.session.commit()
        flash("Review submitted successfully!")
        return redirect(url_for('dashboard'))
    return render_template('unit_review.html', form=form)

@application.route('/add_unit', methods=['GET', 'POST'])
def add_unit():
    form = AddUnitForm()
    if form.validate_on_submit():
        faculty = Faculty.query.filter_by(name=form.add_faculty.data).first()
        if not faculty:
            #Adds non-existing faculty to the database
            faculty = Faculty(name=form.add_faculty.data, university_id=form.add_uni.data)
            db.session.add(faculty)
            db.session.commit()
        unit = Unit(
            code=form.add_code.data.upper(), #capslocks unit code before adding to database
            title=form.add_unit_name.data,
            faculty_id=form.add_faculty.data,
            level=form.add_unit_level.data,
            university_id=form.add_uni.data
        )
        db.session.add(unit)
        db.session.commit()
        flash("Unit added successfully!")
        return redirect(url_for('search_results'))
    return render_template('add_unit.html', form=form)

@application.route('/search_results', methods=['GET'])
def search_results():  
    all_units = Unit.query.all()

    return render_template('unit_search.html', results=all_units)

@application.route('/logout')
@login_required
def logout():
    """
    Logs the user out and redirects them to the login page.
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))