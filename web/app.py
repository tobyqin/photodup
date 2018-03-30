import os
from collections import OrderedDict

from flask import render_template, Flask, send_file, request
from flask_bootstrap import Bootstrap

from config import web_show_counts
from db import get_dup_by_hash, get_file_by_id, get_dup_by_name, delete_file_by_id
from web import Config

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


def get_hash_dup(limit=web_show_counts):
    rows = get_dup_by_hash(limit)
    data = {}

    for row in rows:
        hash = row[1]
        if hash not in data:
            data[hash] = []

        data[hash].append(list(row))

    return data


def get_name_dup(limit=web_show_counts):
    rows = get_dup_by_name(limit)
    data = {}

    for row in rows:
        name = row[2]
        if name not in data:
            data[name] = []

        data[name].append(list(row))

    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        for file_id in request.form:
            delete_file_by_id(file_id)

    by = request.args.get('by', 'hash')
    data = get_name_dup() if by == 'name' else get_hash_dup()
    data = OrderedDict(sorted(data.items(), key=lambda x: -len(x[1])))  # sort by count desc
    return render_template('index.html', data=data, by=by)


@app.route('/file/<id>', methods=['GET'])
def file(id):
    file = get_file_by_id(id)
    file_path = file[3] if file else 'no such file!!!'
    ext = os.path.splitext(file_path)[-1].lower()

    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(__file__), 'static/404.jpg')

    elif ext not in ['.jpg', '.png', '.gif', '.bmp', '.jpeg']:
        file_path = os.path.join(os.path.dirname(__file__), 'static/not_supported.jpg')

    return send_file(file_path)
