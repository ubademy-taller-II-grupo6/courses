def create_message_response(message):
    return {
        "message": message
    }


def validate_nulls(list):
    for value in list:
        if value == "":
            return True
        return False


def get_courses_dict(courses_data):
    courses = {}
    for data in courses_data:
        courses[data.id] = data.title
    return courses
