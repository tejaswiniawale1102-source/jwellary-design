from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Check current products
cur.execute("SELECT COUNT(*) FROM products")
total = cur.fetchone()[0]

print(f"Current products in database: {total}")

if total > 0:
    print("\nExisting products:")
    cur.execute("SELECT product_id, name, category FROM products ORDER BY product_id")
    for row in cur.fetchall():
        print(f"  ID {row[0]}: {row[1]} ({row[2]})")

cur.close()
conn.close()
