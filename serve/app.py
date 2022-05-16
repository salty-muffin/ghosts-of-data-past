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


# TEMPORARY
def flow(sender: str, text: str = '', image_path: str = None) -> None:
    alt = ''
    if image_path:
        with open(image_path, 'rb') as file:
            image_data = file.read()

        alt = os.path.basename(image_path)
    else:
        image_data = b''

    socketio.emit(
        'chat_message',
        {
            'id': shortuuid.uuid(),
            'sender': sender,
            'text': text,
            'imageData': image_data,
            'alt': alt,
            'timestamp': int(time.time() * 1000)
            }
        )


# background task function
def chat():
    while True:
        socketio.sleep(20)
        flow('scientist', text='Are you still there?')
        socketio.sleep(15)
        flow('artist', text='Yes, I\'m here')
        socketio.sleep(10)
        flow('artist', image_path=os.path.join('images', 'seed0000.jpg'))
        socketio.sleep(20)
        flow(
            'scientist',
            text=
            'It is rather fascinating to think that we would give up absolute control over computers, one of the few domain where we ever held "absolute control", in favor of them doing more things for us'
            )


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