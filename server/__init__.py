from flask import Flask, render_template, jsonify


app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


# cheating a bit for now
from glob import glob
from eclair.models import Email
from flanker.mime.message.errors import DecodingError
from eclair.network import build_network
from networkx.readwrite import json_graph

files = glob('data/rubio_emails/*.eml')

emails = []
for file in files[:500]:
    with open(file, 'r') as f:
        data = f.read()

    try:
        emails.append( Email(data) )

    # Malformed email
    except DecodingError:
        continue
G = build_network(emails)

@app.route('/graph.json')
def graph():
    return jsonify(json_graph.node_link_data(G))

