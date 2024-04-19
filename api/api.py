import time
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

DB_FILE = 'scholarDB.sqlite'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/papers', methods=['GET'])
def get_papers():
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        # Select all papers from the 'papers' table
        cursor.execute("SELECT * FROM papers")
        papers_data = cursor.fetchall()

        connection.close()

        # Convert papers data into a list of dictionaries
        papers_list = []
        for paper in papers_data:
            paper_dict = {
                'paper_id': paper[0],
                'title': paper[1],
                'topic': paper[2],
                'abstract': paper[3],
                'status': paper[4],
                'submission_date': paper[5]
            }
            papers_list.append(paper_dict)

        return jsonify({'papers': papers_list}), 200

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    
    
if __name__ == '__main__':
    app.run(debug=True)