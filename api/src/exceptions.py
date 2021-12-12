class InvalidOperationException(Exception):
    def __init__(self, message: str):
        self.message = "Operación Inválida: " + message

    def __str__(self):
        return self.message


class InvalidCourseIdException(Exception):
    def __init__(self, id):
        self.message = " No existen cursos con el id " + str(id)

    def __str__(self):
        return self.message


class InvalidFilterException(Exception):
    def __init__(self):
        self.message = " El filtro no es válido"

    def __str__(self):
        return self.message
