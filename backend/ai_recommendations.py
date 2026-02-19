import numpy as np
from typing import Dict, List
from backend.models import CityData, SustainabilityMetrics

class AIRecommendationEngine:
    """AI-powered personalized recommendations for each city"""
    
    def __init__(self):
        self.priority_weights = {
            'critical': 1.0,
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
    
    def generate_personalized_plan(self, city: CityData, metrics: SustainabilityMetrics) -> Dict:
        """Generate AI-powered personalized action plan for each city"""
        
        # Analyze city's specific weaknesses
        weaknesses = self._identify_weaknesses(city, metrics)
        
        # Generate timeframe-based recommendations
        short_term = self._generate_short_term(city, weaknesses)
        mid_term = self._generate_mid_term(city, weaknesses)
        long_term = self._generate_long_term(city, weaknesses)
        
        return {
            'city_name': city.name,
            'overall_priority': self._calculate_priority(metrics.sustainability_score),
            'weaknesses': weaknesses,
            'short_term': short_term,  # 0-6 months
            'mid_term': mid_term,      # 6-24 months
            'long_term': long_term,    # 2-5 years
            'estimated_impact': self._estimate_impact(weaknesses),
            'budget_estimate': self._estimate_budget(city, weaknesses)
        }
    
    def _identify_weaknesses(self, city: CityData, metrics: SustainabilityMetrics) -> Dict:
        """AI identifies specific weaknesses for each city"""
        weaknesses = {}
        
        # Air Quality Analysis
        if city.aqi > 150:
            weaknesses['air_quality'] = {
                'severity': 'critical',
                'current_aqi': city.aqi,
                'target_aqi': 50,
                'gap': city.aqi - 50,
                'main_cause': 'High PM2.5 and PM10 levels' if city.pm25 > 60 else 'Traffic emissions'
            }
        elif city.aqi > 100:
            weaknesses['air_quality'] = {
                'severity': 'high',
                'current_aqi': city.aqi,
                'target_aqi': 50,
                'gap': city.aqi - 50
            }
        
        # Green Space Analysis
        if metrics.green_space_per_capita < 9:
            deficit = 9 - metrics.green_space_per_capita
            weaknesses['green_space'] = {
                'severity': 'critical' if deficit > 6 else 'high',
                'current': metrics.green_space_per_capita,
                'target': 9,
                'deficit_per_capita': deficit,
                'total_deficit_sqkm': (deficit * city.population) / 1000000
            }
        
        # Traffic Analysis
        if city.traffic_density == 'High':
            weaknesses['traffic'] = {
                'severity': 'high',
                'current_density': city.traffic_density,
                'vehicle_count': city.vehicle_count,
                'public_transport_usage': city.public_transport_usage
            }
        
        # Urban Density Analysis
        if city.built_up_percentage > 70:
            weaknesses['urban_density'] = {
                'severity': 'medium',
                'built_up': city.built_up_percentage,
                'available_space': 100 - city.built_up_percentage
            }
        
        # Tree Coverage Analysis
        if city.tree_coverage < 15:
            weaknesses['tree_coverage'] = {
                'severity': 'medium',
                'current': city.tree_coverage,
                'target': 20,
                'gap': 20 - city.tree_coverage
            }
        
        return weaknesses
    
    def _generate_short_term(self, city: CityData, weaknesses: Dict) -> List[Dict]:
        """0-6 months: Quick wins and immediate actions"""
        actions = []
        
        if 'air_quality' in weaknesses:
            if weaknesses['air_quality']['severity'] == 'critical':
                actions.append({
                    'action': 'Emergency Air Quality Response',
                    'description': f'Implement odd-even vehicle scheme in {city.name}',
                    'timeline': '1-2 months',
                    'cost': 'Low',
                    'impact': 'High',
                    'specific_to': f'{city.name} has AQI of {city.aqi}',
                    'steps': [
                        'Deploy air quality monitoring stations',
                        'Restrict heavy vehicle entry during peak hours',
                        'Increase public transport frequency by 30%',
                        'Launch awareness campaigns'
                    ]
                })
            
            actions.append({
                'action': 'Anti-Dust Campaign',
                'description': f'Control construction dust in {city.name}',
                'timeline': '2-3 months',
                'cost': 'Low',
                'impact': 'Medium',
                'specific_to': f'PM10 levels at {city.pm10} in {city.name}',
                'steps': [
                    'Mandate dust covers at construction sites',
                    'Water spraying on major roads',
                    'Fine violators'
                ]
            })
        
        if 'green_space' in weaknesses:
            actions.append({
                'action': 'Rapid Greening Initiative',
                'description': f'Plant {int(city.population * 0.001)} trees in {city.name}',
                'timeline': '3-6 months',
                'cost': 'Medium',
                'impact': 'High',
                'specific_to': f'{city.name} needs {weaknesses["green_space"]["total_deficit_sqkm"]:.1f} sq km more green space',
                'steps': [
                    f'Identify {int(city.existing_parks * 0.5)} vacant plots',
                    'Community tree plantation drives',
                    'School/college campus greening',
                    'Roadside avenue plantation'
                ]
            })
        
        if 'traffic' in weaknesses:
            actions.append({
                'action': 'Smart Traffic Management',
                'description': f'Deploy AI traffic signals in {city.name}',
                'timeline': '4-6 months',
                'cost': 'Medium',
                'impact': 'Medium',
                'specific_to': f'{city.name} has {city.vehicle_count:,} vehicles',
                'steps': [
                    'Install smart traffic lights at 20 junctions',
                    'Real-time traffic monitoring',
                    'Optimize signal timing using AI'
                ]
            })
        
        return actions
    
    def _generate_mid_term(self, city: CityData, weaknesses: Dict) -> List[Dict]:
        """6-24 months: Structural improvements"""
        actions = []
        
        if 'green_space' in weaknesses:
            deficit = weaknesses['green_space']['total_deficit_sqkm']
            actions.append({
                'action': 'Urban Forest Development',
                'description': f'Create {int(deficit * 2)} new urban forests in {city.name}',
                'timeline': '12-18 months',
                'cost': 'High',
                'impact': 'Very High',
                'specific_to': f'{city.name} needs {deficit:.1f} sq km green space',
                'steps': [
                    f'Acquire {deficit:.1f} sq km land',
                    'Design mini-forests using Miyawaki method',
                    'Plant native species',
                    'Create walking trails and amenities',
                    'Involve local communities'
                ]
            })
            
            actions.append({
                'action': 'Rooftop Garden Program',
                'description': f'Convert {int(city.population * 0.0001)} rooftops to gardens',
                'timeline': '12-24 months',
                'cost': 'Medium',
                'impact': 'High',
                'specific_to': f'{city.name} has {city.built_up_percentage}% built-up area',
                'steps': [
                    'Subsidize rooftop garden kits',
                    'Train building owners',
                    'Tax incentives for green roofs',
                    'Showcase model projects'
                ]
            })
        
        if 'air_quality' in weaknesses:
            actions.append({
                'action': 'Clean Energy Transition',
                'description': f'Convert {city.name} public transport to electric',
                'timeline': '18-24 months',
                'cost': 'Very High',
                'impact': 'Very High',
                'specific_to': f'{city.name} AQI is {city.aqi}',
                'steps': [
                    'Procure 100 electric buses',
                    'Install charging infrastructure',
                    'Phase out old diesel buses',
                    'Promote electric auto-rickshaws'
                ]
            })
        
        if 'traffic' in weaknesses:
            actions.append({
                'action': 'Dedicated Bus Corridors',
                'description': f'Build {int(city.area * 0.5)} km bus rapid transit in {city.name}',
                'timeline': '18-24 months',
                'cost': 'Very High',
                'impact': 'High',
                'specific_to': f'{city.name} public transport usage only {city.public_transport_usage}%',
                'steps': [
                    'Identify key corridors',
                    'Design dedicated bus lanes',
                    'Construct stations',
                    'Integrate with existing transport'
                ]
            })
        
        return actions
    
    def _generate_long_term(self, city: CityData, weaknesses: Dict) -> List[Dict]:
        """2-5 years: Transformational changes"""
        actions = []
        
        actions.append({
            'action': 'Smart Sustainable City Vision 2030',
            'description': f'Transform {city.name} into a model sustainable city',
            'timeline': '3-5 years',
            'cost': 'Very High',
            'impact': 'Transformational',
            'specific_to': f'{city.name} current score: {int(city.population/1000)}',
            'steps': [
                'Develop comprehensive master plan',
                'Create green corridors connecting all parks',
                'Build circular economy infrastructure',
                'Achieve 50% renewable energy',
                'Zero-waste management system',
                'Smart city IoT integration'
            ]
        })
        
        if 'green_space' in weaknesses:
            actions.append({
                'action': 'Green Belt Development',
                'description': f'Create {int(city.area * 0.1)} sq km green belt around {city.name}',
                'timeline': '3-4 years',
                'cost': 'Very High',
                'impact': 'Very High',
                'specific_to': f'{city.name} needs major green infrastructure',
                'steps': [
                    'Acquire peripheral land',
                    'Plant 1 million trees',
                    'Create biodiversity zones',
                    'Build eco-tourism facilities',
                    'Establish research centers'
                ]
            })
        
        if 'air_quality' in weaknesses:
            actions.append({
                'action': 'Zero Emission Zone',
                'description': f'Make {city.name} city center emission-free',
                'timeline': '4-5 years',
                'cost': 'Very High',
                'impact': 'Transformational',
                'specific_to': f'{city.name} needs drastic air quality improvement',
                'steps': [
                    'Ban all fossil fuel vehicles in core area',
                    'Deploy electric shuttle services',
                    'Create pedestrian-only zones',
                    'Install air purification towers',
                    'Achieve WHO air quality standards'
                ]
            })
        
        actions.append({
            'action': 'Climate Resilient Infrastructure',
            'description': f'Future-proof {city.name} for climate change',
            'timeline': '3-5 years',
            'cost': 'Very High',
            'impact': 'Very High',
            'specific_to': f'{city.name} population {city.population:,} needs protection',
            'steps': [
                'Build flood management systems',
                'Create urban cooling infrastructure',
                'Develop water harvesting network',
                'Establish climate monitoring centers',
                'Train disaster response teams'
            ]
        })
        
        return actions
    
    def _calculate_priority(self, score: float) -> str:
        """Calculate overall priority based on score"""
        if score < 40:
            return 'CRITICAL - Immediate action required'
        elif score < 60:
            return 'HIGH - Urgent improvements needed'
        elif score < 75:
            return 'MEDIUM - Steady progress required'
        else:
            return 'LOW - Maintain and optimize'
    
    def _estimate_impact(self, weaknesses: Dict) -> Dict:
        """Estimate potential impact of addressing weaknesses"""
        total_impact = 0
        impacts = {}
        
        for weakness, data in weaknesses.items():
            severity = data.get('severity', 'low')
            impact = self.priority_weights.get(severity, 0.5) * 20
            impacts[weakness] = f'+{impact:.1f} points'
            total_impact += impact
        
        return {
            'by_category': impacts,
            'total_potential': f'+{total_impact:.1f} points',
            'target_score': f'Can reach {min(100, 50 + total_impact):.1f}'
        }
    
    def _estimate_budget(self, city: CityData, weaknesses: Dict) -> Dict:
        """Estimate budget requirements"""
        base_cost_per_capita = 500  # INR per person
        
        severity_multiplier = {
            'critical': 2.0,
            'high': 1.5,
            'medium': 1.0,
            'low': 0.5
        }
        
        total_multiplier = sum(severity_multiplier.get(w.get('severity', 'low'), 1.0) 
                              for w in weaknesses.values())
        
        total_budget = city.population * base_cost_per_capita * total_multiplier
        
        return {
            'short_term': f'₹{total_budget * 0.2 / 10000000:.1f} Cr',
            'mid_term': f'₹{total_budget * 0.5 / 10000000:.1f} Cr',
            'long_term': f'₹{total_budget * 0.3 / 10000000:.1f} Cr',
            'total_5_year': f'₹{total_budget / 10000000:.1f} Cr',
            'per_capita': f'₹{base_cost_per_capita * total_multiplier:.0f}'
        }
