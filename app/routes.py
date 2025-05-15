from flask import render_template, redirect, url_for, flash, request
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm

from app.forms.unit_review import AddUnitForm, create_review_form
from app.forms.share_form import ShareDiaryForm
from .models import db, User, Unit, DiaryEntry, Faculty, AssessmentType, UnitAssessmentType, DiaryShare
import difflib
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
from .controllers import *
from app.blueprints import blueprint
from app import db

@blueprint.route('/')
def home():
    return render_template('intro.html')

@blueprint.route('/unit-summary/<unit_id>')
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
    assessment_types=get_assessment_types_for_unit(unit_id)
    return render_template('unit_summary.html', unit=unit, avg_rating=avg_rating, unit_reviews=unit_reviews, review_count=review_count, workload=avg_workload, difficulty_level=difficulty_level, unit_coord_rating=unit_coord_rating, overall_rating_count=overall_rating_count, assessment_types=assessment_types)


@blueprint.route('/dashboard') #temporary, somewhere to go to after successful login
def dashboard():
    return redirect(url_for('blueprint.diary', user_id=current_user.id))


@blueprint.route('/signup', methods=['GET', 'POST'])
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
        print('User added:', user)
        users = User.query.all()
        print('All users:', users)
        flash("Registration successful. Please log in.")
        return redirect(url_for('blueprint.login'))
    flash("Please fill in all fields.")
    return render_template('sign_up_page.html', form=form)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('blueprint.dashboard'))  # Redirect if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        print('Form submitted')
        print('Email entered:', form.email.data)
        print("All users: ", User.query.all())
        user = User.query.filter_by(email=form.email.data).first()
        print('User found:', user)
        print('Password entered:', form.password.data)
        if user:
            print('User exists')
            flash('User exists')
        if user and user.check_password(form.password.data):
            print('Password is correct')
            login_user(user) 
            return redirect(url_for('blueprint.dashboard')) 
        else:
            flash('Invalid email or password.')

    return render_template('login_page.html', form=form)
  
@blueprint.route('/unit_diary/<int:user_id>', methods=['GET'])
def diary(user_id):
    units_taken = get_diary_entries_from_user(user_id)
    total_units = get_total_units_logged(user_id)
    highest_wam_area = get_highest_wam_faculty(user_id)
    percent_by_faculty = get_percentage_by_faculty(user_id)
    total_credits = get_total_credits_passed(user_id)
    avg_difficulty = get_average_difficulty(user_id)
    is_shared_view=False
    user=current_user
    if user_id != current_user.id:
        user = User.query.get(user_id)
        is_shared_view=True
    return render_template('unitdiary.html', show_user_info=True, user=user,units_taken=units_taken,
                           highest_wam_area=highest_wam_area, percent_by_faculty=percent_by_faculty, total_credits=total_credits, avg_difficulty=avg_difficulty, is_shared_view=is_shared_view)

@blueprint.route('/submit_review', methods=['GET', 'POST'])
def review():
    form = create_review_form()
    if form.validate_on_submit():
        unit = Unit.query.filter_by(code=form.rev_code.data).first()
        if not unit:
            flash("Unit not found.")
            return redirect(url_for('blueprint.add_unit'))
        existing_entry = DiaryEntry.query.filter_by(
        user_id=current_user.id,
        unit_id=unit.id,
        semester=form.rev_semester.data
        ).first()

        if existing_entry:
            flash("You have already submitted a review for this unit in this semester.")
            return redirect(url_for('blueprint.dashboard')) 

        dataEntry = DiaryEntry(
            user_id=current_user.id, 
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

        unit = Unit.query.filter_by(code=form.rev_code.data).first()
        selected_assessments = form.get_selected_assessments()
        if selected_assessments:
            for assessment in selected_assessments:
                assessment_id=AssessmentType.query.filter_by(name=assessment).first().id
                existing_association = UnitAssessmentType.query.filter_by(
                            unit_id=unit.id,
                            assessment_type_id=assessment_id
                        ).first()
                if not existing_association:
                    association = UnitAssessmentType(
                        unit_id=unit.id,
                        assessment_type_id=assessment_id
                    )
                    db.session.add(association)
        
        db.session.commit()
        flash('Review submitted successfully!')
        return redirect(url_for('blueprint.dashboard'))
    return render_template('unit_review.html', form=form)

@blueprint.route('/add_unit', methods=['GET', 'POST'])
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
        return redirect(url_for('blueprint.search_results'))
    return render_template('add_unit.html', form=form)

@blueprint.route('/search_results', methods=['GET'])
def search_results():  
    all_units = Unit.query.all()

    return render_template('unit_search.html', results=all_units)

@blueprint.route('/logout')
@login_required
def logout():
    """
    Logs the user out and redirects them to the login page.
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('blueprint.login'))


#shared diaries page!!
@blueprint.route('/shared-diaries')
@login_required
def shared_diaries():
    # Get shares where the current user is the recipient
    shares = DiaryShare.query.filter_by(recipient_id=current_user.id).all()

    diaries = []
    for s in shares:
        owner = User.query.get(s.owner_id)
        if owner:
            diaries.append({
                "user_id": owner.id,
                "username": owner.username,
                "faculty": owner.study_field
            })
    
    form = ShareDiaryForm()

    return render_template(
        "shared_diaries.html",
        diaries=diaries,
        show_user_info=True,
        share_form=form
    )


#pop up form to share your diary with new user
@blueprint.route('/share-form', methods=['POST'])
@login_required
def share_form():
    form = ShareDiaryForm()
    
    if form.validate_on_submit():
        recipient = User.query.filter_by(email=form.recipient_email.data).first()

        if not recipient:
            flash('User not found with that email.', 'danger')
        elif recipient.id == current_user.id:
            flash('You cannot share your diary with yourself.', 'warning')
        else:
            existing_share = DiaryShare.query.filter_by(owner_id=current_user.id, recipient_id=recipient.id).first()
            if existing_share:
                flash('You’ve already shared your diary with this user.', 'info')
            else:
                new_share = DiaryShare(owner_id=current_user.id, recipient_id=recipient.id)
                db.session.add(new_share)
                db.session.commit()
                flash(f'Shared your diary with {recipient.email}!', 'success')

        return redirect(url_for('blueprint.shared_diaries'))

    return render_template('shared_diaries.html', form=form)


# view shared diary page
@blueprint.route('/shared-diary/<int:user_id>')
@login_required
def view_shared_diary(user_id):
    # Check permission
    share = DiaryShare.query.filter_by(recipient_id=current_user.id, owner_id=user_id).first()

    if not share:
        flash("You don't have permission to view this diary.", "danger")
        return redirect(url_for('blueprint.shared_diaries'))
    owner = User.query.get_or_404(user_id)
    entries = DiaryEntry.query.filter_by(user_id=user_id).all()

    return redirect(url_for('blueprint.diary', user_id=user_id))  