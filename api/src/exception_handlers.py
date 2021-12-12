from fastapi import status, Request, FastAPI
from starlette.responses import JSONResponse

from api.src.exceptions import InvalidOperationException, InvalidCourseIdException, InvalidFilterException
from api.src.utils import create_message_response


async def invalid_operation_exception_handler(request: Request, exc: InvalidOperationException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=create_message_response(exc.message))


async def invalid_course_id_exception_handler(request: Request, exc: InvalidCourseIdException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=create_message_response(exc.message))


async def invalid_filter_exception_handler(request: Request, exc: InvalidFilterException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=create_message_response(exc.message))


def add_user_exception_handlers(app: FastAPI):
    app.add_exception_handler(InvalidOperationException, invalid_operation_exception_handler)
    app.add_exception_handler(InvalidCourseIdException, invalid_course_id_exception_handler)
    app.add_exception_handler(InvalidFilterException, invalid_filter_exception_handler)
