import uvicorn
import os
import courses_api
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.src.exception_handlers import add_user_exception_handlers
from api.src.exceptions import InvalidFilterException
from db import SessionLocal
from schema import Type, Favorite, CourseExam, CreateCourseModel, UpdateCourseModel, CourseCollaboratorModel

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


@app.get('/courses/{id}')
def get_course(id: int, db=Depends(db)):
    return courses_api.get_course(db, id)


@app.put('/courses/{id}')
def update_course(id: int, course: UpdateCourseModel, db=Depends(db)):
    return courses_api.update_course(db, id, course)


@app.get('/courses')
def get_courses(db=Depends(db)):
    return courses_api.get_courses(db)


@app.get('/courses/{filter_type}/{filter_value}')
def filter_courses(filter_type, filter_value, db=Depends(db)):
    if filter_type == 'suscription':
        response = courses_api.get_courses_by_suscription(db, filter_value)
    elif filter_type == 'category':
        response = courses_api.get_courses_by_category(db, filter_value)
    elif filter_type == 'creator':
        response = courses_api.get_courses_by_creator(db, filter_value)
    else:
        raise InvalidFilterException()
    return response


@app.post('/collaborators')
def add_collaborator(request: CourseCollaboratorModel, db=Depends(db)):
    return courses_api.add_collaborator(db, request.course_id, request.collaborator_id)


@app.delete('/collaborators')
def remove_collaborator(request: CourseCollaboratorModel, db=Depends(db)):
    return courses_api.remove_collaborator(db, request.course_id, request.collaborator_id)


@app.get('/collaborators/{course_id}')
def get_collaborators_by_course(course_id, db=Depends(db)):
    return courses_api.get_collaborators_by_course(db, course_id)


@app.get('/collaborators/courses/{collaborator_id}')
def get_courses_by_collaborator(collaborator_id, db=Depends(db)):
    return courses_api.get_courses_by_collaborator(db, collaborator_id)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
