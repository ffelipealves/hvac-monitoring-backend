from pydantic import BaseModel, Field

from ..vo.name import Name

class Campus(BaseModel):
    id: int | None = Field(default=None)
    name: Name

