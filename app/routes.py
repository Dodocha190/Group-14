from app import application
from flask import render_template, redirect, url_for, flash, request
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm
from app.forms.unit_review import AddUnitForm
from app.forms.unit_review import ReviewForm
from .models import db, User, Unit, DiaryEntry, Faculty
import difflib

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/unit-summary')
def unit_summary():
    return render_template('unit_summary.html')


@application.route('/dashboard') #temporary, somewhere to go to after successful login
def dashboard():
        return render_template('dashboard.html', username=current_user.email)

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        alert("Registration successful. Please log in.")
        return redirect(url_for('login'))
    flash("Please fill in all fields.")
    return render_template('sign_up_page.html', form=form)

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.guest.data:
            guest = User.query.filter_by(email='guest@classmate.com').first()
            if not guest:
                guest = User(email='guest@classmate.com')
                guest.set_password('')
                db.session.add(guest)
                db.session.commit()
                return redirect(url_for('userhome')) #dashboard for now, will decide on it later
        else:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                return redirect(url_for('userhome'))
            flash("Invalid email or password.")

    return render_template('login_page.html', form=form)

  
@application.route('/search')
def search():
    return render_template('unit_search.html')


@application.route('/submit_review', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        unit = Unit.query.filter_by(code=form.rev_code.data).first()
        if not unit:
            flash("Unit not found.")
            return redirect(url_for('add_unit'))
        dataEntry = DiaryEntry(
            user_email='test', #To replace with current_user.email
            unit_id=form.rev_code.data,
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
        return redirect(url_for('unit_summary'))
    return render_template('add_unit.html', form=form)

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
            code=form.add_code.data,
            title=form.add_unit_name.data,
            faculty_id=form.add_faculty.data,
            level=form.add_unit_level.data,
            university_id=form.add_uni.data
        )
        db.session.add(unit)
        db.session.commit()
        flash("Unit added successfully!")
        return redirect(url_for('unit_summary'))
    return render_template('add_unit.html', form=form)

@application.route('/search_results', methods=['GET'])
def search_results():  
    all_units = Unit.query.all()

    return render_template('unit_search.html', results=all_units)