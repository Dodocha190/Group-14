from app import application
from flask import render_template, redirect, url_for, flash
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm
from .models import db, User
from flask_login import login_user, logout_user, login_required, current_user

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/dashboard') #temporary, somewhere to go to after successful login
@login_required
def dashboard():
    return f"Welcome, {current_user.username}!"

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('application.login'))
    return render_template('sign_up_page.html', form=form)

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.guest.data:
            guest_user = User.query.filter_by(username='guest').first()
            if not guest_user:
                guest_user = User(username='guest')
                guest_user.set_password('')
                db.session.add(guest_user)
                db.session.commit()
            login_user(guest_user)
            return redirect(url_for('application.dashboard')) #dashboard for now, will decide on it later
        else:
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('application.dashboard')) #same
            flash("Invalid username or password.")

    return render_template('login_page.html', form=form)

@application.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('application.login'))
