
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


config = Flask(__name__)


if __name__ == '__main__':
    config.run()
