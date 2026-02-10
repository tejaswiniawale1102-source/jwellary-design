from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("FIXING PRODUCT IMAGE PATHS")
print("="*80)

# Update products with correct image paths that exist in static/images
updates = [
    # JEWELRY
    (101, '/static/images/sapphire_premium.png'),
    (108, '/static/images/ring1.jpg'),
    (109, '/static/images/jwelery_update_1.jpg'),
    (110, '/static/images/jwelery_update_2.jpg'),
    (111, '/static/images/jwelery_update_3.jpg'),
    (507, '/static/images/ring2.jpg'),
    (527, '/static/images/jwelery_update_4.jpg'),
    (528, '/static/images/bracelet1.jpg'),
    (529, '/static/images/bracelet2.jpg'),
    (530, '/static/images/ring3.jpg'),
    (531, '/static/images/ring4.jpg'),
    (532, '/static/images/jwelery_update_5.jpg'),
    
    # WOMENS
    (201, '/static/images/royal_lehenga.png'),
    (202, '/static/images/emerald_gown.png'),
    (508, '/static/images/women8.jpg'),
    (509, '/static/images/women9.jpg'),
    (510, '/static/images/women2.jpg'),
    (511, '/static/images/women3.jpg'),
    (512, '/static/images/women4.jpg'),
    (513, '/static/images/women5.jpg'),
    (514, '/static/images/women6.jpg'),
    (515, '/static/images/women10.jpg'),
    
    # MENS
    (301, '/static/images/mens1.jpg'),
    (302, '/static/images/mens2.jpg'),
    (303, '/static/images/mens3.jpg'),
    (304, '/static/images/mens4.jpg'),
    (305, '/static/images/mens5.jpg'),
    (306, '/static/images/mens6.jpg'),
    (307, '/static/images/mens7.jpg'),
    (308, '/static/images/mens8.jpg'),
    (309, '/static/images/mens9.jpg'),
    
    # DECOR
    (401, '/static/images/decor1.jpg'),
    (402, '/static/images/decor2.jpg'),
    (403, '/static/images/decor3.jpg'),
    (404, '/static/images/decor4.jpg'),
    (405, '/static/images/decor5.jpg'),
    (406, '/static/images/decor6.jpg'),
    (407, '/static/images/decor7.jpg'),
    (408, '/static/images/decor8.jpg'),
    
    # EVENT TOOLS
    (501, '/static/images/event_tool1.jpg'),
    (502, '/static/images/event_tool2.jpg'),
    (503, '/static/images/event_tool3.jpg'),
    (504, '/static/images/event_tool4.jpg'),
    (505, '/static/images/event_tool5.jpg'),
    (506, '/static/images/event_tool6.jpg'),
    
    # DRESSES
    (205, '/static/images/women8.jpg'),
    (206, '/static/images/women9.jpg'),
]

print(f"\nUpdating {len(updates)} product image paths...")
updated_count = 0

for product_id, image_path in updates:
    try:
        cur.execute("""
            UPDATE products 
            SET image_path = :1 
            WHERE product_id = :2
        """, (image_path, product_id))
        if cur.rowcount > 0:
            updated_count += 1
            print(f"  Updated product {product_id} -> {image_path}")
    except Exception as e:
        print(f"  Error updating product {product_id}: {e}")

conn.commit()

print(f"\nUpdated {updated_count} product image paths")

# Verify
print("\nSample products with updated paths:")
cur.execute("SELECT product_id, name, image_path FROM products WHERE ROWNUM <= 5")
for row in cur.fetchall():
    print(f"  ID {row[0]}: {row[1]} -> {row[2]}")

cur.close()
conn.close()

print("\n" + "="*80)
print("IMAGE PATHS FIXED!")
print("="*80)
