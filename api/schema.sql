DROP TABLE users;

-- Create User Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(255),
    password VARCHAR(255),
    email VARCHAR(255),
    affiliation VARCHAR(255),
    bio TEXT,
    avatar VARCHAR(255),
    status VARCHAR(255)
);

-- Create Paper Table
CREATE TABLE IF NOT EXISTS papers (
    paper_id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    topic VARCHAR(255),
    abstract TEXT,
    status VARCHAR(255),
    submission_date DATE
);

-- Create Authorship Table
CREATE TABLE IF NOT EXISTS authorship (
    user_id INTEGER,
    paper_id INTEGER,
    PRIMARY KEY (user_id, paper_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE
);

-- Create PaperList Table
CREATE TABLE IF NOT EXISTS paper_lists (
    list_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    list_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create PaperListContents Table
CREATE TABLE IF NOT EXISTS paper_list_contents (
    list_id INTEGER,
    paper_id INTEGER,
    PRIMARY KEY (list_id, paper_id),
    FOREIGN KEY (list_id) REFERENCES paper_lists(list_id) ON DELETE CASCADE,
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE
);

-- Create Follow Table
CREATE TABLE IF NOT EXISTS follows (
    follower_id INTEGER,
    followed_id INTEGER,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (followed_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create Comments Table
CREATE TABLE IF NOT EXISTS comments (
    comment_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    paper_id INTEGER,
    comment_date DATE,
    content TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE
);
