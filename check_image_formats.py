from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CHECKING IMAGE PATH FORMAT")
print("="*80)

# Get all unique image paths
cur.execute("SELECT DISTINCT image_path FROM products ORDER BY image_path")
paths = [row[0] for row in cur.fetchall()]

print(f"\nFound {len(paths)} unique image paths:")
for path in paths[:10]:
    print(f"  {path}")

# Check if any paths are missing /static/images/
print("\nPaths NOT starting with /static/images/:")
for path in paths:
    if not path.startswith('/static/images/'):
        print(f"  WRONG: {path}")

# Check sample products
print("\nSample products from each category:")
cur.execute("""
    SELECT category, product_id, name, image_path 
    FROM (
        SELECT category, product_id, name, image_path,
               ROW_NUMBER() OVER (PARTITION BY category ORDER BY product_id) as rn
        FROM products
    )
    WHERE rn = 1
    ORDER BY category
""")
for row in cur.fetchall():
    print(f"  {row[0]:15s}: ID {row[1]:3d} {row[2]:30s} -> {row[3]}")

cur.close()
conn.close()
