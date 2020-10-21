# This file's purpose is to setup the configurations for our Flask server
# Abstracting this because as the application gets more complex,
# we get more and more spaghetti code, so this should help with organization
# ----------------------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from sqlalchemy.pool import QueuePool
from flask_minify import minify
from flask_caching import Cache
import os
# ----------------------
# The ServerObject class is used to encapsulate our server and its configurations
class ServerObject:
    # The class contains a couple variables that are associated with the server, below
    application = None
    cache = None
    db = None
    cache_timeout = None
    # ----------------------
    # Object initializer method, takes in no parameters as the ServerObject's data is predefined above
    def __init__(self):
        self.application = self.create_app()
        self.cache = self.create_cache(self.application)
        self.db = self.create_db_cursor(self.application)
        self.cache_timeout = 1800 # Cache timeout = 30 minutes
    # ----------------------
    # ServerObject's own method to create a Flask application object, as well as assign app configs
    def create_app(self):
        # Create Flask app object
        application = Flask(__name__)

        # From flask_minify, wrap app around minify module to minify the HTML/CSS/JS responses
        minify(app=application, html=True, js=True, cssless=True)

        # Designate application URL routing to occur with or without a trailing slash
        # By default, all of the routes defined below exist without a trailing slash
        application.url_map.strict_slashes = False

        ''' Use Talisman to force any http:// prefixed requests to redirect to https:// '''
        # Edit the CSP in order to serve CSS styles and JavaScript files
        Talisman(application, content_security_policy=None)
        application.secret_key = os.environ.get('KEY')

        # Configure flask app with info stored locally within environment (locally or AWS)
        # To install mysqlclient, needed to run brew install mysql
        application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('RDS_URI')
        return application
    # ----------------------
    def create_cache(self, app):
        # Setup simple cache instance configuration
        cache = Cache(config={'CACHE_TYPE': 'simple'})
        # Bind cache instance to app
        cache.init_app(app)
        return cache
    # ----------------------
    def create_db_cursor(self, app):
        # Bind app to db obj
        db = SQLAlchemy(app)
        # Was running into a timeouterror for mySQL on Heroku's clearDB instance.
        # Referencing stackoverflow, "the only work around I could find for this by
        # talking to the ClearDB people is to add in the pessimistic ping when creating the engine."
        # Not ideal since its pings DB everytime before you do a query, but avoids 500 Internal Server Error
        db = SQLAlchemy(engine_options={"pool_size": 10, "poolclass":QueuePool, "pool_pre_ping":True})
        return db
    # ----------------------
