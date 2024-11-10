# backend/app/models/data_models.py
from pydantic import BaseModel
from typing import List

class DataSummary(BaseModel):
    columns: List[str]
    row_count: int
    column_count: int