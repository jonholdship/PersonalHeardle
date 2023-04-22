from flask import Flask
from flask_session import Session
import yaml
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

for key, value in config.items():
    os.environ[key] = value

# this is how flask says to do it :shrug:
import personal_heardle.views
