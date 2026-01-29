from typing import List
from pydantic import BaseModel


class ColumnCreate(BaseModel):
    name: str
    type: str


class DatasetCreate(BaseModel):
    fqn: str
    source_type: str
    columns: List[ColumnCreate]


class DatasetResponse(BaseModel):
    fqn: str
    source_type: str

    class Config:
        from_attributes = True


class LineageCreate(BaseModel):
    upstream_fqn: str
    downstream_fqn: str
