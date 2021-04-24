## How to run

### FastAPI
```shell
uvicorn main:api
```

### Docker
```shell
docker docker build -t fastapi-weather .
docker run -p 80:8000 --name fastapi-weather-api --rm fastapi-weather
```