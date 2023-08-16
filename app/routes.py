from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
import requests
from . import app
from .forms import LoginForm
REGISTERED_USERS ={}

pokemon_collection= []
storage = []
@app.route('/', methods=['GET', 'POST'])
def login():
    flash_message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in REGISTERED_USERS and password == REGISTERED_USERS[email]['password']:
            flash_message = f'welcome back, {email}!'
            flash(flash_message)
            return redirect(url_for('get_pokedex_num'))
        else:
            if email not in REGISTERED_USERS:
                REGISTERED_USERS[email] = {'password':password}
                flash_message = f"Welcome, {email}"
                flash(flash_message)
                return redirect(url_for('get_pokedex_num'))
            else:
                flash_message = 'a user with that email already exists, check your password.'
                flash(flash_message)
                return render_template('login.html', flash_message=flash)


    else:
        return render_template('login.html')

@app.route('/pokedex', methods=['GET','POST'])
def get_pokedex_num():
    flash_messages = get_flashed_messages()
    if request.method == 'POST':
        action = request.form.get('action')
        number = request.form.get('number')
        url = f'https://pokeapi.co/api/v2/pokemon/{number}'
        response = requests.get(url)
        
        if response.ok:
            data = response.json()
            pokemon_info_data = [data]  
            pokemon = get_pokemon_info(pokemon_info_data)
            pokemon_collection.extend(pokemon)
            if len(pokemon_collection) >= 6:
                data = response.json()
                pokemon_info_data = [data]  
                pokemon_store = get_pokemon_info(pokemon_info_data)
                storage.append(pokemon_store)
            return render_template('pokedex.html', pokemon_set=pokemon_collection, storage = storage, flash_message=flash_messages)
        
        if action == 'release':
            release_pokemon(request.form.get('pokemon_name'))
            return render_template('pokedex.html', pokemon_set=pokemon_collection, storage = storage)
    
    return render_template('pokedex.html', pokemon_set=pokemon_collection, storage = storage, flash_message=flash_messages)





def get_pokemon_info(data):
    pokemon_data = []
    for pokemon in data:
        pokemon_dict = {
            'sprite': pokemon["sprites"]["front_shiny"],
            'pokedex_number': pokemon['id'],
            'pokemon_name': pokemon["forms"][0]["name"],
            'base_hp': pokemon["stats"][1]["base_stat"],
            'base_defense': pokemon["stats"][2]["base_stat"],
            'base_attack': pokemon["stats"][0]["base_stat"],
            'ability': pokemon["abilities"][0]["ability"]["name"] + ", " + pokemon["abilities"][1]["ability"]["name"]
        }
        pokemon_data.append(pokemon_dict)
    return pokemon_data

def release_pokemon(pokemon_name):

    for pokemon in pokemon_collection:
        if pokemon['pokemon_name'] == pokemon_name:
            pokemon_collection.remove(pokemon) 

    for stored_pokemon in storage:
        if stored_pokemon['pokemon_name'] == pokemon_name:
            storage.remove(stored_pokemon)