from flask import Flask, render_template, session, url_for, redirect, flash
from wtforms import *
from functions import *
from configparser import ConfigParser
import mariadb
import os
from init_classes import RegForm, LogForm

config = ConfigParser()
config.read('config.cfg')

app = Flask(__name__)
app.config['SECRET_KEY'] = config.get("DEFAULT", "secret_key")

connection = mariadb.connect(
    user=os.environ.get('username'),
    password=config.get('DEFAULT', 'db_password'),
    host='localhost',
    database="spotify_music")

cur = connection.cursor()

# main page
@app.route('/')
def main():
    response = get_artist_info(session)
    return render_template('index.html', data=response, s=session)

# page with releases
@app.route('/releases')
def releases():
    response = {}
    return render_template('new.html', data=response, s=session)

# user profile page
@app.route('/profile')
def profile():
    if 'username' in session.keys():
        return render_template('profile.html', s=session)
    else:
        return redirect(url_for('/'))

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('log_form.html', s=session)

# registration page
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegForm(request.form)

    if request.method != "POST":
        return render_template('reg_form.html', s=session, form=form)
    
    if form.validate():
        username  = form.username.data
        password = form.password.data

        cur.execute("SELECT * FROM users WHERE login=?;", (username, ))
        check = cur.fetchall()
        if len(check) > 0:
            flash('This username is already taken.')
            return render_template('reg_form.html', s=session, form=form)
        else:
            try:
                cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (username, password, ))
                return render_template('message.html', msg="Registration is completed succesfully!")
            except mariadb.Error as e:
                return render_template('message.html', msg=e)
    

if __name__ == '__main__':
    app.run(port=12555, debug=True)
