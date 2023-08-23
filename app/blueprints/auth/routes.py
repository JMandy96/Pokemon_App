from . import auth
from .forms import LoginForm, SignupForm
from flask import request, flash, redirect, render_template, url_for
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user


@auth.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'welcome back, {current_user.first_name}!!', category='success')
        return redirect(url_for('main.catchpokemon', user_id=current_user.id))
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        #query user object from database
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'welcome back, {queried_user.first_name}!!', category='success')
            
            return redirect(url_for('main.catchpokemon', user_id= current_user.id))
        elif queried_user and not check_password_hash(queried_user.password, password):
            flash("you have input the wrong password, please try again.",  category='danger')    
            return render_template('login.html', form=form)
        else:
           
            flash(f"That username does not exist, please sign up:", 'primary')
            
            return redirect(url_for('auth.sign_up'))

    else:
        return render_template('login.html', form=form)
    
@auth.route('/signup', methods = ['GET','POST'])
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
        return redirect(url_for('main.catchpokemon', flash=flash, user_id= current_user.id))


        # return redirect(url_for('get_pokedex_num'))
    else:
        return render_template('signup.html', form=form)
    
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.login'))