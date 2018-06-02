from flask import Flask, jsonify

app = Flask('ToDo')
tasks = []

@app.route('/task')
def list():
    return jsonify(tasks)
