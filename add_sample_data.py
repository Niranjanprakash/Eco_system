from backend.database import Database
from backend.models import CityData
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set PostgreSQL password
os.environ['PGPASSWORD'] = 'Pvbn@7738'

# Initialize database
db = Database()

# Sample cities
cities = [
    {
        'name': 'Chennai',
        'area': 426,
        'population': 7088000,
        'population_density': 16632,
        'built_up_percentage': 65,
        'green_space_area': 15,
        'open_land_area': 10,
        'green_coverage_percentage': 3.5,
        'existing_parks': 25,
        'tree_coverage': 12,
        'aqi': 120,
        'pm25': 45,
        'pm10': 85,
        'co2_estimation': 15000,
        'traffic_density': 'High',
        'vehicle_count': 4500000,
        'public_transport_usage': 35,
        'latitude': 13.0827,
        'longitude': 80.2707
    },
    {
        'name': 'Mumbai',
        'area': 603,
        'population': 12442373,
        'population_density': 20634,
        'built_up_percentage': 70,
        'green_space_area': 30,
        'open_land_area': 15,
        'green_coverage_percentage': 5,
        'existing_parks': 35,
        'tree_coverage': 15,
        'aqi': 150,
        'pm25': 55,
        'pm10': 95,
        'co2_estimation': 25000,
        'traffic_density': 'High',
        'vehicle_count': 3500000,
        'public_transport_usage': 45,
        'latitude': 19.0760,
        'longitude': 72.8777
    },
    {
        'name': 'Bangalore',
        'area': 741,
        'population': 8443675,
        'population_density': 11391,
        'built_up_percentage': 60,
        'green_space_area': 50,
        'open_land_area': 25,
        'green_coverage_percentage': 6.7,
        'existing_parks': 45,
        'tree_coverage': 20,
        'aqi': 100,
        'pm25': 38,
        'pm10': 75,
        'co2_estimation': 18000,
        'traffic_density': 'High',
        'vehicle_count': 6000000,
        'public_transport_usage': 30,
        'latitude': 12.9716,
        'longitude': 77.5946
    }
]

print("Adding sample cities to PostgreSQL...")
for city in cities:
    city_id = db.add_city(city)
    if city_id:
        print(f"[OK] Added {city['name']} (ID: {city_id})")
    else:
        print(f"[X] Failed to add {city['name']}")

print(f"\n[OK] Total cities in database: {len(db.get_all_cities())}")
print("\nNow open pgAdmin and check 'ecoplan' database!")
print("You should see 4 tables: cities, analysis_results, simulations, recommendations")
