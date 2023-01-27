# script for running a flask websocket server
# which pushes chat messages to clients
#
# zeno gries 2023

import os
from threading import Lock
import flask
from flask import Flask, request
from flask_socketio import SocketIO
import redis
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

gate = os.environ.get('GATE')
passwd = os.environ.get('PASSWD')

# threading
thread = None
thread_lock = Lock()

connections = 0

# flask & socketio setup
app = Flask(
    __name__, static_url_path='', static_folder=os.path.join('site', 'build')
    )
app.config.from_object('config.ProdConfig')
socketio = SocketIO(app)


# background task function
def chat():
    logging.info('connecting to redis database')
    database = redis.Redis(host='localhost', port=6379, db=0)
    subscriber = database.pubsub()
    subscriber.psubscribe('__keyspace@0__:*')

    while True:
        message = subscriber.get_message()
        if message:
            # get the key of the changed item
            key = str(message['channel']).split(':', 1)[1].strip('\'')

            if '*' not in key:
                # get writing event updates
                if 'writing' in key:
                    writing_state = database.hgetall(key)
                    socketio.emit(
                        'writing_state',
                        {
                            'writer': writing_state[b'writer'].decode('utf-8'),
                            'state':
                            int(writing_state[b'state'].decode('utf-8')),
                            'gate': gate if gate else ''
                            },
                        )
                # get incoming messages
                else:
                    chat_message = database.hgetall(key)
                    socketio.emit(
                        'chat_message',
                        {
                            'id': key,
                            'sender': chat_message[b'sender'].decode('utf-8'),
                            'text': chat_message[b'text'].decode('utf-8'),
                            'imageData': chat_message[b'image_data'],
                            'alt': chat_message[b'alt'].decode('utf-8'),
                            'soundData': chat_message[b'sound_data'],
                            'timestamp': int(time.time() * 1000),
                            'gate': gate if gate else ''
                            }
                        )
        socketio.sleep(0.1)


# on connect start the background thread (if it's the first connect)
@socketio.on('connect')
def connect():
    global connections
    connections += 1

    logging.info('client connected')
    global thread
    with thread_lock:
        if thread is None:
            logging.info('starting background thread')
            thread = socketio.start_background_task(chat)


@socketio.on('disconnect')
def disconnect():
    global connections
    connections -= 1

    logging.info('client disconnected')


# index page
@app.route('/')
def index():
    if request.args.get('gate') == gate or not gate:
        return flask.send_file('site/build/index.html')
    else:
        return flask.send_file('site/build/lost.html')


# status page
@app.route('/status')
def status():
    if request.args.get('passwd') == passwd or not passwd:
        return {'gate': gate, 'connection': connections}
    else:
        return flask.send_file('site/build/404.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.send_file('site/build/404.html')


# @app.route('/background')
# def background():
#     return flask.send_file('site/build/background.html')

# @app.route('/credits')
# def credit():
#     return flask.send_file('site/build/credits.html')

# @app.route('/source')
# def source():
#     return flask.send_file('site/build/source.html')

# run server
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(
                os.path.join(
                    'logs',
                    f'serve_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
                    ),
                encoding='utf-8'
                ),
            logging.StreamHandler()
            ]
        )

    logging.info('starting serve server on port 5000')
    socketio.run(app, host='0.0.0.0', port=5000)