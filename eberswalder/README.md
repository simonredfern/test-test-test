# Brandenburg Weather Data Fetcher

🌤️ A comprehensive weather data fetching system for Brandenburg, Germany, with **no API key required!**

This project provides both real API integration (OpenWeatherMap) and a complete **mock simulation system** that generates realistic weather data for all major Brandenburg cities without needing any external services.

## ✨ Features

- **🏙️ Complete Brandenburg Coverage**: Weather data for 10 major cities
- **🌡️ Current Weather**: Real-time temperature, humidity, pressure, wind conditions
- **📊 Weather Forecasts**: Multi-day forecasts with 3-hour intervals
- **🌬️ Air Quality Data**: AQI and pollutant levels monitoring
- **📍 Coordinate-based Weather**: Get weather for any location in Brandenburg
- **💾 Data Export**: Save weather data in JSON and CSV formats
- **🎯 Weather Analysis**: Temperature trends, statistics, and comparisons
- **✨ Mock Mode**: Complete offline operation with realistic simulated data

## 🏙️ Supported Brandenburg Cities

| City | Key | Coordinates |
|------|-----|-------------|
| **Potsdam** (Capital) | `potsdam` | 52.3906°N, 13.0645°E |
| **Eberswalde** | `eberswalde` | 52.8339°N, 13.8217°E |
| **Cottbus** | `cottbus` | 51.7606°N, 14.3349°E |
| **Frankfurt (Oder)** | `frankfurt_oder` | 52.3481°N, 14.5507°E |
| **Brandenburg an der Havel** | `brandenburg_havel` | 52.4125°N, 12.5492°E |
| **Oranienburg** | `oranienburg` | 52.7545°N, 13.2369°E |
| **Rathenow** | `rathenow` | 52.6047°N, 12.3367°E |
| **Senftenberg** | `senftenberg` | 51.5255°N, 14.0025°E |
| **Neuruppin** | `neuruppin` | 52.9245°N, 12.8012°E |
| **Schwedt/Oder** | `schwedt` | 53.0606°N, 14.2825°E |

## 🚀 Quick Start

### Option 1: Mock Mode (No Setup Required!)

```bash
# Run the mock weather fetcher immediately
python mock_weather_fetcher.py

# Try the interactive weather explorer
python interactive_weather.py

# Run demos and tests
python test_demo.py
```

### Option 2: Real API Mode

