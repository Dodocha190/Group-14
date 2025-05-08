from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField(
        'Enter your email',validators=[DataRequired(message="Email is required."),
                                    Email(message="Enter a valid email address.")])
    
    password = PasswordField('Enter your password', validators=[DataRequired(message="Password is required."),
                                                                Length(min=6, message="Password must be at least 6 characters long.")])
    submit = SubmitField('Log In')