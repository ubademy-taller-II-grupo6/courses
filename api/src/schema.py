from pydantic import BaseModel


class CreateCourseModel(BaseModel):
    title: str
    description: str
    hashtags: str
    type: str
    category: str
    exams: int
    subscription: str
    location: str
    creator: int
    enrollment_conditions: str
    unenrollment_conditions: str


class UpdateCourseModel(BaseModel):
    title: str
    description: str
    hashtags: str
    type: str
    exams: int
    subscription: str
    location: str
    enrollment_conditions: str
    unenrollment_conditions: str


class CourseCollaboratorModel(BaseModel):
    course_id: int
    collaborator_email: str


class FavoriteModel(BaseModel):
    student_id: int
    course_id: int