1. **Get a free API key** from [OpenWeatherMap](https://openweathermap.org/api)
2. **Set environment variable**:
   ```bash
   export OPENWEATHER_API_KEY='your_api_key_here'
   ```
3. **Run with real data**:
   ```bash
   python weather_fetcher.py
   python example_usage.py
   python quick_test.py
   ```

## 📁 Project Structure

```
eberswalder/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── config.py                   # Configuration settings
│
├── weather_fetcher.py          # Real API weather fetcher (needs API key)
├── mock_weather_fetcher.py     # Mock weather fetcher (no API key needed)
├── interactive_weather.py     # Interactive CLI explorer
│
├── example_usage.py           # Comprehensive examples (real API)
├── test_demo.py              # Demo without API key
├── quick_test.py             # Quick API test
│
└── *.json                    # Generated weather data files
```

## 💻 Usage Examples

### Basic Weather Fetching (Mock Mode)

```python
from mock_weather_fetcher import MockBrandenburgWeatherFetcher

# Initialize fetcher (no API key needed!)
fetcher = MockBrandenburgWeatherFetcher()

# Get current weather for Eberswalde
weather = fetcher.get_current_weather("eberswalde")
print(fetcher.format_current_weather(weather))

# Get weather for all Brandenburg cities
all_weather = fetcher.get_all_brandenburg_weather()
for city, data in all_weather["cities"].items():
    temp = data["main"]["temp"]
    city_name = data["city_info"]["name"]
    print(f"{city_name}: {temp}°C")
```

### Weather Forecast

```python
# Get 3-day forecast for Potsdam
forecast = fetcher.get_forecast("potsdam", days=3)

for item in forecast["list"][:8]:  # First day
    dt = datetime.fromtimestamp(item["dt"])
    temp = item["main"]["temp"]
    condition = item["weather"][0]["description"]
    print(f"{dt.strftime('%H:%M')}: {temp}°C - {condition}")
```

### Air Quality Monitoring

```python
# Check air quality in Cottbus
air_quality = fetcher.get_air_quality("cottbus")
aqi = air_quality["list"][0]["main"]["aqi"]
pm25 = air_quality["list"][0]["components"]["pm2_5"]

print(f"Air Quality Index: {aqi}")
print(f"PM2.5: {pm25} μg/m³")
```

### Weather by Coordinates

```python
# Get weather for specific location
weather = fetcher.get_weather_for_coordinates(52.5200, 13.4050)
print(f"Temperature: {weather['main']['temp']}°C")
```

## 🎯 Sample Output

```
🌤️  Weather in Eberswalde:
   🌡️  Temperature: 18.5°C (feels like 17.8°C)
   ☁️  Condition: Clear Sky
   💧 Humidity: 65%
   🔽 Pressure: 1013 hPa
   💨 Wind Speed: 3.2 m/s
   📅 Data: 2025-09-18T14:48:12.930184
   🔧 Source: Mock Simulation (No API needed!)

🏙️  Weather Summary for All Brandenburg Cities:
   Cottbus               21.0°C - light rain
   Schwedt/Oder          19.9°C - broken clouds
   Potsdam               19.5°C - scattered clouds
   Frankfurt (Oder)      19.1°C - overcast clouds
   Rathenow              18.2°C - clear sky
   Brandenburg an der Havel  17.8°C - broken clouds
   Eberswalde            17.7°C - scattered clouds
   Neuruppin             17.1°C - overcast clouds
   Senftenberg           16.9°C - moderate rain
   Oranienburg           15.3°C - broken clouds
```

## 🌟 Key Features

### Mock Weather System
- **Realistic Data**: Temperature ranges based on Brandenburg's continental climate
- **Seasonal Variation**: Different weather patterns for winter, spring, summer, autumn
- **Daily Cycles**: Temperature variations throughout the day
- **Regional Differences**: Northern cities slightly cooler than southern ones
- **Weather Conditions**: Appropriate conditions for Brandenburg (rain, clouds, clear sky, etc.)

### Real API Integration
- **OpenWeatherMap API**: Professional weather data service
- **Free Tier**: 1,000 API calls per day
- **Comprehensive Data**: Current weather, forecasts, air quality, weather maps
- **Rate Limiting**: Built-in request throttling
- **Error Handling**: Graceful handling of API failures

## 📊 Data Features

### Weather Data Includes:
- Temperature (current, feels-like, min/max)
- Humidity and atmospheric pressure
- Wind speed and direction
- Weather conditions and descriptions
- Visibility and cloud coverage
- Sunrise/sunset times

### Air Quality Data:
- Air Quality Index (AQI)
- PM2.5 and PM10 particulate matter
- NO₂, O₃, SO₂, CO, NH₃ levels
- Health impact assessments

### Forecast Data:
- Up to 5-day forecasts
- 3-hour interval predictions
- Probability of precipitation
- Temperature trends

## 🛠️ Installation

```bash
# Clone or download the project
git clone <repository-url>
cd eberswalder

# Install dependencies
pip install -r requirements.txt

# Run immediately with mock data
python mock_weather_fetcher.py
```

## 📝 Configuration

Edit `config.py` to customize:

```python
# API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
DEFAULT_UNITS = "metric"  # metric, imperial, kelvin
DEFAULT_LANGUAGE = "en"   # en, de, etc.

# Brandenburg Settings
DEFAULT_CITY = "eberswalde"
REGION_NAME = "Brandenburg"
TIMEZONE = "Europe/Berlin"

# Data Storage
DATA_DIR = "weather_data"
DATA_RETENTION_DAYS = 30
```

## 🎮 Interactive Mode

Run the interactive weather explorer:

```bash
python interactive_weather.py
```

Features:
- 🌡️ Get weather for specific cities
- 🏙️ Compare weather across all cities
- 📊 View weather forecasts
- 🌬️ Check air quality
- 📍 Weather by coordinates
- 🎯 Weather analysis & trends
- 💾 Export data (JSON/CSV)

## 📈 Weather Analysis

The system provides comprehensive weather analysis:

- **Temperature Statistics**: Average, min, max, range
- **Humidity Analysis**: Regional humidity patterns
- **Pressure Monitoring**: Atmospheric pressure variations
- **Wind Patterns**: Wind speed and direction analysis
- **Condition Distribution**: Weather condition frequencies
- **Seasonal Trends**: Climate pattern recognition

## 💾 Data Export

Export weather data in multiple formats:

```python
# Export to JSON
fetcher.save_weather_data(weather_data, "weather_export.json")

# Interactive export (CSV/JSON)
python interactive_weather.py
# Choose option 7: Export weather data
```

## 🔧 API Rate Limits

### OpenWeatherMap Free Tier:
- **1,000 calls/day**
- **60 calls/minute**
- **Current weather**: ✅ Included
- **5-day forecast**: ✅ Included
- **Air pollution**: ✅ Included
- **Weather maps**: ✅ Basic included

### Mock System:
- **Unlimited calls**
- **No rate limits**
- **Instant responses**
- **Perfect for development and testing**

## 🌍 Use Cases

- **🏠 Personal Weather Monitoring**: Track weather in your Brandenburg location
- **🌾 Agriculture**: Weather data for farming and crop management
- **🚲 Outdoor Activities**: Plan hiking, cycling, and outdoor events
- **🏢 Business Intelligence**: Weather impact analysis for businesses
- **📚 Research & Education**: Climate studies and weather pattern analysis
- **🖥️ Software Development**: Test weather-dependent applications
- **📊 Data Analysis**: Historical weather trend analysis

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **API Failures**: Graceful degradation to mock data
- **Network Issues**: Retry mechanisms with backoff
- **Invalid Inputs**: Clear error messages and suggestions
- **Rate Limiting**: Automatic throttling and queuing
- **Data Validation**: Input sanitization and validation

## 🧪 Testing

```bash
# Run all tests without API key
python test_demo.py

# Test mock weather system
python mock_weather_fetcher.py

# Test real API (requires API key)
export OPENWEATHER_API_KEY='your_key'
python quick_test.py
```

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- **Additional Cities**: Add more Brandenburg locations
- **Historical Data**: Implement weather history features
- **Weather Alerts**: Add severe weather notifications
- **Data Visualization**: Charts and graphs
- **Mobile App**: Android/iOS interface
- **Web Interface**: Browser-based dashboard

## 📜 License

This project is open source. Check the LICENSE file for details.

## 🙋 Support

- **Documentation**: This README and inline code comments
- **Examples**: Multiple example scripts provided
- **Mock Data**: Test without external dependencies
- **Error Messages**: Descriptive error handling

## 🌤️ About Brandenburg Weather

Brandenburg has a continental climate characterized by:
- **Cold winters** (December-February): -2°C to 4°C average
- **Mild summers** (June-August): 15°C to 26°C average
- **Moderate precipitation**: ~500-600mm annually
- **Weather variability**: Continental weather patterns
- **Seasonal changes**: Distinct four-season climate

This weather fetcher accounts for all these regional characteristics in its mock data generation!

---

**🎯 Get Started Now:** `python mock_weather_fetcher.py`

**✨ No setup required - realistic weather data instantly!**