from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
    