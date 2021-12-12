import sqlalchemy
from sqlalchemy.orm import Session
import schema
from api.src import db_models
from api.src.exceptions import InvalidOperationException, InvalidCourseIdException
from api.src.utils import create_message_response, validate_nulls, get_courses_dict


def create_course(db: Session, course: schema.CreateCourseModel):
    course_dict = course.dict()
    if validate_nulls(course_dict.values()):
        raise InvalidOperationException("Se encontraron datos faltantes")

    course_model = db_models.Course(**course_dict)
    db.add(course_model)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise InvalidOperationException(" Uno o mas campos son incorrectos")
    response = create_message_response("El curso se creó correctamente")
    return response


def get_course(db: Session, id: int = None):
    course = db.query(db_models.Course).filter(db_models.Course.id == id).first()
    if not course:
        raise InvalidCourseIdException(id)
    return course


def update_course(db: Session, id: int, course: schema.UpdateCourseModel):
    prev_course_data = db.query(db_models.Course).filter(db_models.Course.id == id).first()
    if not prev_course_data:
        raise InvalidCourseIdException(id)
    if validate_nulls(course.dict().values()):
        raise InvalidOperationException("Se encontraron datos faltantes")
    try:
        db.query(db_models.Course).filter(db_models.Course.id == id).update(
            {
                db_models.Course.title: course.title,
                db_models.Course.description: course.description,
                db_models.Course.hashtags: course.hashtags,
                db_models.Course.type: course.type,
                db_models.Course.exams: course.exams,
                db_models.Course.suscription: course.suscription,
                db_models.Course.location: course.location
            }
        )
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise InvalidOperationException(" Uno o mas campos son incorrectos")
    response = create_message_response("Los datos del curso se actualizaron correctamente")
    return response


def get_courses(db: Session):
    courses_data = db.query(db_models.Course).all()
    if not courses_data:
        return create_message_response("No existen cursos")
    return get_courses_dict(courses_data)


def get_courses_by_suscription(db: Session, suscription):
    courses_data = db.query(db_models.Course).filter(db_models.Course.suscription == suscription).all()
    if not courses_data:
        return create_message_response("No existen cursos para el tipo de suscripción " + suscription)
    return get_courses_dict(courses_data)


def get_courses_by_category(db: Session, category):
    courses_data = db.query(db_models.Course).filter(db_models.Course.category == category).all()
    if not courses_data:
        return create_message_response("No existen cursos para la cateogría " + category)
    return get_courses_dict(courses_data)


def get_courses_by_creator(db: Session, creator_id):
    courses_data = db.query(db_models.Course).filter(db_models.Course.creator == creator_id).all()
    if not courses_data:
        return create_message_response("Aún no ha creado ningún curso")
    return get_courses_dict(courses_data)


def add_collaborator(db: Session, course_id, collaborator_id):
    if course_id=="" or collaborator_id=="":
        raise InvalidOperationException("Uno o mas campos se encuentran vacíos")
    collaborator_model = db_models.Collaborators(course_id = course_id, collaborator_id=collaborator_id)
    db.add(collaborator_model)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.rollback()
        if e.orig.pgcode == '23505':
            raise InvalidOperationException("El colaborador ya se encuentra asociado al curso.")
        else:
            raise InvalidOperationException("Uno o mas campos son incorrectos")
    response = create_message_response("El colaborador se agregó correctamente")
    return response


def get_collaborators_by_course(db: Session, course_id):
    data = db.query(db_models.Collaborators.collaborator_id, db_models.Users.name + " " + db_models.Users.lastname).join(db_models.Users).filter\
        (db_models.Collaborators.course_id == course_id).all()
    if not data:
        return create_message_response("No Hay colaboradores asociados al curso")
    collaborators = {}
    for result in data:
        key = result[0]
        value = result[1]
        collaborators[key] = value
    return collaborators


def get_courses_by_collaborator(db: Session, collaborator_id):
    data = db.query(db_models.Collaborators.course_id, db_models.Course.title).join(db_models.Course).filter\
        (db_models.Collaborators.collaborator_id == collaborator_id).all()
    if not data:
        return create_message_response("El colaborador no se encuentra asociado a ningun curso")
    courses = {}
    for result in data:
        key = result[0]
        value = result[1]
        courses[key] = value
    return courses


def remove_collaborator(db:Session, course_id, collaborator_id):
    result = db.query(db_models.Collaborators).filter(db_models.Collaborators.collaborator_id == collaborator_id).filter(
        db_models.Collaborators.course_id == course_id).delete()
    if not result:
        raise InvalidOperationException("La operación no es válida")
    db.commit()
    return create_message_response("El colaborador se ha removido con éxito")