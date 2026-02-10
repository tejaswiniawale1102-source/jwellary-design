from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CREATING PERMANENT BACKUP TABLES")
print("="*80)

try:
    # Drop existing backup tables if they exist
    print("\nDropping old backup tables (if they exist)...")
    tables = ['products_backup', 'bookings_backup', 'booking_details_backup', 'customers_backup']
    for table in tables:
        try:
            cur.execute(f"DROP TABLE {table}")
            print(f"  Dropped {table}")
        except:
            print(f"  {table} doesn't exist (OK)")
    
    # Create backup tables
    print("\nCreating new backup tables...")
    
    cur.execute("CREATE TABLE products_backup AS SELECT * FROM products")
    print("  Created products_backup")
    
    cur.execute("CREATE TABLE bookings_backup AS SELECT * FROM bookings")
    print("  Created bookings_backup")
    
    cur.execute("CREATE TABLE booking_details_backup AS SELECT * FROM booking_details")
    print("  Created booking_details_backup")
    
    cur.execute("CREATE TABLE customers_backup AS SELECT * FROM customers")
    print("  Created customers_backup")
    
    conn.commit()
    
    # Verify
    print("\nBackup table record counts:")
    cur.execute("SELECT COUNT(*) FROM products_backup")
    print(f"  Products: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM bookings_backup")
    print(f"  Bookings: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM booking_details_backup")
    print(f"  Booking Details: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM customers_backup")
    print(f"  Customers: {cur.fetchone()[0]}")
    
    print("\n" + "="*80)
    print("BACKUP TABLES CREATED SUCCESSFULLY!")
    print("="*80)
    
except Exception as e:
    print(f"\nError: {e}")
    conn.rollback()

cur.close()
conn.close()
