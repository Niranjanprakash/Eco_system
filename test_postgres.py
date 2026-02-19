import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='Pvbn@7738',
        port=5432
    )
    print("[OK] PostgreSQL connection successful!")
    
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print(f"[OK] PostgreSQL version: {version[0]}")
    
    cursor.close()
    conn.close()
    
    # Create database in separate connection
    conn2 = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='Pvbn@7738',
        port=5432
    )
    conn2.autocommit = True
    cursor2 = conn2.cursor()
    
    cursor2.execute("SELECT 1 FROM pg_database WHERE datname='ecoplan'")
    exists = cursor2.fetchone()
    
    if not exists:
        cursor2.execute('CREATE DATABASE ecoplan')
        print("[OK] Database 'ecoplan' created")
    else:
        print("[OK] Database 'ecoplan' already exists")
    
    cursor2.close()
    conn2.close()
    print("\n[OK] PostgreSQL is working! Ready for deployment.")
    
except Exception as e:
    print(f"[X] PostgreSQL connection failed: {e}")
    print("\nMake sure:")
    print("1. PostgreSQL is installed")
    print("2. PostgreSQL service is running")
    print("3. Password is correct: Pvbn@7738")
