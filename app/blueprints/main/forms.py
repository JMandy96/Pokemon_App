from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField



class PokedexForm(FlaskForm):
    pokemon = StringField('pokemon')
    action = SelectField('action', choices=[('capture', 'Capture'), ('store','Store')])
    search = SubmitField('Capture')
    release_pokemon_name = StringField('Release Pokémon Name')
    release_submit = SubmitField('Release')
