from api import db

# DB_FILE = 'scholarDB.sqlite'


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    affiliation = db.Column(db.String(255))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    status = db.Column(db.String(255))

    def get_user_id(self):
        return self.user_id

    def get_user_name(self):
        return self.user_name
    
    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

    def get_affiliation(self):
        return self.affiliation

    def get_bio(self):
        return self.bio

    def get_avatar(self):
        return self.avatar

    def get_status(self):
        return self.status 

class Paper(db.Model):
    __tablename__ = 'papers'
    paper_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    abstract = db.Column(db.Text)
    status = db.Column(db.String(255))
    submission_date = db.Column(db.Date)
    video_url = db.Column(db.String(255))
    bibtex = db.Column(db.String(255))
    pdf_url = db.Column(db.String(255))

    def get_paper_id(self):
        return self.paper_id

    def get_title(self):
        return self.title

    def get_topic(self):
        return self.topic

    def get_abstract(self):
        return self.abstract

    def get_status(self):
        return self.status

    def get_submission_date(self):
        return self.submission_date
    
    def get_video_url(self):
        return self.video_url
    
    def get_bibtex(self):
        return self.bibtex
    
    def get_pdf_url(self):
        return self.pdf_url

class Authorship(db.Model):
    __tablename__ = 'authorship'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.paper_id'), primary_key=True)

    def get_user_id(self):
        return self.user_id

    def get_paper_id(self):
        return self.paper_id

class PaperList(db.Model):
    __tablename__ = 'paper_lists'
    list_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    list_name = db.Column(db.String(255))

    def get_list_id(self):
        return self.list_id

    def get_user_id(self):
        return self.user_id

    def get_list_name(self):
        return self.list_name

class PaperListContent(db.Model):
    __tablename__ = 'paper_list_contents'
    list_id = db.Column(db.Integer, db.ForeignKey('paper_lists.list_id'), primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.paper_id'), primary_key=True)

    def get_list_id(self):
        return self.list_id

    def get_paper_id(self):
        return self.paper_id
    
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)

    def get_follower_id(self):
        return self.follower_id

    def get_followed_id(self):
        return self.followed_id

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.paper_id'))
    comment_date = db.Column(db.Date)
    content = db.Column(db.Text)

    def get_comment_id(self):
        return self.comment_id

    def get_user_id(self):
        return self.user_id

    def get_paper_id(self):
        return self.paper_id

    def get_comment_date(self):
        return self.comment_date

    def get_content(self):
        return self.content