from    sqlalchemy.orm  import Session
import  schema, models

def get_course_by_id (db: Session, id: int = None):
    if id:
        return db.query (models.Course).filter(models.Course.id == id).first()

def get_type_by_id (db: Session, idtype: str):
    if idtype:
        return db.query (models.Type).filter(models.Type.id == idtype).first()

def get_types (db: Session):
    return db.query (models.Type).all()    
        
def get_courses_by_type (db: Session, idtype: str = None):
    if idtype:
        return db.query (models.Course).filter(models.Course.idtype == idtype).all()        

def get_courses_by_creator (db: Session, idcreator: int = None):
    if id:
        return db.query (models.Course).filter(models.Course.idcreator == idcreator).all()
        
def get_courses(db: Session):
    return db.query (models.Course).all()

def get_exam_by_course(db: Session, idcourse: int, idexam: int):
    if idcourse:
        if idexam:
            return db.query (   models.CourseExam).filter(
                                models.CourseExam.idcourse == idcourse).filter(
                                models.CourseExam.idexam == idexam).first()

def get_exams(db: Session, idcourse: int):
    if idcourse:
        return db.query (models.CourseExam).filter(models.CourseExam.idcourse == idcourse).all()

def create_type(db: Session, type: schema.Type):
    type_model = models.Type(**type.dict())
    db.add(type_model)
    db.commit()
    db.refresh(type_model)
    return type_model
        
def create_course(db: Session, course: schema.Course):
    course_model  = models.Course(**course.dict())
    db.add(course_model)
    db.commit()
    db.refresh(course_model)
    return course_model

def create_courseexam(db: Session, courseexam: schema.CourseExam):
    courseexam_model = models.CourseExam(**courseexam.dict())
    db.add(courseexam_model)
    db.commit()
    db.refresh(courseexam_model)
    return courseexam_model

def update_course(db: Session, id: int, course: schema.Course):
    course_model                    = models.Course(**course.dict())
    course_to_update                = db.query (models.Course).filter(models.Course.id == id).first() 
    course_to_update.title          = course_model.title
    course_to_update.description    = course_model.description
    course_to_update.idtype         = course_model.idtype 
    course_to_update.location       = course_model.location
    course_to_update.price          = course_model.price
    course_to_update.link           = course_model.link
    course_to_update.idcreator      = course_model.idcreator
    db.add(course_to_update)
    db.commit()
    db.refresh(course_to_update)
    return course_to_update

def update_type(db: Session, type: schema.Type):
    type_model                      = models.Type(**type.dict())
    type_to_update                  = db.query (models.Type).filter(models.Type.id == type.id).first()
    type_to_update.description      = type_model.description
    db.add(type_to_update)
    db.commit()
    db.refresh(type_to_update)
    return type_to_update

def get_courses_favorites(db: Session, idstudent):
    return db.query (models.Favorite).filter(models.Favorite.idstudent==idstudent).all()

def get_course_favorite_by_student(db: Session, idcourse, idstudent):
    return db.query (models.Favorite).filter(models.Favorite.idcourse==idcourse).filter(models.Favorite.idstudent==idstudent).first()

def create_course_favorite(db: Session, favorite: schema.Favorite):
    favorite_model  = models.Favorite(**favorite.dict())
    db.add(favorite_model)
    db.commit()
    db.refresh(favorite_model)
    return favorite_model

def delete_course_favorite(db: Session, favorite: schema.Favorite):
    favorite_model      = models.Favorite(**favorite.dict())
    favorite_to_delete  = db.query( models.Favorite).filter(
                                    models.Favorite.idcourse==favorite_model.idcourse).filter(
                                    models.Favorite.idstudent==favorite_model.idstudent).first() 
    db.delete(favorite_to_delete)
    db.commit()
    return favorite

def delete_courseexam (db: Session, courseexam: schema.CourseExam):
    courseexam_model        = models.CourseExam(**courseexam.dict())
    courseexam_to_delete    = db.query( models.CourseExam).filter(
                                        models.CourseExam.idcourse == courseexam_model.idcourse).filter(
                                        models.CourseExam.idexam == courseexam_model.idexam).first() 
    db.delete(courseexam_to_delete)
    db.commit()
    return courseexam

def delete_type (db: Session, type: schema.Type):
    type_model        = models.Type(**type.dict())
    type_to_delete    = db.query(   models.Type).filter(
                                    models.Type.id == type_model.id).first() 
    db.delete(type_to_delete)
    db.commit()
    return type
        
def error_message(message):
    return {
        'error': message
    }
