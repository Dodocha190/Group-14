from app import application
from flask import render_template, redirect, url_for, flash
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm
from .models import db, User

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
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))
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
