from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CREATING MISSING TABLES")
print("="*80)

# Check and create CART table
print("\n1. Creating CART table...")
try:
    cur.execute("DROP TABLE cart")
    print("   Dropped existing cart table")
except:
    print("   No existing cart table")

cur.execute("""
    CREATE TABLE cart (
        cart_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        customer_id NUMBER NOT NULL,
        product_id NUMBER NOT NULL,
        quantity NUMBER DEFAULT 1,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")
conn.commit()
print("   [OK] Cart table created")

# Check and create WISHLIST table
print("\n2. Creating WISHLIST table...")
try:
    cur.execute("DROP TABLE wishlist")
    print("   Dropped existing wishlist table")
except:
    print("   No existing wishlist table")

cur.execute("""
    CREATE TABLE wishlist (
        wishlist_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        customer_id NUMBER NOT NULL,
        product_id NUMBER NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")
conn.commit()
print("   [OK] Wishlist table created")

# Verify all tables exist
print("\n" + "="*80)
print("VERIFICATION:")
print("="*80)

cur.execute("""
    SELECT table_name FROM user_tables 
    WHERE table_name IN ('REVIEWS', 'CART', 'WISHLIST')
    ORDER BY table_name
""")
tables = cur.fetchall()
print("\nFunctional tables created:")
for table in tables:
    print(f"  - {table[0]}")

print("\n[SUCCESS] All missing tables created!")
print("="*80)

cur.close()
conn.close()
