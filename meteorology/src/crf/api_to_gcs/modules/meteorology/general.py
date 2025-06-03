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
        timezone: str
    ):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.timezone: str = timezone
    
class ForecastAPIHandler(WeatherAPIHandler):
    base_url: str = "https://api.open-meteo.com/"
    endpoint: str = "v1/forecast"

    def __init__(
        self,
        latitude: float,
        longitude: float,
        timezone: str
    ):
        super().__init__(latitude, longitude, timezone)
    
    def get_forecast(self, start_date: datetime, end_date: datetime) -> dict:
        """
        Get forecast from Open-Meteo API.

        Args:
        - start_date (datetime): Start date of the forecast period.
        - end_date (datetime): End date of the forecast period.

        Returns:
        - dict: The JSON response from the API, containing the forecast data.
        """
        params: dict = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": "temperature_2m,rain,wind_speed_10m",
            "timezone": self.timezone,
            "start_date": start_date.date(),
            "end_date": end_date.date()
        }
        response: Response = HTTPHandler(self.base_url).get(self.endpoint, params)
        logger.info(f"Response: {response.json()}")
        data: dict = response.json()
        return data
    