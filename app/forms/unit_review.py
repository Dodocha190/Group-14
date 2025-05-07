from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class addUnitForm(FlaskForm):
    adduni = StringField("Universtiy:", validators=[DataRequired()])
    addfaculty = StringField("Faculty:", validators=[DataRequired()])
    addcode = StringField("Unit code:", validators=[DataRequired()])
    addunitname = StringField("Unit name:", validators=[DataRequired()])
    addsubmit = SubmitField("Submit")


class reviewForm(FlaskForm):
    revuni = StringField("Universtiy:", validators=[DataRequired()])
    revcode = StringField("Unit code:", validators=[DataRequired()])
    revunitco = RadioField("Rate the unit coordinator from 1 to 5 (1 being poor, 5 being amazing)",
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    revdifficulty = RadioField("Rate the difficulty of the unit from 1 to 5 (1 being easy, 5 being difficult)",
                               choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    revhours = IntegerField("Hours of contact per week:", validators=[DataRequired()])
    revassessments = SelectMultipleField("Seect all graded assessments",
                                choices=[('final','Final exam'), ('midsem','Midsemester exam'), ('project','Individual project'), ('group','Group project'), ('essay','Essay'), ('test','Test/quiz'), ('lab','Labs'), ('participation','Participation/attendance'), ('other','Other')], validators=[DataRequired()])
    #need to make subform for user to enter weighting of assessments
    revrating = RadioField("Rate the unit overall",
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    revsubmit = SubmitField("Submit")