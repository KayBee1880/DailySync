from flask import Flask
from flask_sqlalchemy import SQLAlchemy

'''This is where we will create the actual app and define its configurations,
also register blueprints for routes we define in the routes folder
'''
def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
    