from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DecimalField
from wtforms.validators import DataRequired

class CreateUserForm(FlaskForm):
    username = StringField('name', validators=[DataRequired()])
    is_person = BooleanField('is_person', validators=[])

class CreateAccountForm(FlaskForm):
    owner_id = IntegerField('owner_id', validators=[DataRequired()])
    initial_balance = DecimalField('initial_balance', places=2, render_kw={'placeholder': 0})
