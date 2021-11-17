import  uvicorn
import  os
import  crud
from    fastapi                 import FastAPI, Depends, HTTPException
from    fastapi.middleware.cors import CORSMiddleware
from    db                      import SessionLocal
from    schema                  import Course, Type, Favorite, CourseExam    
import  models 
                                
app = FastAPI()
app.add_middleware( CORSMiddleware, 
                    allow_origins=["*"], 
                    allow_credentials=True, 
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )

def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
@app.get('/courses/{idcourse}')
def get_course_by_id (idcourse:int, db=Depends(db)):
    course = crud.get_course_by_id(db,idcourse)
    if course:
        return course
    else:
        raise HTTPException(404, crud.error_message(f'No existe el curso con id: {idcourse}'))

@app.get('/courses/')
def get_courses(db=Depends(db)):
    courses = crud.get_courses(db)
    if courses:
        return courses
    else:
        raise HTTPException(404, crud.error_message('No existen cursos'))
    
@app.get('/courses/types/{idtype}')
def get_courses_by_type (idtype:str, db=Depends(db)):
    courses = crud.get_courses_by_type(db,idtype)
    if courses:
        return courses
    else:
        raise HTTPException(404, crud.error_message(f'No existen cursos del tipo id: {idtype}'))

@app.get('/types/{idtype}')
def get_type(idtype: str, db=Depends(db)):                      
    type_exists = crud.get_type_by_id(db, idtype)
    if type_exists: 
        return type_exists
    else:
        raise HTTPException(404, detail= crud.error_message(f'El tipo de curso con id : {idtype} no existe'))

@app.get('/types/')
def get_type(db=Depends(db)):                      
    types_exists = crud.get_types(db)
    if types_exists: 
        return types_exists
    else:
        raise HTTPException(404, detail= crud.error_message(f'No existen tipos de cursos'))
        
@app.post('/types/')
def create_type(type: Type, db=Depends(db)):                      
    type_exists = crud.get_type_by_id(db, type.id)
    if type_exists: 
        raise HTTPException(404, detail= crud.error_message(f'El tipo de curso con id : {type.id} ya existe'))
    else:
        return crud.create_type(db, type)
            
@app.put('/types/')
def update_type(type: Type, db=Depends(db)):                      
    type_exists = crud.get_type_by_id(db, type.id)
    if type_exists: 
        return crud.update_type(db, type)
    else:
        raise HTTPException(404, detail= crud.error_message(f'El tipo de curso con id : {type.id} no existe'))
                 
@app.get('/courses/favorites/{idstudent}')
def get_courses_favorites(idstudent: int, db=Depends(db)):
    courses_favorites = crud.get_courses_favorites(db, idstudent)
    if courses_favorites:
        return courses_favorites
    else:
        raise HTTPException(404, detail= crud.error_message(f'No existen cursos favoritos para el estudiante con id: {idstudent}'))
     
@app.get('/courses/creators/{idcreator}')
def get_courses_by_creator (idcreator:int, db=Depends(db)):
    courses = crud.get_courses_by_creator(db,idcreator)
    if courses:
        return courses
    else:
        raise HTTPException(404, crud.error_message(f'No existen cursos creados por el creador con id: {idcreator}'))

@app.get('/courses/{idcourse}/exams/')
def get_exams (idcourse:int, db=Depends(db)):
    exams = crud.get_exams(db,idcourse)
    if exams:
        return exams
    else:
        raise HTTPException(404, crud.error_message(f'No existen examenes asignados al curso con id: {idcourse}'))
            
@app.get('/courses/{idcourse}/exams/{idexam}/')
def get_exam_by_course (idcourse:int, idexam: int, db=Depends(db)):
    exam = crud.get_exam_by_course (db,idcourse, idexam)
    if exam:
        return exam
    else:
        raise HTTPException(404, crud.error_message(f'El examen con id: {idexam} no esta asignado al curso con id: {idcourse}'))
                
@app.post('/courses/')
def create_course(course: Course, db=Depends(db)):
    return crud.create_course(db, course)

@app.put('/courses/')
def update_course(idcourse: int , course: Course, db=Depends(db)):
    course_exists = crud.get_course_by_id(db, idcourse)
    if course_exists:
        return crud.update_course(db, idcourse, course)
    else:
        raise HTTPException(404, detail= crud.error_message(f'No existe el curso con id: {idcourse}'))
    
@app.post('/courses/favorites/')
def create_course_favorite(favorite: Favorite, db=Depends(db)):
    favorite_exists = crud.get_course_favorite_by_student(db, favorite.idcourse, favorite.idstudent)
    if favorite_exists:
        raise HTTPException(404, detail= crud.error_message(f'El curso con id: {favorite.idcourse} ya existe como favorito para el estudiante con id: {favorite.idstudent}'))
    else:    
        return crud.create_course_favorite (db, favorite)
    
@app.delete('/courses/favorites/')
def delete_course_favorite(favorite: Favorite, db=Depends(db)):
    favorite_exists = crud.get_course_favorite_by_student(db, favorite.idcourse, favorite.idstudent)
    if favorite_exists:
        return crud.delete_course_favorite (db, favorite)    
    else:    
        raise HTTPException(404, detail= crud.error_message(f'El curso con id: {favorite.idcourse} no existe como favorito para el estudiante con id: {favorite.idstudent}'))

@app.post('/courses/exams/')
def create_courseexam (courseexam: CourseExam, db=Depends(db)):
    courseexam_exists = crud.get_exam_by_course(db,courseexam.idcourse, courseexam.idexam)   
    if courseexam_exists:
        raise HTTPException(404, detail= crud.error_message(f'El examen con id: {courseexam.idexam} ya esta asignado al curso con id: {courseexam.idcourse}'))
    else:    
        return crud.create_courseexam(db, courseexam)           

@app.delete('/courses/exams/')
def delete_courseexam(courseexam: CourseExam, db=Depends(db)):
    courseexam_exists = crud.get_exam_by_course(db, courseexam.idcourse, courseexam.idexam)
    if courseexam_exists:
        return crud.delete_courseexam (db, courseexam_exists)    
    else:    
        raise HTTPException(404, detail= crud.error_message(f'El examen con id: {courseexam.idexam} no esta asignado al curso con id: {courseexam.idcourse}'))

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT')), reload=True)        
