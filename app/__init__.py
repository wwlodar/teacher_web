from flask import Flask

app = Flask(__name__, template_folder='templates')
app.config['DEBUG'] = True

from app import main