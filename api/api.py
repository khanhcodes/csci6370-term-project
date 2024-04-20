import time
import os 
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

DB_FILE_PATH = 'scholarDB.sqlite'

# Configure the SQLAlchemy part
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), DB_FILE_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from model import Paper, User

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/papers', methods=['GET'])
def get_papers():
    try:
        # Query all papers using SQLAlchemy
        papers_data = Paper.query.all()

        # Convert papers data into a list of dictionaries
        papers_list = [
            {
                'paper_id': paper.paper_id,
                'title': paper.title,
                'topic': paper.topic,
                'abstract': paper.abstract,
                'status': paper.status,
                'submission_date': paper.submission_date.strftime('%Y-%m-%d')  # Formatting date
            }
            for paper in papers_data
        ]

        return jsonify({'papers': papers_list}), 200

    except Exception as e:  # It's a good practice to handle specific exceptions, adjust accordingly
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['POST'])
def sign_up():
    data = request.get_json()
    data = {
        "user_name":"peng shu",
        "user_email":"aaa@uga.edu",
        "user_id": 0,
        "password": "1234"
    }

    # Basic validation to check if all fields are provided
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required_fields = ['user_name', 'password', 'user_email']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': 'Missing data, fields required: ' + ', '.join(missing_fields)}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(user_name=data['user_name']).first()
    if existing_user is not None:
        return jsonify({'error': 'Username already exists'}), 409
    existing_email = User.query.filter_by(email=data['user_email']).first()
    if existing_email is not None:
        return jsonify({'error': 'Email already exists'}), 409
    
    # Hash the password for security
    hashed_password = generate_password_hash(data['password'])

    # Create new User instance
    new_user = User(
        user_name=data['user_name'],
        password=hashed_password,
        email=data['user_email'],
        # affiliation=data.get('affiliation'),  # Optional field
        # bio=data.get('bio'),                  # Optional field
        # avatar=data.get('avatar'),            # Optional field
        # status=data.get('status')             # Optional field
    )

    # Add the new user to the database
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if not exist, should be removed in production
    app.run(debug=True)