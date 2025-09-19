#!/usr/bin/env python3
"""
Mock Weather Data Fetcher for Brandenburg

This module simulates realistic weather data for Brandenburg cities without
requiring any external API or API keys. Perfect for testing, development,
and demonstrations.

The mock data includes:
- Realistic temperature ranges for Brandenburg climate
- Seasonal variations
- Proper weather conditions for the region
- Air quality simulation
- Forecast data generation
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time
import math


class MockBrandenburgWeatherFetcher:
    """
    A mock weather fetcher that simulates realistic weather data for Brandenburg.
    No API key or internet connection required!
    """
    
    def __init__(self):
        """Initialize the mock weather fetcher."""
        self.base_url = "mock://api.weather.local"
        
        # Brandenburg cities with coordinates
        self.brandenburg_cities = {
            "potsdam": {"lat": 52.3906, "lon": 13.0645, "name": "Potsdam"},
            "cottbus": {"lat": 51.7606, "lon": 14.3349, "name": "Cottbus"},
            "brandenburg_havel": {"lat": 52.4125, "lon": 12.5492, "name": "Brandenburg an der Havel"},
            "frankfurt_oder": {"lat": 52.3481, "lon": 14.5507, "name": "Frankfurt (Oder)"},
            "eberswalde": {"lat": 52.8339, "lon": 13.8217, "name": "Eberswalde"},
            "oranienburg": {"lat": 52.7545, "lon": 13.2369, "name": "Oranienburg"},
            "rathenow": {"lat": 52.6047, "lon": 12.3367, "name": "Rathenow"},
            "senftenberg": {"lat": 51.5255, "lon": 14.0025, "name": "Senftenberg"},
            "neuruppin": {"lat": 52.9245, "lon": 12.8012, "name": "Neuruppin"},
            "schwedt": {"lat": 53.0606, "lon": 14.2825, "name": "Schwedt/Oder"}
        }
        
        # Weather conditions typical for Brandenburg
        self.weather_conditions = [
            {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"},
            {"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02d"},
            {"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"},
            {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"},
            {"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"},
            {"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"},
            {"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"},
            {"id": 300, "main": "Drizzle", "description": "light drizzle", "icon": "09d"},
            {"id": 200, "main": "Thunderstorm", "description": "thunderstorm", "icon": "11d"},
            {"id": 600, "main": "Snow", "description": "light snow", "icon": "13d"},
            {"id": 701, "main": "Mist", "description": "mist", "icon": "50d"}
        ]
        
        # Seed random for consistent but varied results
        random.seed(int(time.time()) % 1000)
    
    def _get_seasonal_temp_range(self, month: int) -> tuple:
        """Get realistic temperature ranges for Brandenburg by season."""
        # Brandenburg climate: continental, cold winters, mild summers
        temp_ranges = {
            1: (-5, 3),    # January
            2: (-3, 5),    # February  
            3: (2, 10),    # March
            4: (6, 15),    # April
            5: (11, 20),   # May
            6: (15, 24),   # June
            7: (17, 26),   # July
            8: (16, 25),   # August
            9: (12, 20),   # September
            10: (7, 14),   # October
            11: (2, 8),    # November
            12: (-2, 4)    # December
        }
        return temp_ranges.get(month, (10, 20))
    
    def _generate_realistic_temperature(self, city_key: str) -> float:
        """Generate realistic temperature based on location and season."""
        city = self.brandenburg_cities[city_key]
        now = datetime.now()
        month = now.month
        hour = now.hour
        
        # Get base temperature range for season
        min_temp, max_temp = self._get_seasonal_temp_range(month)
        
        # Add daily variation (colder at night, warmer in afternoon)
        daily_variation = 3 * math.sin((hour - 6) * math.pi / 12)
        
        # Add some randomness
        base_temp = random.uniform(min_temp, max_temp)
        temp = base_temp + daily_variation + random.uniform(-2, 2)
        
        # Slight regional variations (northern cities slightly cooler)
        if city["lat"] > 52.5:  # Northern cities
            temp -= random.uniform(0, 1.5)
        
        return round(temp, 1)
    
    def _choose_weather_condition(self, month: int) -> Dict:
        """Choose realistic weather condition based on season."""
        # Weight conditions by season
        if month in [12, 1, 2]:  # Winter
            weights = [0.3, 0.2, 0.25, 0.15, 0.05, 0.02, 0.01, 0.01, 0.01, 0.08, 0.02]
        elif month in [6, 7, 8]:  # Summer
            weights = [0.4, 0.25, 0.15, 0.1, 0.03, 0.03, 0.02, 0.01, 0.01, 0.0, 0.01]
        elif month in [3, 4, 5]:  # Spring
            weights = [0.25, 0.2, 0.2, 0.15, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01, 0.02]
        else:  # Autumn
            weights = [0.2, 0.15, 0.25, 0.2, 0.1, 0.05, 0.02, 0.02, 0.01, 0.0, 0.03]
        
        return random.choices(self.weather_conditions, weights=weights)[0]
    
    def get_current_weather(self, city_key: str = "potsdam") -> Dict[str, Any]:
        """
        Get simulated current weather for a Brandenburg city.
        
        Args:
            city_key (str): Key for the city (default: "potsdam")
            
        Returns:
            Dict containing simulated weather data
        """
        if city_key not in self.brandenburg_cities:
            raise ValueError(f"City '{city_key}' not found. Available cities: {list(self.brandenburg_cities.keys())}")
        
        city = self.brandenburg_cities[city_key]
        now = datetime.now()
        
        # Generate realistic data
        temp = self._generate_realistic_temperature(city_key)
        feels_like = temp + random.uniform(-3, 3)
        humidity = random.randint(40, 85)
        pressure = random.randint(995, 1025)
        wind_speed = random.uniform(0.5, 8.0)
        wind_deg = random.randint(0, 360)
        visibility = random.randint(8000, 10000)
        clouds = random.randint(0, 100)
        
        weather_condition = self._choose_weather_condition(now.month)
        
        # Simulate sunrise/sunset times (approximate for Brandenburg)
        sunrise_offset = random.randint(6*3600, 8*3600)  # 6-8 AM
        sunset_offset = random.randint(16*3600, 20*3600)  # 4-8 PM
        
        # Create realistic weather data structure
        weather_data = {
            "coord": {
                "lon": city["lon"],
                "lat": city["lat"]
            },
            "weather": [weather_condition],
            "base": "stations",
            "main": {
                "temp": temp,
                "feels_like": round(feels_like, 1),
                "temp_min": round(temp - random.uniform(1, 4), 1),
                "temp_max": round(temp + random.uniform(1, 4), 1),
                "pressure": pressure,
                "humidity": humidity
            },
            "visibility": visibility,
            "wind": {
                "speed": round(wind_speed, 1),
                "deg": wind_deg
            },
            "clouds": {
                "all": clouds
            },
            "dt": int(now.timestamp()),
            "sys": {
                "type": 2,
                "id": random.randint(2000000, 3000000),
                "country": "DE",
                "sunrise": int((now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() + sunrise_offset)),
                "sunset": int((now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() + sunset_offset))
            },
            "timezone": 7200,  # Central European Time
            "id": random.randint(2900000, 3000000),
            "name": city["name"],
            "cod": 200,
            "city_info": city,
            "fetch_time": now.isoformat(),
            "data_source": "mock_simulation"
        }
        
        return weather_data
    
    def get_forecast(self, city_key: str = "potsdam", days: int = 5) -> Dict[str, Any]:
        """
        Get simulated weather forecast for a Brandenburg city.
        
        Args:
            city_key (str): Key for the city (default: "potsdam")
            days (int): Number of days to forecast (1-5, default: 5)
            
        Returns:
            Dict containing forecast data
        """
        if city_key not in self.brandenburg_cities:
            raise ValueError(f"City '{city_key}' not found. Available cities: {list(self.brandenburg_cities.keys())}")
        
        if not 1 <= days <= 5:
            raise ValueError("Days must be between 1 and 5")
        
        city = self.brandenburg_cities[city_key]
        now = datetime.now()
        
        forecast_list = []
        
        # Generate forecast for next few days (8 forecasts per day, 3-hour intervals)
        for i in range(days * 8):
            forecast_time = now + timedelta(hours=3 * (i + 1))
            
            # Generate weather data for this time
            temp = self._generate_realistic_temperature(city_key)
            # Add some trend variation over time
            temp += random.uniform(-1, 1) * (i / 10)
            
            weather_condition = self._choose_weather_condition(forecast_time.month)
            
            forecast_item = {
                "dt": int(forecast_time.timestamp()),
                "main": {
                    "temp": round(temp, 1),
                    "feels_like": round(temp + random.uniform(-2, 2), 1),
                    "temp_min": round(temp - random.uniform(1, 3), 1),
                    "temp_max": round(temp + random.uniform(1, 3), 1),
                    "pressure": random.randint(995, 1025),
                    "sea_level": random.randint(1000, 1020),
                    "grnd_level": random.randint(990, 1015),
                    "humidity": random.randint(40, 85),
                    "temp_kf": round(random.uniform(-1, 1), 1)
                },
                "weather": [weather_condition],
                "clouds": {
                    "all": random.randint(0, 100)
                },
                "wind": {
                    "speed": round(random.uniform(0.5, 8.0), 1),
                    "deg": random.randint(0, 360),
                    "gust": round(random.uniform(1.0, 12.0), 1)
                },
                "visibility": random.randint(8000, 10000),
                "pop": round(random.uniform(0, 0.8), 2),  # Probability of precipitation
                "sys": {
                    "pod": "d" if 6 <= forecast_time.hour <= 18 else "n"  # day/night
                },
                "dt_txt": forecast_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            forecast_list.append(forecast_item)
        
        forecast_data = {
            "cod": "200",
            "message": 0,
            "cnt": len(forecast_list),
            "list": forecast_list,
            "city": {
                "id": random.randint(2900000, 3000000),
                "name": city["name"],
                "coord": {
                    "lat": city["lat"],
                    "lon": city["lon"]
                },
                "country": "DE",
                "population": random.randint(50000, 200000),
                "timezone": 7200,
                "sunrise": int(now.timestamp()) + random.randint(6*3600, 8*3600),
                "sunset": int(now.timestamp()) + random.randint(16*3600, 20*3600)
            },
            "city_info": city,
            "fetch_time": now.isoformat(),
            "data_source": "mock_simulation"
        }
        
        return forecast_data
    
    def get_weather_for_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get simulated weather for specific coordinates in Brandenburg.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            Dict containing weather data
        """
        # Find closest city or create generic location
        closest_city = None
        min_distance = float('inf')
        
        for key, city in self.brandenburg_cities.items():
            distance = abs(city["lat"] - lat) + abs(city["lon"] - lon)
            if distance < min_distance:
                min_distance = distance
                closest_city = key
        
        # If coordinates are close to a known city, use that as base
        if min_distance < 0.1:  # Very close to a known city
            weather = self.get_current_weather(closest_city)
            weather["coord"]["lat"] = lat
            weather["coord"]["lon"] = lon
            weather["name"] = f"Location near {weather['name']}"
        else:
            # Create weather for unknown location
            temp = random.uniform(8, 22)  # Average Brandenburg temp
            weather_condition = self._choose_weather_condition(datetime.now().month)
            
            weather = {
                "coord": {"lon": lon, "lat": lat},
                "weather": [weather_condition],
                "main": {
                    "temp": round(temp, 1),
                    "feels_like": round(temp + random.uniform(-2, 2), 1),
                    "pressure": random.randint(995, 1025),
                    "humidity": random.randint(40, 85)
                },
                "wind": {
                    "speed": round(random.uniform(0.5, 8.0), 1),
                    "deg": random.randint(0, 360)
                },
                "name": f"Location ({lat:.4f}, {lon:.4f})",
                "fetch_time": datetime.now().isoformat(),
                "data_source": "mock_simulation"
            }
        
        return weather
    
    def get_all_brandenburg_weather(self) -> Dict[str, Any]:
        """
        Get simulated current weather for all major Brandenburg cities.
        
        Returns:
            Dict with weather data for all cities
        """
        all_weather = {}
        
        for city_key in self.brandenburg_cities:
            try:
                all_weather[city_key] = self.get_current_weather(city_key)
                # Small delay to vary the data slightly
                time.sleep(0.01)
            except Exception as e:
                all_weather[city_key] = {"error": str(e)}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "cities": all_weather,
            "data_source": "mock_simulation"
        }
    
    def get_air_quality(self, city_key: str = "potsdam") -> Dict[str, Any]:
        """
        Get simulated air quality data for a Brandenburg city.
        
        Args:
            city_key (str): Key for the city (default: "potsdam")
            
        Returns:
            Dict containing air quality data
        """
        if city_key not in self.brandenburg_cities:
            raise ValueError(f"City '{city_key}' not found. Available cities: {list(self.brandenburg_cities.keys())}")
        
        city = self.brandenburg_cities[city_key]
        now = datetime.now()
        
        # Brandenburg generally has good air quality
        aqi = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]  # Mostly good to fair
        
        air_quality_data = {
            "coord": {
                "lon": city["lon"],
                "lat": city["lat"]
            },
            "list": [
                {
                    "main": {
                        "aqi": aqi
                    },
                    "components": {
                        "co": round(random.uniform(200, 400), 2),
                        "no": round(random.uniform(0, 5), 2),
                        "no2": round(random.uniform(10, 30), 2),
                        "o3": round(random.uniform(80, 120), 2),
                        "so2": round(random.uniform(5, 15), 2),
                        "pm2_5": round(random.uniform(8, 25), 2),
                        "pm10": round(random.uniform(15, 35), 2),
                        "nh3": round(random.uniform(1, 8), 2)
                    },
                    "dt": int(now.timestamp())
                }
            ],
            "city_info": city,
            "fetch_time": now.isoformat(),
            "data_source": "mock_simulation"
        }
        
        return air_quality_data
    
    def save_weather_data(self, data: Dict[str, Any], filename: str):
        """
        Save weather data to a JSON file.
        
        Args:
            data (Dict): Weather data to save
            filename (str): Name of the file to save to
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Mock weather data saved to {filename}")
    
    def format_current_weather(self, weather_data: Dict[str, Any]) -> str:
        """
        Format current weather data into a readable string.
        
        Args:
            weather_data (Dict): Weather data from mock API
            
        Returns:
            Formatted weather string
        """
        if "error" in weather_data:
            return f"❌ Error: {weather_data['error']}"
        
        city_name = weather_data.get("city_info", {}).get("name", weather_data.get("name", "Unknown"))
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        description = weather_data["weather"][0]["description"].title()
        wind_speed = weather_data["wind"]["speed"]
        
        return f"""
