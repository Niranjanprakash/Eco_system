"""
Load Tamil Nadu cities data and train ML model
"""
from backend.database import Database
from backend.ml_predictor import MLPredictor
from backend.models import CityAnalyzer, CityData
from utils.data_processor import DataProcessor
import pandas as pd

def load_tamilnadu_data():
    print("Loading Tamil Nadu cities dataset...")
    
    db = Database()
    processor = DataProcessor()
    analyzer = CityAnalyzer()
    
    # Load CSV
    df = pd.read_csv('data/tamilnadu_cities.csv')
    print(f"Loaded {len(df)} Tamil Nadu cities")
    
    # Convert to city objects
    cities = processor.df_to_city_data(df)
    
    # Add to database
    added = 0
    for city in cities:
        try:
            db.add_city(city.__dict__)
            added += 1
            print(f"Added: {city.name}")
        except Exception as e:
            print(f"Skipped {city.name}: {e}")
    
    print(f"\nTotal cities added: {added}")
    
    # Train ML model
    print("\nTraining ML model...")
    ml = MLPredictor()
    
    # Get all cities and calculate scores
    all_cities = []
    scores = []
    
    for city in cities:
        metrics = analyzer.analyze_city(city)
        all_cities.append(city)
        scores.append(metrics.sustainability_score)
        
        # Save analysis to DB
        city_data = db.get_city(city.name)
        if city_data:
            db.save_analysis(city_data['id'], metrics.__dict__)
    
    # Train model
    ml.train(all_cities, scores)
    ml.save_model()
    
    print("ML model trained and saved!")
    
    # Show feature importance
    print("\nFeature Importance:")
    for feature, importance in ml.get_feature_importance():
        print(f"  {feature}: {importance:.4f}")
    
    print(f"\nDatabase ready with {added} Tamil Nadu cities!")
    print("ML model trained on Tamil Nadu data!")

if __name__ == '__main__':
    load_tamilnadu_data()
