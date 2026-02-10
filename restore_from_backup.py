from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("RESTORING FROM BACKUP TABLES")
print("="*80)

try:
    # Clear current tables
    print("\nClearing current tables...")
    cur.execute("DELETE FROM booking_details")
    cur.execute("DELETE FROM bookings")
    cur.execute("DELETE FROM products")
    cur.execute("DELETE FROM customers")
    print("  Tables cleared")
    
    # Restore from backup
    print("\nRestoring from backup...")
    
    cur.execute("INSERT INTO customers SELECT * FROM customers_backup")
    print(f"  Restored {cur.rowcount} customers")
    
    cur.execute("INSERT INTO products SELECT * FROM products_backup")
    print(f"  Restored {cur.rowcount} products")
    
    cur.execute("INSERT INTO bookings SELECT * FROM bookings_backup")
    print(f"  Restored {cur.rowcount} bookings")
    
    cur.execute("INSERT INTO booking_details SELECT * FROM booking_details_backup")
    print(f"  Restored {cur.rowcount} booking details")
    
    conn.commit()
    
    # Verify
    print("\nCurrent table record counts:")
    cur.execute("SELECT COUNT(*) FROM products")
    print(f"  Products: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM bookings")
    print(f"  Bookings: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM customers")
    print(f"  Customers: {cur.fetchone()[0]}")
    
    print("\n" + "="*80)
    print("DATABASE RESTORED FROM BACKUP!")
    print("="*80)
    print("\nYou can now refresh your website - all data is back!")
    
except Exception as e:
    print(f"\nError: {e}")
    conn.rollback()

cur.close()
conn.close()
