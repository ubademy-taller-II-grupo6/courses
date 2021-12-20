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
                db_models.Course.suscription: course.subscription,
                db_models.Course.location: course.location,
                db_models.Course.conditions: course.enrollment_conditions,
                db_models.Course.unenrollment_conditions: course.unenrollment_conditions
            }
        )
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise InvalidOperationException(" Uno o mas campos son incorrectos")
    response = create_message_response("Los datos del curso se actualizaron correctamente")
    return response


def get_courses(db: Session, id, category, subscription, creator):
    query = db.query(db_models.Course)
    if id:
        query = query.filter(db_models.Course.id == id)
    if creator:
        query = query.filter(db_models.Course.creator == creator)
    if category:
        query = query.filter(db_models.Course.category == category)
    if subscription:
        query = query.filter(db_models.Course.subscription == subscription)
    courses = query.all()
    if not courses:
        return create_message_response("No existen cursos")
    return courses


def add_collaborator(db: Session, course_id, collaborator_email):
    creator = db.query(db_models.User).join(db_models.Course).filter(db_models.Course.id == course_id, db_models.User.id == db_models.Course.creator).first()
    if not creator:
        raise InvalidOperationException("El curso no existe")
    if creator.email == collaborator_email:
        raise InvalidOperationException("No se puede añadir como colaborador al usuario creador del curso")
    else:
       user= db.query(db_models.User).filter(db_models.User.email == collaborator_email).first()
       if not user:
           raise InvalidOperationException("El usuario no existe")
       collaborator_model = db_models.Collaborators(course_id=course_id, collaborator_id=user.id)
       db.add(collaborator_model)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        if e.orig.pgcode == '23505':
            raise InvalidOperationException("El colaborador ya se encuentra asociado al curso.")
    response = create_message_response("El colaborador se agregó correctamente")
    return response


def get_collaborators_by_course(db: Session, course_id):
    data = db.query(db_models.Collaborators.collaborator_id, db_models.User.name + " " + db_models.User.lastname).join(
        db_models.User).filter \
        (db_models.Collaborators.course_id == course_id).all()
    if not data:
        return create_message_response("No Hay colaboradores asociados al curso")
    collaborators = {}
    for result in data:
        key = result[0]
        value = result[1]
        collaborators[key] = value
    return collaborators


def get_courses_by_collaborator(db: Session, collaborator_email):
    data = db.query(db_models.Course.id,db_models.Course.title).join(db_models.Collaborators).join(db_models.User).filter \
        (db_models.User.email == collaborator_email).all()
    if not data:
        return create_message_response("El colaborador no se encuentra asociado a ningun curso")
    courses = {}
    for result in data:
        key = result[0]
        value = result[1]
        courses[key] = value
    return courses


def remove_collaborator(db: Session, course_id, collaborator_email):
    collaborator = db.query(db_models.User).filter(db_models.User.email==collaborator_email).first()
    if not collaborator:
        raise InvalidOperationException("El colaborador no existe")
    result = db.query(db_models.Collaborators).filter(
        db_models.Collaborators.collaborator_id == collaborator.id).filter(
        db_models.Collaborators.course_id == course_id).delete()
    if not result:
        raise InvalidOperationException("El colaborador no se encuentra asociado al curso")
    db.commit()
    return create_message_response("El colaborador se ha removido con éxito")


def add_to_favorites(db: Session, favorite: schema.FavoriteModel):
    favorite_model = db_models.Favorite(student_id=favorite.student_id, course_id=favorite.course_id)
    db.add(favorite_model)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        db.rollback()
        if e.orig.pgcode == '23505':
            raise InvalidOperationException("El alumno ya ha marcado el curso como favorito")
        else:
            raise InvalidOperationException("Uno o mas campos son incorrectos")
    response = create_message_response("Se agregó el curso a favoritos")
    return response


def delete_favorite(db: Session, favorite: schema.FavoriteModel):
    result = db.query(db_models.Favorite).filter(
        db_models.Favorite.student_id == favorite.student_id).filter(
        db_models.Favorite.course_id == favorite.course_id).delete()
    if not result:
        raise InvalidOperationException("La operación no es válida")
    db.commit()
    return create_message_response("El curso ha sido removido de favoritos")


def get_favorites(db, student_id, category, subscription):
    query= db.query(db_models.Course).join(db_models.Favorite).filter(
    db_models.Favorite.student_id == student_id).filter(db_models.Favorite.course_id == db_models.Course.id)
    if category:
        query = query.filter(db_models.Course.category == category)
    if subscription:
        query = query.filter(db_models.Course.subscription == subscription)
    favorites = query.all()
    if not favorites:
        return create_message_response('El alumno no tiene cursos favoritos')
    return favorites


def get_subscriptions(db):
    subscritpions = db.query(db_models.Subscription).all()
    response = []
    for subscription in subscritpions:
        response.append(subscription.id)
    return response


def get_categories(db):
    categories = db.query(db_models.Category).all()
    response = []
    for category in categories:
        response.append(category.id)
    return response
