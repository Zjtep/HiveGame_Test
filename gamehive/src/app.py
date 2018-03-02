from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request, redirect, url_for, jsonify

import sys
from sqlalchemy import or_
from sqlalchemy.orm import load_only


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/gamehive'


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/')
def root():
    my_player = Player.query.all()
    one_item = Player.query.filter_by(username="catman").all()
    return render_template('add_user.html', my_player=my_player, one_item=one_item)


@app.route('/create_player', methods=['POST'])
def create_player():
    # {"username": "abcd", "email": "abcd@gmail.com"}

    data = request.get_json()

    query_username = Player.query.filter_by(username=data['username']).first()
    query_user_email = Player.query.filter_by(username=data['email']).first()
    if query_username or query_user_email is not None:
        return "user already in database"
    else:
        player = Player(data['username'], data['email'])
        db.session.add(player)
        db.session.commit()
        # return jsonify(player)
        return "added user"
        # return jsonify(data['username'], data['email'])


@app.route('/edit_player', methods=['POST'])
def edit_player():
    # {"username":"bbabcde","email":"abcd@gmail.com","id":1}
    data = request.get_json()

    try:
        query_user = Player.query.filter_by(id=data['id']).first()
    except:
        return "Enter ID"

    if query_user is not None:
        Player.query.filter_by(id=query_user.id).update(dict(username=data['username'], email=data['email']))
        db.session.commit()
        return "updated user"
    else:
        return "can't find user"


@app.route('/delete_player', methods=['POST'])
def delete_player():
    # {"id":"1"}
    data = request.get_json()

    # player = Player(data['username'], data['email'])
    try:
        query_user = Player.query.filter_by(id=data['id']).first()
    except:
        return "Enter ID"

    # query_username = Player.query.filter_by(username=data['username']).first()
    # query_email = Player.query.filter_by(username=data['email']).first()

    if query_user is not None:
        # Player.query.filter_by(id=query_user.id).delete()
        Player.query.filter_by(id=query_user.id).update(dict(status='disabled'))
        db.session.commit()
        return "deleted user"
    else:
        return "cant find user"


@app.route('/add_player_to_guild', methods=['POST'])
def add_player_to_guild():
    # {"guild_id": "1", "player_id": "1"}
    data = request.get_json()
    try:
        query_user = Player.query.filter_by(id=data['player_id']).first()
        query_guild = Guild.query.filter_by(id=data['guild_id']).first()
    except:
        return "Enter player/guild"

    if query_user and query_guild is not None:
        Player.query.filter_by(id=query_user.id).update(dict(guild_id=data['guild_id']))
        db.session.commit()
        return "added to guild"
    else:
        return "cant find player or guild"


@app.route('/pickup_item', methods=['POST'])
def pickup_item():
    # {"item_id": "1", "player_id": "1"}
    data = request.get_json()

    try:
        query_user = Player.query.filter_by(id=data['player_id']).first()
        query_item = Item.query.filter_by(id=data['item_id']).first()
    except:
        return "Enter player/item"

    if query_user and query_item is not None:
        if query_user.guild_id is None:
            temp = query_user.skill_points + 1
            Player.query.filter_by(id=query_user.id).update(dict(skill_points=temp))
            db.session.commit()
            return "added to Skill"
        else:
            return "your in guild"
    else:
        return "cant find player or item"


@app.route('/create_guild', methods=['POST'])
def create_guild():
    # {"guild_name": "foodies", "country_code": "canada"}

    data = request.get_json()

    query_guild = Guild.query.filter_by(guild_name=data['guild_name']).first()

    if query_guild is not None:
        return "guide_name already in database"
    else:
        guild = Guild(data['guild_name'], data['country_code'])
        db.session.add(guild)
        db.session.commit()
        return "added guild"


@app.route('/edit_guild', methods=['POST'])
def edit_guild():
    # {"country_code":"USA","guild_name":"FunTown","id":1}
    data = request.get_json()

    try:
        query_guild = Guild.query.filter_by(id=data['id']).first()
    except:
        return "Enter ID"

    if query_guild is not None:
        Guild.query.filter_by(id=query_guild.id).update(
            dict(guild_name=data['guild_name'], country_code=data['country_code']))
        db.session.commit()
        return "updated guild_name"
    else:
        return "can't find guild_name"


@app.route('/delete_guild', methods=['POST'])
def delete_guild():
    # {"id":"1"}
    data = request.get_json()

    # player = Player(data['username'], data['email'])
    try:
        query_guild = Guild.query.filter_by(id=data['id']).first()
    except:
        return "Enter ID"

    if query_guild is not None:
        # Guild.query.filter_by(id=query_guild.id).delete()
        Guild.query.filter_by(id=query_guild.id).update(dict(status='disabled'))
        db.session.commit()
        return "deleted guild"
    else:
        return "cant find guild"


@app.route('/create_item', methods=['POST'])
def create_item():
    item = Item()
    db.session.add(item)
    db.session.commit()
    return "added item"


class Guild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild_name = db.Column(db.String(120), unique=True)
    country_code = db.Column(db.String(120), unique=False)
    players = db.relationship('Player', backref='guild', lazy='dynamic')
    status = db.Column(db.String(120), unique=False)

    def __init__(self, guild_name, country_code):
        self.guild_name = guild_name
        self.country_code = country_code
        self.status = "active"

    def __repr__(self):
        return '<Guild:{}>'.format(self.id)


item_ownership = db.Table('item_ownership',db.Model.metadata,
    db.Column('id', db.Integer, db.ForeignKey('players.id')),
    db.Column('id', db.Integer, db.ForeignKey('items.id'))
)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    skill_points = db.Column(db.Integer, unique=False)
    status = db.Column(db.String(120), unique=False)
    backpack = db.relationship('Item',secondary=item_ownership)
    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id', ondelete='CASCADE'))

    # id = db.Column(db.Integer, db.ForeignKey('sensor_data.id', ondelete='CASCADE'), primary_key=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.status = "active"
        self.skill_points = 0

    def __repr__(self):
        return '<Player:{}>'.format(self.id)




if __name__ == '__main__':
    # bob = Player(username='Bob', email='bob@gmail.com')
    # lisa = Player(username='lisa', email='lisa@gmail.com')
    # john = Player(username='john', email='john@gmail.com')

    # apple = Item()
    # apple2 = Item()
    # apple3 = Item()
    # apple4 = Item()
    # apple5 = Item()
    # coke = Guild(guild_name='coke', country_code="canada")
    # sprite = Guild(guild_name='sprite', country_code="canada")
    #
    # # bob.books = [dune, moby_dick]
    # # carol.books = [fahrenheit]
    #
    # db.session.add(apple)
    # db.session.add(apple2)
    # db.session.add(apple3)
    # db.session.add(apple4)
    # db.session.add(apple5)
    #
    # johnny = Player(username='johnny', email='johnny@gmail.com')
    # apple6 = Item()
    # johnny.children.append(s)
    # db.session.add(bob)
    # db.session.add(lisa)
    # db.session.add(john)
    # db.session.add(sprite)
    # db.session.add(coke)
    # db.session.commit()
    db.create_all()

    app.run(debug=True, host='0.0.0.0')
