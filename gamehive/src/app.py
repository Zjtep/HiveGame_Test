from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request, redirect, url_for, jsonify
import sys
from sqlalchemy import or_


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
    # return 'Game Hive Player API']
    # print (request.form, file=sys.stderr)
    # print("moooooooo", file=sys.stderr)


    # player = Player(request.arg.get('username'), request.arg.get('email'))
    # db.session.add(player)
    # db.session.commit()
    # return redirect(url_for('root'))
    # return '<h1> Hello{}.'.format(player)

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
    return jsonify(data['username'], data['email'])


@app.route('/edit_player', methods=['POST'])
def edit_player():
    data = request.get_json()

    query_user = Player.query.filter_by(username=data['username']).first()

    if query_user is not None:
        Player.query.filter_by(id=query_user.id).update(dict(username=data['username'], email=data['email']))
        db.session.commit()
        return "updated"
    else:
        return "can't find user"
        # return jsonify(player)
        # return jsonify(data['username'], data['email'])


@app.route('/delete_player', methods=['POST'])
def delete_player():
    data = request.get_json()

    # player = Player(data['username'], data['email'])

    query_user_id = Player.query.filter_by(id=data['id']).first()
    # query_username = Player.query.filter_by(username=data['username']).first()
    # query_email = Player.query.filter_by(username=data['email']).first()

    if query_user_id is not None:
        Player.query.filter_by(id=query_user_id.id).delete()
        db.session.commit()
        return "deleted"
    else:
        return "cant find"


@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.get_json()

    query_user_id = Player.query.filter_by(id=data['player_id']).first()
    if query_user_id is not None:
        Player.query.filter_by(id=query_user_id.id).update(dict(guild_id=data['guild_id']))
        db.session.commit()
        return "added to guild"
    else:
        return "cant find player"


@app.route('/create_guild', methods=['POST'])
def create_guild():
    data = request.get_json()

    query_guide_name = Guild.query.filter_by(guild_name=data['guild_name']).first()

    if query_guide_name is not None:
        return "guide_name already in database"
    else:
        guild = Guild(data['guide_name'], data['country_code'])
        db.session.add(guild)
        db.session.commit()
        return "added guild"


class Guild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild_name = db.Column(db.String(120), unique=True)
    country_code = db.Column(db.String(120), unique=False)
    players = db.relationship('Player', backref='guild', lazy='dynamic')

    def __init__(self, guild_name, country_code):
        self.guild_name = guild_name
        self.country_code = country_code

    def __repr__(self):
        return '<Guild:{}>'.format(self.id)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    skill_points = db.Column(db.Integer, unique=False)
    items = db.Column(db.Integer, unique=False)
    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<Player:{}>'.format(self.id)


# class Guilds(db.Model):


if __name__ == '__main__':
    # bob = Player(username='Bob', email='bob@gmail.com')
    # lisa = Player(username='lisa', email='lisa@gmail.com')
    # john = Player(username='john', email='john@gmail.com')
    #
    #
    # coke = Guild(guild_name='coke', country_code="canada")
    # sprite = Guild(guild_name='sprite', country_code="canada")
    #
    # # bob.books = [dune, moby_dick]
    # # carol.books = [fahrenheit]
    #
    # db.session.add(bob)
    # db.session.add(lisa)
    # db.session.add(john)
    # db.session.add(sprite)
    # db.session.add(coke)
    # db.session.commit()
    db.create_all()

    app.run(debug=True, host='0.0.0.0')
