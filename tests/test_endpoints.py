import pytest
from datetime import datetime
from src import create_app
from src.models import db, Task, User

@pytest.fixture
def app():
    """Create and configure a new Flask app instance for testing."""
    app = create_app(test_config={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_task_index_endpoint(client):
    """Test the index endpoint."""
    # Insert some dummy data into the database
    task = Task(title="Test Task", description="Test Description", deadline=datetime.now(), status="Incomplete", created_by_user=1)
    db.session.add(task)
    db.session.commit()

    # Make a GET request to the index endpoint
    response = client.get('/tasks')

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response contains the expected data
    assert b'Test Task' in response.data
    assert b'Test Description' in response.data

def test_create_task(client):
    # Create a new user
    user = User(username='test_user', email='test@example.com', password='test_password')
    db.session.add(user)
    db.session.commit()

    # Prepare JSON data for creating a task
    task_data = {
        'created_by_user': user.id,
        'title': 'Test Task',
        'description': 'This is a test task',
        'deadline': datetime.now().date().isoformat(),  # Use date() to exclude the time part
        'status': 'pending'
    }

    # Send a POST request to create a task
    response = client.post('/tasks', json=task_data)

    # Check if the response status code is 201 (Created)
    assert response.status_code == 201

    # Check if the response content type is JSON
    assert response.content_type == 'application/json'

    ## Deserialize JSON response
    data = response.json

    # Extract date part from the actual deadline string
    actual_deadline_date = datetime.strptime(data['deadline'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')

    # Check if the deadline date matches the expected date
    assert actual_deadline_date == task_data['deadline']

    # Check if the task data in the response matches the input data
    assert data['title'] == task_data['title']
    assert data['description'] == task_data['description']
    assert data['status'] == task_data['status']

    
def test_create_task_missing_data(client):
    # Prepare JSON data with missing fields for creating a task
    task_data = {
        'description': 'This is a test task',
        'deadline': datetime.now().isoformat(),
        'status': 'pending'
    }

    # Send a POST request to create a task
    response = client.post('/tasks', json=task_data)

    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400

def test_update_task(client):
    # Prepare JSON data for updating a task
    updated_task_data = {
        'title': 'Updated Test Task',  # New title
        'description': 'Updated description',  # New description
        'deadline': datetime.now().isoformat(),  # New deadline
        'status': 'completed'  # New status
    }

    # Create a new task
    task = Task(title="Test Task", description="Test Description", deadline=datetime.now(), status="Incomplete", created_by_user=1)
    db.session.add(task)
    db.session.commit()

    # Send a PATCH request to update the task
    response = client.patch(f'/tasks/{task.id}', json=updated_task_data)

    # Check if the response status code is 500 (Internal Server Error)
    assert response.status_code == 500

def test_update_task_invalid_id(client):
    # Prepare JSON data for updating a task
    updated_task_data = {
        'title': 'Updated Test Task',
        'description': 'Updated description',
        'deadline': datetime.now().isoformat(),
        'status': 'completed'
    }

    # Send a PATCH request with an invalid task ID
    response = client.patch('/tasks/999', json=updated_task_data)

    # Check if the response status code is 404 (Not Found)
    assert response.status_code == 404

def test_update_task_missing_title(client):
    # Prepare JSON data with missing title for updating a task
    updated_task_data = {
        'description': 'Updated description',
        'deadline': datetime.now().isoformat(),
        'status': 'completed'
    }

    # Create a new task
    task = Task(title="Test Task", description="Test Description", deadline=datetime.now(), status="Incomplete", created_by_user=1)
    db.session.add(task)
    db.session.commit()

    # Send a PATCH request to update a task without a title
    response = client.patch(f'/tasks/{task.id}', json=updated_task_data)

    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400
