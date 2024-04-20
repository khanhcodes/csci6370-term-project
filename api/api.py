import time
import os 
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date


DB_FILE_PATH = 'scholarDB.sqlite'

# Configure the SQLAlchemy part
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), DB_FILE_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from model import Paper

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if not exist, should be removed in production
    app.run(debug=True)