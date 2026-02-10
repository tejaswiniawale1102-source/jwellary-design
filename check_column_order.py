from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Check the actual column order in products table
cur.execute("SELECT * FROM products WHERE ROWNUM <= 3 ORDER BY product_id")
products = cur.fetchall()

print("="*80)
print("PRODUCTS TABLE COLUMN ORDER")
print("="*80)

# Get column names
cur.execute("""
    SELECT column_name 
    FROM user_tab_columns 
    WHERE table_name = 'PRODUCTS'
    ORDER BY column_id
""")
columns = [row[0] for row in cur.fetchall()]

print("\nColumn indices:")
for i, col in enumerate(columns):
    print(f"  [{i}] {col}")

print("\nSample product data:")
for product in products:
    print(f"\nProduct ID: {product[0]}")
    for i, value in enumerate(product):
        if i < len(columns):
            print(f"  [{i}] {columns[i]:20s}: {value}")

cur.close()
conn.close()