🌤️  Weather in {city_name}:
   🌡️  Temperature: {temp}°C (feels like {feels_like}°C)
   ☁️  Condition: {description}
   💧 Humidity: {humidity}%
   🔽 Pressure: {pressure} hPa
   💨 Wind Speed: {wind_speed} m/s
   📅 Data: {weather_data.get('fetch_time', 'Unknown')}
   🔧 Source: Mock Simulation (No API needed!)
        """.strip()


def main():
    """
    Example usage of the MockBrandenburgWeatherFetcher class.
    
    This runs completely offline with no API key required!
    """
    
    print("🌤️  Mock Brandenburg Weather Data Fetcher")
    print("✨ No API key required - runs completely offline!")
    print("=" * 50)
    
    # Initialize the mock weather fetcher
    fetcher = MockBrandenburgWeatherFetcher()
    
    try:
        # Test 1: Get current weather for Eberswalde
        print("\n📍 Current Weather in Eberswalde:")
        eberswalde_weather = fetcher.get_current_weather("eberswalde")
        print(fetcher.format_current_weather(eberswalde_weather))
        
        # Save the data
        fetcher.save_weather_data(eberswalde_weather, "eberswalde_mock_weather.json")
        
        # Test 2: Get weather for all Brandenburg cities
        print("\n🏙️  Weather Summary for All Brandenburg Cities:")
        all_weather = fetcher.get_all_brandenburg_weather()
        
        temps = []
        for city_key, weather_data in all_weather["cities"].items():
            if "error" not in weather_data:
                city_name = weather_data.get("city_info", {}).get("name", city_key)
                temp = weather_data["main"]["temp"]
                condition = weather_data["weather"][0]["description"]
                temps.append((temp, city_name, condition))
        
        # Sort by temperature
        temps.sort(reverse=True)
        
        for temp, city_name, condition in temps:
            print(f"   {city_name:<20} {temp:>5.1f}°C - {condition}")
        
        # Save all weather data
        fetcher.save_weather_data(all_weather, "brandenburg_mock_all_weather.json")
        
        # Test 3: Get forecast for Potsdam
        print("\n📊 3-Day Forecast for Potsdam:")
        forecast = fetcher.get_forecast("potsdam", 2)  # 2 days
        
        current_date = None
        for item in forecast["list"][:8]:  # Show first 8 forecasts (1 day)
            dt = datetime.fromtimestamp(item["dt"])
            date_str = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M")
            
            if current_date != date_str:
                if current_date is not None:
                    print()
                print(f"\n   📅 {date_str}:")
                current_date = date_str
            
            temp = item["main"]["temp"]
            description = item["weather"][0]["description"]
            pop = item["pop"] * 100
            print(f"     {time_str}: {temp:>4.1f}°C - {description:<15} (rain: {pop:>3.0f}%)")
        
        # Test 4: Air quality
        print("\n🌬️  Air Quality in Cottbus:")
        air_quality = fetcher.get_air_quality("cottbus")
        
        city_name = air_quality["city_info"]["name"]
        aqi = air_quality["list"][0]["main"]["aqi"]
        components = air_quality["list"][0]["components"]
        
        aqi_meanings = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        
        print(f"   Air Quality Index: {aqi} ({aqi_meanings.get(aqi, 'Unknown')})")
        print(f"   PM2.5: {components.get('pm2_5', 'N/A')} μg/m³")
        print(f"   PM10: {components.get('pm10', 'N/A')} μg/m³")
        print(f"   NO₂: {components.get('no2', 'N/A')} μg/m³")
        
        print("\n" + "=" * 50)
        print("✅ All mock weather tests completed successfully!")
        print("📁 Data saved to JSON files for further analysis")
        print("🎯 This demonstrates exactly how real weather data would work")
        
    except Exception as e:
        print(f"\n❌ Error during mock weather fetch: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()