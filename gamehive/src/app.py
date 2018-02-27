from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request,redirect,url_for
import sys

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/gamehive'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route('/')
def root():
    return render_template('add_user.html')

@app.route('/post_player', methods = ['POST'])
def post_player():
    # return 'Game Hive Player API']
    print (request.form, file=sys.stderr)
    print("moooooooo", file=sys.stderr)
    player = Player(request.form['username'],request.form['email'])
    db.session.add(player)
    db.session.commit()
    return redirect(url_for('root'))
    # return


class Player(db.Model):
    unique_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    email = db.Column(db.String(120), unique = True)
    skill_points = db.Column(db.Integer, unique = False)
    items = db.Column(db.Integer, unique = False)

    def __init__(self,username,email):
        self.username = username
        self.email = email

# class Guilds(db.Model):


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')


