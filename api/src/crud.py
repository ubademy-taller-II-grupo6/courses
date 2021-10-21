from    sqlalchemy.orm  import Session
import  schema, models

def get_course_by_id (db: Session, id: int = None):
    if id:
        return db.query (models.Course).filter(models.Course.id == id).first()
        
def get_courses_by_type (db: Session, idtype: str = None):
    if idtype:
        return db.query (models.Course).filter(models.Course.idtype == idtype).all()        

def get_courses_by_creator (db: Session, idcreator: int = None):
    if id:
        return db.query (models.Course).filter(models.Course.idcreator == idcreator).all()
        
def get_courses(db: Session):
    return db.query (models.Course).all()
        
def create_course(db: Session, course: schema.Course):
    course_model  = models.Course(**course.dict())
    db.add(course_model)
    db.commit()
    db.refresh(course_model)
    return course_model

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

def error_message(message):
    return {
        'error': message
    }
