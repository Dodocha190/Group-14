from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, SelectMultipleField, FloatField, FieldList, FormField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional
from app.models import AssessmentType


class AddUnitForm(FlaskForm):
    add_uni = StringField("University:", validators=[DataRequired()])
    add_faculty = StringField("Faculty:", validators=[DataRequired()])
    add_code = StringField("Unit code:", validators=[DataRequired()])
    add_unit_name = StringField("Unit name:", validators=[DataRequired()])
    add_unit_level = IntegerField("Unit level:", validators=[DataRequired(), NumberRange(min=1, max=10, message="Please enter a valid unit level")])
    add_submit = SubmitField("Submit")

def create_review_form():
    class ReviewForm(FlaskForm):
        rev_semester = IntegerField("Semester:", validators=[DataRequired(), NumberRange(min=1, max=5, message="Please enter a valid semester")])
        rev_year = IntegerField("Year taken:", validators=[DataRequired(), NumberRange(min=1900, max=2050, message="Please enter a valid year")])
        rev_unit_coord_rating = RadioField("Rate the unit coordinator from 1 to 5 (1 being poor, 5 being amazing)",
                                choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
        rev_difficulty = RadioField("Rate the difficulty of the unit from 1 to 5 (1 being easy, 5 being difficult)",
                                    choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
        rev_hours = IntegerField("Hours of contact per week:", validators=[DataRequired()])
        rev_grade = FloatField("Your grade:", validators=[DataRequired(), NumberRange(min=0, max=100)])
        rev_avg_hours = IntegerField("Average hours of study per week:", validators=[DataRequired()])
        rev_rating = RadioField("Rate the unit overall",
                                choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
        rev_comments=StringField("Add any additional comments regarding the unit:")
        rev_submit = SubmitField("Submit")
        assessment_fields = AssessmentType.query.all()  # Get assessment types
        for assessment in assessment_fields:
            field_name = f"assessment_{assessment.name.lower().replace(' ', '_')}"
            field_label = f"{assessment.name}"
            locals()[field_name] = BooleanField(field_label, default=False) 

        def get_selected_assessments(self):
            selected_assessments = []
            for field_name, field in self._fields.items():
                print(f"Field name: {field_name}, Field data: {field.data}")
                if field_name.startswith("assessment_") and field.data == True:
                    assessment_name = field_name.replace("assessment_", "").replace("_", " ").title()
                    selected_assessments.append(assessment_name)
                    print(f"Selected assessment: {assessment_name}")
            return selected_assessments

    return ReviewForm()