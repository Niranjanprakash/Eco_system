-- EcoPlan MySQL Database Setup Script
-- Database: Eco_system_db
-- Password: Pvbn@7738

-- Create database (run this first if database doesn't exist)
CREATE DATABASE IF NOT EXISTS Eco_system_db;
USE Eco_system_db;

-- Cities table
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Analysis results table
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
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
    INDEX idx_city (city_id),
    INDEX idx_analyzed (analyzed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Simulations table
CREATE TABLE IF NOT EXISTS simulations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    simulation_type VARCHAR(100),
    parameters TEXT,
    results TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
    INDEX idx_city (city_id),
    INDEX idx_type (simulation_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    category VARCHAR(100),
    priority VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    impact_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
    INDEX idx_city (city_id),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample queries for verification
-- SELECT COUNT(*) as total_cities FROM cities;
-- SELECT * FROM cities ORDER BY created_at DESC LIMIT 10;
-- SELECT c.name, a.sustainability_score FROM cities c LEFT JOIN analysis_results a ON c.id = a.city_id;
