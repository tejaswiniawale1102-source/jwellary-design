from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CHECKING DATABASE TABLES")
print("="*80)

# Check what tables exist
cur.execute("""
    SELECT table_name 
    FROM user_tables 
    ORDER BY table_name
""")

tables = cur.fetchall()
print("\nExisting tables:")
for table in tables:
    print(f"  - {table[0]}")

# Check if reviews table exists
reviews_exists = any('REVIEWS' in str(table[0]).upper() for table in tables)
print(f"\nReviews table exists: {reviews_exists}")

# Count confirmed bookings
cur.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Confirmed'")
confirmed = cur.fetchone()[0]
print(f"\nConfirmed bookings: {confirmed}")

cur.close()
conn.close()
