# script for running a flask websocket server
# which pushes chat messages to clients
#
# zeno gries 2022

import os
import flask
from flask import Flask

# flask & socketio setup
app = Flask(
    __name__, static_url_path='', static_folder=os.path.join('site', 'build')
    )
app.config.from_object('config.ProdConfig')

# generate random


# index page
@app.route('/')
def index():
    return flask.send_file('site/build/index.html')


# run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)