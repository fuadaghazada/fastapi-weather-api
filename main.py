import asyncio
import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import weather
from models.location import Location
from models.report import ReportRequest
from services import openweather
from services.report import add_report
from views import home

api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()
    configure_fake_data()


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(weather.router)


def configure_api_keys():
    file = Path('settings.json').absolute()
    if not file.exists():
        raise Exception("ERROR: settings.json not found!")

    with open('settings.json') as f:
        settings = json.load(f)
        openweather.api_key = settings.get('api_key')


def configure_fake_data():
    loop = None
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        pass

    if not loop:
        loop = asyncio.get_event_loop()

    try:
        data1 = ReportRequest(description="Dummy desc 1", location=Location(city="Baku", country="AZ"))
        data2 = ReportRequest(description="Dummy desc 2", location=Location(city="Ankara", country="TR"))

        loop.run_until_complete(add_report(data2))
        loop.run_until_complete(add_report(data1))

    except RuntimeError:
        print("Something went wrong on creating fake data")


if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()
