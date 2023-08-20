from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
import requests
from app import app
from .forms import LoginForm, SignupForm, PokedexForm
from flask_login import current_user, login_user,logout_user, login_required
from .models import User, db
from werkzeug.security import check_password_hash

pokemon_collection= []
storage = []
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'welcome back, {current_user.first_name}!!', category='success')
        return redirect(url_for('get_pokedex_num'))
    form = LoginForm(request.form)
    flash_message = None
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        #query user object from database
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'welcome back, {queried_user.first_name}!!', category='success')
            
            return render_template('pokedex.html',current_user=current_user)
        elif queried_user and not check_password_hash(queried_user.password, password):
            flash("you have input the wrong password, please try again.",  category='danger')    
            return render_template('login.html', form=form)
        else:
            flash_message = f"That username does not exist, please sign up:"
            flash(flash_message, 'primary')
            
            return redirect(url_for('sign_up'))



    else:
        return render_template('login.html', form=form)
    
@app.route('/signup', methods = ['GET','POST'])
def sign_up():
    form = SignupForm()


    if request.method == 'POST' and form.validate_on_submit():
        
        # grabbing our sign up form data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        ## create an instance of the user model

        queried_user = User.query.filter(User.email == email).first()
        if queried_user is not None:
            flash('A user with that email already exists, please sign in.', category='danger')
            return render_template('login.html', form=form)

        new_user = User(first_name, last_name, email, password)
        ## adds new user to db
        db.session.add(new_user)
        db.session.commit()

        flash(f'Welcome {new_user.first_name}, {new_user.last_name}!!', category='primary')
        return redirect(url_for('get_pokedex_num', flash=flash))


        # return redirect(url_for('get_pokedex_num'))
    else:
        return render_template('signup.html', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('login'))

@app.route('/pokedex', methods=['GET','POST'])
@login_required
def get_pokedex_num():
    form = PokedexForm()
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
                pokemon_store = get_pokemon_info(pokemon_info_data)
                storage.append(pokemon_store)
            return render_template('pokedex.html', pokemon_set=pokemon_collection, storage = storage)
        
        if action == 'release':
            release_pokemon(request.form.get('pokemon_name'))
            return render_template('pokedex.html', form=form, pokemon_set=pokemon_collection, storage = storage)
    
    return render_template('pokedex.html', form=form, pokemon_set=pokemon_collection, storage = storage)





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