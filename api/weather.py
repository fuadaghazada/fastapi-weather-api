from typing import Optional, List

import fastapi
from fastapi import Depends

from infra.weather_cache import get_weather, set_weather
from models.location import Location
from models.report import Report, ReportRequest
from models.validation import ValidationError
from services.openweather import get_report
from services.report import get_reports, add_report

router = fastapi.APIRouter()


@router.get('/api/weather/{city}')
async def weather(location: Location = Depends(), units: Optional[str] = 'metric'):
    if forecast := get_weather(location.city, location.state, location.country, units):
        return forecast

    try:
        report = await get_report(location.city, location.state, location.country, units)
    except ValidationError as e:
        return fastapi.Response(content=e.error_msg, status_code=e.status_code)

    set_weather(location.city, location.state, location.country, units, report)

    return report


@router.get('/api/reports', name='all_reports', response_model=List[Report])
async def list_reports() -> List[Report]:
    return await get_reports()


@router.post('/api/reports', name='add_report', status_code=201, response_model=Report)
async def post_report(report: ReportRequest) -> Report:
    return await add_report(report)
