import imp
from multiprocessing.spawn import import_main_path
from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes