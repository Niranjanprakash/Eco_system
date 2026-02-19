from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import json
import os
import requests
from werkzeug.utils import secure_filename
from backend.models import CityAnalyzer, RecommendationEngine, CityData, SustainabilityMetrics
from backend.database import Database
from backend.ml_predictor import MLPredictor
from backend.ai_recommendations import AIRecommendationEngine
from utils.data_processor import DataProcessor
from utils.api_integration import DataEnricher

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Add built-in functions to Jinja2 templates
app.jinja_env.globals.update(min=min, max=max)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
analyzer = CityAnalyzer()
recommendation_engine = RecommendationEngine()
ai_recommender = AIRecommendationEngine()
data_processor = DataProcessor()
data_enricher = DataEnricher()
db = Database()
ml_predictor = MLPredictor()
ml_predictor.load_model()  # Load if exists

@app.route('/')
def index():
    cities = db.get_all_cities()
    data_status = {
        'total_cities': len(cities),
        'total_results': len(cities),
        'sources_count': len(cities)
    }
    return render_template('index.html', data_status=data_status)

@app.route('/upload', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'GET':
        return render_template('upload.html')
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith(('.csv', '.xlsx', '.xls')):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Load and validate data
            df = data_processor.load_from_file(filepath)
            errors = data_processor.validate_data(df)
            
            if errors:
                return jsonify({'error': 'Data validation failed', 'details': errors}), 400
            
            # Clean data
            df_clean = data_processor.clean_data(df)
            
            # Convert to city objects and save to database
            new_cities = data_processor.df_to_city_data(df_clean)
            
            for city in new_cities:
                db.add_city(city.__dict__)
            
            return jsonify({
                'message': f'File uploaded successfully. Added {len(new_cities)} cities.',
                'cities_count': len(new_cities),
                'total_cities': len(db.get_all_cities()),
                'cities': [city.name for city in new_cities]
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/manual_input', methods=['GET', 'POST'])
def manual_input():
    if request.method == 'GET':
        return render_template('manual_input.html')
    
    try:
        data = request.json
        print(f"Received data: {data}")  # Debug log
        
        # Validate required fields
        required_fields = ['name', 'area', 'population', 'built_up_percentage', 'green_space_area', 'green_coverage_percentage', 'traffic_density']
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Calculate population density if not provided
        if 'population_density' not in data or not data['population_density']:
            data['population_density'] = data['population'] / data['area']
        
        # Enrich with external API data
        try:
            enriched_data = data_enricher.enrich_city_data(data)
        except Exception as e:
            print(f"API enrichment failed: {e}")
            enriched_data = data
        
        # Save to database
        city_id = db.add_city(enriched_data)
        
        return jsonify({
            'message': f'City "{enriched_data["name"]}" added successfully.',
            'city_name': enriched_data['name'],
            'total_cities': len(db.get_all_cities())
        })
        
    except Exception as e:
        print(f"Manual input error: {e}")  # Debug log
        return jsonify({'error': str(e)}), 500

@app.route('/analyze')
def analyze():
    cities_data = db.get_all_cities()
    if not cities_data:
        return redirect(url_for('index'))
    
    results = []
    for city_dict in cities_data:
        # Remove database-specific fields
        city_data = {k: v for k, v in city_dict.items() if k not in ['id', 'created_at', 'updated_at']}
        
        # Fetch coordinates if missing
        if not city_data.get('latitude') or not city_data.get('longitude'):
            try:
                enriched = data_enricher.enrich_city_data(city_data)
                city_data['latitude'] = enriched.get('latitude')
                city_data['longitude'] = enriched.get('longitude')
                db.update_city_coordinates(city_data['name'], city_data['latitude'], city_data['longitude'])
            except:
                pass
        
        city = CityData(**city_data)
        metrics = analyzer.analyze_city(city)
        recommendations = recommendation_engine.generate_recommendations(city, metrics)
        
        # Save analysis to database
        db.save_analysis(city_dict['id'], metrics.__dict__)
        db.save_recommendations(city_dict['id'], recommendations)
        
        results.append({
            'city': city,
            'metrics': metrics,
            'recommendations': recommendations
        })
    
    return render_template('results.html', results=results)

@app.route('/api/city/<city_name>')
def get_city_analysis(city_name):
    city_data = db.get_city(city_name)
    if not city_data:
        return jsonify({'error': 'City not found'}), 404
    analysis = db.get_latest_analysis(city_data['id'])
    recommendations = db.get_city_recommendations(city_data['id'])
    return jsonify({'city': city_data, 'analysis': analysis, 'recommendations': recommendations})

@app.route('/dashboard')
def dashboard():
    cities_data = db.get_all_cities()
    if not cities_data:
        return redirect(url_for('index'))
    
    results = []
    for city_dict in cities_data:
        city_data = {k: v for k, v in city_dict.items() if k not in ['id', 'created_at', 'updated_at']}
        city = CityData(**city_data)
        analysis = db.get_latest_analysis(city_dict['id'])
        
        if analysis:
            metrics = SustainabilityMetrics(**analysis)
        else:
            metrics = analyzer.analyze_city(city)
            db.save_analysis(city_dict['id'], metrics.__dict__)
        
        recommendations = db.get_city_recommendations(city_dict['id'])
        results.append({'city': city, 'metrics': metrics, 'recommendations': recommendations})
    
    # Generate maps
    maps = {}
    try:
        from utils.visualization import MapGenerator
        map_generator = MapGenerator()
        
        if len(results) == 1:
            # Single city map
            city = results[0]['city']
            metrics = results[0]['metrics']
            maps['city_map'] = map_generator.create_city_map(city, metrics)
        else:
            # Multi-city map
            cities_data = []
            for result in results:
                cities_data.append({
                    'name': result['city'].name,
                    'sustainability_score': result['metrics'].sustainability_score,
                    'category': result['metrics'].category,
                    'latitude': result['city'].latitude,
                    'longitude': result['city'].longitude
                })
            maps['multi_city_map'] = map_generator.create_multi_city_map(cities_data)
    except Exception as e:
        print(f"Map generation error: {e}")
        maps = {}
    
    return render_template('dashboard_simple.html', results=results, sources=[], total_cities=len(cities_data), maps=maps)

@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    if request.method == 'GET':
        cities_data = db.get_all_cities()
        if not cities_data:
            return redirect(url_for('index'))
        results = []
        for city_dict in cities_data:
            city_data = {k: v for k, v in city_dict.items() if k not in ['id', 'created_at', 'updated_at']}
            city = CityData(**city_data)
            analysis = db.get_latest_analysis(city_dict['id'])
            if analysis:
                metrics = SustainabilityMetrics(**analysis)
            else:
                metrics = analyzer.analyze_city(city)
            results.append({'city': city, 'metrics': metrics})
        return render_template('simulate.html', results=results)
    
    try:
        data = request.json
        city_name = data.get('city_name')
        scenarios = data.get('scenarios', {})
        
        # Find the city
        city_data = db.get_city(city_name)
        if not city_data:
            return jsonify({'error': 'City not found'}), 404
        
        city_dict = {k: v for k, v in city_data.items() if k not in ['id', 'created_at', 'updated_at']}
        original_city = CityData(**city_dict)
        original_metrics = analyzer.analyze_city(original_city)
        modified_city = CityData(**city_dict)
        
        # Apply scenarios
        if 'green_space_increase' in scenarios:
            increase = scenarios['green_space_increase'] / 100
            modified_city.green_space_area *= (1 + increase)
            modified_city.green_coverage_percentage *= (1 + increase)
        
        if 'tree_plantation' in scenarios:
            trees_added = scenarios['tree_plantation']
            # Estimate impact on green coverage (rough calculation)
            area_per_tree = 0.0001  # sq km per tree
            modified_city.green_space_area += trees_added * area_per_tree
        
        if 'traffic_reduction' in scenarios:
            reduction = scenarios['traffic_reduction'] / 100
            modified_city.vehicle_count = int(modified_city.vehicle_count * (1 - reduction))
            # Improve AQI based on traffic reduction
            modified_city.aqi *= (1 - reduction * 0.3)
        
        # Analyze modified city
        new_metrics = analyzer.analyze_city(modified_city)
        db.save_simulation(city_data['id'], 'what-if', scenarios, {'original_score': original_metrics.sustainability_score, 'new_score': new_metrics.sustainability_score})
        improvements = {
            'sustainability_score_change': new_metrics.sustainability_score - original_metrics.sustainability_score,
            'aqi_change': original_city.aqi - modified_city.aqi,
            'green_space_change': new_metrics.green_space_per_capita - original_metrics.green_space_per_capita
        }
        return jsonify({'original_metrics': original_metrics.__dict__, 'new_metrics': new_metrics.__dict__, 'improvements': improvements})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/<format>')
def export_data(format):
    cities_data = db.get_all_cities()
    if not cities_data:
        return jsonify({'error': 'No data to export'}), 404
    results = []
    for city_dict in cities_data:
        city_data = {k: v for k, v in city_dict.items() if k not in ['id', 'created_at', 'updated_at']}
        city = CityData(**city_data)
        analysis = db.get_latest_analysis(city_dict['id'])
        if analysis:
            metrics = SustainabilityMetrics(**analysis)
        else:
            metrics = analyzer.analyze_city(city)
        recommendations = db.get_city_recommendations(city_dict['id'])
        results.append({'city': city, 'metrics': metrics, 'recommendations': recommendations})
    
    if format == 'json':
        export_data = []
        for result in results:
            export_data.append({
                'city': result['city'].__dict__,
                'metrics': result['metrics'].__dict__,
                'recommendations': result['recommendations']
            })
        
        return jsonify(export_data)
    
    elif format == 'csv':
        # Create CSV data
        csv_data = []
        for result in results:
            row = {
                'City': result['city'].name,
                'Sustainability Score': result['metrics'].sustainability_score,
                'Category': result['metrics'].category,
                'Green Space per Capita': result['metrics'].green_space_per_capita,
                'WHO Compliance': result['metrics'].who_standard_compliance,
                'Required Green Space': result['metrics'].required_green_space,
                'Recommended Parks': result['metrics'].recommended_parks,
                'Recommended Trees': result['metrics'].recommended_trees,
                'CO2 Reduction Potential': result['metrics'].co2_reduction_potential
            }
            csv_data.append(row)
        
        df = pd.DataFrame(csv_data)
        return df.to_csv(index=False)
    
    return jsonify({'error': 'Invalid format'}), 400

@app.route('/sample_data')
def get_sample_data():
    sample_df = data_processor.create_sample_data()
    new_cities = data_processor.df_to_city_data(sample_df)
    
    added = 0
    for city in new_cities:
        try:
            db.add_city(city.__dict__)
            added += 1
        except:
            pass
    
    return jsonify({
        'message': f'Sample data loaded. Added {added} cities.',
        'cities_count': added,
        'total_cities': len(db.get_all_cities())
    })

@app.route('/clear_data', methods=['POST'])
def clear_data():
    cities = db.get_all_cities()
    for city in cities:
        db.delete_city(city['name'])
    return jsonify({'message': 'All data cleared successfully'})

@app.route('/data_sources')
def data_sources():
    cities = db.get_all_cities()
    return jsonify({'total_cities': len(cities), 'cities': [city['name'] for city in cities]})

@app.route('/api/city_suggestions/<query>')
def get_city_suggestions(query):
    """Get city suggestions for autocomplete"""
    if len(query) < 2:
        return jsonify({'suggestions': []})
    
    try:
        api_key = data_enricher.geo_api.api_key
        if not api_key:
            return jsonify({'suggestions': []})
        
        url = "https://api.geoapify.com/v1/geocode/autocomplete"
        params = {
            'text': query,
            'apiKey': api_key,
            'limit': 5,
            'type': 'city',
            'filter': 'countrycode:in',
            'format': 'json'
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            suggestions = []
            
            if data.get('results'):
                for result in data['results']:
                    city_name = result.get('city') or result.get('name', '')
                    state = result.get('state', '')
                    country = result.get('country', '')
                    
                    if city_name:
                        display_name = city_name
                        if state:
                            display_name += f", {state}"
                        # Only show India cities
                        if country == 'India':
                            suggestions.append({
                                'city': city_name,
                                'display': display_name,
                                'lat': result.get('lat'),
                                'lon': result.get('lon')
                            })
            
            return jsonify({'suggestions': suggestions})
        else:
            return jsonify({'suggestions': []})
            
    except Exception as e:
        print(f"City suggestions error: {e}")
        return jsonify({'suggestions': []})

@app.route('/api/fetch_city_data/<city_name>')
def fetch_city_data(city_name):
    """Fetch coordinates and weather data for a city"""
    try:
        # Get coordinates
        coords = data_enricher.geo_api.geocode_city(city_name)
        if not coords:
            return jsonify({'error': f'Could not find coordinates for {city_name}'}), 404
        
        lat, lon = coords
        
        # Get weather/pollution data
        pollution_data = data_enricher.weather_api.get_air_pollution(lat, lon)
        
        result = {
            'city_name': city_name,
            'latitude': lat,
            'longitude': lon,
            'coordinates_found': True
        }
        
        if pollution_data:
            result.update({
                'aqi': pollution_data['aqi'] * 50,  # Convert to standard AQI
                'pm25': pollution_data['pm25'],
                'pm10': pollution_data['pm10'],
                'weather_data_found': True
            })
        else:
            result['weather_data_found'] = False
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ml_predict', methods=['POST'])
def ml_predict():
    """Predict sustainability using ML model"""
    try:
        data = request.json
        city_data = CityData(**data)
        
        ml_score = ml_predictor.predict_sustainability(city_data)
        rule_based_metrics = analyzer.analyze_city(city_data)
        
        return jsonify({
            'ml_prediction': float(ml_score) if ml_score else None,
            'rule_based_score': rule_based_metrics.sustainability_score,
            'difference': float(ml_score - rule_based_metrics.sustainability_score) if ml_score else None,
            'model_trained': ml_predictor.is_trained
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ml_feature_importance')
def ml_feature_importance():
    """Get ML model feature importance"""
    importance = ml_predictor.get_feature_importance()
    if importance:
        return jsonify({
            'features': [{'name': f, 'importance': float(i)} for f, i in importance],
            'model_trained': True
        })
    return jsonify({'error': 'Model not trained', 'model_trained': False}), 404

@app.route('/api/train_ml', methods=['POST'])
def train_ml():
    """Train ML model on current database"""
    try:
        cities_data = db.get_all_cities()
        if len(cities_data) < 5:
            return jsonify({'error': 'Need at least 5 cities to train'}), 400
        
        cities = []
        scores = []
        
        for city_dict in cities_data:
            city_data = {k: v for k, v in city_dict.items() if k not in ['id', 'created_at', 'updated_at']}
            city = CityData(**city_data)
            metrics = analyzer.analyze_city(city)
            
            cities.append(city)
            scores.append(metrics.sustainability_score)
        
        ml_predictor.train(cities, scores)
        ml_predictor.save_model()
        
        return jsonify({
            'message': 'ML model trained successfully',
            'cities_count': len(cities),
            'feature_importance': [{'name': f, 'importance': float(i)} 
                                  for f, i in ml_predictor.get_feature_importance()]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai_plan/<city_name>')
def get_ai_plan(city_name):
    """Get AI-powered personalized action plan for a city"""
    try:
        city_data = db.get_city(city_name)
        if not city_data:
            return jsonify({'error': 'City not found'}), 404
        
        city_dict = {k: v for k, v in city_data.items() if k not in ['id', 'created_at', 'updated_at']}
        city = CityData(**city_dict)
        metrics = analyzer.analyze_city(city)
        
        # Generate AI-powered personalized plan
        ai_plan = ai_recommender.generate_personalized_plan(city, metrics)
        
        return jsonify(ai_plan)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)