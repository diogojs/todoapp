from todo import app, tasks

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


