from flask import Flask, render_template, jsonify, request
from eclair.cluster import cluster


app = Flask(__name__, static_folder='static', static_url_path='')


# cheating a bit for now
from glob import glob
from eclair.models import Email
from flanker.mime.message.errors import DecodingError
from eclair.network import build_network
from networkx.readwrite import json_graph
from eclair.heuristics import guess_signatures, guess_keywords

files = glob('data/rubio_emails/*.eml')

print('Processing emails...')
emails = []
for file in files:
    with open(file, 'r') as f:
        data = f.read()

    try:
        emails.append( Email(data) )

    # Malformed email
    except DecodingError:
        continue

print('Guessing signatures...')
guess_signatures(emails)

print('Guessing keywords...')
guess_keywords(emails)

# cache for now
print('Building graph...')
G = build_network(emails, min_degree=2)

print('Ready')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/force')
def force():
    return render_template('force.html')

@app.route('/cluster')
def clustering():
    n_clusters = request.args.get('n_clusters', None)
    if n_clusters is not None:
        n_clusters = int(n_clusters)
    clusters = cluster(emails, n_clusters)
    return render_template('cluster.html', clusters=clusters)

@app.route('/graph.json')
def graph():
    return jsonify(json_graph.node_link_data(G))

