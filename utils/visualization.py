import plotly.graph_objects as go
import plotly.express as px
import folium
from folium import plugins
import pandas as pd
from typing import Dict, List
from backend.models import CityData, SustainabilityMetrics

class ChartGenerator:
    def __init__(self):
        self.colors = {
            'Poor': '#FF6B6B',
            'Moderate': '#FFE66D',
            'Sustainable': '#4ECDC4'
        }
    
    def create_sustainability_gauge(self, score: float, category: str) -> str:
        """Create a gauge chart for sustainability score"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Sustainability Score"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': self.colors.get(category, '#4ECDC4')},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 70], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_comparison_chart(self, cities_data: List[Dict]) -> str:
        """Create comparison chart for multiple cities"""
        df = pd.DataFrame(cities_data)
        
        fig = px.bar(
            df, 
            x='name', 
            y='sustainability_score',
            color='category',
            color_discrete_map=self.colors,
            title="City Sustainability Comparison"
        )
        
        fig.update_layout(
            xaxis_title="Cities",
            yaxis_title="Sustainability Score",
            height=400
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_metrics_radar(self, metrics: Dict) -> str:
        """Create radar chart for city metrics"""
        categories = ['Green Coverage', 'Air Quality', 'Traffic', 'Land Use', 'Transport']
        values = [
            metrics.get('green_score', 0),
            metrics.get('air_quality_score', 0),
            metrics.get('traffic_score', 0),
            metrics.get('land_use_score', 0),
            metrics.get('transport_score', 0)
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current Metrics'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="City Performance Metrics",
            height=400
        )
        
        return fig.to_html(include_plotlyjs='cdn')

class MapGenerator:
    def __init__(self):
        self.default_location = [20.5937, 78.9629]  # India center
    
    def create_city_map(self, city: CityData, metrics: SustainabilityMetrics) -> str:
        """Create an interactive map for a city"""
        if city.latitude and city.longitude:
            center = [city.latitude, city.longitude]
            print(f"Creating map for {city.name} at {center}")
        else:
            center = self.default_location
            print(f"No coordinates for {city.name}, using default location")
        
        m = folium.Map(location=center, zoom_start=12 if city.latitude else 5)
        
        # Add city marker with detailed popup
        color = self._get_marker_color(metrics.category)
        popup_html = f"""
        <div style="width: 250px;">
            <h4><b>{city.name}</b></h4>
            <hr>
            <p><b>Population:</b> {city.population:,}</p>
            <p><b>Area:</b> {city.area} sq km</p>
            <p><b>Sustainability Score:</b> <span style="color: {self._get_color_code(metrics.category)};"><b>{metrics.sustainability_score}</b></span></p>
            <p><b>Category:</b> <span style="color: {self._get_color_code(metrics.category)};"><b>{metrics.category}</b></span></p>
            <p><b>Green Space per Capita:</b> {metrics.green_space_per_capita:.1f} m²</p>
            <p><b>WHO Compliance:</b> {metrics.who_standard_compliance:.1f}%</p>
            <p><b>AQI:</b> {city.aqi}</p>
            <p><b>Traffic:</b> {city.traffic_density}</p>
            {f'<p><b>Coordinates:</b> {city.latitude:.4f}, {city.longitude:.4f}</p>' if city.latitude else ''}
        </div>
        """
        
        folium.Marker(
            center,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{city.name} - {metrics.category}",
            icon=folium.Icon(color=color, icon='leaf', prefix='fa')
        ).add_to(m)
        
        # Add pollution heatmap if coordinates available
        if city.latitude and city.longitude:
            self._add_pollution_heatmap(m, city)
        
        return m._repr_html_()
    
    def create_multi_city_map(self, cities_data: List[Dict]) -> str:
        """Create map with multiple cities"""
        m = folium.Map(location=self.default_location, zoom_start=5)
        
        for city_data in cities_data:
            if city_data.get('latitude') and city_data.get('longitude'):
                color = self._get_marker_color(city_data.get('category', 'Moderate'))
                
                folium.Marker(
                    [city_data['latitude'], city_data['longitude']],
                    popup=f"""
                    <b>{city_data['name']}</b><br>
                    Sustainability Score: {city_data.get('sustainability_score', 0)}<br>
                    Category: {city_data.get('category', 'Unknown')}
                    """,
                    icon=folium.Icon(color=color, icon='info-sign')
                ).add_to(m)
        
        return m._repr_html_()
    
    def _get_marker_color(self, category: str) -> str:
        """Get marker color based on sustainability category"""
        color_map = {
            'Poor': 'red',
            'Moderate': 'orange',
            'Sustainable': 'green'
        }
        return color_map.get(category, 'blue')
    
    def _get_color_code(self, category: str) -> str:
        """Get color code for category"""
        color_map = {
            'Poor': '#dc3545',
            'Moderate': '#ffc107', 
            'Sustainable': '#28a745'
        }
        return color_map.get(category, '#6c757d')
    
    def _add_pollution_heatmap(self, map_obj: folium.Map, city: CityData):
        """Add pollution heatmap layer"""
        # Simulate pollution hotspots around the city
        heat_data = []
        base_lat, base_lon = city.latitude, city.longitude
        
        # Create sample pollution points
        for i in range(10):
            lat_offset = (i - 5) * 0.01
            lon_offset = (i - 5) * 0.01
            intensity = city.aqi / 200  # Normalize AQI
            heat_data.append([base_lat + lat_offset, base_lon + lon_offset, intensity])
        
        plugins.HeatMap(heat_data).add_to(map_obj)