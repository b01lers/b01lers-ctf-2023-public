from base64 import b64decode
import flask

app = flask.Flask(__name__)

@app.route('/<name>')
def index2(name):
    name = b64decode(name)
    if (validate(name)):
        return "This file is blocked!"
    try:
        file = open(name, 'r').read()
    except:
        return "File Not Found"
    return file

@app.route('/')
def index():
    return flask.redirect('/aW5kZXguaHRtbA==')

def validate(data):
    if data == b'flag.txt':
        return True
    return False


if __name__ == '__main__':
    app.run()