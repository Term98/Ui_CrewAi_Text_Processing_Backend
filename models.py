from typing import List
from pydantic import BaseModel


class InputProcess(BaseModel):
    input: str
    inputProcessed:str


class inputProcessedList(BaseModel):
    input: List[InputProcess]
