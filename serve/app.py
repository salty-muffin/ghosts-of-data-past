"""runs a flask websocket server"""

import os
from threading import Lock
import flask
from flask import Flask
from flask_socketio import SocketIO

import time

# flask & socketio setup
app = Flask(
    __name__, static_url_path='', static_folder=os.path.join('site', 'build')
    )
app.config.from_object('config.DevConfig')
socketio = SocketIO(app)

# threading
thread = None
thread_lock = Lock()


def chat():
    while True:
        socketio.sleep(10)

        filename = 'seed0000.jpg'
        with open(os.path.join('images', filename), 'rb') as file:
            image_data = file.read()
        socketio.emit(
            'chat_item', {
                'type': 'image', 'imageData': image_data, 'text': filename
                }
            )

        socketio.sleep(10)

        socketio.emit(
            'chat_item',
            {
                'type': 'message',
                'imageData': '',
                'text': f'a new message at {time.time()}'
                }
            )


@socketio.on('connect')
def connect():
    print('client connected')
    global thread
    with thread_lock:
        if thread is None:
            print('starting background thread')
            thread = socketio.start_background_task(chat)


@app.route('/')
def index():
    # return flask.render_template('index.html')
    return flask.send_file('site/build/index.html')


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0')
    socketio.run(app)