from app import application
from flask import render_template, redirect, url_for, flash, request
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm
from app.forms.unit_review import AddUnitForm
from app.forms.unit_review import ReviewForm
from .models import db, User, Unit, DiaryEntry, Faculty, AssessmentBreakdown
import difflib
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .controllers import *

@application.route('/')
def home():
    return render_template('intro.html')

@application.route('/unit-summary/<unit_id>')
def unit_summary(unit_id):
    unit= db.session.get(Unit, unit_id)
    review_exists = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).first()
    if not review_exists:
        flash("No reviews found for this unit.")
        return render_template('unit_summary.html', no_reviews=True)
    avg_rating=get_avg_rating_for_unit(unit_id)
    avg_workload=get_workload_avg_for_unit(unit_id)
    unit_reviews = get_optional_comments_for_unit(unit_id)  
    review_count = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).count()
    unit_coord_rating = avg_rating_for_unit_coord(unit_id)
    difficulty_level = get_difficulty_rating_avg_for_unit(unit_id)
    overall_rating_count = get_overall_rating_count_for_unit(unit_id)
    return render_template('unit_summary.html', unit=unit, avg_rating=avg_rating, unit_reviews=unit_reviews, review_count=review_count, workload=avg_workload, difficulty_level=difficulty_level, unit_coord_rating=unit_coord_rating, overall_rating_count=overall_rating_count)


@application.route('/dashboard') #temporary, somewhere to go to after successful login
def dashboard():
    units_taken = get_diary_entries_from_user(current_user.email)
    return render_template('unitdiary.html', show_user_info=True, user_email=current_user.email, units_taken=units_taken)

def get_diary_entries_from_user(user_email):
    """
    Fetches all diary entries associated with a given user email, including their units.
    """ 
    query = db.session.query(DiaryEntry, Unit).join(Unit, DiaryEntry.unit_id == Unit.id).order_by(DiaryEntry.year.desc(), DiaryEntry.semester.desc())
    results = query.filter(DiaryEntry.user_email == user_email).all()
    return results

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
        existing_entry = DiaryEntry.query.filter_by(
        user_email=current_user.email,
        unit_id=unit.id,
        semester=form.rev_semester.data
        ).first()

        if existing_entry:
            flash("You have already submitted a review for this unit in this semester.")
            return redirect(url_for('dashboard')) 
        dataEntry = DiaryEntry(
            user_email=current_user.email, 
            unit_id=unit.id,
            semester=form.rev_semester.data,
            year=form.rev_year.data,
            grade=form.rev_grade.data,
            overall_rating=form.rev_rating.data,
            difficulty_rating=form.rev_difficulty.data,
            coordinator_rating=form.rev_unit_coord_rating.data,
            workload_hours_per_week=form.rev_avg_hours.data,
            optional_comments=form.rev_comments.data
        )

        db.session.add(dataEntry)
        db.session.commit()
    # TODO: Refine this section to add assessment breakdowns
    #     selected_assessments = form.rev_assessments.data
    #     for assessment_value in selected_assessments:
    #         weight_field_name = f'weight_{assessment_value}'
    #         weight = request.form.get(weight_field_name)
    #         if weight:
    #             assessment = AssessmentBreakdown(
    #                 entry_id=diary_entry.id,
    #                 type=assessment_value,
    #                 percentage=int(weight)
    #             )
    #             db.session.add(assessment)

    # try:
    #     db.session.commit()
    #     flash('Review submitted successfully!', 'success')
    # except Exception as e:
    #     db.session.rollback()
    #     flash(f'Error saving review: {str(e)}', 'error')
    flash('Review submitted successfully!')
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

@application.route('/shared_diary', methods=['GET', 'POST'])
def shared_diary():
    """
    Displays the shared diary entries for the current user.
    """
    return render_template('unit_search.html')