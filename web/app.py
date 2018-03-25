from flask import render_template, Flask
from flask_bootstrap import Bootstrap

from web import Config

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('hash.html')
