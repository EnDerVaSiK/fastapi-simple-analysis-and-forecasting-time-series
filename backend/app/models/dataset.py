from pydantic import BaseModel
from typing import List
import pandas as pd

class CSVDataset(BaseModel):
    date_column: str
    value_column: str
    data: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True
