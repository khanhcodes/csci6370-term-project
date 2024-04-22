import sqlite3
import random
import hashlib
from datetime import datetime, timedelta

# Define the path to your SQLite database file
DB_FILE = 'scholarDB.sqlite'
SCHEMA_FILE = 'schema.sql'

# Function to generate a random date
def random_date(start, end):
    return (start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))).date()

def init_db():
    # Connect to SQLite database
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Read and execute the schema.sql file to create tables
    with open(SCHEMA_FILE, 'r') as schema_file:
        schema_sql = schema_file.read()
        cursor.executescript(schema_sql)

    # # Insert test data into the users table
    # users_data = [
    #     (3, 'Kaitlyn Nguyen', 'dumb', 'john@example.com', 'University A', 'Bio for Kaitlyn', 'avatar1.jpg', 'Active'),
    #     (4, 'Shu Peng', 'hellohello', 'jane@example.com', 'University B', 'Bio for Shu', 'avatar2.jpg', 'Inactive')
    # ]
    # cursor.executemany("INSERT INTO users (user_id, user_name, password, email, affiliation, bio, avatar, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", users_data)

    # # Insert test data into the papers table
    # papers_data = [
    #     (3, 'Paper_1', 'Topic A', 'Abstract for Paper 1', 'Submitted', '2024-04-20', 'https://www.youtube.com/',
    #    r"""@article{vaswani2017attention,
    # title={Attention is all you need},
    # author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\L}ukasz and Polosukhin, Illia},
    # journal={Advances in neural information processing systems},
    # volume={30},
    # year={2017}
    # }""", 'https://proceedings.neurips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf'),

    #     (4, 'Paper_2', 'Topic B', 'Abstract for Paper 2', 'Under Review', '2024-04-21', 'https://www.youtube.com/watch?v=vFqTzBj575Y',
    #     r"""@article{koroteev2021bert,
    # title={BERT: a review of applications in natural language processing and understanding},
    # author={Koroteev, MV},
    # journal={arXiv preprint arXiv:2103.11943},
    # year={2021}
    # }""", 'https://arxiv.org/ftp/arxiv/papers/2103/2103.11943.pdf')
    # ]
    # cursor.executemany("INSERT INTO papers (paper_id, title, topic, abstract, status, submission_date, video_url, bibtex, pdf_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", papers_data)

    # # Insert test data into the authorship table
    # authorship_data = [
    #     (1, 3),  
    #     (2, 4)   
    # ]
    # cursor.executemany("INSERT INTO authorship (user_id, paper_id) VALUES (?, ?)", authorship_data)

        # Generate users
    for i in range(1, 51):
        user_id = i
        user_name = f'user_{i}'
        password = hashlib.sha256(f'password_{i}'.encode()).hexdigest()
        email = f'user_{i}@example.com'
        affiliation = f'Affiliation {i}'
        bio = f'Bio of user {i}.'
        avatar = f'avatars/avatar{i}.jpg'
        status = 'active'
        cursor.execute('INSERT INTO users (user_id, user_name, password, email, affiliation, bio, avatar, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                    (user_id, user_name, password, email, affiliation, bio, avatar, status))

    # Generate papers
    for i in range(1, 51):
        paper_id = i
        title = f'Paper Title {i}'
        topic = f'Topic {i}'
        abstract = f'Abstract for Paper {i}.'
        status = 'submitted'
        submission_date = random_date(datetime(2020, 1, 1), datetime.now())
        video_url = f'videos/video{i}.mp4'
        bibtex = f'BibTeX{i}'
        pdf_url = f'papers/paper{i}.pdf'
        cursor.execute('INSERT INTO papers (paper_id, title, topic, abstract, status, submission_date, video_url, bibtex, pdf_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                    (paper_id, title, topic, abstract, status, submission_date, video_url, bibtex, pdf_url))

    # Generate authorship
    for i in range(1, 51):
        cursor.execute('INSERT INTO authorship (user_id, paper_id) VALUES (?, ?)', (i, i))

    # # Generate paper_lists
    # for i in range(1, 51):
    #     list_name = f'List Name {i}'
    #     cursor.execute('INSERT INTO paper_lists (user_id, list_name) VALUES (?, ?)', (i, list_name))

    # # Generate paper_list_contents
    # for i in range(1, 51):
    #     cursor.execute('INSERT INTO paper_list_contents (list_id, paper_id) VALUES (?, ?)', (i, i))

    # Generate follows
    for i in range(1, 51):
        follower_id = i
        followed_id = i + 1 if i < 50 else 1
        cursor.execute('INSERT INTO follows (follower_id, followed_id) VALUES (?, ?)', (follower_id, followed_id))

    # Generate comments
    for i in range(1, 51):
        comment_id = i
        user_id = i
        comment_date = random_date(datetime(2020, 1, 1), datetime.now())
        content = f'Comment content {i}.'
        cursor.execute('INSERT INTO comments (user_id, paper_id, comment_date, content) VALUES (?, ?, ?, ?)', 
                    (comment_id, user_id, comment_date, content))    

    # Commit changes and close connection
    connection.commit()
    connection.close()

def check_table_existence(table_name):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Query SQLite system table to check if the table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    result = cursor.fetchone()

    connection.close()

    return result is not None

def print_papers_table():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Select all rows from the 'papers' table
    cursor.execute("SELECT * FROM comments")
    papers_data = cursor.fetchall()

    connection.close()

    # Print the contents of the 'papers' table
    if papers_data:
        print("Contents of 'papers' table:")
        for row in papers_data:
            print(row)
    else:
        print("No data found in 'papers' table.")

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")

    table_name = 'comments'
    exists = check_table_existence(table_name)
    if exists:
        print(f"Table '{table_name}' exists in the database.")
        # Print contents of the 'papers' table
        print_papers_table()
    else:
        print(f"Table '{table_name}' does not exist in the database.")

