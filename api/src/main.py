import uvicorn
import os
import courses_api
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.src.exception_handlers import add_user_exception_handlers
from api.src.exceptions import InvalidFilterException, InvalidOperationException
from db import SessionLocal
from schema import CreateCourseModel, UpdateCourseModel, CourseCollaboratorModel, FavoriteModel

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )
add_user_exception_handlers(app)


def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/courses')
def create_course(course: CreateCourseModel, db=Depends(db)):
    return courses_api.create_course(db, course)


@app.get('/courses')
def get_courses(id=None, category=None, subscription=None, creator =None, db=Depends(db)):
    return courses_api.get_courses(db, id, category, subscription, creator)


@app.put('/courses/{id}')
def update_course(id: int, course: UpdateCourseModel, db=Depends(db)):
    return courses_api.update_course(db, id, course)


@app.post('/courses/collaborators')
def add_collaborator(request: CourseCollaboratorModel, db=Depends(db)):
    return courses_api.add_collaborator(db, request.course_id, request.collaborator_email)


@app.get('/courses/collaborators')
def get_courses_collaborators(course_id = None , collaborator_email = None, db=Depends(db)):
    if course_id:
        return courses_api.get_collaborators_by_course(db, course_id)
    elif collaborator_email:
        return courses_api.get_courses_by_collaborator(db, collaborator_email)
    raise InvalidOperationException("Operacion invalida")


@app.delete('/courses/collaborators')
def remove_collaborator(request: CourseCollaboratorModel, db=Depends(db)):
    return courses_api.remove_collaborator(db, request.course_id, request.collaborator_email)


@app.get('/courses/favorites/{student_id}')
def get_favorites(student_id, category=None, subscription=None, db=Depends(db)):
    return courses_api.get_favorites(db, student_id, category, subscription)


@app.post('/courses/favorites')
def add_to_favorites(favorite: FavoriteModel, db=Depends(db)):
    return courses_api.add_to_favorites(db, favorite)


@app.delete('/courses/favorites')
def delete_favorite(favorite: FavoriteModel, db=Depends(db)):
    return courses_api.delete_favorite(db, favorite)


@app.get('/courses/categories')
def get_categories(db=Depends(db)):
    return courses_api.get_categories(db)



if __name__ == '__main__':
    #uvicorn.run('main:app', reload=True)
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT')), reload=True)
