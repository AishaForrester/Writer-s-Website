""" ________________Models__________________

*userAccount
*userBooks
*Tag
*BookTags
*Projects
*Chapter
*Page
*Poem
*BookTags
git push -u origin database-restructure

 """

from . import db, bcryptHash
from flask_login import  UserMixin
from datetime import datetime
from sqlalchemy.sql import func


class userAccount(db.Model, UserMixin): #user class
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(80))
    username = db.Column(db.String(100))
    password = db.Column(db.String(255))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    image = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    datecreated = db.Column(db.DateTime)
    #from sqlalchemy.sql import func

    # One-to-many relationship: a user can have many projects
    projects = db.relationship('Projects', backref='user', lazy=True)


    def __init__(self, fname, lname,uname,password,age,gender,bio, image):
        self.first_name = fname
        self.last_name = lname
        self.username = uname
        self.password = password
        self.age = age
        self.gender = gender
        self.bio = bio
        self.image = image
    
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self): #actual users must return Flase
        return False
    def get_id(self):
        try:
            return str(self.id)
        except NameError:
            return str(self.id)
    
    def __repr__(self): #string representation of an object in the database
        return '<User %r' % (self.username)

class userBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(100))
    publication_date = db.Column(db.Date)
    genre = db.Column(db.String(50))
    language = db.Column(db.String(50))
    page_count = db.Column(db.Integer)
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    currency = db.Column(db.String(10))
    cover_image = db.Column(db.String(255))
    book_format = db.Column(db.String(50))
    availability = db.Column(db.Boolean, default=True)
    author_bio = db.Column(db.Text)
    series = db.Column(db.String(100))
    country = db.Column(db.String(50))
    book_url = db.Column(db.String(255))

    #Foreign key to Projects
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    project = db.relationship('Projects', backref='user_books', lazy=True)

    #Setting up a many-to-many relationship where a book can have many tags and a tag can have many 
    tags = db.relationship('Tag', secondary='book_tags', backref=db.backref('books', lazy='dynamic')) #keywords for fining books


    def __init__(self, title, author, genre, price, description, cover_image, book_format, project_id,
                  author_bio=None, series=None, country=None, book_url=None,tags= None, rating=0, stock=0, 
                  availability=0, publisher=None, publication_date=None,language=None, currency=None):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publication_date = publication_date
        self.genre = genre
        self.language = language
        self.description = description
        self.currency = currency
        self.cover_image = cover_image
        self.book_format = book_format
        self.tags = tags or []
        self.author_bio = author_bio
        self.series = series
        self.country = country
        self.book_url = book_url
        self.rating = rating
        self.stock = stock
        self.price = price
        self.availability = availability
        self.project_id = project_id

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"<Tag {self.name}>"

"""Association table
A many-to-many relationship where userBooks and tags are linked"""
class BookTags(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('user_books.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

"""
_____________Relationships here___________
The Projects table have fields such as title, synopsis, price, genre, image, created_at and project_type.
The project_type can be a book, short story or poem. We have relationships with other models from the 
Project table. chapter relationship: chapters = db.relationship('Chapter', backref='book', lazy=True),
means that Project (object) can have many chapters associated with it. backref='book' means a reverse
relationship where you can access the parent Projects object from a chapter instance via the book attribute

pages = db.relationship('Page', backref='story', lazy=True) means that the Projects object can have many Page 
objects. the backref='story' allows access to the Projects object from a Page instance using the story attribute

poem_content = db.relationship('Poem', backref='poem', lazy=True) means that the Projects object can have 
many Poem objects. The backref='poem' allows access back to the Projects object from a Poem instnace via
poem attribute  
"""  

class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text)
    price = db.Column(db.Float)
    genre = db.Column(db.String(100))
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    project_type = db.Column(db.String(100),nullable=False) #book, short_story or poem

    #relationships
    chapters = db.relationship('Chapter', backref='book', lazy=True, cascade='all, delete-orphan') #cascade deletes all child objects when parent is deleted
    pages = db.relationship('Page', backref='story', lazy=True, cascade='all, delete-orphan')
    poem_content = db.relationship('Poem',backref='poem', lazy=True, cascade='all, delete-orphan')

    #foreign key associated with the userAccount table
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, title, synopsis, genre,price, image, project_type, user_id):
        self.title = title
        self.synopsis =synopsis
        self.genre = genre
        self.price = price
        self.image = image
        self.project_type = project_type
        self.user_id = user_id

    def __repr__(self): #string representation of an object in the database
        return  f"<Project {self.title}  ({self.project_type})>"



class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    chapter_number = db.Column(db.Integer, nullable=False)  # Ensure ordering of chapters
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    # Rename the backref to "pages" instead of "chapter"
    #pages = db.relationship('Page', backref='parent_chapter', lazy=True)  # Renamed backref to "parent_chapter"s
    pages = db.relationship('Page', backref='chapter', lazy=True, cascade='all, delete-orphan')

    #Relationships with pages
    #pages = db.relationship('Page', backref='chapter', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Chapter {self.chapter_number} - {self.title}>"

class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete="CASCADE"), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id', ondelete="CASCADE"), nullable=True)
    content = db.Column(db.Text, nullable=False) 
    page_number = db.Column(db.Integer, nullable=False)  # Ensure ordering of pages
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    

    def __repr__(self):
        return f"<Page {self.page_number}>"

class Poem(db.Model):
    __tablename__ = 'poems'

    id = db.Column(db.Integer, primary_key=True)
    poem_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Poem {self.id}>"


    