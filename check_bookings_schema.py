from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Check bookings table structure
cur.execute("""
    SELECT column_name, data_type 
    FROM user_tab_columns 
    WHERE table_name = 'BOOKINGS'
    ORDER BY column_id
""")

print("BOOKINGS table columns:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

cur.close()
conn.close()
