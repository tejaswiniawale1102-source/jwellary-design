from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("FIXING BOOKINGS TABLE - ADDING MISSING COLUMNS")
print("="*80)

# Check current columns
cur.execute("""
    SELECT column_name FROM user_tab_columns
    WHERE table_name = 'BOOKINGS'
""")
current_columns = [row[0] for row in cur.fetchall()]
print(f"\nCurrent columns: {', '.join(current_columns)}")

# Add missing columns if they don't exist
missing_columns = {
    'PHONE': 'VARCHAR2(15)',
    'ADDRESS': 'VARCHAR2(500)',
    'LOCATION': 'VARCHAR2(200)'
}

for col_name, col_type in missing_columns.items():
    if col_name not in current_columns:
        print(f"\nAdding column: {col_name} ({col_type})")
        cur.execute(f"ALTER TABLE bookings ADD {col_name} {col_type}")
        conn.commit()
        print(f"  [OK] {col_name} added")
    else:
        print(f"\n{col_name} already exists - skipping")

# Verify final structure
cur.execute("""
    SELECT column_name, data_type
    FROM user_tab_columns
    WHERE table_name = 'BOOKINGS'
    ORDER BY column_id
""")

print("\n" + "="*80)
print("FINAL BOOKINGS TABLE STRUCTURE:")
print("="*80)
for col in cur.fetchall():
    print(f"  - {col[0]:20s} {col[1]}")

print("\n[SUCCESS] Bookings table updated!")
print("="*80)

cur.close()
conn.close()
