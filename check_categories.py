from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Check all distinct categories
cur.execute("SELECT DISTINCT category FROM products ORDER BY category")
categories = [row[0] for row in cur.fetchall()]

print("Categories in database:")
for cat in categories:
    print(f"  - '{cat}'")

# Count products per category
print("\nProduct count per category:")
for cat in categories:
    cur.execute("SELECT COUNT(*) FROM products WHERE category = :1", (cat,))
    count = cur.fetchone()[0]
    print(f"  {cat}: {count} products")

cur.close()
conn.close()
