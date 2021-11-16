from pydantic                   import BaseModel

class Course (BaseModel):
    title                   :   str
    description             :   str 
    idtype                  :   str
    location                :   str
    price                   :   float
    link                    :   str
    idcreator               :   int
    
    class Config:
        orm_mode = True
        
class Favorite (BaseModel):
    idcourse                :   int
    idstudent               :   int
    class Config:
        orm_mode = True                
        
class CourseExam (BaseModel):
    idcourse                :   int
    idexam                  :   int
    class Config:
        orm_mode = True                        