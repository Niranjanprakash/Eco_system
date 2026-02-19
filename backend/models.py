import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class CityData:
    name: str
    area: float  # sq km
    population: int
    population_density: float
    built_up_percentage: float
    green_space_area: float
    open_land_area: float
    green_coverage_percentage: float
    existing_parks: int
    tree_coverage: float
    aqi: float
    pm25: float
    pm10: float
    co2_estimation: float
    traffic_density: str  # Low/Medium/High
    vehicle_count: int
    public_transport_usage: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@dataclass
class SustainabilityMetrics:
    green_space_per_capita: float
    who_standard_compliance: float
    sustainability_score: float
    category: str  # Poor/Moderate/Sustainable
    badge_level: str  # Enhanced badge classification
    required_green_space: float
    recommended_parks: int
    recommended_trees: int
    co2_reduction_potential: float
    sustainability_debt: Dict[str, float]  # Debt breakdown
    score_explanation: Dict[str, Dict]  # Score breakdown with explanations

@dataclass
class SustainabilityDebt:
    total_debt: float
    green_space_debt: float
    air_quality_debt: float
    traffic_debt: float
    land_use_debt: float
    transport_debt: float

class CityAnalyzer:
    WHO_GREEN_STANDARD = 9  # sq meters per capita
    SAFE_AQI_THRESHOLD = 50  # Good air quality
    OPTIMAL_GREEN_COVERAGE = 40  # Optimal green coverage percentage
    MAX_ACCEPTABLE_DENSITY = 10000  # people per sq km
    
    def __init__(self):
        self.traffic_multipliers = {"Low": 1.0, "Medium": 1.5, "High": 2.0}
        # Enhanced thresholds for better differentiation
        self.sustainability_thresholds = {
            'excellent': 80,  # Top tier cities
            'good': 65,       # Well-performing cities
            'moderate': 45,   # Average cities
            'poor': 25        # Cities needing urgent attention
        }
        
    def calculate_green_space_per_capita(self, city: CityData) -> float:
        return (city.green_space_area * 1000000) / city.population  # Convert to sq meters
    
    def assess_who_compliance(self, green_per_capita: float) -> float:
        return min(100, (green_per_capita / self.WHO_GREEN_STANDARD) * 100)
    
    def calculate_sustainability_score(self, city: CityData) -> Tuple[float, Dict[str, Dict]]:
        # Enhanced scoring with better differentiation
        components = {}
        
        # Green coverage (30%) - Enhanced scoring
        green_per_capita = self.calculate_green_space_per_capita(city)
        green_ratio = green_per_capita / self.WHO_GREEN_STANDARD
        if green_ratio >= 1.5:  # Excellent
            green_score = 100
        elif green_ratio >= 1.0:  # Good
            green_score = 80 + (green_ratio - 1.0) * 40
        elif green_ratio >= 0.5:  # Moderate
            green_score = 40 + (green_ratio - 0.5) * 80
        else:  # Poor
            green_score = green_ratio * 80
        
        components['green_space'] = {
            'score': round(green_score, 1),
            'weight': 30,
            'value': green_per_capita,
            'standard': self.WHO_GREEN_STANDARD,
            'status': 'Excellent' if green_ratio >= 1.5 else 'Good' if green_ratio >= 1.0 else 'Moderate' if green_ratio >= 0.5 else 'Poor'
        }
        
        # Air quality (25%) - Enhanced with realistic thresholds
        if city.aqi <= 50:  # Good
            aqi_score = 100
        elif city.aqi <= 100:  # Moderate
            aqi_score = 80 - ((city.aqi - 50) * 0.6)
        elif city.aqi <= 150:  # Unhealthy for sensitive
            aqi_score = 50 - ((city.aqi - 100) * 0.4)
        elif city.aqi <= 200:  # Unhealthy
            aqi_score = 30 - ((city.aqi - 150) * 0.3)
        else:  # Very unhealthy
            aqi_score = max(0, 15 - ((city.aqi - 200) * 0.1))
        
        components['air_quality'] = {
            'score': round(aqi_score, 1),
            'weight': 25,
            'value': city.aqi,
            'standard': self.SAFE_AQI_THRESHOLD,
            'status': 'Good' if city.aqi <= 50 else 'Moderate' if city.aqi <= 100 else 'Unhealthy' if city.aqi <= 150 else 'Very Unhealthy'
        }
        
        # Traffic impact (20%) - Enhanced differentiation
        traffic_multiplier = self.traffic_multipliers.get(city.traffic_density, 1.5)
        density_factor = min(2.0, city.population_density / self.MAX_ACCEPTABLE_DENSITY)
        traffic_score = max(0, 100 - (traffic_multiplier * 25) - (density_factor * 15))
        
        components['traffic'] = {
            'score': round(traffic_score, 1),
            'weight': 20,
            'value': city.traffic_density,
            'density_factor': round(density_factor, 2),
            'status': 'Low Impact' if traffic_score >= 80 else 'Moderate Impact' if traffic_score >= 60 else 'High Impact'
        }
        
        # Land utilization (15%) - Enhanced with optimal targets
        if city.built_up_percentage <= 60:  # Good balance
            land_score = 100 - (city.built_up_percentage * 0.5)
        elif city.built_up_percentage <= 80:  # Moderate density
            land_score = 70 - ((city.built_up_percentage - 60) * 1.5)
        else:  # High density
            land_score = max(0, 40 - ((city.built_up_percentage - 80) * 2))
        
        components['land_use'] = {
            'score': round(land_score, 1),
            'weight': 15,
            'value': city.built_up_percentage,
            'status': 'Optimal' if city.built_up_percentage <= 60 else 'Dense' if city.built_up_percentage <= 80 else 'Over-developed'
        }
        
        # Public transport (10%) - Enhanced scoring
        if city.public_transport_usage >= 50:  # Excellent
            transport_score = 100
        elif city.public_transport_usage >= 30:  # Good
            transport_score = 80 + ((city.public_transport_usage - 30) * 1.0)
        elif city.public_transport_usage >= 15:  # Moderate
            transport_score = 50 + ((city.public_transport_usage - 15) * 2.0)
        else:  # Poor
            transport_score = city.public_transport_usage * 3.33
        
        components['transport'] = {
            'score': round(transport_score, 1),
            'weight': 10,
            'value': city.public_transport_usage,
            'status': 'Excellent' if city.public_transport_usage >= 50 else 'Good' if city.public_transport_usage >= 30 else 'Moderate' if city.public_transport_usage >= 15 else 'Poor'
        }
        
        # Calculate weighted total
        total_score = (
            components['green_space']['score'] * 0.30 +
            components['air_quality']['score'] * 0.25 +
            components['traffic']['score'] * 0.20 +
            components['land_use']['score'] * 0.15 +
            components['transport']['score'] * 0.10
        )
        
        return round(total_score, 2), components
    
    def categorize_sustainability(self, score: float) -> Tuple[str, str]:
        """Enhanced categorization with badge system"""
        if score >= self.sustainability_thresholds['excellent']:
            return "Sustainable", "🏆 Excellent"
        elif score >= self.sustainability_thresholds['good']:
            return "Sustainable", "🌟 Good"
        elif score >= self.sustainability_thresholds['moderate']:
            return "Moderate", "⚠️ Moderate"
        elif score >= self.sustainability_thresholds['poor']:
            return "Poor", "🚨 Poor"
        else:
            return "Poor", "❌ Critical"
    
    def calculate_sustainability_debt(self, city: CityData, components: Dict[str, Dict]) -> Dict[str, float]:
        """Calculate sustainability debt across different dimensions"""
        debt = {}
        
        # Green space debt (deficit from WHO standard)
        green_per_capita = self.calculate_green_space_per_capita(city)
        green_deficit = max(0, self.WHO_GREEN_STANDARD - green_per_capita)
        debt['green_space_debt'] = round((green_deficit * city.population) / 1000000, 2)  # sq km
        
        # Air quality debt (excess pollution)
        aqi_excess = max(0, city.aqi - self.SAFE_AQI_THRESHOLD)
        debt['air_quality_debt'] = round(aqi_excess / self.SAFE_AQI_THRESHOLD * 100, 1)  # percentage over safe limit
        
        # Traffic debt (congestion impact)
        traffic_impact = self.traffic_multipliers.get(city.traffic_density, 1.5)
        density_pressure = city.population_density / self.MAX_ACCEPTABLE_DENSITY
        debt['traffic_debt'] = round(max(0, (traffic_impact - 1.0) * 50 + (density_pressure - 1.0) * 30), 1)
        
        # Land use debt (over-development)
        optimal_built_up = 60  # Optimal built-up percentage
        land_excess = max(0, city.built_up_percentage - optimal_built_up)
        debt['land_use_debt'] = round(land_excess, 1)
        
        # Transport debt (lack of public transport)
        optimal_transport = 40  # Optimal public transport usage
        transport_deficit = max(0, optimal_transport - city.public_transport_usage)
        debt['transport_debt'] = round(transport_deficit, 1)
        
        # Total debt (weighted sum)
        debt['total_debt'] = round(
            debt['green_space_debt'] * 0.3 +
            debt['air_quality_debt'] * 0.25 +
            debt['traffic_debt'] * 0.2 +
            debt['land_use_debt'] * 0.15 +
            debt['transport_debt'] * 0.1, 2
        )
        
        return debt
    
    def calculate_required_green_space(self, city: CityData) -> float:
        current_per_capita = self.calculate_green_space_per_capita(city)
        if current_per_capita >= self.WHO_GREEN_STANDARD:
            return 0
        deficit = self.WHO_GREEN_STANDARD - current_per_capita
        return (deficit * city.population) / 1000000  # Convert to sq km
    
    def recommend_parks(self, required_area: float) -> int:
        if required_area <= 0:
            return 0
        avg_park_size = 0.05  # 5 hectares = 0.05 sq km
        return max(1, int(required_area / avg_park_size))
    
    def recommend_trees(self, city: CityData, required_area: float) -> int:
        if required_area <= 0:
            return max(100, int(city.population * 0.01))  # Minimum maintenance trees
        trees_per_hectare = 100
        return int(required_area * 100 * trees_per_hectare)  # Convert to hectares
    
    def estimate_co2_reduction(self, trees: int) -> float:
        co2_per_tree_per_year = 22  # kg
        return (trees * co2_per_tree_per_year) / 1000  # Convert to tons
    
    def analyze_city(self, city: CityData) -> SustainabilityMetrics:
        green_per_capita = self.calculate_green_space_per_capita(city)
        who_compliance = self.assess_who_compliance(green_per_capita)
        sustainability_score, score_components = self.calculate_sustainability_score(city)
        category, badge_level = self.categorize_sustainability(sustainability_score)
        sustainability_debt = self.calculate_sustainability_debt(city, score_components)
        required_green = self.calculate_required_green_space(city)
        recommended_parks = self.recommend_parks(required_green)
        recommended_trees = self.recommend_trees(city, required_green)
        co2_reduction = self.estimate_co2_reduction(recommended_trees)
        
        return SustainabilityMetrics(
            green_space_per_capita=green_per_capita,
            who_standard_compliance=who_compliance,
            sustainability_score=sustainability_score,
            category=category,
            badge_level=badge_level,
            required_green_space=required_green,
            recommended_parks=recommended_parks,
            recommended_trees=recommended_trees,
            co2_reduction_potential=co2_reduction,
            sustainability_debt=sustainability_debt,
            score_explanation=score_components
        )

