from db import get_connection

connection = get_connection()
cursor = connection.cursor()

# Check column order from SELECT *
cursor.execute("SELECT * FROM products WHERE product_id = 102")
product = cursor.fetchone()

print("Columns from SELECT * FROM products:")
print(f"Index 0: {product[0]}")
print(f"Index 1: {product[1]}")
print(f"Index 2: {product[2]}")
print(f"Index 3: {product[3]}")
print(f"Index 4: {product[4]}")
print(f"Index 5: {product[5]}")

cursor.close()
connection.close()
