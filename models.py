from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

from flask import Blueprint

snippet = Blueprint('snippet', __name__)

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Snippet(Base):
    __tablename__ = 'Snippets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=True)
    def __init__(self, content=None):
        self.content = content

# Create tables.
Base.metadata.create_all(bind=engine)