import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
"""Models for Blogly."""

db = SQLAlchemy()

#Models go below:
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.String(50),
                     nullable = False,
                     unique = False)
    
    last_name = db.Column(db.String(50),
                          nullable = False,
                          unique = False)
    
    image_url = db.Column(db.Text,
                          nullable = False)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """Blog Post"""

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable = False)
    create_at = db.Column(db.DateTime, 
                          nullable = False,
                          default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable = False)
    
    @property
    
    def format_date(self):
        """Return a formated date"""
        
        return self.create_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class PostTag(db.Model):
    """Tag on a post"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)
    
class Tag(db.Model):
    """Tag that can be added to posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, 
                  primary_key = True)
    name = db.Column(db.Text, 
                     nullable = False,
                     unique=True)
    posts = db.relationship('Post',
                            secondary="posts_tags",
                            cascade = "all, delete",
                            backreg='tags')

def connect_db(app):
    """Connect db to Flask app"""

    db.app = app
    db.init_app(app)