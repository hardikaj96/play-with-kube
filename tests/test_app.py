import json
from flask_sqlalchemy import SQLAlchemy
import pytest
import jwt
from app.app import app, db, User


@pytest.fixture
def client():
    with app.test_client() as client2:
        with app.app_context():
            db.create_all()
            yield client2
            db.drop_all()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'Healthy!!!'}

def test_register(client):
    # Make a registration request
    response = client.post('/register', json={'username': 'test_user', 'password': 'test_password'})
    assert response.status_code == 201
    assert json.loads(response.data) == {'message': 'User created successfully'}
    user = User.query.filter_by(username='test_user').first()
    assert user is not None

def test_login(client):
    _ = client.post('/register', json={'username': 'test_user', 'password': 'test_password'})
    # Make a login request with the registered user
    response = client.post('/login', json={'username': 'test_user', 'password': 'test_password'})
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data)

    # Make a login request with invalid credentials
    response_invalid = client.post('/login', json={'username': 'nonexistent_user', 'password': 'wrong_password'})
    assert response_invalid.status_code == 401
    assert json.loads(response_invalid.data) == {'message': 'Invalid credentials'}


def test_protected_endpoint_with_valid_token(client):
    _ = client.post('/register', json={'username': 'test_user', 'password': 'test_password'})
    # Make a login request with the registered user
    response = client.post('/login', json={'username': 'test_user', 'password': 'test_password'})
    valid_token = json.loads(response.data)['access_token']
    # Make a request with a valid token
    headers = {'Authorization': valid_token}
    response = client.get('/protected', headers=headers)

    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Hello, test_user! This is a protected endpoint.'}

def test_protected_endpoint_with_invalid_token(client):
    # Make a request with an invalid token
    headers = {'Authorization': 'invalid_token'}
    response = client.get('/protected', headers=headers)

    assert response.status_code == 401
    assert json.loads(response.data) == {'message': 'Invalid token'}

def test_protected_endpoint_with_expired_token(client):
    # Make a request with an expired token
    expired_token = jwt.encode({'exp': 1}, app.config['SECRET_KEY'], algorithm='HS256')
    headers = {'Authorization': expired_token}
    response = client.get('/protected', headers=headers)

    assert response.status_code == 401
    assert json.loads(response.data) == {'message': 'Token has expired'}

def test_protected_endpoint_without_token(client):
    # Make a request without a token
    response = client.get('/protected')

    assert response.status_code == 401
    assert json.loads(response.data) == {'message': 'Token is missing'}
