import mysql.connector
from mysql.connector import Error

def test_connection():
    print("Testing MySQL Connection...")
    print("-" * 50)
    
    # Test 1: Connect without database
    try:
        print("\n1. Testing connection to MySQL server...")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pvbn@7738'
        )
        print("[OK] Connected to MySQL server successfully!")
        
        # Test 2: Check if database exists
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE 'Eco_system_db'")
        result = cursor.fetchone()
        
        if result:
            print("[OK] Database 'Eco_system_db' exists")
        else:
            print("[X] Database 'Eco_system_db' does NOT exist")
            print("\nCreating database...")
            cursor.execute("CREATE DATABASE Eco_system_db")
            print("[OK] Database 'Eco_system_db' created successfully!")
        
        cursor.close()
        conn.close()
        
        # Test 3: Connect to specific database
        print("\n2. Testing connection to Eco_system_db...")
        conn = mysql.connector.connect(
            host='localhost',
            database='Eco_system_db',
            user='root',
            password='Pvbn@7738'
        )
        print("[OK] Connected to Eco_system_db successfully!")
        conn.close()
        
        print("\n" + "=" * 50)
        print("All tests passed! Database is ready.")
        print("=" * 50)
        return True
        
    except Error as e:
        print(f"\n[X] Connection failed: {e}")
        print("\nPossible solutions:")
        print("1. Check if MySQL service is running")
        print("2. Verify password: Pvbn@7738")
        print("3. Check if port 3306 is available")
        print("4. Try: mysql -u root -p")
        return False

if __name__ == '__main__':
    test_connection()
