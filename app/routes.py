from app import application
from flask import render_template
from app.forms.login_form import LoginForm
from app.forms.sign_up_form import SignUpForm

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/signup')
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Handle sign-up logic here
        pass
    return render_template('sign_up_page.html', form=form)

@application.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle login logic here
        pass

    return render_template('login_page.html', form=form)