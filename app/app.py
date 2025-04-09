from flask import Flask, Blueprint
from dotenv import load_dotenv
import os
from extensions import db, migrate, login_manager, bcrypt
from routes.auth_routes import auth_bp
from routes.habit_routes import habits_bp
from routes.settings_routes import settings_bp
from routes.test_routes import test_bp
from models import User
from seeds_data import run_all_seeds
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect

'''This is where we will create the actual app and define its configurations,
also register blueprints for routes we define in the routes folder
'''

#load environment variables
load_dotenv()


#create app + fetch configurations from config file
app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')

#app configurations
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DTABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://habit_tracker_user:T3%40Mdatabase%21@127.0.0.1:5555/teamprojectdb?options=-c%20search_path=new_schema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'options': '-csearch_path=public'}
}
#csrf = CSRFProtect(app)


#initialize entension objects with app
db.init_app(app)
migrate.init_app(app,db)
login_manager.init_app(app)
bcrypt.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#register blueprints from routes folder
app.register_blueprint(auth_bp)
app.register_blueprint(habits_bp, url_prefix='/habits')
app.register_blueprint(settings_bp, url_prefix='/settings')

#test routes for debugging purposes
app.register_blueprint(test_bp, url_prefix="/test")


with app.app_context():
    db.session.execute(text('SET search_path TO public;'))  # Wrap SQL query with text()
    db.session.commit()  # Commit if required
    #db.drop_all()
    db.create_all()
    run_all_seeds()

#template filters

@app.template_filter('format_date')
def format_date(date):
    return date.strftime('%b %d')  # Format the date as 'Mar 22'
#run app
if __name__ == '__main__':
    app.run(debug=True)