from monitoring_backend.domain.exceptions.base import DomainException

class InvalidNameException(DomainException):
    def __init__(self, message: str = "Nome inválido"):
        super().__init__(message=message, field="name", code="INVALID_NAME")
