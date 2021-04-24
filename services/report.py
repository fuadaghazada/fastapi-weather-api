import datetime
import uuid
from typing import List

from models.report import Report, ReportRequest

__reports: List[Report] = []


async def get_reports() -> List[Report]:
    return list(__reports)


async def add_report(request: ReportRequest) -> Report:
    now = datetime.datetime.now()
    report = Report(
        id=str(uuid.uuid4()),
        description=request.description,
        location=request.location,
        created_date=now
    )

    # Simulate db save
    __reports.append(report)
    __reports.sort(key=lambda r: r.created_date, reverse=True)

    return report
