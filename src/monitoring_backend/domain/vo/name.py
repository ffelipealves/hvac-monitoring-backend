from pydantic import BaseModel, Field, field_validator

from monitoring_backend.domain.exceptions.common import InvalidNameException

class Name(BaseModel):
    """
    Value Object para Nome do Cliente.
    - Mantém validação no domínio.
    - Imutável (frozen).
    """
    value: str

    @field_validator("value", mode="before")
    @classmethod
    def _strip_whitespace(cls, v: str) -> str:
        if v is None:
            return v
        return v.strip()

    @field_validator("value")
    @classmethod
    def _validate_not_empty_and_length(cls, v: str) -> str:
        # Se chegou aqui, já foi stripado pelo validator acima
        if not v:
            raise InvalidNameException("Nome não pode ser vazio")
        if len(v) < 3:
            raise InvalidNameException("Nome deve ter pelo menos 3 caracteres")
        if len(v) > 100:
            raise InvalidNameException("Nome deve ter no máximo 100 caracteres")
        
        # outras validações de domínio podem ser adicionadas aqui (ex.: caracteres inválidos)
        return v

    model_config = {
        "frozen": True,  # torna o VO imutável
    }

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Name(value={self.value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Name):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
