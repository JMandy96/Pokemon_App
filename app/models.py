from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

partied_pokemon = db.Table(
    'partied_pokemon',
    db.Column('trainer_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('partied_pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)

stored_pokemon = db.Table(
    'stored_pokemon',
    db.Column('trainer_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('stored_pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    partied_pokemon = db.relationship('Pokemon', secondary=partied_pokemon,
                            backref=db.backref('partied_by_user', lazy='dynamic'),
                            lazy='dynamic')

    stored_pokemon = db.relationship('Pokemon', secondary=stored_pokemon,
                        backref=db.backref('stored_by_user', lazy='dynamic'),
                        lazy='dynamic')
    

    def __init__(self, first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sprite= db.Column(db.String, nullable=False)
    number= db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    element = db.Column(db.String, nullable=False)
    base_hp= db.Column(db.Integer, nullable=False)
    base_defense = db.Column(db.Integer, nullable=False)
    base_attack = db.Column(db.Integer, nullable=False)
    abilities = db.Column(db.String, nullable=False)


    def __init__(self,sprite,number,name,element,base_hp,base_defense,base_attack,abilities):
        self.sprite=sprite
        self.number=number
        self.name= name
        self.element = element
        self.base_hp = base_hp
        self.base_defense=base_defense
        self.base_attack = base_attack
        self.abilities = abilities



