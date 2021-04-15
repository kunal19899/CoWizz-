from flask import Flask
from v3.config import Config

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(Config)

from v3 import routes




