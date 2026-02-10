import oracledb
import sys

print("="*80)
print("DEEP DATABASE INVESTIGATION - FINDING THE REAL PROBLEM")
print("="*80)

# Test 1: Check if we're using the right Oracle driver
print("\n1. Oracle Driver Information:")
print(f"   Driver: {oracledb.__name__}")
print(f"   Version: {oracledb.__version__}")

# Test 2: Create connection and check settings
conn = oracledb.connect(
    user="system",
    password="system",
    host="localhost",
    port=1521,
    service_name="XEPDB1"
)

print("\n2. Connection Settings:")
print(f"   Autocommit: {conn.autocommit}")
print(f"   Service Name: XEPDB1")

cur = conn.cursor()

# Test 3: Check Oracle session parameters
print("\n3. Oracle Session Parameters:")
cur.execute("SELECT name, value FROM v$parameter WHERE name IN ('commit_logging', 'commit_wait')")
for row in cur.fetchall():
    print(f"   {row[0]}: {row[1]}")

# Test 4: Check if there are multiple sessions modifying data
print("\n4. Active Database Sessions:")
cur.execute("""
    SELECT username, program, status, COUNT(*) as session_count
    FROM v$session 
    WHERE username = 'SYSTEM'
    GROUP BY username, program, status
""")
for row in cur.fetchall():
    print(f"   User: {row[0]}, Program: {row[1]}, Status: {row[2]}, Count: {row[3]}")

# Test 5: Check current data
print("\n5. Current Data Count:")
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]
print(f"   Products: {products}")

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]
print(f"   Bookings: {bookings}")

# Test 6: THE CRITICAL TEST - Check if data persists after commit
print("\n6. Testing Data Persistence:")
print("   Inserting test record...")
cur.execute("INSERT INTO products (product_id, name, category, price, market_price, image_path) VALUES (9999, 'TEST_PRODUCT', 'Test', 100, 200, '/test.jpg')")
conn.commit()
print("   Committed test record")

cur.execute("SELECT COUNT(*) FROM products WHERE product_id = 9999")
test_exists = cur.fetchone()[0]
print(f"   Test record exists: {test_exists == 1}")

# Clean up test
cur.execute("DELETE FROM products WHERE product_id = 9999")
conn.commit()

print("\n" + "="*80)
print("DIAGNOSIS:")
print("="*80)

if products < 48:
    print("❌ DATA IS MISSING AGAIN!")
    print("\nPOSSIBLE CAUSES:")
    print("1. Multiple SQL Developer sessions are open and rolling back")
    print("2. Database is configured with delayed commit")
    print("3. Someone is running scripts that delete data")
else:
    print("✅ Data is intact")

print("="*80)

cur.close()
conn.close()
