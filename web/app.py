import os

from flask import render_template, Flask, send_file
from flask_bootstrap import Bootstrap

from db import get_dup_by_hash, get_file_by_id
from web import Config

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


def get_hash_dup(limit=10):
    rows = get_dup_by_hash(limit)
    data = {}

    for row in rows:
        hash = row[1]
        path = row[3]
        if hash not in data:
            data[hash] = []

        row = list(row)
        row.append('file://' + path.replace('\\', '/'))

        data[hash].append(list(row))

    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', data=get_hash_dup())


@app.route('/file/<id>', methods=['GET'])
def file(id):
    file = get_file_by_id(id)
    file_path = file[3] if file else 'no such file!!!'

    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(__file__), 'static/404.jpg')

    return send_file(file_path)
