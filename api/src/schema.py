from pydantic import BaseModel


class CreateCourseModel(BaseModel):
    title: str
    description: str
    hashtags: str
    type: str
    category: str
    exams: int
    suscription: str
    location: str
    creator: int


class UpdateCourseModel(BaseModel):
    title: str
    description: str
    hashtags: str
    type: str
    exams: int
    suscription: str
    location: str


class CourseCollaboratorModel(BaseModel):
    course_id: int
    collaborator_id: int
