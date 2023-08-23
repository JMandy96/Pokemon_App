from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField



class PokedexForm(FlaskForm):
    pokemon = StringField('pokemon')
    action = SelectField('action', choices=[('capture', 'Capture'), ('release','Release'), ('store','Store')])
    search = SubmitField('Search')