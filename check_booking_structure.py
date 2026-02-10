from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CHECKING BOOKING TABLES STRUCTURE")
print("="*80)

# Check bookings table structure
print("\n1. BOOKINGS table columns:")
cur.execute("""
    SELECT column_name, data_type, nullable
    FROM user_tab_columns
    WHERE table_name = 'BOOKINGS'
    ORDER BY column_id
""")
for col in cur.fetchall():
    print(f"   - {col[0]:20s} {col[1]:15s} {'NULL' if col[2] == 'Y' else 'NOT NULL'}")

# Check booking_details table structure
print("\n2. BOOKING_DETAILS table columns:")
cur.execute("""
    SELECT column_name, data_type, nullable
    FROM user_tab_columns
    WHERE table_name = 'BOOKING_DETAILS'
    ORDER BY column_id
""")
for col in cur.fetchall():
    print(f"   - {col[0]:20s} {col[1]:15s} {'NULL' if col[2] == 'Y' else 'NOT NULL'}")

# Check if there are any constraints
print("\n3. Foreign key constraints:")
cur.execute("""
    SELECT constraint_name, constraint_type, table_name
    FROM user_constraints
    WHERE table_name IN ('BOOKINGS', 'BOOKING_DETAILS')
    AND constraint_type IN ('R', 'P')
""")
for constraint in cur.fetchall():
    print(f"   - {constraint[2]:20s} {constraint[0]:30s} Type: {constraint[1]}")

print("\n" + "="*80)

cur.close()
conn.close()
