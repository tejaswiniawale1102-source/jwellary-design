from db import get_connection

# Test the get_recommendations function
def get_recommendations(category, current_product_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        # Find 4 items in same category, excluding current
        cursor.execute("SELECT * FROM products WHERE category = :1 AND product_id != :2 FETCH FIRST 4 ROWS ONLY", (category, current_product_id))
        items = cursor.fetchall()
        cursor.close()
        connection.close()
        return items
    except Exception as e:
        print(f"Error: {e}")
        return []

# Test with product 101 (Sapphire Premium Set - Jewelry category)
connection = get_connection()
cursor = connection.cursor()
cursor.execute("SELECT product_id, name, category FROM products WHERE product_id = 101")
current_product = cursor.fetchone()
cursor.close()
connection.close()

print(f"Current Product: ID={current_product[0]}, Name={current_product[1]}, Category={current_product[2]}")
print("\nRecommendations:")

recommendations = get_recommendations(current_product[2], current_product[0])
if recommendations:
    for rec in recommendations:
        print(f"  - ID={rec[0]}, Name={rec[1]}, Category={rec[2]}, Price={rec[3]}")
else:
    print("  No recommendations found!")
