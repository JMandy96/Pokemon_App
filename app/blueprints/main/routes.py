from . import main
from app.blueprints.auth import auth
from flask import render_template, request, flash,redirect, url_for
import requests
from .forms import PokedexForm
from flask_login import current_user, login_required
from app.models import Pokemon, db, User
import random


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
                    current_hp=pokemon_info[0]['current_hp'],
                    base_defense=pokemon_info[0]['base_defense'],
                    base_attack=pokemon_info[0]['base_attack'],
                    abilities=pokemon_info[0]['abilities']
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
                    current_hp=pokemon_info[0]['current_hp'],
                    base_defense=pokemon_info[0]['base_defense'],
                    base_attack=pokemon_info[0]['base_attack'],
                    abilities=pokemon_info[0]['abilities']
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
                    current_hp=pokemon_info[0]['current_hp'],
                    base_defense=pokemon_info[0]['base_defense'],
                    base_attack=pokemon_info[0]['base_attack'],
                    abilities=pokemon_info[0]['abilities']
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

    pokemon_li = []
    for pokemon in data:
        if len(pokemon["abilities"]) == 1:
            ability_string = pokemon["abilities"][0]["ability"]["name"]
        else:
            ability_string = pokemon["abilities"][0]["ability"]["name"] + ", " + pokemon["abilities"][1]["ability"]["name"]
        pokemon_set = {
            'sprite': pokemon["sprites"]["front_shiny"],
            'pokedex_number': pokemon['id'],
            'pokemon_name': pokemon["forms"][0]["name"],
            'element':pokemon["types"][0]["type"]["name"],
            'base_hp': pokemon["stats"][0]["base_stat"],
            'current_hp': pokemon["stats"][0]["base_stat"],
            'base_defense': pokemon["stats"][2]["base_stat"],
            'base_attack': pokemon["stats"][1]["base_stat"],
            'abilities': ability_string
        }
        pokemon_li.append(pokemon_set)
    return pokemon_li



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
    form = PokedexForm()
    url = 'https://pokeapi.co/api/v2/pokemon?limit=151'
    response = requests.get(url)
    
    if response.ok:
        data = response.json()
        pokemon_results = data['results']
        existing_pokemon_names = [pokemon.name for pokemon in current_user.partied_pokemon] + [pokemon.name for pokemon in current_user.stored_pokemon]
        filtered_pokemon = [pokemon for pokemon in pokemon_results if pokemon['name'] not in existing_pokemon_names] 

        random_pokemon = random.sample(filtered_pokemon,10)
        
        random_pokemon_list = []
      
        for pokemon in random_pokemon:
            pokemon_url = pokemon['url']
            pokemon_response = requests.get(pokemon_url)
            
            if pokemon_response.ok:
                pokemon_data = pokemon_response.json()
                pokemon_info = get_pokemon_info([pokemon_data])  
                
                random_pokemon_list.append(pokemon_info[0])
        
        return render_template('all_pokemon.html', pokemon_list=random_pokemon_list, form=form)
    
    return render_template('all_pokemon.html', error='Failed to fetch Pokémon data')


@main.route('/trainers')
def all_trainers():
    trainers = User.query.filter(User.id != current_user.id).all()
    return render_template('trainers.html', trainers=trainers)

@main.route('/battle/<int:user_id1>/<int:user_id2>', methods=['GET', 'POST'])
@login_required
def battle(user_id1, user_id2):
    user1 = current_user
    user2 = User.query.get(user_id2)
    
    user1_pokemon = user1.partied_pokemon.all()
    user2_pokemon = user2.partied_pokemon.all() 
    
    battle_results = []
    
    while user1_pokemon and user2_pokemon:


        user1_pokemon[0].current_hp, user2_pokemon[0].current_hp = battle_pokemon(user1, user1_pokemon[0], user2, user2_pokemon[0])

        battle_results.append((user1_pokemon[0], user2_pokemon[0]))
        
        if user1_pokemon[0].current_hp <= 0:
            user1_pokemon.pop(0)
        
        if user2_pokemon[0].current_hp <= 0:
            user2_pokemon.pop(0)


    winner = None

    if not user1_pokemon:
        winner = user2
        flash(f"{user2.first_name} has defeated you, reform your team and get your revenge!", 'danger')
    elif not user2_pokemon:
        winner = user1
        flash(f"congratulations {current_user.first_name} YOU WON!!", "success")

    

    return render_template('battle.html', user1=user1, user2=user2, battle_results=battle_results, winner=winner, flash=flash)

def battle_pokemon(attacker_user, attacker_pokemon, defender_user, defender_pokemon):
    attacker_current_health = attacker_pokemon.current_hp
    defender_current_health = defender_pokemon.current_hp
    
    while attacker_current_health > 0 and defender_current_health > 0:
        damage_to_defender = max(0, attacker_pokemon.base_attack - defender_pokemon.base_defense)
        defender_current_health -= damage_to_defender
        
        
        if defender_current_health <= 0:
            break
        
        damage_to_attacker = max(0, defender_pokemon.base_attack - attacker_pokemon.base_defense)
        attacker_current_health -= damage_to_attacker
    
    return attacker_current_health, defender_current_health