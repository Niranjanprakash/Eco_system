"""
MySQL Database Management Utility for EcoPlan
Run this script to view, backup, or manage the database
"""

from backend.database import Database
import json

def view_all_cities():
    db = Database()
    cities = db.get_all_cities()
    print(f"\n{'='*70}")
    print(f"Total Cities: {len(cities)}")
    print(f"{'='*70}\n")
    
    for city in cities:
        print(f"ID: {city['id']} | Name: {city['name']} | Population: {city['population']:,}")
        print(f"   Area: {city['area']} sq km | Green Space: {city['green_space_area']} sq km")
        print(f"   Added: {city['created_at']}")
        print("-" * 70)

def view_city_details(city_name):
    db = Database()
    city = db.get_city(city_name)
    
    if not city:
        print(f"City '{city_name}' not found!")
        return
    
    print(f"\n{'='*70}")
    print(f"City Details: {city['name']}")
    print(f"{'='*70}\n")
    
    for key, value in city.items():
        if key not in ['created_at', 'updated_at']:
            print(f"{key}: {value}")
    
    # Get analysis
    analysis = db.get_latest_analysis(city['id'])
    if analysis:
        print(f"\n{'='*70}")
        print("Latest Analysis")
        print(f"{'='*70}\n")
        print(f"Sustainability Score: {analysis['sustainability_score']}")
        print(f"Category: {analysis['category']}")
        print(f"Badge: {analysis['badge_level']}")
        print(f"Green Space per Capita: {analysis['green_space_per_capita']:.2f} m²")
        print(f"WHO Compliance: {analysis.get('who_compliance', 0):.1f}%")
    
    # Get recommendations
    recommendations = db.get_city_recommendations(city['id'])
    if recommendations:
        print(f"\n{'='*70}")
        print(f"Recommendations ({len(recommendations)})")
        print(f"{'='*70}\n")
        for rec in recommendations[:5]:
            print(f"- [{rec['priority']}] {rec['title']}")

def delete_city(city_name):
    db = Database()
    confirm = input(f"Are you sure you want to delete '{city_name}'? (yes/no): ")
    if confirm.lower() == 'yes':
        db.delete_city(city_name)
        print(f"City '{city_name}' deleted successfully!")
    else:
        print("Deletion cancelled.")

def clear_all_data():
    db = Database()
    confirm = input("Are you sure you want to clear ALL data? (yes/no): ")
    if confirm.lower() == 'yes':
        cities = db.get_all_cities()
        for city in cities:
            db.delete_city(city['name'])
        print("All data cleared successfully!")
    else:
        print("Operation cancelled.")

def database_stats():
    db = Database()
    cities = db.get_all_cities()
    
    print(f"\n{'='*70}")
    print("Database Statistics")
    print(f"{'='*70}\n")
    print(f"Total Cities: {len(cities)}")
    
    total_pop = sum(city['population'] for city in cities)
    total_area = sum(city['area'] for city in cities)
    
    print(f"Total Population: {total_pop:,}")
    print(f"Total Area: {total_area:.2f} sq km")
    
    if cities:
        avg_score = 0
        analyzed = 0
        for city in cities:
            analysis = db.get_latest_analysis(city['id'])
            if analysis:
                avg_score += analysis['sustainability_score']
                analyzed += 1
        
        if analyzed > 0:
            print(f"Cities Analyzed: {analyzed}")
            print(f"Average Sustainability Score: {avg_score/analyzed:.2f}")

def main():
    print("\n" + "="*70)
    print("EcoPlan MySQL Database Management")
    print("="*70)
    print("\n1. View all cities")
    print("2. View city details")
    print("3. Database statistics")
    print("4. Delete a city")
    print("5. Clear all data")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ")
    
    if choice == '1':
        view_all_cities()
    elif choice == '2':
        city_name = input("Enter city name: ")
        view_city_details(city_name)
    elif choice == '3':
        database_stats()
    elif choice == '4':
        city_name = input("Enter city name to delete: ")
        delete_city(city_name)
    elif choice == '5':
        clear_all_data()
    elif choice == '6':
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")
    
    input("\nPress Enter to continue...")
    main()

if __name__ == '__main__':
    main()
