from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Check a sample product's image path
cur.execute("SELECT product_id, name, image_path FROM products WHERE product_id = 101")
product = cur.fetchone()
print(f"Product ID: {product[0]}")
print(f"Name: {product[1]}")
print(f"Image Path: {product[2]}")

cur.close()
conn.close()
