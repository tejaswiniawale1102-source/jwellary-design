from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("EMERGENCY DATABASE CHECK")
print("="*80)

# Check current data
print("\nCURRENT DATABASE STATE:")
print("-" * 80)

cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]
print(f"Products: {products}")

cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]
print(f"Customers: {customers}")

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]
print(f"Bookings: {bookings}")

# Check backup tables
print("\nBACKUP TABLES:")
print("-" * 80)

try:
    cur.execute("SELECT COUNT(*) FROM products_backup")
    products_backup = cur.fetchone()[0]
    print(f"Products backup: {products_backup}")
except:
    print("Products backup: NOT FOUND")
    products_backup = 0

try:
    cur.execute("SELECT COUNT(*) FROM bookings_backup")
    bookings_backup = cur.fetchone()[0]
    print(f"Bookings backup: {bookings_backup}")
except:
    print("Bookings backup: NOT FOUND")
    bookings_backup = 0

try:
    cur.execute("SELECT COUNT(*) FROM customers_backup")
    customers_backup = cur.fetchone()[0]
    print(f"Customers backup: {customers_backup}")
except:
    print("Customers backup: NOT FOUND")
    customers_backup = 0

print("\n" + "="*80)
print("DIAGNOSIS:")
print("="*80)

if products == 0:
    print("CRITICAL: All products are missing!")
    if products_backup > 0:
        print(f"SOLUTION: Can restore {products_backup} products from backup")
else:
    print(f"OK: {products} products found")

if bookings == 0:
    print("CRITICAL: All bookings are missing!")
    if bookings_backup > 0:
        print(f"SOLUTION: Can restore {bookings_backup} bookings from backup")
else:
    print(f"OK: {bookings} bookings found")

if customers == 0:
    print("CRITICAL: All customers are missing!")
    if customers_backup > 0:
        print(f"SOLUTION: Can restore {customers_backup} customers from backup")
else:
    print(f"OK: {customers} customers found")

print("="*80)

cur.close()
conn.close()
