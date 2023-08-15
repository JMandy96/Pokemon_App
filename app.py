from flask import Flask, request, render_template
import requests

app = Flask(__name__)
pokemon_collection= []
storage = []
@app.route('/', methods=['GET', 'POST'])
def get_pokedex_num():
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
            return render_template('pokedex.html', pokemon_set=pokemon_collection, storage = storage)
        
        if action == 'release':
            release_pokemon(request.form.get('pokemon_name'))
            return render_template('pokedex.html', pokemon_set=pokemon_collection, storage = storage)
    
    return render_template('pokedex.html')





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
            'ability': pokemon["abilities"][0]["ability"]["name"],
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