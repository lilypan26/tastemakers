"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from yaml import load, Loader
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import atexit

def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )

    return pool


app = Flask(__name__)
# other_db = SQLAlchemy(app)
# print(type(other_db))
db = init_connection_engine()
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
base = declarative_base()

min_ingredient_id = -1
with open('app\secret_file.txt', 'r') as f:
  for line in f:
    min_ingredient_id = int(line)
    print(min_ingredient_id)
# print(type(db))

#defining function to run on shutdown
def save_min_ingredient_id():
    global min_ingredient_id
    print(min_ingredient_id)
    f = open('app\secret_file.txt', 'w')
    f.write(str(min_ingredient_id))
    f.close()
    # print("finihsed writing secret")
#Register the function to be called on exit
atexit.register(save_min_ingredient_id)

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes