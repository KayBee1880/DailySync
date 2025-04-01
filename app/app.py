from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

'''This is where we will create the actual app and define its configurations,
also register blueprints for routes we define in the routes folder
'''

#initialize flask extensions


#create app + fetch configurations from config file
app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
app.config.from_object('config.Config')


#run app
if __name__ == '__main__':
    app.run(debug=True)