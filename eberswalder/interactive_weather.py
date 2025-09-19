#!/usr/bin/env python3
"""
Interactive Weather Explorer for Brandenburg

This script provides an interactive command-line interface to explore
mock weather data for Brandenburg cities. No API key required!

Features:
- Interactive menu system
- Real-time weather simulation
- Historical comparison
- Weather trends analysis
- Data export options
"""

import os
import sys
import json
from datetime import datetime, timedelta
from mock_weather_fetcher import MockBrandenburgWeatherFetcher


class InteractiveWeatherExplorer:
    """Interactive weather exploration interface"""
    
    def __init__(self):
        self.fetcher = MockBrandenburgWeatherFetcher()
        self.weather_cache = {}
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_menu(self):
        """Display the main menu"""
        self.clear_screen()
        print("🌤️  Interactive Brandenburg Weather Explorer")
        print("✨ Mock weather data - no API key needed!")
        print()
        print("Choose an option:")
        print()
        print("1. 🌡️  Get current weather for a city")
        print("2. 🏙️  Compare weather across all cities")
        print("3. 📊 Get weather forecast")
        print("4. 🌬️  Check air quality")
        print("5. 📍 Weather by coordinates")
        print("6. 🎯 Weather analysis & trends")
        print("7. 💾 Export weather data")
        print("8. 🔄 Refresh all weather data")
        print("9. ℹ️  Show available cities")
        print("0. 🚪 Exit")
        print()
        print("=" * 60)
    
    def show_cities(self):
        """Display available cities"""
        self.print_header("Available Brandenburg Cities")
        print()
        print("You can use any of these cities:")
        print()
        
        for i, (key, city) in enumerate(self.fetcher.brandenburg_cities.items(), 1):
            print(f"{i:2d}. {city['name']:<25} (key: '{key}')")
            print(f"     📍 {city['lat']:.4f}°N, {city['lon']:.4f}°E")
            print()
        
        input("\nPress Enter to continue...")
    
    def get_city_weather(self):
        """Get weather for a specific city"""
        self.print_header("Current Weather for City")
        
        # Show available cities
        print("Available cities:")
        cities = list(self.fetcher.brandenburg_cities.keys())
        for i, city_key in enumerate(cities, 1):
            city_name = self.fetcher.brandenburg_cities[city_key]["name"]
            print(f"{i:2d}. {city_name} ({city_key})")
        
        print()
        choice = input("Enter city number or city key: ").strip().lower()
        
        # Handle number input
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(cities):
                city_key = cities[idx]
            else:
                print("❌ Invalid city number!")
                input("Press Enter to continue...")
                return
        # Handle key input
        elif choice in self.fetcher.brandenburg_cities:
            city_key = choice
        else:
            print("❌ City not found!")
            input("Press Enter to continue...")
            return
        
        try:
            weather = self.fetcher.get_current_weather(city_key)
            print("\n" + self.fetcher.format_current_weather(weather))
            
            # Cache for later use
            self.weather_cache[city_key] = weather
            
            # Ask if user wants to save
            save = input("\nSave this data to file? (y/N): ").strip().lower()
            if save == 'y':
                filename = f"{city_key}_weather_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
                self.fetcher.save_weather_data(weather, filename)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def compare_all_cities(self):
        """Compare weather across all cities"""
        self.print_header("Weather Comparison - All Brandenburg Cities")
        
        print("🔄 Fetching weather data for all cities...")
        all_weather = self.fetcher.get_all_brandenburg_weather()
        
        # Store in cache
        self.weather_cache.update(all_weather["cities"])
        
        print("\n🌡️  Temperature Ranking:")
        print("-" * 50)
        
        # Sort cities by temperature
        city_temps = []
        for city_key, weather_data in all_weather["cities"].items():
            if "error" not in weather_data:
                city_name = weather_data["city_info"]["name"]
                temp = weather_data["main"]["temp"]
                condition = weather_data["weather"][0]["description"].title()
                humidity = weather_data["main"]["humidity"]
                wind = weather_data["wind"]["speed"]
                city_temps.append((temp, city_name, condition, humidity, wind))
        
        city_temps.sort(reverse=True)
        
        for i, (temp, city_name, condition, humidity, wind) in enumerate(city_temps, 1):
            print(f"{i:2d}. {city_name:<20} {temp:>5.1f}°C - {condition}")
            print(f"     💧 {humidity}% humidity, 💨 {wind} m/s wind")
            print()
        
        # Show weather statistics
        temps = [temp for temp, _, _, _, _ in city_temps]
        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)
        
        print("📊 Weather Statistics:")
        print(f"   🔥 Warmest: {max_temp:.1f}°C")
        print(f"   ❄️  Coldest: {min_temp:.1f}°C")
        print(f"   📊 Average: {avg_temp:.1f}°C")
        print(f"   📏 Range: {max_temp - min_temp:.1f}°C")
        
        input("\nPress Enter to continue...")
    
    def get_forecast(self):
        """Get weather forecast for a city"""
        self.print_header("Weather Forecast")
        
        city_key = input("Enter city key (e.g., 'eberswalde'): ").strip().lower()
        
        if city_key not in self.fetcher.brandenburg_cities:
            print("❌ City not found!")
            input("Press Enter to continue...")
            return
        
        try:
            days = input("How many days? (1-5, default 3): ").strip()
            days = int(days) if days.isdigit() and 1 <= int(days) <= 5 else 3
            
            forecast = self.fetcher.get_forecast(city_key, days)
            city_name = forecast["city_info"]["name"]
            
            print(f"\n📊 {days}-Day Forecast for {city_name}:")
            print("-" * 60)
            
            current_date = None
            for item in forecast["list"][:days * 4]:  # Show 4 times per day
                dt = datetime.fromtimestamp(item["dt"])
                date_str = dt.strftime("%Y-%m-%d")
                time_str = dt.strftime("%H:%M")
                
                # Print date header when date changes
                if current_date != date_str:
                    if current_date is not None:
                        print()
                    print(f"\n📅 {dt.strftime('%A, %B %d, %Y')}:")
                    current_date = date_str
                
                temp = item["main"]["temp"]
                feels_like = item["main"]["feels_like"]
                description = item["weather"][0]["description"].title()
                humidity = item["main"]["humidity"]
                pop = item["pop"] * 100
                
                print(f"  {time_str}: {temp:>4.1f}°C (feels {feels_like:>4.1f}°C)")
                print(f"         {description}, {humidity}% humidity, {pop:.0f}% rain chance")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def check_air_quality(self):
        """Check air quality for a city"""
        self.print_header("Air Quality Check")
        
        city_key = input("Enter city key (e.g., 'potsdam'): ").strip().lower()
        
        if city_key not in self.fetcher.brandenburg_cities:
            print("❌ City not found!")
            input("Press Enter to continue...")
            return
        
        try:
            air_quality = self.fetcher.get_air_quality(city_key)
            city_name = air_quality["city_info"]["name"]
            aqi = air_quality["list"][0]["main"]["aqi"]
            components = air_quality["list"][0]["components"]
            
            aqi_meanings = {
                1: ("Good", "🟢"),
                2: ("Fair", "🟡"), 
                3: ("Moderate", "🟠"),
                4: ("Poor", "🔴"),
                5: ("Very Poor", "🟣")
            }
            
            meaning, emoji = aqi_meanings.get(aqi, ("Unknown", "❓"))
            
            print(f"\n🌬️  Air Quality in {city_name}:")
            print(f"   {emoji} Air Quality Index: {aqi} ({meaning})")
            print()
            print("   Pollutant Levels (μg/m³):")
            print(f"   💨 CO (Carbon Monoxide):     {components.get('co', 'N/A'):>8}")
            print(f"   💨 NO₂ (Nitrogen Dioxide):   {components.get('no2', 'N/A'):>8}")
            print(f"   💨 O₃ (Ozone):               {components.get('o3', 'N/A'):>8}")
            print(f"   💨 PM2.5 (Fine Particles):  {components.get('pm2_5', 'N/A'):>8}")
            print(f"   💨 PM10 (Coarse Particles): {components.get('pm10', 'N/A'):>8}")
            print(f"   💨 SO₂ (Sulfur Dioxide):    {components.get('so2', 'N/A'):>8}")
            print(f"   💨 NH₃ (Ammonia):            {components.get('nh3', 'N/A'):>8}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def weather_by_coordinates(self):
        """Get weather for specific coordinates"""
        self.print_header("Weather by Coordinates")
        
        print("Enter coordinates for Brandenburg region:")
        print("(Brandenburg spans roughly 51.4-53.1°N, 11.3-14.8°E)")
        print()
        
        try:
            lat = float(input("Latitude (°N): ").strip())
            lon = float(input("Longitude (°E): ").strip())
            
            weather = self.fetcher.get_weather_for_coordinates(lat, lon)
            print(f"\n📍 Weather at coordinates ({lat:.4f}, {lon:.4f}):")
            print(self.fetcher.format_current_weather(weather))
            
        except ValueError:
            print("❌ Invalid coordinates! Please enter numbers.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def weather_analysis(self):
        """Analyze weather trends and patterns"""
        self.print_header("Weather Analysis & Trends")
        
        if not self.weather_cache:
            print("🔄 Fetching weather data for analysis...")
            all_weather = self.fetcher.get_all_brandenburg_weather()
            self.weather_cache.update(all_weather["cities"])
        
        # Temperature analysis
        temps = []
        humidities = []
        pressures = []
        wind_speeds = []
        conditions = {}
        
        for city_key, weather in self.weather_cache.items():
            if "error" not in weather and "main" in weather:
                temps.append(weather["main"]["temp"])
                humidities.append(weather["main"]["humidity"])
                pressures.append(weather["main"]["pressure"])
                wind_speeds.append(weather["wind"]["speed"])
                
                condition = weather["weather"][0]["main"]
                conditions[condition] = conditions.get(condition, 0) + 1
        
        if not temps:
            print("❌ No weather data available for analysis")
            input("Press Enter to continue...")
            return
        
        print("📊 Regional Weather Analysis:")
        print()
        print("🌡️  Temperature Statistics:")
        print(f"   Average: {sum(temps)/len(temps):.1f}°C")
        print(f"   Maximum: {max(temps):.1f}°C")
        print(f"   Minimum: {min(temps):.1f}°C")
        print(f"   Range:   {max(temps) - min(temps):.1f}°C")
        
        print("\n💧 Humidity Statistics:")
        print(f"   Average: {sum(humidities)/len(humidities):.1f}%")
        print(f"   Range:   {min(humidities):.0f}% - {max(humidities):.0f}%")
        
        print("\n🔽 Pressure Statistics:")
        print(f"   Average: {sum(pressures)/len(pressures):.0f} hPa")
        print(f"   Range:   {min(pressures):.0f} - {max(pressures):.0f} hPa")
        
        print("\n💨 Wind Statistics:")
        print(f"   Average: {sum(wind_speeds)/len(wind_speeds):.1f} m/s")
        print(f"   Maximum: {max(wind_speeds):.1f} m/s")
        
        print("\n☁️  Weather Conditions Distribution:")
        total_cities = sum(conditions.values())
        for condition, count in sorted(conditions.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_cities) * 100
            print(f"   {condition:<15} {count:>2} cities ({percentage:>4.1f}%)")
        
        input("\nPress Enter to continue...")
    
    def export_weather_data(self):
        """Export weather data to files"""
        self.print_header("Export Weather Data")
        
        if not self.weather_cache:
            print("🔄 Fetching weather data to export...")
            all_weather = self.fetcher.get_all_brandenburg_weather()
            self.weather_cache.update(all_weather["cities"])
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        print("Choose export format:")
        print("1. JSON (detailed data)")
        print("2. CSV (summary data)")
        print("3. Both")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice in ['1', '3']:
            # Export JSON
            filename = f"brandenburg_weather_export_{timestamp}.json"
            export_data = {
                "export_time": datetime.now().isoformat(),
                "data_source": "mock_simulation",
                "cities": self.weather_cache
            }
            self.fetcher.save_weather_data(export_data, filename)
            print(f"✅ JSON data exported to {filename}")
        
        if choice in ['2', '3']:
            # Export CSV
            filename = f"brandenburg_weather_export_{timestamp}.csv"
            with open(filename, 'w') as f:
                f.write("City,Temperature,FeelsLike,Humidity,Pressure,WindSpeed,Condition,Timestamp\n")
                for city_key, weather in self.weather_cache.items():
                    if "error" not in weather and "main" in weather:
                        city_name = weather["city_info"]["name"]
                        temp = weather["main"]["temp"]
                        feels_like = weather["main"]["feels_like"]
                        humidity = weather["main"]["humidity"]
                        pressure = weather["main"]["pressure"]
                        wind_speed = weather["wind"]["speed"]
                        condition = weather["weather"][0]["description"]
                        timestamp = weather.get("fetch_time", "")
                        
                        f.write(f'"{city_name}",{temp},{feels_like},{humidity},{pressure},{wind_speed},"{condition}","{timestamp}"\n')
            print(f"✅ CSV data exported to {filename}")
        
        input("\nPress Enter to continue...")
    
    def refresh_weather_data(self):
        """Refresh all weather data"""
        self.print_header("Refreshing Weather Data")
        
        print("🔄 Fetching fresh weather data for all cities...")
        all_weather = self.fetcher.get_all_brandenburg_weather()
        self.weather_cache = all_weather["cities"]
        
        print("✅ Weather data refreshed!")
        print(f"📊 Updated data for {len(self.weather_cache)} cities")
        print(f"🕒 Last update: {all_weather['timestamp']}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main program loop"""
        while self.running:
            self.print_menu()
            
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == '1':
                self.get_city_weather()
            elif choice == '2':
                self.compare_all_cities()
            elif choice == '3':
                self.get_forecast()
            elif choice == '4':
                self.check_air_quality()
            elif choice == '5':
                self.weather_by_coordinates()
            elif choice == '6':
                self.weather_analysis()
            elif choice == '7':
                self.export_weather_data()
            elif choice == '8':
                self.refresh_weather_data()
            elif choice == '9':
                self.show_cities()
            elif choice == '0':
                self.clear_screen()
                print("👋 Thanks for using Brandenburg Weather Explorer!")
                print("   Mock weather data - no APIs harmed! 🌤️")
                self.running = False
            else:
                print("❌ Invalid choice! Please enter 0-9.")
                input("Press Enter to try again...")


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("🌤️  Interactive Brandenburg Weather Explorer")
        print()
        print("This is an interactive weather exploration tool that uses")
        print("realistic mock data for Brandenburg cities. No API key needed!")
        print()
        print("Features:")
        print("• Current weather for all major Brandenburg cities")
        print("• Weather forecasts and trends")
        print("• Air quality monitoring")
        print("• Weather by coordinates")
        print("• Data analysis and export")
        print("• Completely offline operation")
        print()
        print("Usage: python interactive_weather.py")
        return
    
    try:
        explorer = InteractiveWeatherExplorer()
        explorer.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()