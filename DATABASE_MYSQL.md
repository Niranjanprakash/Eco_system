# EcoPlan MySQL Database Documentation

## Database Configuration

**Database Name**: `Eco_system_db`  
**Username**: `root`  
**Password**: `Pvbn@7738`  
**Host**: `localhost`  
**Port**: `3306` (default)

## Setup Instructions

### 1. Install MySQL
If MySQL is not installed:
- Download from: https://dev.mysql.com/downloads/mysql/
- Or install via package manager

### 2. Create Database
Open MySQL command line or MySQL Workbench:

```sql
CREATE DATABASE Eco_system_db;
```

Or run the provided SQL script:
```bash
mysql -u root -p < database_setup.sql
```
Enter password: `Pvbn@7738`

### 3. Install Python MySQL Connector
```bash
pip install mysql-connector-python
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python app.py
```

The database tables will be created automatically on first run.

## Database Schema

### Tables Overview

#### 1. **cities** - Main city data
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| name | VARCHAR(255) | City name (unique) |
| area | FLOAT | Total area in sq km |
| population | INT | Population count |
| population_density | FLOAT | People per sq km |
| built_up_percentage | FLOAT | Built-up area % |
| green_space_area | FLOAT | Green space in sq km |
| open_land_area | FLOAT | Open land in sq km |
| green_coverage_percentage | FLOAT | Green coverage % |
| existing_parks | INT | Number of parks |
| tree_coverage | FLOAT | Tree coverage % |
| aqi | FLOAT | Air Quality Index |
| pm25 | FLOAT | PM2.5 levels |
| pm10 | FLOAT | PM10 levels |
| co2_estimation | FLOAT | CO2 estimation |
| traffic_density | VARCHAR(50) | Low/Medium/High |
| vehicle_count | INT | Vehicle count |
| public_transport_usage | FLOAT | Public transport % |
| latitude | FLOAT | Latitude coordinate |
| longitude | FLOAT | Longitude coordinate |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

#### 2. **analysis_results** - Sustainability analysis
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| city_id | INT | Foreign key to cities |
| sustainability_score | FLOAT | Overall score (0-100) |
| category | VARCHAR(100) | Poor/Moderate/Sustainable |
| badge_level | VARCHAR(100) | Badge classification |
| green_space_per_capita | FLOAT | Green space per person (m²) |
| who_compliance | FLOAT | WHO standard compliance % |
| required_green_space | FLOAT | Required green space |
| recommended_parks | INT | Recommended park count |
| recommended_trees | INT | Recommended tree count |
| co2_reduction_potential | FLOAT | CO2 reduction potential |
| score_components | TEXT | JSON - Score breakdown |
| sustainability_debt | TEXT | JSON - Debt breakdown |
| analyzed_at | TIMESTAMP | Analysis timestamp |

#### 3. **simulations** - What-if scenarios
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| city_id | INT | Foreign key to cities |
| simulation_type | VARCHAR(100) | Type of simulation |
| parameters | TEXT | JSON - Input parameters |
| results | TEXT | JSON - Simulation results |
| created_at | TIMESTAMP | Creation timestamp |

#### 4. **recommendations** - AI recommendations
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| city_id | INT | Foreign key to cities |
| category | VARCHAR(100) | Recommendation category |
| priority | VARCHAR(50) | Priority level |
| title | VARCHAR(255) | Recommendation title |
| description | TEXT | Detailed description |
| impact_score | FLOAT | Impact score |
| created_at | TIMESTAMP | Creation timestamp |

## Features

### Automatic Features
- **Auto-increment IDs**: Primary keys auto-generated
- **Timestamps**: Automatic creation and update tracking
- **Cascade Delete**: Deleting a city removes all related data
- **Unique Constraints**: Prevents duplicate city names
- **Indexes**: Optimized for fast queries

### Data Persistence
- All data stored permanently in MySQL
- Survives server restarts
- Shared across all users
- Transaction support for data integrity

## Usage

### Python API

