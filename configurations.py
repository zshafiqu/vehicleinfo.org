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
class ServerObject:
    # The ServerObject class is used to encapsulate our server and its configurations
    # The class contains a couple variables that are associated with the server, below
    app = None
    cache = None
    db = None
    cache_timeout = None

    # Object initializer method, takes in no parameters as the ServerObject's data is predefined above
    def __init__(self):
        self.app =
    # 
    # # ServerObject's own method to create a Flask application object
    # def create_app():
    #     # Activate virtual env with - source env/bin/activate
    #     # Initialize flask app, enable auto deploy from master branch for heroku
    #     app = Flask(__name__)
    #
    #     # From flask_minify, wrap app around minify module to minify the HTML/CSS/JS responses
    #     minify(app=app, html=True, js=True, cssless=True)
    #
    #     # Designate application URL routing to occur with or without a trailing slash
    #     # By default, all of the routes defined below exist without a trailing slash
    #     app.url_map.strict_slashes = False
    #
    #     # Use Talisman to force any http:// prefixed requests to redirect to https://
    #     # Edit the CSP in order to serve CSS styles and JavaScript files
    #     Talisman(app, content_security_policy=None)
    #     app.secret_key = os.environ.get('KEY')
    #
    #     # Configure flask app with info stored locally within environment (locally or heroku)
    #     # To install mysqlclient, needed to run brew install mysql
    #     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('BASE_URI')
    #
    #     return app
    #
    # # Use this class to hold our app, it's cache object, and its database cursor
    # def __init__(self, app, cache, db):
    #     self.app = app
    #     self.cache = cache
    #     self.db = db
    #     self.cache_timeout = 1800 # Cache timeout is 30 minutes





























# ----------------------
def create_cache_instance(app):
    # Setup simple cache instance configuration & Initialize it to app instance
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)

    return cache
# ----------------------
def create_db_cursor(app):
    # Bind app to db obj
    db = SQLAlchemy(app)
    # Was running into a timeouterror for mySQL on Heroku's clearDB instance.
    # Referencing stackoverflow, "the only work around I could find for this by
    # talking to the ClearDB people is to add in the pessimistic ping when creating the engine."
    # Not ideal since its pings DB everytime before you do a query, but avoids 500 Internal Server Error
    db = SQLAlchemy(engine_options={"pool_size": 10, "poolclass":QueuePool, "pool_pre_ping":True})

    return db
# ----------------------
def create_app():
    # Activate virtual env with - source env/bin/activate
    # Initialize flask app, enable auto deploy from master branch for heroku
    app = Flask(__name__)

    # From flask_minify, wrap app around minify module to minify the HTML/CSS/JS responses
    minify(app=app, html=True, js=True, cssless=True)

    # Designate application URL routing to occur with or without a trailing slash
    # By default, all of the routes defined below exist without a trailing slash
    app.url_map.strict_slashes = False

    # Use Talisman to force any http:// prefixed requests to redirect to https://
    # Edit the CSP in order to serve CSS styles and JavaScript files
    Talisman(app, content_security_policy=None)
    app.secret_key = os.environ.get('KEY')

    # Configure flask app with info stored locally within environment (locally or heroku)
    # To install mysqlclient, needed to run brew install mysql
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('BASE_URI')

    return app
# ----------------------
def create_server_instance():
    # Use this method to create a configured application
    # Then return it as an instance of the server_object
    app = create_app()
    cache = create_cache_instance(app)
    db = create_db_cursor(app)
    # Instance variable
    server = ServerObject(app, cache, db)

    return server
# ----------------------
