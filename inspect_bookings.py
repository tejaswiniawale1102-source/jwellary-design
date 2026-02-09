import oracledb
from db import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type, data_length FROM user_tab_columns WHERE table_name = 'BOOKINGS'")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
