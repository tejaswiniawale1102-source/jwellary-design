from db import get_connection

def show_menu():
    print("\n" + "="*80)
    print("DATABASE NORMALIZATION DEMONSTRATION - RentEasyIndia")
    print("="*80)
    print("\n1. Show 1NF (Atomic Values)")
    print("2. Show 2NF (No Partial Dependencies)")
    print("3. Show 3NF (No Transitive Dependencies)")
    print("4. Show All Normalization Forms")
    print("5. Exit")
    print("-"*80)

def show_1nf():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("1NF DEMONSTRATION: All values are ATOMIC (indivisible)")
    print("="*80)
    
    print("\nPRODUCTS Table Sample:")
    print("-"*80)
    cur.execute("SELECT product_id, name, category, price FROM products WHERE ROWNUM <= 5")
    print(f"{'ID':<5} {'Name':<35} {'Category':<15} {'Price':<10}")
    print("-"*80)
    for row in cur.fetchall():
        print(f"{row[0]:<5} {row[1]:<35} {row[2]:<15} Rs.{row[3]:<10.0f}")
    
    print("\nCONCLUSION: Each cell contains a SINGLE value (not a list or set)")
    print("            Example: Category is 'Jewelry', not 'Jewelry, Decor, Mens'")
    cur.close()
    conn.close()

def show_2nf():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("2NF DEMONSTRATION: No Partial Dependencies")
    print("="*80)
    
    print("\nBOOKING_DETAILS has composite key (booking_id + product_id)")
    print("All attributes must depend on BOTH keys, not just one")
    print("-"*80)
    cur.execute("""
        SELECT bd.booking_id, bd.product_id, bd.quantity, bd.price
        FROM booking_details bd
        WHERE ROWNUM <= 5
    """)
    print(f"{'Booking ID':<12} {'Product ID':<12} {'Quantity':<10} {'Price':<10}")
    print("-"*80)
    for row in cur.fetchall():
        print(f"{row[0]:<12} {row[1]:<12} {row[2]:<10} Rs.{row[3]:<10.0f}")
    
    print("\nCONCLUSION: 'quantity' and 'price' depend on BOTH booking_id AND product_id")
    print("            (Not just one of them - no partial dependency!)")
    cur.close()
    conn.close()

def show_3nf():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("3NF DEMONSTRATION: No Transitive Dependencies")
    print("="*80)
    
    print("\nBOOKINGS table stores customer_id, NOT customer name")
    print("Customer name is retrieved via JOIN from CUSTOMERS table")
    print("-"*80)
    cur.execute("""
        SELECT b.booking_id, b.customer_id, c.customername, b.total_price
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        WHERE ROWNUM <= 5
    """)
    print(f"{'Booking':<10} {'Cust ID':<10} {'Customer Name':<25} {'Total':<10}")
    print("-"*80)
    for row in cur.fetchall():
        print(f"{row[0]:<10} {row[1]:<10} {row[2]:<25} Rs.{row[3]:<10.0f}")
    
    print("\nCONCLUSION: Customer name is NOT stored in BOOKINGS table")
    print("            It's in CUSTOMERS table - no transitive dependency!")
    print("            (customername doesn't depend on booking_id through customer_id)")
    cur.close()
    conn.close()

def show_all():
    show_1nf()
    input("\nPress Enter to continue to 2NF...")
    show_2nf()
    input("\nPress Enter to continue to 3NF...")
    show_3nf()
    print("\n" + "="*80)
    print("DATABASE IS PROPERLY NORMALIZED TO 3NF!")
    print("="*80)

# Main program
while True:
    show_menu()
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        show_1nf()
    elif choice == '2':
        show_2nf()
    elif choice == '3':
        show_3nf()
    elif choice == '4':
        show_all()
    elif choice == '5':
        print("\nThank you for using the Normalization Demonstration Tool!")
        break
    else:
        print("\nInvalid choice! Please enter 1-5.")
    
    input("\nPress Enter to continue...")
