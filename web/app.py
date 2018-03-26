import os

from flask import render_template, Flask, send_file, request
from flask_bootstrap import Bootstrap

from db import get_dup_by_hash, get_file_by_id, get_dup_by_name
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

        row = list(row)

        data[hash].append(list(row))

    return data


def get_name_dup(limit=10):
    rows = get_dup_by_name(limit)
    data = {}

    for row in rows:
        name = row[2]
        if name not in data:
            data[name] = []

        row = list(row)

        data[name].append(list(row))

    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        to_be_deleted = request.form
        print(to_be_deleted)

    by = request.args.get('by', 'hash')

    if by == 'name':
        data = get_name_dup()
    else:
        data = get_hash_dup()

    return render_template('index.html', data=data, by=by)


@app.route('/file/<id>', methods=['GET'])
def file(id):
    file = get_file_by_id(id)
    file_path = file[3] if file else 'no such file!!!'

    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(__file__), 'static/404.jpg')

    return send_file(file_path)
