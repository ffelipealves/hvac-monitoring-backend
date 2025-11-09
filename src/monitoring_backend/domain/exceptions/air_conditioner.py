from monitoring_backend.domain.exceptions.base import DomainException


class AirConditionerAlreadyAssociatedException(DomainException):
    """Lançada quando um ar-condicionado já está associado a uma unidade de monitoramento."""

    def __init__(self, message: str = "AirConditioner já está associado a esta unidade."):
        super().__init__(message)
