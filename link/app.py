import os
import flask

app = flask.Flask(
    __name__, static_url_path="/", static_folder=os.path.join("site", "build")
)


@app.route("/")
def hello_world():
    return flask.send_file("site/build/index.html")
