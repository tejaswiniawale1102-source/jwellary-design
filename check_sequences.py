from db import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT sequence_name FROM user_sequences WHERE sequence_name LIKE '%BOOKING%'")
sequences = [row for row in cur.fetchall()]
print("Booking sequences:", sequences)

cur.execute("SELECT trigger_name FROM user_triggers WHERE table_name = 'BOOKINGS'")
triggers = [row for row in cur.fetchall()]
print("Booking triggers:", triggers)

cur.close()
conn.close()
