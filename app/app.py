from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['TESTING'] = os.environ.get('DEBUG') == '0'

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True  # Set TESTING to True for Flask to use a separate test database

app.config.from_object(DevelopmentConfig)  # Default to development configuration
if app.config['TESTING']:
    app.config.from_object(TestConfig)  # Use test configuration if TESTING is True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create an application context before running the code
with app.app_context():
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'Healthy!!!'})
    
    # Endpoint for user registration
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        new_user = User(username=data['username'], password=data['password'])
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return jsonify({'message': 'Error creating user'}), 500
        finally:
            db.session.close()

    # Endpoint for user login
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(username=data['username'], password=data['password']).first()

        if user:
            # Create a JWT token
            expiration_time = datetime.utcnow() + timedelta(hours=1)  # Adjust the expiration time as needed
            token = jwt.encode({'username': data['username'], 'exp': expiration_time}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify(access_token=token), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/protected', methods=['GET'])
    def protected():
        # Check if there's a token in the request headers
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode the token and extract the username
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = payload['username']
            return jsonify({'message': f'Hello, {user}! This is a protected endpoint.'}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

    if __name__ == '__main__':
        db.create_all()
        app.run(host='0.0.0.0', port='5000', debug=True)
