from sqlalchemy.sql.sqltypes import DECIMAL
from db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    hashtags = Column(String)
    type = Column(String)
    category = Column(String)
    exams = Column(Integer)
    suscription = Column(String)
    location = Column(String)
    creator = Column(Integer)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name =Column(String)
    lastname = Column(String)
    email = Column(String)
    blocked = Column(Boolean)


class Collaborators(Base):
    __tablename__ = 'collaborators'
    course_id = Column(Integer, ForeignKey(Course.id), primary_key=True)
    collaborator_id = Column(Integer, ForeignKey(Users.id), primary_key=True)
