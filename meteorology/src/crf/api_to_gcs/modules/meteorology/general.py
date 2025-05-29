from modules.helpers.http import HTTPHandler
from datetime import datetime
from requests import Response
import logging

logger: logging.Logger = logging.getLogger(__name__)

class WeatherAPIHandler:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        start_date: datetime,
        end_date: datetime,
        timezone: str
    ):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.timezone: str = timezone
    
class ForecastAPIHandler(WeatherAPIHandler):
    base_url: str = "https://api.open-meteo.com/"
    endpoint: str = "v1/forecast"

    def __init__(
        self,
        latitude: float,
        longitude: float,
        start_date: datetime,
        end_date: datetime,
        timezone: str
    ):
        super().__init__(latitude, longitude, start_date, end_date, timezone)
    
    def get_forecast(self) -> dict:
        params: dict = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": "temperature_2m,rain,wind_speed_10m",
            "timezone": self.timezone,
            "start_date": self.start_date.date(),
            "end_date": self.end_date.date()
        }
        response: Response = HTTPHandler(self.base_url).get(self.endpoint, params)
        logger.info(f"Response: {response.json()}")
        json: dict = response.json()
        return json
    