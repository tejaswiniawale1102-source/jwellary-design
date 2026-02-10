from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Check what the womens_collection route is querying
print("Testing womens_collection route query:")
cur.execute("SELECT * FROM products WHERE category = :1 ORDER BY product_id ASC", ('Dresses',))
dresses_products = cur.fetchall()
print(f"\nProducts with category='Dresses': {len(dresses_products)}")
for p in dresses_products[:5]:
    print(f"  - {p[0]}: {p[1]}")

print("\n" + "="*80)
print("\nProducts with category='Womens':")
cur.execute("SELECT * FROM products WHERE category = :1 ORDER BY product_id DESC", ('Womens',))
womens_products = cur.fetchall()
print(f"Total: {len(womens_products)}")
for p in womens_products[:5]:
    print(f"  - {p[0]}: {p[1]}")

cur.close()
conn.close()
