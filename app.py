import os
from  flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from resources.climbs import climbs
from resources.users import users
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)


app.secret_key = 'this is my secret key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(data={'error': 'user has not logged in'}, message="you must login to access that resource", status=401), 401

CORS(climbs, origins=['http://localhost:3000', 'https://climb-on-api.herokuapp.com'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000', 'https://climb-on-api.herokuapp.com'], supports_credentials=True)

app.register_blueprint(climbs, url_prefix='/api/v1/climbs')
app.register_blueprint(users, url_prefix='/api/v1/users')




@app.route('/', methods=['GET'])
def hello_world():
    return 'hello-world'
    
if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)