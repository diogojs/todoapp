from todo import app, tasks
import json

def test_list_tasks_return_status_200():
    with app.test_client() as client:
        response = client.get('/task')
        assert response.status_code == 200

def test_list_tasks_type_json():
    with app.test_client() as client:
        response = client.get('/task')
        assert response.content_type == 'application/json'

def test_list_tasks_empty():
    with app.test_client() as client:
        response = client.get('/task')
        assert response.data == b'[]\n'

def test_list_tasks_not_empty():
    tasks.append({
        'id': 1,
        'title': 'tarefa 1',
        'desc': 'primeira tarefa',
        'state': False
        })
    with app.test_client() as client:
        response = client.get('/task')
        assert response.data == (b'[{"desc":"primeira tarefa",'
                                 b'"id":1,'
                                 b'"state":false,'
                                 b'"title":"tarefa 1"}]\n')

def test_create_task_post():
    with app.test_client() as client:
        response = client.post('/task')
        assert response.status_code != 405

def test_create_task_return():
    tasks.clear()
    client = app.test_client()
    response = client.post('/task', data=json.dumps({
        'title': 'titulo',
        'desc': 'descricao'
        }),
        content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert data['id'] == 1
    assert data['title'] == 'titulo'
    assert data['desc'] == 'descricao'
    assert data['state'] is False
    assert response.status_code == 201

def test_create_task_adds_to_database():
    tasks.clear()
    client = app.test_client()
    # realiza a requisição utilizando o verbo POST
    client.post('/task', data=json.dumps({
        'title': 'titulo',
        'desc': 'descricao'}),
        content_type='application/json')
    assert len(tasks) > 0

def test_create_task_without_desc():
    # status code should be 400 indicating client error
    client = app.test_client()
    response = client.post('/task', data=json.dumps({
        'title': 'titulo'
        }),
        content_type='application/json')
    assert response.status_code == 400

def test_create_task_without_title():
    # status code should be 400 indicating client error
    client = app.test_client()
    response = client.post('/task', data=json.dumps({
        'desc': 'descricao'
        }),
        content_type='application/json')
    assert response.status_code == 400

def test_list_tasks_show_not_finished_first():
    tasks.clear()
    tasks.append({'id': 1, 'title': 'tarefa 1', 'desc': 'tarefa de numero 1',
                    'state': True})
    tasks.append({'id': 2, 'title': 'tarefa 2', 'desc': 'tarefa de numero 2',
                    'state': False})
    with app.test_client() as client:
        response = client.get('/task')
        data = json.loads(response.data.decode('utf-8'))
        primeira_task, segunda_task = data
        assert primeira_task['title'] == 'tarefa 2'
        assert segunda_task['title'] == 'tarefa 1'