from db import get_connection

print("="*80)
print("CREATING PERMANENT BACKUP OF CURRENT DATABASE STATE")
print("="*80)

conn = get_connection()
cur = conn.cursor()

# First, check what we currently have
print("\n1. CHECKING CURRENT DATABASE STATE...")
cur.execute("SELECT COUNT(*) FROM products")
product_count = cur.fetchone()[0]
print(f"   Current products: {product_count}")

cur.execute("SELECT COUNT(*) FROM bookings")
booking_count = cur.fetchone()[0]
print(f"   Current bookings: {booking_count}")

cur.execute("SELECT COUNT(*) FROM customers")
customer_count = cur.fetchone()[0]
print(f"   Current customers: {customer_count}")

if product_count == 0:
    print("\n⚠️  WARNING: No products found! Cannot create backup of empty database.")
    print("   Please restore data first before creating backup.")
    cur.close()
    conn.close()
    exit(1)

# Drop existing backup tables if they exist
print("\n2. DROPPING OLD BACKUP TABLES (if they exist)...")
try:
    cur.execute("DROP TABLE products_backup_permanent")
    print("   Dropped products_backup_permanent")
except:
    print("   products_backup_permanent doesn't exist (OK)")

try:
    cur.execute("DROP TABLE bookings_backup_permanent")
    print("   Dropped bookings_backup_permanent")
except:
    print("   bookings_backup_permanent doesn't exist (OK)")

try:
    cur.execute("DROP TABLE customers_backup_permanent")
    print("   Dropped customers_backup_permanent")
except:
    print("   customers_backup_permanent doesn't exist (OK)")

# Create permanent backup tables
print("\n3. CREATING PERMANENT BACKUP TABLES...")

cur.execute("""
    CREATE TABLE products_backup_permanent AS 
    SELECT * FROM products
""")
print(f"   ✓ Created products_backup_permanent with {product_count} records")

cur.execute("""
    CREATE TABLE bookings_backup_permanent AS 
    SELECT * FROM bookings
""")
print(f"   ✓ Created bookings_backup_permanent with {booking_count} records")

cur.execute("""
    CREATE TABLE customers_backup_permanent AS 
    SELECT * FROM customers
""")
print(f"   ✓ Created customers_backup_permanent with {customer_count} records")

# CRITICAL: COMMIT THE CHANGES
print("\n4. COMMITTING BACKUP TO DATABASE...")
conn.commit()
print("   ✓ BACKUP COMMITTED PERMANENTLY!")

print("\n" + "="*80)
print("BACKUP SUMMARY:")
print("="*80)
print(f"Products backed up:  {product_count}")
print(f"Bookings backed up:  {booking_count}")
print(f"Customers backed up: {customer_count}")
print("\nBackup tables created:")
print("  - products_backup_permanent")
print("  - bookings_backup_permanent")
print("  - customers_backup_permanent")
print("="*80)

cur.close()
conn.close()
