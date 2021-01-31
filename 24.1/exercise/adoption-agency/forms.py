from flask_wtf import FlaskForm, validators
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Optional, NumberRange


class PetForm(FlaskForm):
    name = StringField('Pet Name*',
                       validators=[InputRequired(message='Pet Name is required')])
    species = StringField('Species*',
                          validators=[InputRequired(message='Species is required')])
    photo_url = StringField('Photo URL')
    age = IntegerField('Age',
                       validators=[Optional(), NumberRange(0, 150, message='Age must be between 0 and 150 or empty.')])
    notes = StringField('Notes')
    available = BooleanField('Available', default='yes')
