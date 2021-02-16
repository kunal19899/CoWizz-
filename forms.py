from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class InputForm(FlaskForm):
    periodLength = SelectField(label="Period Length", choices=["Select a Period Length", 3, 5, 7, 10, 14], validators=[DataRequired()])
    start_of_startDate = DateField('Start Date', format = '%d/%m/%Y', validators=[DataRequired()])
    start_of_endDate = DateField('End Date', validators=[DataRequired()])
    interval = SelectField(label='% Interval', choices=["% Interval", 1,2,3,4,5,6,7,8], validators=[DataRequired()])
    submit = SubmitField()
