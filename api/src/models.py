from sqlalchemy.sql.sqltypes import DECIMAL
from db                  import Base
from sqlalchemy          import Column, Integer, String, Boolean

class Course(Base):
    __tablename__   = 'courses'
    id              = Column(Integer, primary_key = True)
    title           = Column(String)
    description     = Column(String)
    idtype          = Column(String)
    location        = Column(String)
    price           = Column(DECIMAL)
    link            = Column(String)
    idcreator       = Column(Integer)
    
class Favorite(Base):
    __tablename__   = 'favorites'
    idcourse        = Column(Integer, primary_key = True)
    idstudent       = Column(Integer, primary_key = True)
    
class CourseExam(Base):
    __tablename__   = 'coursesexams'
    id              = Column(Integer, primary_key = True)
    idcourse        = Column(Integer)
    idexam          = Column(Integer)    
        
    