import time
import os 
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import date


DB_FILE_PATH = 'scholarDB.sqlite'

# Configure the SQLAlchemy part
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), DB_FILE_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from model import Paper, User, Follow

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
    
@app.route('/papers', methods=['POST'])
def create_paper():
    data = request.get_json()
    new_paper = Paper(
        title=data['title'],
        topic=data['topic'],
        abstract=data['abstract'],
        status=data['status'],
        submission_date=date.today()  # Assuming submission_date is set to current date
    )
    db.session.add(new_paper)
    db.session.commit()
    return jsonify({'message': 'Paper created successfully'}), 201

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

# Endpoint to create a follow relationship between users
@app.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    follower_id = data.get('follower_id')
    followed_id = data.get('followed_id')

    if not follower_id or not followed_id:
        return jsonify({'error': 'Both follower_id and followed_id are required'}), 400

    # Check if both users exist in the database
    follower = User.query.get(follower_id)
    if not follower:
        return jsonify({'error': 'Follower not found'}), 404

    user_to_follow = User.query.get(followed_id)
    if not user_to_follow:
        return jsonify({'error': 'User to follow not found'}), 404

    # Check if the follow relationship already exists
    existing_follow = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if existing_follow:
        return jsonify({'message': 'Follow relationship already exists'}), 200

    # Create a new follow relationship in the database
    new_follow = Follow(follower_id=follower_id, followed_id=followed_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({'message': 'Follow relationship created successfully'}), 201
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if not exist, should be removed in production
    app.run(debug=True)