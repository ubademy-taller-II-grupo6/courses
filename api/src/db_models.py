from sqlalchemy.sql.sqltypes import DECIMAL
from db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name =Column(String)
    lastname = Column(String)
    email = Column(String)
    blocked = Column(Boolean)


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(String, primary_key=True)


class Category(Base):
    __tablename__ = 'courses_categories'
    id = Column(String, primary_key=True)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    hashtags = Column(String)
    type = Column(String)
    category = Column(String)
    exams = Column(Integer)
    subscription = Column(String)
    location = Column(String)
    creator = Column(Integer, ForeignKey(User.id))
    enrollment_conditions = Column(String)
    unenrollment_conditions = Column(String)


class Collaborators(Base):
    __tablename__ = 'collaborators'
    course_id = Column(Integer, ForeignKey(Course.id), primary_key=True)
    collaborator_id = Column(Integer, ForeignKey(User.id), primary_key=True)


class Favorite(Base):
    __tablename__ = 'favorites'
    student_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    course_id = Column(Integer, ForeignKey(Course.id), primary_key=True)