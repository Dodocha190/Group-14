from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class reviewForm(FlaskForm):
    revuni = StringField("Universtiy:", validators=[DataRequired()])
    revfaculty = StringField("Faculty:", validators=[DataRequired()])
    revcode = StringField("Unit code:", validators=[DataRequired()])
    #could have validator that checks if unit code is already in database - do both submit a review and add a new unit in one form
    revunitname = StringField("Unit name:", validators=[DataRequired()])
    revunitco = RadioField("Rate the unit coordinator from 1 to 5 (1 being poor, 5 being amazing)",
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    revdifficulty = RadioField("Rate the difficulty of the unit from 1 to 5 (1 being easy, 5 being difficult)",
                               choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    revhours = IntegerField("Hours of contact per week:", validators=[DataRequired()])
    revassessments = SelectMultipleField("Tick all graded assessments",
                                choices=[('final','Final exam'), ('midsem','Midsemester exam'), ('project','Individual project'), ('group','Group project'), ('essay','Essay'), ('test','Test/quiz'), ('lab','Labs'), ('participation','Participation/attendance'), ('other','Other')], validators=[DataRequired()])
    #need to make subform for user to enter weighting of assessments
    revrating = RadioField("Your overall rating of the unit:",
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    revsubmit = SubmitField("Submit")