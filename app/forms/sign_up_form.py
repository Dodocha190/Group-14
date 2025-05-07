from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User

class SignUpForm(FlaskForm):
    email = StringField('Enter your email:', validators=[
        DataRequired(message="Email is required."),
        Email(message="Enter a valid email address.")])
    username = StringField('Create a username:', validators=[DataRequired()])
    password = PasswordField('Create a password:', validators=[DataRequired()])
    study_field = StringField('Enter your major:', validators=[DataRequired()])
    submit = SubmitField('Join for free')

def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("An account with this email already exists.")
