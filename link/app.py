# script for running a flask websocket server
# which shows the link & qrcode
#
# zeno gries 2023

import os
import flask
import logging
from datetime import datetime
from flask import Flask

# flask & socketio setup
app = Flask(
    __name__, static_url_path='', static_folder=os.path.join('site', 'build')
    )
app.config.from_object('config.ProdConfig')


# index page
@app.route('/')
def index():
    return flask.send_file('site/build/index.html')


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
                    f'link_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
                    ),
                encoding='utf-8'
                ),
            logging.StreamHandler()
            ]
        )

    logging.info('starting link server on port 8000')
    app.run(host='0.0.0.0', port=8000)