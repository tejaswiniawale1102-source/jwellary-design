import oracledb
import datetime
import traceback
import sys
from db import get_connection

# Mock data
customer_id = 1
product_id = 101
total_rent = "47000"
today_str = datetime.date.today().strftime('%Y-%m-%d')
end_date_str = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
phone = "+91 1234567890"
address = "123 Test St"
location = "Near Park"

print("Starting test...", flush=True)

try:
    print("Connecting...", flush=True)
    connection = get_connection()
    cursor = connection.cursor()
    
    print("Testing INSERT with RETURNING INTO...", flush=True)
    booking_id_var = cursor.var(int)
    cursor.execute("""
        INSERT INTO bookings (customer_id, total_price, booking_date, rent_date, return_date, status, phone, address, location)
        VALUES (:1, :2, SYSDATE, TO_DATE(:3, 'YYYY-MM-DD'), TO_DATE(:4, 'YYYY-MM-DD'), 'Confirmed', :5, :6, :7)
        RETURN booking_id INTO :8
    """, [customer_id, total_rent, today_str, end_date_str, phone, address, location, booking_id_var])
    
    print("Getting value...", flush=True)
    val = booking_id_var.getvalue()
    print(f"Var getvalue() type: {type(val)}, value: {val}", flush=True)
    
    new_booking_id = val[0]
    print(f"Extracted ID: {new_booking_id}", flush=True)
    
    print("Testing child INSERT...", flush=True)
    cursor.execute("""
        INSERT INTO booking_details (booking_id, product_id, quantity, price)
        VALUES (:1, :2, 1, :3)
    """, (new_booking_id, product_id, total_rent))
    
    connection.rollback() # Don't actually commit
    print("Test successful!", flush=True)
    
except Exception as e:
    print(f"FAILED: {e}", flush=True)
    print("Full traceback:", flush=True)
    traceback.print_exc(file=sys.stdout)
    sys.stdout.flush()
finally:
    if 'connection' in locals():
        connection.close()
    print("Script complete", flush=True)
