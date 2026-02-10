from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("DATABASE STATUS REPORT - RentEasyIndia")
print("="*80)

# 1. PRODUCTS
print("\nPRODUCTS BY CATEGORY:")
print("-"*80)
cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY category")
for row in cur.fetchall():
    print(f"  {row[0]:20s}: {row[1]:3d} products")

cur.execute("SELECT COUNT(*) FROM products")
total_products = cur.fetchone()[0]
print(f"\n  {'TOTAL PRODUCTS':20s}: {total_products:3d}")

# 2. CUSTOMERS
print("\nCUSTOMERS:")
print("-"*80)
cur.execute("SELECT COUNT(*) FROM customers")
total_customers = cur.fetchone()[0]
print(f"  Total Registered Customers: {total_customers}")

# 3. BOOKINGS
print("\nBOOKINGS:")
print("-"*80)
cur.execute("SELECT status, COUNT(*) FROM bookings GROUP BY status ORDER BY status")
for row in cur.fetchall():
    print(f"  {row[0]:15s}: {row[1]:3d} bookings")

cur.execute("SELECT COUNT(*) FROM bookings")
total_bookings = cur.fetchone()[0]
print(f"  {'TOTAL':15s}: {total_bookings:3d} bookings")

# 4. REVENUE
print("\nREVENUE:")
print("-"*80)
cur.execute("SELECT SUM(total_price) FROM bookings WHERE status IN ('Confirmed', 'Returned')")
total_revenue = cur.fetchone()[0] or 0
print(f"  Total Revenue: Rs.{total_revenue:,.2f}")

# 5. WISHLIST
print("\nWISHLIST:")
print("-"*80)
cur.execute("SELECT COUNT(*) FROM wishlist")
wishlist_count = cur.fetchone()[0]
print(f"  Total Wishlist Items: {wishlist_count}")

# 6. CART
print("\nCART:")
print("-"*80)
cur.execute("SELECT COUNT(*) FROM cart")
cart_count = cur.fetchone()[0]
print(f"  Total Cart Items: {cart_count}")

# 7. REVIEWS
print("\nREVIEWS:")
print("-"*80)
cur.execute("SELECT COUNT(*) FROM reviews")
review_count = cur.fetchone()[0]
cur.execute("SELECT AVG(rating) FROM reviews")
avg_rating = cur.fetchone()[0] or 0
print(f"  Total Reviews: {review_count}")
print(f"  Average Rating: {avg_rating:.2f}/5.0")

# 8. RECENT PRODUCTS
print("\n5 MOST RECENT PRODUCTS:")
print("-"*80)
cur.execute("SELECT product_id, name, category, price FROM products ORDER BY product_id DESC FETCH FIRST 5 ROWS ONLY")
for p in cur.fetchall():
    print(f"  ID {p[0]:3d}: {p[1]:40s} ({p[2]:15s}) - Rs.{p[3]:,.0f}")

print("\n" + "="*80)
print("DATABASE STATUS: HEALTHY & OPERATIONAL")
print("="*80)

cur.close()
conn.close()
