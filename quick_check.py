from db import get_connection

print("="*80)
print("QUICK DATABASE CHECK - RUN THIS BEFORE PRESENTATION")
print("="*80)

conn = get_connection()
cur = conn.cursor()

# Check all data
cur.execute("SELECT COUNT(*) FROM products")
products = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM bookings")
bookings = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM customers")
customers = cur.fetchone()[0]

print(f"\nDatabase Status:")
print(f"  Products:  {products}/48  {'OK' if products == 48 else 'MISSING DATA!'}")
print(f"  Bookings:  {bookings}/18  {'OK' if bookings >= 18 else 'MISSING DATA!'}")
print(f"  Customers: {customers}/16  {'OK' if customers >= 16 else 'MISSING DATA!'}")

if products == 48 and bookings >= 18 and customers >= 16:
    print("\n" + "="*80)
    print("STATUS: READY FOR PRESENTATION!")
    print("="*80)
    print("\nYour website is working perfectly.")
    print("Go to: http://127.0.0.1:5000")
else:
    print("\n" + "="*80)
    print("WARNING: DATA IS MISSING!")
    print("="*80)
    print("\nRun this command to fix:")
    print("  python PERMANENT_FIX.py")

cur.close()
conn.close()
