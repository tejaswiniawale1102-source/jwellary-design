from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("CREATING REVIEWS TABLE")
print("="*80)

# Drop if exists
try:
    cur.execute("DROP TABLE reviews")
    print("\nDropped existing reviews table")
except:
    print("\nNo existing reviews table to drop")

# Create reviews table
cur.execute("""
    CREATE TABLE reviews (
        review_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        product_id NUMBER NOT NULL,
        customer_id NUMBER NOT NULL,
        rating NUMBER(1) CHECK (rating BETWEEN 1 AND 5),
        comment_text VARCHAR2(1000),
        verdict VARCHAR2(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")

conn.commit()
print("✓ Reviews table created successfully!")

# Add some sample reviews
print("\nAdding sample reviews...")

sample_reviews = [
    (101, 1, 5, "Absolutely stunning jewelry! Perfect for my wedding.", "Highly Recommended"),
    (108, 2, 4, "Beautiful ring, good quality.", "Recommended"),
    (1, 3, 5, "Great blazer, perfect fit!", "Highly Recommended"),
    (201, 4, 4, "Nice lehenga, good fabric quality.", "Recommended"),
    (301, 5, 5, "Amazing decor items, made my event special!", "Highly Recommended"),
]

for product_id, customer_id, rating, comment, verdict in sample_reviews:
    try:
        cur.execute("""
            INSERT INTO reviews (product_id, customer_id, rating, comment_text, verdict)
            VALUES (:1, :2, :3, :4, :5)
        """, (product_id, customer_id, rating, comment, verdict))
    except Exception as e:
        print(f"  Error adding review for product {product_id}: {e}")

conn.commit()

# Verify
cur.execute("SELECT COUNT(*) FROM reviews")
review_count = cur.fetchone()[0]
print(f"\n✓ Added {review_count} sample reviews")

print("\n" + "="*80)
print("REVIEWS TABLE READY!")
print("="*80)

cur.close()
conn.close()