```python
from backend.database import Database

db = Database()

# Add a city
city_data = {
    'name': 'Mumbai',
    'area': 603.4,
    'population': 12442373,
    'population_density': 20634,
    'built_up_percentage': 75.5,
    'green_space_area': 15.2,
    'green_coverage_percentage': 25.3,
    'traffic_density': 'High',
    # ... other fields
}
city_id = db.add_city(city_data)

# Get a city
city = db.get_city('Mumbai')

# Get all cities
cities = db.get_all_cities()

# Save analysis
analysis_data = {
    'sustainability_score': 65.5,
    'category': 'Moderate',
    'badge_level': 'Good',
    # ... other fields
}
db.save_analysis(city_id, analysis_data)

# Get latest analysis
analysis = db.get_latest_analysis(city_id)

# Save recommendations
recommendations = [
    {
        'category': 'Green Space',
        'priority': 'High',
        'title': 'Add more parks',
        'description': 'Create 10 new parks',
        'impact_score': 8.5
    }
]
db.save_recommendations(city_id, recommendations)

# Get recommendations
recs = db.get_city_recommendations(city_id)

# Delete a city
db.delete_city('Mumbai')
```

### Database Management Tool

Run the management utility:
```bash
python manage_db.py
```

**Options:**
1. View all cities
2. View city details (with analysis & recommendations)
3. Database statistics
4. Delete a city
5. Clear all data
6. Exit

### Direct MySQL Queries

```sql
-- View all cities
SELECT * FROM cities;

-- View cities with analysis
SELECT c.name, a.sustainability_score, a.category 
FROM cities c 
LEFT JOIN analysis_results a ON c.id = a.city_id
ORDER BY a.sustainability_score DESC;

-- View recommendations for a city
SELECT r.* FROM recommendations r
JOIN cities c ON r.city_id = c.id
WHERE c.name = 'Mumbai'
ORDER BY r.impact_score DESC;

-- Get city statistics
SELECT 
    COUNT(*) as total_cities,
    SUM(population) as total_population,
    AVG(sustainability_score) as avg_score
FROM cities c
LEFT JOIN analysis_results a ON c.id = a.city_id;
```

## Backup & Recovery

### Backup Database
```bash
mysqldump -u root -p Eco_system_db > backup.sql
```

### Restore Database
```bash
mysql -u root -p Eco_system_db < backup.sql
```

### Export Specific Table
```bash
mysqldump -u root -p Eco_system_db cities > cities_backup.sql
```

## Troubleshooting

### Connection Error
**Problem**: Can't connect to MySQL
**Solution**:
- Check MySQL service is running
- Verify credentials (root/Pvbn@7738)
- Check port 3306 is not blocked

### Database Not Found
**Problem**: Database 'Eco_system_db' doesn't exist
**Solution**:
```sql
CREATE DATABASE Eco_system_db;
```

### Permission Denied
**Problem**: Access denied for user 'root'
**Solution**:
- Verify password is correct
- Grant permissions:
```sql
GRANT ALL PRIVILEGES ON Eco_system_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Foreign Key Constraint Error
**Problem**: Cannot delete city with related data
**Solution**: This shouldn't happen (CASCADE DELETE enabled), but if it does:
```sql
SET FOREIGN_KEY_CHECKS=0;
DELETE FROM cities WHERE name = 'CityName';
SET FOREIGN_KEY_CHECKS=1;
```

## Performance Optimization

### Indexes
Already created on:
- `cities.name`
- `cities.created_at`
- `analysis_results.city_id`
- `simulations.city_id`
- `recommendations.city_id`

### Query Optimization Tips
- Use indexes for WHERE clauses
- Limit results with LIMIT
- Use JOIN instead of subqueries
- Cache frequently accessed data

## Security

### Best Practices
- ✅ Use environment variables for credentials
- ✅ Limit database user permissions
- ✅ Regular backups
- ✅ Use prepared statements (prevents SQL injection)
- ✅ Enable SSL for remote connections

### Production Recommendations
1. Create dedicated database user (not root)
2. Use strong password
3. Enable MySQL SSL
4. Regular security updates
5. Monitor database logs

## Migration from Session Storage

**Before**: In-memory session storage (data lost on restart)  
**After**: MySQL persistent storage (data survives restarts)

All existing functionality works the same, but now with:
- Permanent data storage
- Multi-user support
- Better performance
- Data integrity
- Backup capabilities

## Monitoring

### Check Database Size
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = 'Eco_system_db';
```

### Check Record Counts
```sql
SELECT 
    (SELECT COUNT(*) FROM cities) as cities,
    (SELECT COUNT(*) FROM analysis_results) as analyses,
    (SELECT COUNT(*) FROM simulations) as simulations,
    (SELECT COUNT(*) FROM recommendations) as recommendations;
```

## Support

For issues or questions:
1. Check this documentation
2. Run `python manage_db.py` for database inspection
3. Check MySQL error logs
4. Verify database connection settings
