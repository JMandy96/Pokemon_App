from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email Address: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Sign In')

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Register')


class PokedexForm(FlaskForm):
    pokemon = StringField('Pokemon:')
    submit = SubmitField('search')

class ReleaseForm(FlaskForm):
    action = StringField()
    pokemon_name = StringField('Release:')
    submit_release = SubmitField('Release')

class SendToStorageForm(FlaskForm):
    action = StringField()
    move_to_storage = StringField('Send to storage:')
    submit_send_to_storage = SubmitField('Send to Storage')

class RemoveForm(FlaskForm):
    action = StringField()
    stored = StringField('Release:')
    submit_remove = SubmitField('Release')

class SendToPartyForm(FlaskForm):
    action = StringField()
    move_to_party = StringField('Send to Party:')
    submit_send_to_party = SubmitField('Send to Party')