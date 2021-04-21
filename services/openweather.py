from typing import Optional, Tuple

import httpx
from httpx import Response

from models.validation import ValidationError

api_key: Optional[str] = None


async def get_report(city, state: Optional[str], country: str, units: str) -> dict:
    city, state, country, units = validate_units(city, state, country, units)

    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        response: Response = await client.get(url)
        if response.status_code != 200:
            raise ValidationError(response.text, status_code=response.status_code)

    data = response.json()
    forecast = data.get('main')

    return forecast


def validate_units(city: str, state: Optional[str], country: Optional[str], units: str) -> \
        Tuple[str, Optional[str], str, str]:
    city = city.lower().strip()
    if not country:
        country = "us"
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f"Invalid country: {country}. It must be a two letter abbreviation such as US or GB."
        raise ValidationError(status_code=400, error_msg=error)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f"Invalid state: {state}. It must be a two letter abbreviation such as CA or KS (use for US only)."
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.strip().lower()

    valid_units = {'standard', 'metric', 'imperial'}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units
