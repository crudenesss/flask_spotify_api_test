from flask import Flask, render_template, session, redirect, flash
from wtforms import *
from functions import *
from commands import setup
import mariadb, os, logging
from init_classes import RegForm, LogForm, SongForm
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

app.config['SECRET_KEY'] = os.environ.get('KEY')

logging.basicConfig(filename = 'logs.log', 
    format = '[%(asctime)s]     %(levelname)s     %(name)s : %(message)s')

db_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': 'db',
    'database': "spotify_music"
}

connection = mariadb.connect(**db_config)
cur = connection.cursor()

setup(connection, cur)

# main page
@app.route('/')
def main():
    response = get_artist_info(session)
    print(response)
    return render_template('index.html', data=response, s=session)


# page with releases
@app.route('/releases')
def releases():
    response = get_releases(session)
    parsed = response['albums']['items']
    total = response['albums']['total']
    return render_template('new.html', data=parsed, items=total, s=session)

# user profile page
@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    if not 'username' in session.keys():
        return redirect('/')
    
    form = SongForm(request.form)

    cur.execute(
        "SELECT item_id, name, album, artist, u_id FROM liked_music JOIN users ON u_id=user_id JOIN songs ON s_id=song_id WHERE login=?;",
        (session['username'], )
        )
    songs = cur.fetchall()

    if request.method == "POST":
        if form.validate():

            cur.execute("SELECT user_id FROM users WHERE login=?;", (session['username'], ))
            u_id = cur.fetchall()[0][0]

            title = form.name.data
            album = form.album.data
            artist = form.artist.data

            cur.execute(
                "SELECT * FROM songs WHERE name=? AND album=? AND artist=?;", 
                (title, album, artist, )
                )
            
            check = cur.fetchall()
            if len(check) != 0:
                id = check[0][0]
                cur.execute(
                    "SELECT * FROM liked_music WHERE u_id=? AND s_id=?;",
                    (u_id, id, )
                    )
                if len(cur.fetchall()) != 0:
                    flash("Songs must be different")
                    return redirect('/profile/')
                
            else:
                id = create_code(16)
                cur.execute(
                    "INSERT INTO songs VALUES (?, ?, ?, ?);",
                    (id, title, album, artist, ))
            
            cur.execute(
                "INSERT INTO liked_music (u_id, s_id) VALUES (?, ?);", 
                (u_id, id, )
                )
            connection.commit()

            return redirect('/profile/')

    return render_template('profile.html', s=session, data=songs, form=form)

# delete song
@app.route('/profile/<id>', methods=['GET', 'POST'])
def delete(id):

    if request.method == "POST":

        if not 'username' in session.keys():
            return redirect('/')

        cur.execute(
            """SELECT * FROM liked_music 
                WHERE 
                s_id IN (SELECT s_id FROM liked_music WHERE item_id=?) AND
                u_id IN (SELECT user_id FROM users WHERE login=?)""",
            (id, session['username'])
        )

        resp = cur.fetchall()

        if len(resp) == 0:
            return redirect('/profile/')
        elif len() > 1:
            cur.execute(
                "DELETE FROM liked_music WHERE item_id=?",
                (id, )
                )
        else:
            cur.execute(
                "DELETE FROM songs WHERE song_id IN (SELECT s_id FROM liked_music WHERE item_id=?)",
                (id, )
            )

        connection.commit()
    return redirect('/profile/')


# login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LogForm(request.form)

    if request.method != "POST":
        return render_template('log_form.html', s=session, form=form)
    
    if form.validate():
        username = form.username.data
        password = form.password.data

        cur.execute("SELECT * FROM users WHERE login=? AND password=?;", (username, password,))
        check = cur.fetchall()
        if len(check) != 1:
            flash("Incorrect login or password.")
            return render_template('log_form.html', s=session, form=form)
        else:
            session['username'] = username
            return redirect('/')

    return render_template('log_form.html', s=session, form=form)

# logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# registration page
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegForm(request.form)

    if request.method != "POST":
        return render_template('reg_form.html', s=session, form=form)
    
    if form.validate():
        username = form.username.data
        password = form.password.data

        cur.execute("SELECT * FROM users WHERE login=?;", (username, ))
        check = cur.fetchall()
        if len(check) > 0:
            flash('This username is already taken.')
            return render_template('reg_form.html', s=session, form=form)
        else:
            try:
                cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (username, password, ))
                connection.commit()
                return render_template('message.html', msg="Registration is completed succesfully!")
            except mariadb.Error as e:
                return render_template('message.html', msg=e)
    
    return render_template('reg_form.html', s=session, form=form)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0")
