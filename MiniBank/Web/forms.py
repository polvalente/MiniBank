from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class CreateUserForm(FlaskForm):
    username = StringField('name', validators=[DataRequired()])
    is_person = BooleanField('is_person', validators=[])
