from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Get the most recently added products (highest product_ids)
cur.execute("SELECT product_id, name, category, price FROM products ORDER BY product_id DESC FETCH FIRST 10 ROWS ONLY")
recent_products = cur.fetchall()

print("10 Most Recently Added Products:")
print("-" * 80)
for p in recent_products:
    print(f"ID: {p[0]:3d} | Category: {p[2]:15s} | Name: {p[1]}")

cur.close()
conn.close()
