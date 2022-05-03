"""runs a flask websocket server"""

import os
from threading import Lock
import flask
from flask import Flask
from flask_socketio import SocketIO
import shortuuid
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


# background task function
def chat():
    id_counter = 0

    while True:
        socketio.sleep(10)

        filename = 'seed0000.jpg'
        with open(os.path.join('images', filename), 'rb') as file:
            image_data = file.read()
        socketio.emit(
            'chat_message',
            {
                'id': shortuuid.uuid(),
                'sender': 'artist',
                'text': '',
                'imageData': image_data,
                'alt': filename,
                'timestamp': int(time.time() * 1000)
                }
            )
        id_counter += 1

        socketio.sleep(10)

        socketio.emit(
            'chat_message',
            {
                'id': shortuuid.uuid(),
                'sender': 'artist',
                'text': 'Lorem ipsum dolor sit amet',
                'imageData': b'',
                'alt': '',
                'timestamp': int(time.time() * 1000)
                }
            )

        id_counter += 1

        socketio.sleep(10)

        socketio.emit(
            'chat_message',
            {
                'id': shortuuid.uuid(),
                'sender': 'scientist',
                'text':
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec in eqat sagittis, consectetur nulqa eu, volutpat orci. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vestibulum ante ipsum primis in faucibus orci luctus et ultrices',
                'imageData': b'',
                'alt': '',
                'timestamp': int(time.time() * 1000)
                }
            )

        id_counter += 1


# on connect start the background thread (if it's the first connect)
@socketio.on('connect')
def connect():
    print('client connected')
    global thread
    with thread_lock:
        if thread is None:
            print('starting background thread')
            thread = socketio.start_background_task(chat)


# index page
@app.route('/')
def index():
    return flask.send_file('site/build/index.html')


# about page
@app.route('/about')
def about():
    return flask.send_file('site/build/about.html')


# run server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    # socketio.run(app)