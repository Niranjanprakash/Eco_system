import requests
import os
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

class GeoapifyAPI:
    def __init__(self):
        self.api_key = os.getenv('GEOAPIFY_API_KEY')
        self.base_url = "https://api.geoapify.com/v1"
    
    def geocode_city(self, city_name: str) -> Optional[Tuple[float, float]]:
        """Get latitude and longitude for a city"""
        if not self.api_key or self.api_key == 'your_geoapify_api_key_here':
            print("No valid Geoapify API key found")
            return None
            
        url = f"{self.base_url}/geocode/search"
        params = {
            'text': city_name,
            'apiKey': self.api_key,
            'limit': 1,
            'format': 'json'
        }
        
        try:
            print(f"Geocoding request for: {city_name}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Handle response encoding properly
            response.encoding = 'utf-8'
            data = response.json()
            
            print(f"Geoapify response status: {response.status_code}")
            
            # Check for results in the response
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                lat = result.get('lat')
                lon = result.get('lon')
                
                if lat is not None and lon is not None:
                    print(f"Found coordinates for {city_name}: {lat}, {lon}")
                    return float(lat), float(lon)
                else:
                    print(f"Coordinates missing in result for {city_name}")
                    return None
            else:
                print(f"No results found for {city_name}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error for {city_name}: {str(e)}")
            return None
        except Exception as e:
            print(f"Geocoding error for {city_name}: {str(e)}")
            return None

class OpenWeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_air_pollution(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current air pollution data"""
        if not self.api_key or self.api_key == 'your_openweather_api_key_here':
            print("No valid OpenWeather API key found")
            return None
            
        url = f"{self.base_url}/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        try:
            print(f"Fetching air pollution for coordinates: {lat}, {lon}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"OpenWeather response: {data}")
            
            if data.get('list') and len(data['list']) > 0:
                pollution_data = data['list'][0]
                result = {
                    'aqi': pollution_data['main']['aqi'],
                    'pm25': pollution_data['components'].get('pm2_5', 0),
                    'pm10': pollution_data['components'].get('pm10', 0),
                    'co': pollution_data['components'].get('co', 0)
                }
                print(f"Pollution data extracted: {result}")
                return result
            else:
                print("No pollution data in response")
                return None
        except Exception as e:
            print(f"Air pollution API error: {e}")
            return None

class DataEnricher:
    def __init__(self):
        self.geo_api = GeoapifyAPI()
        self.weather_api = OpenWeatherAPI()
    
    def enrich_city_data(self, city_data: Dict) -> Dict:
        """Enrich city data with external API data"""
        city_name = city_data.get('name', '')
        print(f"Enriching data for: {city_name}")
        
        # Get coordinates first
        coords = self.geo_api.geocode_city(city_name)
        if coords:
            city_data['latitude'] = coords[0]
            city_data['longitude'] = coords[1]
            print(f"Coordinates found: {coords[0]}, {coords[1]}")
            
            # Get air pollution data using coordinates
            pollution_data = self.weather_api.get_air_pollution(coords[0], coords[1])
            if pollution_data:
                print(f"Pollution data fetched: AQI={pollution_data['aqi']}")
                # Update with real data if not provided or if provided data is 0
                if not city_data.get('aqi') or city_data.get('aqi') == 0:
                    city_data['aqi'] = pollution_data['aqi'] * 50  # Convert to standard AQI
                if not city_data.get('pm25') or city_data.get('pm25') == 0:
                    city_data['pm25'] = pollution_data['pm25']
                if not city_data.get('pm10') or city_data.get('pm10') == 0:
                    city_data['pm10'] = pollution_data['pm10']
            else:
                print("No pollution data available")
        else:
            print(f"No coordinates found for {city_name}")
        
        return city_data