from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CURRENT DATABASE STATUS")
print("="*80)

# Check products
cur.execute("SELECT COUNT(*) FROM products")
total_products = cur.fetchone()[0]
print(f"\nTotal Products: {total_products}")

# Check products by category
print("\nProducts by Category:")
cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY category")
for row in cur.fetchall():
    print(f"  {row[0]:15s}: {row[1]:2d} products")

# Check bookings
cur.execute("SELECT COUNT(*) FROM bookings")
total_bookings = cur.fetchone()[0]
print(f"\nTotal Bookings: {total_bookings}")

# Check sample product images
print("\nSample Product Image Paths:")
cur.execute("SELECT product_id, name, image_path FROM products WHERE ROWNUM <= 10 ORDER BY product_id")
for row in cur.fetchall():
    print(f"  ID {row[0]:3d}: {row[1]:35s} -> {row[2]}")

# Check if images exist
print("\nChecking if image files exist:")
import os
cur.execute("SELECT DISTINCT image_path FROM products WHERE ROWNUM <= 5")
for row in cur.fetchall():
    image_path = row[0]
    # Convert /static/images/file.jpg to actual path
    if image_path and image_path.startswith('/static/'):
        file_path = image_path.replace('/static/', 'static/')
        full_path = f"c:/Users/Tejaswini/OneDrive/Desktop/RentEasyIndia/{file_path}"
        exists = os.path.exists(full_path)
        status = "EXISTS" if exists else "MISSING"
        print(f"  {image_path} -> {status}")

cur.close()
conn.close()

print("\n" + "="*80)
