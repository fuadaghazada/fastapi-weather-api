from typing import Optional

import fastapi
from fastapi import Depends

from infra.weather_cache import get_weather, set_weather
from models.location import Location
from models.validation import ValidationError
from services.openweather import get_report

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
