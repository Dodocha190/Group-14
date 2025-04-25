from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from .models import db, User
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

#Login route
@main.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('main.dashboard'))
        else:
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('main.dashboard'))
            flash("Invalid username or password.")
    return render_template('login.html', form=form)

#Register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

#An example of how to implement certain sections that only logged in users can access (like an account dashboard)
@main.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome, {current_user.username}!"

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.login'))
