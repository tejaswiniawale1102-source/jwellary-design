from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("FINAL VERIFICATION CHECK")
print("="*80)

# 1. Check products
print("\n1. PRODUCTS:")
cur.execute("SELECT COUNT(*) FROM products")
product_count = cur.fetchone()[0]
print(f"   Total: {product_count} products")

cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY category")
for row in cur.fetchall():
    print(f"   - {row[0]:15s}: {row[1]:2d} products")

# 2. Check bookings
print("\n2. BOOKINGS:")
cur.execute("SELECT COUNT(*) FROM bookings")
booking_count = cur.fetchone()[0]
print(f"   Total: {booking_count} bookings")

# 3. Check image paths
print("\n3. IMAGE PATHS:")
cur.execute("SELECT product_id, name, image_path FROM products WHERE ROWNUM <= 3 ORDER BY product_id")
for row in cur.fetchall():
    print(f"   ID {row[0]:3d}: {row[1]:30s} -> {row[2]}")

# 4. Check backup tables exist
print("\n4. BACKUP TABLES:")
try:
    cur.execute("SELECT COUNT(*) FROM products_backup")
    backup_count = cur.fetchone()[0]
    print(f"   products_backup: {backup_count} records - OK")
except:
    print("   products_backup: MISSING - Need to create!")

print("\n" + "="*80)
print("VERIFICATION SUMMARY:")
print("="*80)
print(f"Products: {product_count}/48 {'OK' if product_count == 48 else 'NEEDS FIX'}")
print(f"Bookings: {booking_count}/18 {'OK' if booking_count == 18 else 'NEEDS FIX'}")
print("="*80)

cur.close()
conn.close()
