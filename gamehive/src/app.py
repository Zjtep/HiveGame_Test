from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request, redirect, url_for, jsonify
import sys


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

    player = Player(data['username'], data['email'])
    db.session.add(player)
    db.session.commit()
    # return jsonify(player)
    return jsonify(data['username'], data['email'])


@app.route('/delete_player', methods=['POST'])
def delete_player():
    data = request.get_json()

    # player = Player(data['username'], data['email'])
    query_user = Player.query.filter_by(username=data['username']).first()

    if query_user is not None:
        Player.query.filter_by(id=query_user.id).delete()
        db.session.commit()
        return "deleted"
    else:
        return "cant find"
    # if temp_query:
    #     db.session.delete(temp_query)
    # db.session.add(player)
    # db.session.commit()

    # return one_item
    # return jsonify(data['username'], data['email'])
    # return "hello"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    skill_points = db.Column(db.Integer, unique=False)
    items = db.Column(db.Integer, unique=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


# class Guilds(db.Model):


if __name__ == '__main__':
    db.create_all()

    app.run(debug=True, host='0.0.0.0')
