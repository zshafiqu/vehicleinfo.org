
# This file's purpose is to setup the configurations for our Flask server
# Abstracting this because as the application gets more complex,
# we get more and more spaghetti code, so this should help with organization
# ----------------------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
# from flask_wtf import FlaskForm
# from wtforms import SelectField
from sqlalchemy.pool import QueuePool
from flask_minify import minify
from flask_caching import Cache
import os

# Activate virtual env with - source env/bin/activate
# Initialize flask app, enable auto deploy from master branch for heroku
app = Flask(__name__)
# Setup simple cache instance configuration & Initialize it to app instance
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
# From flask_minify, wrap app around minify module to minify the HTML/CSS/JS responses
minify(app=app, html=True, js=True, cssless=True)
# Designate application URL routing to occur with or without a trailing slash
# By default, all of the routes defined below exist without a trailing slash
app.url_map.strict_slashes = False
# Use Talisman to force any http:// prefixed requests to redirect to https://
# Edit the CSP in order to serve CSS styles and JavaScript files
Talisman(app, content_security_policy=None)
app.secret_key = os.environ.get('KEY')
# ----------------------
# Configure flask app with info stored locally within environment (locally or heroku)
# To install mysqlclient, needed to run brew install mysql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('BASE_URI')

if __name__ == '__main__':
    app.run()
