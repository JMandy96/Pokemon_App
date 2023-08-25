from . import main
from app.blueprints.auth import auth
from flask import render_template, request, flash,redirect, url_for
import requests
from .forms import PokedexForm
from flask_login import current_user, login_required
from app.models import Pokemon, db, User


@main.route('/pokedex/<int:user_id>', methods=['GET', 'POST'])
@login_required
def catchpokemon(user_id):

    form = PokedexForm()
    captured_pokemon_list = current_user.partied_pokemon.all()
    stored_pokemon_list = current_user.stored_pokemon.all()

    if request.method == 'POST' and form.validate_on_submit():
        action = form.action.data
        pokemon = form.pokemon.data
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        
        if response.ok:
            data = response.json()
            pokemon_info_data = [data]  
            pokemon_info = get_pokemon_info(pokemon_info_data)
            
        if action == 'capture':
            existing_pokemon = next((p for p in captured_pokemon_list if p.name == pokemon_info[0]['pokemon_name']), None)
            if existing_pokemon:
                flash(f'You already have {pokemon_info[0]["pokemon_name"]} in your party.')
            elif len(captured_pokemon_list) < 6:
                    captured_pokemon = Pokemon(
                    sprite=pokemon_info[0]['sprite'],
                    number=pokemon_info[0]['pokedex_number'],
                    name=pokemon_info[0]['pokemon_name'],
                    element=pokemon_info[0]['element'],
                    base_hp=pokemon_info[0]['base_hp'],
                    base_defense=pokemon_info[0]['base_defense'],
                    base_attack=pokemon_info[0]['base_attack'],
                    abilities=pokemon_info[0]['ability']
                    )
                    db.session.add(captured_pokemon)
                    current_user.partied_pokemon.append(captured_pokemon) 
                    captured_pokemon_list.append(captured_pokemon)
                    db.session.commit()
                    
            else:
                stored_pokemon = Pokemon(
                    sprite=pokemon_info[0]['sprite'],
                    number=pokemon_info[0]['pokedex_number'],
                    name=pokemon_info[0]['pokemon_name'],
                    element=pokemon_info[0]['element'],
                    base_hp=pokemon_info[0]['base_hp'],
                    base_defense=pokemon_info[0]['base_defense'],
                    base_attack=pokemon_info[0]['base_attack'],
                    abilities=pokemon_info[0]['ability']
                )
                db.session.add(stored_pokemon)
                current_user.stored_pokemon.append(stored_pokemon)
                stored_pokemon_list.append(stored_pokemon)
                db.session.commit()
                stored_pokemon_list.append(stored_pokemon)
                flash(f'Your party is full. {stored_pokemon.name} has been sent to storage.')
            
        elif action == 'store':
                stored_pokemon = Pokemon(
                    sprite=pokemon_info[0]['sprite'],
                    number=pokemon_info[0]['pokedex_number'],
                    name=pokemon_info[0]['pokemon_name'],
                    element=pokemon_info[0]['element'],
                    base_hp=pokemon_info[0]['base_hp'],
                    base_defense=pokemon_info[0]['base_defense'],
                    base_attack=pokemon_info[0]['base_attack'],
                    abilities=pokemon_info[0]['ability']
                )
                db.session.add(stored_pokemon)
                db.session.commit()
                stored_pokemon_list.append(stored_pokemon)
                flash(f'{stored_pokemon.name} has been stored.')

    return render_template(
        'pokedex.html',
        form=form,
        pokemon_set=captured_pokemon_list,
        storage= stored_pokemon_list,
    )


def get_pokemon_info(data):
    pokemon_data = []
    for pokemon in data:
        pokemon_dict = {
            'sprite': pokemon["sprites"]["front_shiny"],
            'pokedex_number': pokemon['id'],
            'pokemon_name': pokemon["forms"][0]["name"],
            'element':pokemon["types"][0]["type"]["name"],
            'base_hp': pokemon["stats"][0]["base_stat"],
            'base_defense': pokemon["stats"][2]["base_stat"],
            'base_attack': pokemon["stats"][1]["base_stat"],
            'ability': pokemon["abilities"][0]["ability"]["name"] + ", " + pokemon["abilities"][1]["ability"]["name"]
        }
        pokemon_data.append(pokemon_dict)
    return pokemon_data



@main.route('/release/<int:user_id>/<pokemon_name>', methods=['GET','POST'])
@login_required
def release_pokemon(user_id, pokemon_name):
    captured_pokemon_list = current_user.partied_pokemon.all()
    stored_pokemon_list = current_user.stored_pokemon.all()

    released_pokemon = None

    for captured_pokemon in captured_pokemon_list:
        if captured_pokemon.name == pokemon_name:
            released_pokemon = captured_pokemon
            break

    for stored_pokemon in stored_pokemon_list:
         if stored_pokemon.name == pokemon_name:
            released_pokemon = stored_pokemon
            break
    
    if released_pokemon:
        db.session.delete(released_pokemon)
        db.session.commit()
        
        if released_pokemon in captured_pokemon_list:
            captured_pokemon_list.remove(released_pokemon)
        elif released_pokemon in stored_pokemon_list:
            stored_pokemon_list.remove(released_pokemon)

        flash(f'You have released your {released_pokemon.name}.')

    return redirect(url_for('main.catchpokemon', user_id=current_user.id))

@main.route('/all_pokemon')
def all_pokemon():
    pokemon_list = Pokemon.query.all()
    return render_template('all_pokemon.html', pokemon_list=pokemon_list)