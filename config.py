import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
# Connect to the database
# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://fyyur:fyyur123@localhost:5432/dbfyyur1'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.urandom(32)