class RecommendationEngine:
    def __init__(self):
        self.analyzer = CityAnalyzer()
    
    def generate_recommendations(self, city: CityData, metrics: SustainabilityMetrics) -> Dict:
        recommendations = {
            "immediate_actions": [],
            "short_term": [],
            "long_term": [],
            "zone_specific": {}
        }
        
        # Immediate actions
        if metrics.sustainability_score < 40:
            recommendations["immediate_actions"].extend([
                "Implement emergency tree plantation drive",
                "Create temporary green spaces in vacant lots",
                "Introduce car-free days to reduce pollution"
            ])
        
        # Short-term (1-2 years)
        if metrics.required_green_space > 0:
            recommendations["short_term"].extend([
                f"Develop {metrics.recommended_parks} new parks",
                f"Plant {metrics.recommended_trees:,} trees",
                "Convert rooftops to green spaces",
                "Create urban gardens in residential areas"
            ])
        
        if city.aqi > 100:
            recommendations["short_term"].append("Implement strict vehicle emission controls")
        
        # Long-term (3-5 years)
        recommendations["long_term"].extend([
            "Develop urban forest corridors",
            "Implement smart traffic management",
            "Expand public transportation network",
            "Create green building incentives"
        ])
        
        # Zone-specific recommendations
        if city.traffic_density == "High":
            recommendations["zone_specific"]["traffic_zones"] = [
                "Install air purifying plants along highways",
                "Create buffer green zones around industrial areas"
            ]
        
        return recommendations