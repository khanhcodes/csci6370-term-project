import time
from flask import Flask, jsonify
from models import db, Paper 

app = Flask(__name__)

# DB_FILE = 'scholarDB.sqlite'

# Configure the SQLAlchemy part
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scholarDB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if not exist, should be removed in production
    app.run(debug=True)