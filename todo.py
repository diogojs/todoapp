from flask import Flask, jsonify

app = Flask('ToDo')
tasks = []

@app.route('/task')
def list():
    tasks.append({
        'id': 1,
        'title': 'tarefa 1',
        'desc': 'primeira tarefa',
        'state': False
        })
    return jsonify(tasks)
