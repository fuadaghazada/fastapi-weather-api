import datetime
from typing import Optional

from pydantic import BaseModel

from models.location import Location


class ReportRequest(BaseModel):
    description: str
    location: Location


class Report(ReportRequest):
    id: str
    created_date: Optional[datetime.datetime]
