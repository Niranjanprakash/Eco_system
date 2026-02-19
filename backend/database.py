import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Dict, List, Optional
import json
import os

class Database:
    def __init__(self):

        # Railway MySQL Environment Variables
        self.host = os.environ.get("MYSQLHOST")
        self.database = os.environ.get("MYSQLDATABASE")
        self.user = os.environ.get("MYSQLUSER")
        self.password = os.environ.get("MYSQLPASSWORD")
        self.port = int(os.environ.get("MYSQLPORT", 3306))

        print("DB HOST:", self.host)   # Debug log for Render

        self.ensure_database_exists()
        self.init_database()

    
    def _ensure_database_exists(self):
        """Create database if it doesn't exist"""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            conn.close()
            print(f"[OK] Database '{self.database}' ready")
        except Error as e:
            print(f"[X] Error ensuring database exists: {e}")
    
    def get_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return conn
        except Error as e:
            print(f"[X] Database connection error: {e}")
            print(f"  Host: {self.host}, Database: {self.database}, User: {self.user}")
            return None
    
    def init_database(self):
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # Cities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                area FLOAT NOT NULL,
                population INT NOT NULL,
                population_density FLOAT,
                built_up_percentage FLOAT,
                green_space_area FLOAT,
                open_land_area FLOAT,
                green_coverage_percentage FLOAT,
                existing_parks INT,
                tree_coverage FLOAT,
                aqi FLOAT,
                pm25 FLOAT,
                pm10 FLOAT,
                co2_estimation FLOAT,
                traffic_density VARCHAR(50),
                vehicle_count INT,
                public_transport_usage FLOAT,
                latitude FLOAT,
                longitude FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        
        # Analysis results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_id INT NOT NULL,
                sustainability_score FLOAT,
                category VARCHAR(100),
                badge_level VARCHAR(100),
                green_space_per_capita FLOAT,
                who_compliance FLOAT,
                required_green_space FLOAT,
                recommended_parks INT,
                recommended_trees INT,
                co2_reduction_potential FLOAT,
                score_components TEXT,
                sustainability_debt TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
            )
        ''')
        
        # Simulations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_id INT NOT NULL,
                simulation_type VARCHAR(100),
                parameters TEXT,
                results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
            )
        ''')
        
        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_id INT NOT NULL,
                category VARCHAR(100),
                priority VARCHAR(50),
                title VARCHAR(255),
                description TEXT,
                impact_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        print("[OK] Database tables initialized successfully")
        cursor.close()
        conn.close()
    
    # City operations
    def add_city(self, city_data: Dict) -> int:
        conn = self.get_connection()
        if not conn:
            return 0
        
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO cities 
                (name, area, population, population_density, built_up_percentage,
                 green_space_area, open_land_area, green_coverage_percentage,
                 existing_parks, tree_coverage, aqi, pm25, pm10, co2_estimation,
                 traffic_density, vehicle_count, public_transport_usage,
                 latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                area=%s, population=%s, population_density=%s, built_up_percentage=%s,
                green_space_area=%s, open_land_area=%s, green_coverage_percentage=%s,
                existing_parks=%s, tree_coverage=%s, aqi=%s, pm25=%s, pm10=%s,
                co2_estimation=%s, traffic_density=%s, vehicle_count=%s,
                public_transport_usage=%s, latitude=%s, longitude=%s
            ''', (
                city_data.get('name'),
                city_data.get('area'),
                city_data.get('population'),
                city_data.get('population_density'),
                city_data.get('built_up_percentage'),
                city_data.get('green_space_area'),
                city_data.get('open_land_area', 0),
                city_data.get('green_coverage_percentage'),
                city_data.get('existing_parks', 0),
                city_data.get('tree_coverage', 0),
                city_data.get('aqi', 0),
                city_data.get('pm25', 0),
                city_data.get('pm10', 0),
                city_data.get('co2_estimation', 0),
                city_data.get('traffic_density'),
                city_data.get('vehicle_count', 0),
                city_data.get('public_transport_usage', 0),
                city_data.get('latitude'),
                city_data.get('longitude'),
                # For UPDATE
                city_data.get('area'),
                city_data.get('population'),
                city_data.get('population_density'),
                city_data.get('built_up_percentage'),
                city_data.get('green_space_area'),
                city_data.get('open_land_area', 0),
                city_data.get('green_coverage_percentage'),
                city_data.get('existing_parks', 0),
                city_data.get('tree_coverage', 0),
                city_data.get('aqi', 0),
                city_data.get('pm25', 0),
                city_data.get('pm10', 0),
                city_data.get('co2_estimation', 0),
                city_data.get('traffic_density'),
                city_data.get('vehicle_count', 0),
                city_data.get('public_transport_usage', 0),
                city_data.get('latitude'),
                city_data.get('longitude')
            ))
            
            city_id = cursor.lastrowid
            conn.commit()
            return city_id
        except Error as e:
            print(f"Error adding city: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()
    
    def get_city(self, city_name: str) -> Optional[Dict]:
        conn = self.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM cities WHERE name = %s', (city_name,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    
    def get_all_cities(self) -> List[Dict]:
        conn = self.get_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM cities ORDER BY created_at DESC')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    
    def delete_city(self, city_name: str):
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cities WHERE name = %s', (city_name,))
        conn.commit()
        cursor.close()
        conn.close()
    
    def update_city_coordinates(self, city_name: str, latitude: float, longitude: float):
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute('UPDATE cities SET latitude = %s, longitude = %s WHERE name = %s', 
                      (latitude, longitude, city_name))
        conn.commit()
        cursor.close()
        conn.close()
        conn.close()
    
    # Analysis operations
    def save_analysis(self, city_id: int, analysis_data: Dict):
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO analysis_results
                (city_id, sustainability_score, category, badge_level,
                 green_space_per_capita, who_compliance, required_green_space,
                 recommended_parks, recommended_trees, co2_reduction_potential,
                 score_components, sustainability_debt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                city_id,
                analysis_data.get('sustainability_score'),
                analysis_data.get('category'),
                analysis_data.get('badge_level'),
                analysis_data.get('green_space_per_capita'),
                analysis_data.get('who_standard_compliance'),
                analysis_data.get('required_green_space'),
                analysis_data.get('recommended_parks'),
                analysis_data.get('recommended_trees'),
                analysis_data.get('co2_reduction_potential'),
                json.dumps(analysis_data.get('score_explanation', {})),
                json.dumps(analysis_data.get('sustainability_debt', {}))
            ))
            conn.commit()
        except Error as e:
            print(f"Error saving analysis: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def get_latest_analysis(self, city_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM analysis_results 
            WHERE city_id = %s 
            ORDER BY analyzed_at DESC 
            LIMIT 1
        ''', (city_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            # Map database fields to SustainabilityMetrics fields
            return {
                'green_space_per_capita': row.get('green_space_per_capita', 0),
                'who_standard_compliance': row.get('who_compliance', 0),
                'sustainability_score': row.get('sustainability_score', 0),
                'category': row.get('category', ''),
                'badge_level': row.get('badge_level', ''),
                'required_green_space': row.get('required_green_space', 0),
                'recommended_parks': row.get('recommended_parks', 0),
                'recommended_trees': row.get('recommended_trees', 0),
                'co2_reduction_potential': row.get('co2_reduction_potential', 0),
                'sustainability_debt': json.loads(row['sustainability_debt']) if row.get('sustainability_debt') else {},
                'score_explanation': json.loads(row['score_components']) if row.get('score_components') else {}
            }
        return None
    
    # Simulation operations
    def save_simulation(self, city_id: int, sim_type: str, parameters: Dict, results: Dict):
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO simulations (city_id, simulation_type, parameters, results)
                VALUES (%s, %s, %s, %s)
            ''', (city_id, sim_type, json.dumps(parameters), json.dumps(results)))
            conn.commit()
        except Error as e:
            print(f"Error saving simulation: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def get_city_simulations(self, city_id: int) -> List[Dict]:
        conn = self.get_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM simulations 
            WHERE city_id = %s 
            ORDER BY created_at DESC
        ''', (city_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for row in rows:
            row['parameters'] = json.loads(row['parameters']) if row['parameters'] else {}
            row['results'] = json.loads(row['results']) if row['results'] else {}
        return rows
    
    # Recommendation operations
    def save_recommendations(self, city_id: int, recommendations: List):
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM recommendations WHERE city_id = %s', (city_id,))
            
            for rec in recommendations:
                if isinstance(rec, dict):
                    cursor.execute('''
                        INSERT INTO recommendations
                        (city_id, category, priority, title, description, impact_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (
                        city_id,
                        rec.get('category', ''),
                        rec.get('priority', ''),
                        rec.get('title', ''),
                        rec.get('description', ''),
                        rec.get('impact_score', 0)
                    ))
                else:
                    cursor.execute('''
                        INSERT INTO recommendations
                        (city_id, category, priority, title, description, impact_score)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (city_id, 'General', 'Medium', 'Recommendation', str(rec), 5.0))
            conn.commit()
        except Error as e:
            print(f"Error saving recommendations: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def get_city_recommendations(self, city_id: int) -> List[Dict]:
        conn = self.get_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM recommendations 
            WHERE city_id = %s 
            ORDER BY impact_score DESC
        ''', (city_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
