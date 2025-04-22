from pydantic import BaseModel
from datetime import datetime

class ForecastResult(BaseModel):
    timestamp: str
    value: float
    confidence_lower: float
    confidence_upper: float
