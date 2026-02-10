from db import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*80)
print("RESTORING ALL PRODUCTS")
print("="*80)

# Complete product list with all categories
products = [
    # JEWELRY (13 products)
    (101, 'Sapphire Premium Set', 'Jewelry', 4500, '/static/images/sapphire_premium.png', 'Elegant sapphire jewelry set'),
    (108, 'Emerald Solitaire Ring', 'Jewelry', 3200, '/static/images/ring1.jpg', 'Beautiful emerald ring'),
    (109, 'Antique Temple Set', 'Jewelry', 5200, '/static/images/jwelery_update_1.jpg', 'Traditional temple jewelry'),
    (110, 'Pearl Choker Necklace', 'Jewelry', 2800, '/static/images/jwelery_update_2.jpg', 'Classic pearl choker'),
    (111, 'Ruby Wedding Set', 'Jewelry', 6500, '/static/images/jwelery_update_3.jpg', 'Stunning ruby bridal set'),
    (507, 'Golden Anklet Kada', 'Jewelry', 2500, '/static/images/ring2.jpg', 'Traditional golden anklet'),
    (527, 'Rani Haar', 'Jewelry', 3000, '/static/images/jwelery_update_1.jpg', 'Royal rani haar necklace'),
    (528, 'Classic Chain Bracelet', 'Jewelry', 2999, '/static/images/jwelery_update_2.jpg', 'Elegant chain bracelet'),
    (529, 'Classic Golden Bracelet', 'Jewelry', 1999, '/static/images/jwelery_update_3.jpg', 'Simple golden bracelet'),
    (530, 'Golden Ring', 'Jewelry', 1999, '/static/images/ring1.jpg', 'Classic golden ring'),
    (531, 'Infinity Ring', 'Jewelry', 2999, '/static/images/ring2.jpg', 'Modern infinity design ring'),
    (532, 'Diamond Set with Jhumkas', 'Jewelry', 3999, '/static/images/sapphire_premium.png', 'Complete diamond set'),
    
    # WOMENS (10 products)
    (201, 'Royal Maroon Lehenga', 'Womens', 5500, '/static/images/royal_lehenga.png', 'Bridal maroon lehenga'),
    (202, 'Emerald Silk Gown', 'Womens', 4200, '/static/images/emerald_gown.png', 'Elegant silk gown'),
    (508, 'Royal Red Lehenga', 'Womens', 6500, '/static/images/women8.jpg', 'Premium red lehenga'),
    (509, 'Purple Wedding Lehenga', 'Womens', 7200, '/static/images/women9.jpg', 'Designer purple lehenga'),
    (510, 'Bridal Sandal', 'Womens', 1500, '/static/images/women1.jpg', 'Elegant bridal footwear'),
    (511, 'Green Party Wear Gown', 'Womens', 4800, '/static/images/women3.jpg', 'Stylish party gown'),
    (512, 'Red Velvet One Piece', 'Womens', 3200, '/static/images/women8.jpg', 'Velvet one piece dress'),
    (513, 'Wedding Party Suit', 'Womens', 5900, '/static/images/women9.jpg', 'Designer party suit'),
    (514, 'Anarkali Suit', 'Womens', 4500, '/static/images/women1.jpg', 'Traditional anarkali'),
    (515, 'Classic Black Heels', 'Womens', 2200, '/static/images/women3.jpg', 'Elegant black heels'),
    
    # MENS (9 products)
    (301, 'Royal Blue Sherwani', 'Mens', 6500, '/static/images/men1.jpg', 'Wedding sherwani'),
    (302, 'Black Tuxedo', 'Mens', 5200, '/static/images/men2.jpg', 'Classic tuxedo'),
    (303, 'Grey Office Suit', 'Mens', 3900, '/static/images/men1.jpg', 'Professional suit'),
    (304, 'Cream Wedding Kurta', 'Mens', 2800, '/static/images/men2.jpg', 'Traditional kurta'),
    (305, 'Navy Blazer', 'Mens', 4200, '/static/images/men1.jpg', 'Formal blazer'),
    (306, 'Maroon Sherwani', 'Mens', 7200, '/static/images/men2.jpg', 'Premium sherwani'),
    (307, 'White Formal Shirt', 'Mens', 1500, '/static/images/men1.jpg', 'Classic white shirt'),
    (308, 'Brown Leather Jacket', 'Mens', 5500, '/static/images/men2.jpg', 'Stylish leather jacket'),
    (309, 'Charcoal Suit', 'Mens', 4800, '/static/images/men1.jpg', 'Modern charcoal suit'),
    
    # DECOR (8 products)
    (401, 'Crystal Chandelier', 'Decor', 8500, '/static/images/decor1.jpg', 'Luxury chandelier'),
    (402, 'Floral Backdrop', 'Decor', 3200, '/static/images/decor2.jpg', 'Wedding backdrop'),
    (403, 'LED String Lights', 'Decor', 1200, '/static/images/decor1.jpg', 'Decorative lights'),
    (404, 'Mandap Decoration Set', 'Decor', 12000, '/static/images/decor2.jpg', 'Complete mandap decor'),
    (405, 'Table Centerpieces', 'Decor', 800, '/static/images/decor1.jpg', 'Elegant centerpieces'),
    (406, 'Photo Booth Props', 'Decor', 1500, '/static/images/decor2.jpg', 'Fun photo props'),
    (407, 'Balloon Arch Kit', 'Decor', 2200, '/static/images/decor1.jpg', 'Balloon decoration'),
    (408, 'Stage Backdrop', 'Decor', 5500, '/static/images/decor2.jpg', 'Professional backdrop'),
    
    # EVENT TOOLS (6 products)
    (501, 'Professional DJ System', 'Event Tools', 15000, '/static/images/event1.jpg', 'Complete DJ setup'),
    (502, 'Projector & Screen', 'Event Tools', 5500, '/static/images/event2.jpg', 'HD projector'),
    (503, 'Karaoke Machine', 'Event Tools', 3200, '/static/images/event1.jpg', 'Karaoke system'),
    (504, 'Fog Machine', 'Event Tools', 2800, '/static/images/event2.jpg', 'Professional fog machine'),
    (505, 'LED Dance Floor', 'Event Tools', 18000, '/static/images/event1.jpg', 'Interactive dance floor'),
    (506, 'Live Streaming Gear', 'Event Tools', 8500, '/static/images/event2.jpg', 'Streaming equipment'),
    
    # DRESSES (2 products)
    (205, 'Bridal Red Anarkali', 'Dresses', 6200, '/static/images/women8.jpg', 'Bridal anarkali dress'),
    (206, 'Designer Saree', 'Dresses', 4500, '/static/images/women9.jpg', 'Elegant designer saree'),
]

print(f"\nRestoring {len(products)} products...")
created_count = 0
skipped_count = 0

for product_id, name, category, price, image_path, description in products:
    try:
        cur.execute("""
            INSERT INTO products (product_id, name, category, price, image_path, description)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, (product_id, name, category, price, image_path, description))
        created_count += 1
        print(f"  + {name} ({category})")
    except Exception as e:
        if "ORA-00001" in str(e):
            skipped_count += 1
        else:
            print(f"  Error adding {name}: {e}")

conn.commit()

# Verify
cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY category")
print("\n" + "="*80)
print("PRODUCTS BY CATEGORY:")
print("-"*80)
for row in cur.fetchall():
    print(f"  {row[0]:15s}: {row[1]:2d} products")

cur.execute("SELECT COUNT(*) FROM products")
total = cur.fetchone()[0]
print(f"\n  {'TOTAL':15s}: {total:2d} products")

print(f"\nCreated: {created_count} new products")
print(f"Skipped: {skipped_count} existing products")

cur.close()
conn.close()

print("\n" + "="*80)
print("ALL PRODUCTS RESTORED!")
print("="*80)
