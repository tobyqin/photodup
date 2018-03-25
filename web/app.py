from flask import render_template, Flask
from flask_bootstrap import Bootstrap

from db import get_dup_by_hash
from web import Config

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


def get_hash_dup(limit=10):
    rows = get_dup_by_hash(limit)
    data = {}

    for row in rows:
        hash = row[1]
        if hash not in data:
            data[hash] = []

        data[hash].append(list(row))

    return data


@app.route('/')
def index():
    return render_template('index.html', data=get_hash_dup())
