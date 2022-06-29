from typing import Optional

from sqlmodel import SQLModel, Field

from .. import example


class Example(example.Example, SQLModel):
    __tablename__: str = "example"

    id: Optional[int] = Field(default=None, primary_key=True)
