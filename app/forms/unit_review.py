from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, SelectMultipleField, FloatField
from wtforms.validators import DataRequired, NumberRange


class AddUnitForm(FlaskForm):
    add_uni = StringField("University:", validators=[DataRequired()])
    add_faculty = StringField("Faculty:", validators=[DataRequired()])
    add_code = StringField("Unit code:", validators=[DataRequired()])
    add_unit_name = StringField("Unit name:", validators=[DataRequired()])
    add_unit_level = IntegerField("Unit level:", validators=[DataRequired(), NumberRange(min=1, max=10, message="Please enter a valid unit level")])
    add_submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    rev_uni = StringField("University:", validators=[DataRequired()])
    rev_semester = IntegerField("Semester:", validators=[DataRequired()])
    rev_code = StringField("Unit code:", validators=[DataRequired()])
    rev_year = IntegerField("Year taken:", validators=[DataRequired(), NumberRange(min=1900, max=2050, message="Please enter a valid year")])
    rev_unit_coord_rating = RadioField("Rate the unit coordinator from 1 to 5 (1 being poor, 5 being amazing)",
                             choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    rev_difficulty = RadioField("Rate the difficulty of the unit from 1 to 5 (1 being easy, 5 being difficult)",
                                 choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    rev_hours = IntegerField("Hours of contact per week:", validators=[DataRequired()])
    rev_assessments = SelectMultipleField("Select all graded assessments",
                                         choices=[('final', 'Final exam'), ('midsem', 'Midsemester exam'), ('project', 'Individual project'), ('group', 'Group project'), ('essay', 'Essay'), ('test', 'Test/quiz'), ('lab', 'Labs'), ('participation', 'Participation/attendance'), ('other', 'Other')], validators=[DataRequired()])
    # need to make subform for user to enter weighting of assessments
    rev_grade = FloatField("Your grade:", validators=[DataRequired(), NumberRange(min=0, max=100)])
    rev_avg_hours = IntegerField("Average hours of study per week:", validators=[DataRequired()])
    rev_rating = RadioField("Rate the unit overall",
                            choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    rev_submit = SubmitField("Submit")