from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    email = StringField('Enter your email:', validators=[DataRequired()])
    username = StringField('Create a username:', validators=[DataRequired()])
    password = PasswordField('Create a password:', validators=[DataRequired()])
    study_field = StringField('Enter your study field:', validators=[DataRequired()])
    submit = SubmitField('Join for free')

def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Username already taken.")
