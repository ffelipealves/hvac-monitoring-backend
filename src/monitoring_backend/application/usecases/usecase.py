from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class UseCase(ABC, Generic[InputDTO, OutputDTO]):
    """
    Classe base para casos de uso.
    Cada caso de uso deve implementar o método execute, 
    recebendo um DTO de entrada e retornando um DTO de saída.
    """
    @abstractmethod
    def execute(self, request: InputDTO) -> OutputDTO:
        ...
