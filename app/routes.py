from app import application
from flask import render_template, redirect, url_for, flash, request 
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm
from app.forms.unit_review import addUnitForm
from app.forms.unit_review import reviewForm
from .models import db, User
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required

@application.route('/')
def home():
    return render_template('intro.html')

@application.route('/unit-summary')
def unit_summary():
    return render_template('unit_summary.html')


@application.route('/userhome') #temporary, somewhere to go to after successful login
def userhome():
        return render_template('userhome.html', show_user_info=True, user_email=current_user.username)

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
            study_field=form.study_field.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))
    return render_template('sign_up_page.html', form=form)

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('userhome'))
        flash("Invalid email or password.")

    return render_template('login_page.html', form=form)

@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))  

@application.route('/search')
def search():
    return render_template('unit_search.html')


@application.route('/submit_review')
def review():
    form = reviewForm()
    return render_template('unit_review.html', form=form)

@application.route('/add_unit')
def addunit():
    form = addUnitForm()
    return render_template('add_unit.html', form=form)