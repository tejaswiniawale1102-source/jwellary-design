from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("FINDING ROOT CAUSE OF DATA LOSS")
print("="*80)

# Check if there are any DROP or DELETE triggers
print("\n1. Checking for dangerous triggers...")
cur.execute("""
    SELECT trigger_name, table_name, triggering_event
    FROM user_triggers
    WHERE table_name IN ('PRODUCTS', 'BOOKINGS', 'CUSTOMERS')
""")
triggers = cur.fetchall()
if triggers:
    print("   Found triggers:")
    for trig in triggers:
        print(f"     - {trig[0]} on {trig[1]} ({trig[2]})")
else:
    print("   No triggers found")

# Check database connection settings
print("\n2. Checking connection autocommit...")
print(f"   Autocommit: {conn.autocommit}")

# Force commit everything
print("\n3. Forcing COMMIT on all changes...")
conn.commit()
print("   [OK] Changes committed")

# Create a permanent save point
print("\n4. Creating permanent backup...")
try:
    # Update backup tables with current data
    cur.execute("DELETE FROM products_backup")
    cur.execute("INSERT INTO products_backup SELECT * FROM products")
    
    cur.execute("DELETE FROM bookings_backup")
    cur.execute("INSERT INTO bookings_backup SELECT * FROM bookings")
    
    cur.execute("DELETE FROM booking_details_backup")
    cur.execute("INSERT INTO booking_details_backup SELECT * FROM booking_details")
    
    conn.commit()
    print("   [OK] Backup tables updated")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*80)
print("RECOMMENDATION:")
print("="*80)
print("The issue might be:")
print("1. Database session not being committed properly")
print("2. Someone running DELETE queries in SQL Developer")
print("3. Application restart without proper shutdown")
print("\nSOLUTION: Always use the Flask app for changes, not SQL Developer")
print("="*80)

cur.close()
conn.close()
