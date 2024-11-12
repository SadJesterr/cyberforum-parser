import os

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv

from utils import *

load_dotenv()
engine = create_engine(f'sqlite:///{os.getenv("DATABASE_NAME")}', echo=False)
session_factory = sessionmaker(engine)

Base = declarative_base()

class Theme(Base):
    __tablename__ = "theme"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)

    def __repr__(self):
        return f"name={self.name}, text={self.text}"

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    nickname = Column(String)

    def __repr__(self):
        return f"nickname={self.name}"

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, ForeignKey('theme.id'))
    author_id = Column(Integer, ForeignKey('author.id'))
    quote_id = Column(Integer, ForeignKey('comment.id'))
    text = Column(String)
    created = Column(String)
    likes = Column(Integer)

    theme = relationship(Theme)
    author = relationship(Author)

    def __repr__(self):
        return f"theme_id={self.theme_id}, author_id={self.author_id}, quote_id={self.quote_id}, text={self.text}, created={self.created}, likes={self.likes}"


def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_data(theme_data, author_data, comment_data):
    with session_factory() as session:
        insert_arr = []
        for i in theme_data:
            insert_arr.append(Theme(name=i[0],
                                    text=i[1]))
        for i in author_data:
            insert_arr.append(Author(nickname=i[0]))
        for i in comment_data:
            insert_arr.append(Comment(text=i[0],
                                      created=i[1],
                                      likes=i[2]))
        session.add_all(list(set(insert_arr)))
        session.commit()