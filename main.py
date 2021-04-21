import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import weather
from services import openweather
from views import home

api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()


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


if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8080, host='127.0.0.1')
else:
    configure()