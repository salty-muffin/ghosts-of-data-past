"""runs a flask websocket server"""

import os
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO

import time

# flask & socketio setup
app = Flask(__name__)
app.config.from_object('config.DevConfig')
socketio = SocketIO(app)

# threading
thread = None
thread_lock = Lock()


def chat():
    while True:
        socketio.sleep(10)

        with open(os.path.join('images', 'seed0000.jpg'), 'rb') as file:
            image_data = file.read()
        socketio.emit('chat_image', {'data': image_data})

        socketio.sleep(10)

        socketio.emit(
            'chat_message', {'data': f'a new message at {time.time()}'}
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
    return render_template('index.html')


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0')
    socketio.run(app)