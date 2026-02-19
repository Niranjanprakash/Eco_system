# EcoPlan: AI-Based Urban Green Space & Sustainability Planning Assistant

![EcoPlan Logo](https://img.shields.io/badge/EcoPlan-Sustainable%20Cities-green?style=for-the-badge&logo=leaf)

## 🌍 Project Overview

EcoPlan is a lightweight, data-driven AI system that analyzes urban data and provides actionable recommendations to improve green spaces, environmental quality, and overall sustainability. Designed for small towns, academic projects, and low-resource environments.

### 🎯 Key Features

- **City & Zone Analysis**: Geocode cities and analyze zones (Residential, Industrial, Commercial)
- **Green Space Assessment**: Calculate green space per capita and WHO compliance
- **AI Recommendation Engine**: Smart suggestions for urban planning improvements
- **What-If Simulations**: Test different scenarios and their impact
- **Interactive Dashboard**: Maps, charts, and visual analytics
- **Multi-City Comparison**: Benchmark cities against each other
- **Export & Reporting**: PDF, CSV, and JSON export capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- 8GB RAM (no GPU required)
- Internet connection for API services

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd eco-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Keys** (Optional but recommended)
```bash
# Edit .env file
GEOAPIFY_API_KEY=your_geoapify_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

## 📊 Data Requirements

### Input Data Format

Your CSV/Excel file should contain these columns:

#### Basic City Data
- `name` - City/Town name
- `area` - Total area (sq km)
- `population` - Population count
- `population_density` - People per sq km
- `built_up_percentage` - Built-up area percentage

#### Green & Environmental Data
- `green_space_area` - Green space area (sq km)
- `open_land_area` - Open/unused land (sq km)
- `green_coverage_percentage` - Green coverage %
- `existing_parks` - Number of parks
- `tree_coverage` - Tree coverage %

#### Pollution Data
- `aqi` - Air Quality Index
- `pm25` - PM2.5 levels (μg/m³)
- `pm10` - PM10 levels (μg/m³)
- `co2_estimation` - CO₂ estimation (tons/year)

#### Traffic & Transport Data
- `traffic_density` - Low/Medium/High
- `vehicle_count` - Vehicle count estimation
- `public_transport_usage` - Public transport usage %

### Sample Data

The system includes sample data from Indian cities (Mumbai, Pune, Nashik, Nagpur) for demonstration.

## 🏗️ System Architecture

```
eco-system/
├── app.py                 # Main Flask application
├── backend/
│   └── models.py         # Data models and analysis logic
├── utils/
│   ├── api_integration.py # External API handlers
│   ├── data_processor.py  # Data processing utilities
│   └── visualization.py   # Chart and map generation
├── templates/            # HTML templates
├── static/              # CSS, JS, images
├── data/                # Data storage
└── requirements.txt     # Dependencies
```

## 🔧 Core Components

### 1. City Analyzer
- Calculates sustainability scores (0-100)
- Assesses WHO green space compliance
- Categorizes cities (Poor/Moderate/Sustainable)

### 2. Recommendation Engine
- Rule-based AI recommendations
- Short-term and long-term action plans
- Zone-specific suggestions

### 3. What-If Simulator
- Green space increase scenarios
- Tree plantation impact
- Traffic reduction effects

### 4. Visualization Engine
- Interactive maps with Folium
- Charts with Plotly
- Sustainability gauges and comparisons

## 📈 Sustainability Scoring

The system calculates a comprehensive sustainability score based on:

- **Green Coverage (30%)** - Parks, trees, green spaces
- **Air Quality (25%)** - AQI, PM2.5, PM10 levels
- **Traffic Impact (20%)** - Vehicle density, congestion
- **Land Utilization (15%)** - Built-up vs available space
- **Public Transport (10%)** - Usage and accessibility

### Score Categories
- **70-100**: Sustainable ✅
- **40-69**: Moderate ⚠️
- **0-39**: Poor ❌

## 🌐 API Integration

### Geoapify API
- Geocoding city coordinates
- Location-based services

### OpenWeather API
- Real-time air pollution data
- Environmental monitoring

*Note: APIs are optional. The system works with manual data input.*

## 📱 User Interface

### Main Pages
1. **Home** - Project overview and navigation
2. **Upload Data** - CSV/Excel file upload
3. **Manual Input** - Form-based data entry
4. **Results** - Analysis results and recommendations
5. **Dashboard** - Interactive visualizations
6. **Simulation** - What-if scenario testing

## 🎯 Use Cases

### Academic Projects
- Urban planning research
- Environmental studies
- Sustainability assessments

### Municipal Planning
- City development strategies
- Green space optimization
- Policy decision support

### Smart City Initiatives
- SDG-11 compliance monitoring
- Environmental impact assessment
- Citizen engagement tools

## 🌱 Environmental Impact

### UN SDG-11 Alignment
EcoPlan directly supports **Sustainable Development Goal 11: Sustainable Cities and Communities** by:

- Promoting inclusive and sustainable urbanization
- Enhancing green and public spaces
- Supporting environmental planning
- Providing data-driven policy insights

### Key Metrics
- Green space per capita (WHO standard: 9m²)
- Air quality improvement potential
- CO₂ reduction through tree plantation
- Traffic impact on environment

## 🔬 Technical Specifications

### Technology Stack
- **Backend**: Flask (Python)
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Plotly, Folium
- **Frontend**: Bootstrap, JavaScript
- **APIs**: Geoapify, OpenWeather

### System Requirements
- **RAM**: 8GB minimum
- **Storage**: 1GB for application + data
- **Network**: Internet for API services
- **Browser**: Modern web browser

### Performance
- Handles 100+ cities simultaneously
- Real-time analysis and visualization
- Lightweight deployment (no GPU required)

## 📊 Sample Analysis Output

```
City: Mumbai
├── Sustainability Score: 42.3 (Moderate)
├── Green Space per Capita: 2.4 m² (WHO: 9 m²)
├── Recommendations:
│   ├── Add 73.2 sq km green space
│   ├── Plant 732,000 trees
│   ├── Create 15 new parks
│   └── Potential CO₂ reduction: 16,104 tons/year
└── Priority Actions:
    ├── Immediate: Emergency tree plantation
    ├── Short-term: Rooftop gardens, urban forests
    └── Long-term: Green corridors, smart transport
```

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment
- **Heroku**: Easy cloud deployment
- **AWS/Azure**: Scalable cloud hosting
- **Docker**: Containerized deployment
- **Local Server**: On-premise installation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- UN Sustainable Development Goals
- WHO Green Space Standards
- OpenStreetMap Community
- Environmental Planning Research

## 📞 Support

For support, email [your-email] or create an issue in the repository.

---

**EcoPlan** - *Building Sustainable Cities with AI* 🌱🏙️