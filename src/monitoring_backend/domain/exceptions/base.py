class DomainException(Exception):
    """Exceção base para erros de domínio."""

    def __init__(self, message: str, field: str | None = None, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code or self.__class__.__name__.upper()