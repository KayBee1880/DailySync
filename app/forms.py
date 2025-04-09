
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class HabitForm(FlaskForm):
    habit_name = StringField('Habit Name')
    submit = SubmitField('Submit')
