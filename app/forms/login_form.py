from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Enter your email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter your password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    guest = BooleanField('Continue as Guest')

    def validate(self, extra_validators=None):
        # default Flask-WTF validators (email format, required fields, etc.)
        rv = super().validate(extra_validators)
        if not rv:
            return False
        
        # If not logging in as guest, ensure email and password are filled
        if not self.guest.data:
            if not self.email.data:
                self.email.errors.append("Email is required.")
                return False
            if not self.password.data:
                self.password.errors.append("Password is required.")
                return False

        return True
