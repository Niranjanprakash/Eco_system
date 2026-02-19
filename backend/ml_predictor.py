import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import os

class MLPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, city_data):
        """Extract features from city data"""
        return np.array([[
            city_data.population_density,
            city_data.green_space_area,
            city_data.green_coverage_percentage,
            city_data.aqi,
            city_data.pm25,
            city_data.pm10,
            city_data.vehicle_count,
            city_data.public_transport_usage,
            city_data.built_up_percentage,
            city_data.existing_parks,
            city_data.tree_coverage
        ]])
    
    def train(self, cities_data, scores):
        """Train model on existing city data"""
        X = []
        for city in cities_data:
            X.append(self.prepare_features(city)[0])
        
        X = np.array(X)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, scores)
        self.is_trained = True
        
    def predict_sustainability(self, city_data):
        """Predict sustainability score using ML"""
        if not self.is_trained:
            return None
        
        X = self.prepare_features(city_data)
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)[0]
    
    def get_feature_importance(self):
        """Get which features matter most"""
        if not self.is_trained:
            return None
        
        features = ['Population Density', 'Green Space Area', 'Green Coverage %', 
                   'AQI', 'PM2.5', 'PM10', 'Vehicle Count', 'Public Transport %',
                   'Built-up %', 'Parks', 'Tree Coverage']
        
        importance = dict(zip(features, self.model.feature_importances_))
        return sorted(importance.items(), key=lambda x: x[1], reverse=True)
    
    def save_model(self, path='data/ml_model.pkl'):
        """Save trained model"""
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler, 'trained': self.is_trained}, f)
    
    def load_model(self, path='data/ml_model.pkl'):
        """Load trained model"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                self.is_trained = data['trained']
            return True
        return False
