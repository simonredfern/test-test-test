"""
Configuration settings for Brandenburg Weather Data Fetcher
"""

import os
from typing import Dict, Any

class WeatherConfig:
    """Configuration class for weather data fetching"""
    
    # API Configuration
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    OPENWEATHER_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
    
    # Request Configuration
    DEFAULT_UNITS = "metric"  # metric, imperial, kelvin
    DEFAULT_LANGUAGE = "en"   # en, de, etc.
    REQUEST_TIMEOUT = 30      # seconds
    
    # Rate Limiting (for free tier)
    MAX_CALLS_PER_MINUTE = 60
    MAX_CALLS_PER_DAY = 1000
    
    # Data Storage
    DATA_DIR = "weather_data"
    SAVE_RAW_DATA = True
    SAVE_PROCESSED_DATA = True
    
    # Brandenburg-specific settings
    DEFAULT_CITY = "eberswalde"
    REGION_NAME = "Brandenburg"
    COUNTRY_CODE = "DE"
    TIMEZONE = "Europe/Berlin"
    
    # File naming patterns
    FILENAME_PATTERNS = {
        "current": "{city}_{date}_current.json",
        "forecast": "{city}_{date}_forecast.json",
        "historical": "{city}_{date}_historical.json",
        "all_cities": "brandenburg_{date}_all_cities.json"
    }
    
    # Data retention (days)
    DATA_RETENTION_DAYS = 30
    
    # Logging configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = "weather_fetcher.log"
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate that API key is set"""
        return bool(cls.OPENWEATHER_API_KEY and cls.OPENWEATHER_API_KEY != "")
    
    @classmethod
    def get_data_dir(cls) -> str:
        """Get the data directory path, create if not exists"""
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)
        return cls.DATA_DIR
    
    @classmethod
    def get_request_params(cls) -> Dict[str, Any]:
        """Get default request parameters"""
        return {
            "units": cls.DEFAULT_UNITS,
            "lang": cls.DEFAULT_LANGUAGE,
            "appid": cls.OPENWEATHER_API_KEY
        }

# Environment-specific overrides
if os.getenv("WEATHER_ENV") == "development":
    WeatherConfig.LOG_LEVEL = "DEBUG"
    WeatherConfig.SAVE_RAW_DATA = True

elif os.getenv("WEATHER_ENV") == "production":
    WeatherConfig.LOG_LEVEL = "WARNING"
    WeatherConfig.DATA_RETENTION_DAYS = 90