from flask import Flask, render_template, session
from functions import *
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

app = Flask(__name__)
app.config['SECRET_KEY'] = config.get("DEFAULT", "secret_key")

@app.route('/')
def main():
    response = get_artist_info(session)
    return render_template('index.html', response=response)

@app.route('/releases')
def releases():
    return render_template('new.html')

if __name__ == '__main__':
    app.run(port=12555)
