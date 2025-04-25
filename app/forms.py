from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField('Sign In')
    guest = BooleanField('Continue as Guest')
    #Guest: All the reviews/search enquiry/sharing resulted will be displayed under guess and stored under guest in the database
    #Anonymous: The user chooses to go anonymous after signing in, using options/settings or clicking on anonymous when submitting the review
     
    #Server based authentication, users can't bypass even if disabling JavaScript
    def validate(self, extra_validators=None):
        #default validators (i.e. username length and password special characters, etc), there's nothing for now but will update if you guys want any validations to be fone on username and password filled in the login page
        rv = super().validate(extra_validators)
        if not rv:
            return False
        
        #If not guest, username and password must be filled out, further configuration in login.html to handle when the user chooses to continue as guest

        if not self.guest.data:
            if not self.username.data:
                self.username.errors.append("Username is required.")
                return False
            if not self.password.data:
                self.password.errors.append("Password is required.")
                return False

        return True
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Username already taken.")