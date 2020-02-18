from  flask import Flask, Blueprint
from flask_cors import CORS
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)


app.secret_key = 'this is my secret key'


@app.route('/', methods=['GET'])
def hello_world():
    return 'hello-world'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)