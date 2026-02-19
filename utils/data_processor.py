import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from backend.models import CityData

class DataProcessor:
    def __init__(self):
        self.required_columns = [
            'name', 'area', 'population', 'population_density',
            'built_up_percentage', 'green_space_area', 'open_land_area',
            'green_coverage_percentage', 'existing_parks', 'tree_coverage',
            'aqi', 'pm25', 'pm10', 'co2_estimation', 'traffic_density',
            'vehicle_count', 'public_transport_usage'
        ]
    
    def validate_data(self, df: pd.DataFrame) -> List[str]:
        """Validate uploaded data and return list of errors"""
        errors = []
        
        # Check required columns
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            errors.append(f"Missing columns: {', '.join(missing_cols)}")
        
        # Check data types and ranges
        if 'population' in df.columns:
            if df['population'].dtype not in ['int64', 'float64'] or (df['population'] < 0).any():
                errors.append("Population must be positive numbers")
        
        if 'area' in df.columns:
            if df['area'].dtype not in ['int64', 'float64'] or (df['area'] <= 0).any():
                errors.append("Area must be positive numbers")
        
        if 'green_coverage_percentage' in df.columns:
            if (df['green_coverage_percentage'] < 0).any() or (df['green_coverage_percentage'] > 100).any():
                errors.append("Green coverage percentage must be between 0-100")
        
        return errors
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data"""
        df_clean = df.copy()
        
        # Handle missing values
        numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_columns] = df_clean[numeric_columns].fillna(0)
        
        # Clean text columns ONLY (not numeric)
        if 'traffic_density' in df_clean.columns:
            # Convert to string first, then apply .str methods
            df_clean['traffic_density'] = df_clean['traffic_density'].astype(str).str.title()
            df_clean['traffic_density'] = df_clean['traffic_density'].replace('Nan', 'Medium')
        
        # Calculate derived fields if missing
        if 'population_density' not in df_clean.columns and 'population' in df_clean.columns and 'area' in df_clean.columns:
            df_clean['population_density'] = df_clean['population'] / df_clean['area']
        
        return df_clean
    
    def load_from_file(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV or Excel file"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel files.")
            
            return df
        except Exception as e:
            raise Exception(f"Error loading file: {str(e)}")
    
    def df_to_city_data(self, df: pd.DataFrame) -> List[CityData]:
        """Convert DataFrame to list of CityData objects"""
        cities = []
        
        for _, row in df.iterrows():
            city = CityData(
                name=str(row.get('name', '')),
                area=float(row.get('area', 0)),
                population=int(row.get('population', 0)),
                population_density=float(row.get('population_density', 0)),
                built_up_percentage=float(row.get('built_up_percentage', 0)),
                green_space_area=float(row.get('green_space_area', 0)),
                open_land_area=float(row.get('open_land_area', 0)),
                green_coverage_percentage=float(row.get('green_coverage_percentage', 0)),
                existing_parks=int(row.get('existing_parks', 0)),
                tree_coverage=float(row.get('tree_coverage', 0)),
                aqi=float(row.get('aqi', 0)),
                pm25=float(row.get('pm25', 0)),
                pm10=float(row.get('pm10', 0)),
                co2_estimation=float(row.get('co2_estimation', 0)),
                traffic_density=str(row.get('traffic_density', 'Medium')),
                vehicle_count=int(row.get('vehicle_count', 0)),
                public_transport_usage=float(row.get('public_transport_usage', 0)),
                latitude=row.get('latitude'),
                longitude=row.get('longitude')
            )
            cities.append(city)
        
        return cities
    
    def create_sample_data(self) -> pd.DataFrame:
        """Create sample data for demonstration"""
        sample_data = {
            'name': ['Mumbai', 'Pune', 'Nashik', 'Nagpur'],
            'area': [603.4, 331.3, 264.5, 227.4],
            'population': [12442373, 3124458, 1486973, 2405421],
            'population_density': [20634, 9429, 5626, 10576],
            'built_up_percentage': [85, 70, 60, 65],
            'green_space_area': [30.2, 49.7, 39.7, 34.1],
            'open_land_area': [50.1, 82.3, 79.4, 68.2],
            'green_coverage_percentage': [15, 25, 30, 20],
            'existing_parks': [45, 78, 34, 56],
            'tree_coverage': [12, 22, 28, 18],
            'aqi': [156, 89, 76, 98],
            'pm25': [78, 45, 38, 52],
            'pm10': [112, 67, 58, 78],
            'co2_estimation': [2340, 890, 670, 1120],
            'traffic_density': ['High', 'Medium', 'Low', 'Medium'],
            'vehicle_count': [2800000, 1200000, 450000, 890000],
            'public_transport_usage': [45, 35, 25, 30]
        }
        
        return pd.DataFrame(sample_data)