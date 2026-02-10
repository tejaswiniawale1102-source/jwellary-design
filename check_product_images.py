from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Find the lehenga and emerald gown products
cur.execute("""
    SELECT product_id, name, image_path 
    FROM products 
    WHERE name LIKE '%Lehenga%' OR name LIKE '%Emerald%' OR name LIKE '%Gown%'
    ORDER BY product_id DESC
""")

products = cur.fetchall()

print("Products matching 'Lehenga' or 'Emerald' or 'Gown':")
print("="*80)
for p in products:
    print(f"ID: {p[0]:3d} | Name: {p[1]:40s} | Image: {p[2]}")

cur.close()
conn.close()
