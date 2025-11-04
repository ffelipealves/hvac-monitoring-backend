from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ErrorDetailDTO:
    field: str
    message: str
    code: str | None = None

@dataclass(frozen=True)
class ErrorResponseDTO:
    errors: List[ErrorDetailDTO]