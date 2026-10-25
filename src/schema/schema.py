from pydantic import BaseModel, Field
from datetime import datetime

class WeatherData(BaseModel):
    date: datetime= Field(...)
    temperature_2m: float
    relative_humidity_2m: float
    apparent_temperature: float
    wind_speed_10m: float= Field(ge=0)
    wind_gusts_10m: float= Field(ge=0)
    wind_direction_10m: float= Field(ge=0, le=360)
    rain: float= Field(ge=0)
    showers: float= Field(ge=0)
    weather_code: int
    precipitation: float= Field(ge=0)
    uv_index: float = Field(ge=0)
    cloud_cover: float= Field(ge=0, le=100)
    visibility: float



