import  uvicorn
import  os
import  crud
from    fastapi                 import FastAPI, Depends, HTTPException
from    fastapi.middleware.cors import CORSMiddleware
from    db                      import SessionLocal
from    schema                  import Course, Favorite     
                                
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
@app.get('/courses/{id}')
def get_course_by_id (id:int, db=Depends(db)):
    course = crud.get_course_by_id(db,id)
    if course:
        return course
    else:
        raise HTTPException(404, crud.error_message(f'No existe el curso con id: {id}'))

@app.get('/courses')
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
            
@app.post('/courses/')
def create_course(course: Course, db=Depends(db)):
    return crud.create_course(db, course)

@app.put('/courses/')
def update_course(id: int , course: Course, db=Depends(db)):
    course_exists = crud.get_course_by_id(db, id)
    if course_exists is None:
        raise HTTPException(404, detail= crud.error_message(f'No existe el curso con id: {id}'))
    return crud.update_course(db, id, course)

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

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT')), reload=True)        
