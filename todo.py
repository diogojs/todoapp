from flask import Flask, jsonify, request, abort
from operator import itemgetter

app = Flask('ToDo')
tasks = []

@app.route('/task')
def list():
    return jsonify(sorted(tasks, key=itemgetter('state')))

@app.route('/task', methods=['POST'])
def create():
    title = request.json.get('title')
    desc = request.json.get('desc')
    if not desc or not title:
        abort(400)
    task = {
        'id':len(tasks)+1,
        'title': title,
        'desc': desc,
        'state': False
    }
    tasks.append(task)
    return jsonify(task), 201
