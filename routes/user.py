from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_connection
from werkzeug.security import generate_password_hash
import datetime

user_bp = Blueprint('user', __name__)

# ---------------- PROFILE ---------------- #

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'customer_id' not in session:
        return redirect(url_for('auth.customer_login'))
    
    customer_id = session['customer_id']
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        new_password = request.form.get('password')

        try:
            if new_password:
                hashed_pw = generate_password_hash(new_password)
                cursor.execute("""
                    UPDATE customers 
                    SET customername = :1, phone = :2, address = :3, password = :4 
                    WHERE customer_id = :5
                """, (name, phone, address, hashed_pw, customer_id))
            else:
                 cursor.execute("""
                    UPDATE customers 
                    SET customername = :1, phone = :2, address = :3 
                    WHERE customer_id = :4
                """, (name, phone, address, customer_id))
            
            connection.commit()
            session['customer_name'] = name # Update session
            flash("Profile updated successfully! ✅")
        except Exception as e:
            flash(f"Error updating profile: {e}")
        finally:
            cursor.close()
            connection.close()
        
        return redirect(url_for('user.profile'))

    # GET REQUEST
    cursor.execute("SELECT customer_id, customername, phone, email, address FROM customers WHERE customer_id = :1", (customer_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('profile.html', user=user)


@user_bp.route('/wishlist')
def wishlist():
    if 'customer_id' not in session:
        flash("Please login to view wishlist")
        return redirect(url_for('auth.customer_login'))
    
    connection = get_connection()
    cursor = connection.cursor()
    # 3NF Update: Join with products table
    cursor.execute("""
        SELECT p.name, p.price, p.image_path, p.product_id 
        FROM wishlist w
        JOIN products p ON w.product_id = p.product_id
        WHERE w.customer_id = :1
    """, (session['customer_id'],))
    items = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('wishlist.html', items=items)

@user_bp.route('/toggle-wishlist', methods=['POST'])
def toggle_wishlist():
    if 'customer_id' not in session:
        return {"status": "error", "message": "Login required"}, 401

    data = request.json
    product_id = data.get('product_id')
    customer_id = session['customer_id']

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check if already in wishlist
        cursor.execute("SELECT wishlist_id FROM wishlist WHERE customer_id = :1 AND product_id = :2", (customer_id, product_id))
        existing_item = cursor.fetchone()

        if existing_item:
            # Remove from wishlist (Unlike)
            cursor.execute("DELETE FROM wishlist WHERE wishlist_id = :1", (existing_item[0],))
            action = "removed"
        else:
            # Add to wishlist (Like)
            cursor.execute("INSERT INTO wishlist (customer_id, product_id) VALUES (:1, :2)",
                           (customer_id, product_id))
            action = "added"

        connection.commit()
        return {"status": "success", "action": action}

    except Exception as e:
        print(f"Error toggling wishlist: {e}")
        return {"status": "error", "message": str(e)}, 500
    finally:
        cursor.close()
        connection.close()


# ---------------- BOOKINGS (RENT NOW) ---------------- #

@user_bp.route('/my-bookings')
def my_bookings():
    if 'customer_id' not in session:
        return redirect(url_for('auth.customer_login'))
        
    connection = get_connection()
    cursor = connection.cursor()
    # 3NF Update: Join with products table and booking_details
    cursor.execute("""
        SELECT b.booking_id, p.name, b.total_price, b.booking_date, b.rent_date, b.return_date, b.status, p.image_path 
        FROM bookings b
        JOIN booking_details bd ON b.booking_id = bd.booking_id
        JOIN products p ON bd.product_id = p.product_id
        WHERE b.customer_id = :1 
        ORDER BY b.booking_id DESC
    """, (session['customer_id'],))
    bookings = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('my_bookings.html', bookings=bookings)

@user_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'customer_id' not in session:
        return redirect(url_for('auth.customer_login'))
    
    connection = get_connection()
    cursor = connection.cursor()

    # Verify ownership and status
    cursor.execute("SELECT status FROM bookings WHERE booking_id = :1 AND customer_id = :2", (booking_id, session['customer_id']))
    booking = cursor.fetchone()

    if booking and booking[0] == 'Confirmed':
        cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_id = :1", (booking_id,))
        connection.commit()
        flash("Booking cancelled successfully.")
    else:
        flash("Cannot cancel this booking.")
    
    cursor.close()
    connection.close()
    return redirect(url_for('user.my_bookings'))

@user_bp.route('/payment', methods=['POST'])
def payment_page():
    if 'customer_id' not in session:
        flash("Please login to rent items")
        return redirect(url_for('auth.customer_login'))

    product_name = request.form.get('product_name')
    product_id = request.form.get('product_id')
    
    price_str = request.form.get('price', '0')
    price = int(''.join(filter(str.isdigit, str(price_str))))
    
    days_str = request.form.get('days', '1')
    days = int(''.join(filter(str.isdigit, str(days_str))))
    
    image = request.form.get('image')
    customer_name = request.form.get('customer_name')
    address = request.form.get('address')
    location = request.form.get('location')

    # Security Deposit Logic (e.g. fixed 2000)
    security_deposit = 2000
    total_amount = (price * days) + security_deposit

    return render_template('payment.html', 
                           product_name=product_name, 
                           product_id=product_id,
                           price=price, 
                           days=days, 
                           total_amount=total_amount,
                           image=image,
                           customer_name=customer_name,
                           address=address,
                           location=location)

@user_bp.route('/rent-now', methods=['POST'])
def rent_now():
    if 'customer_id' not in session:
        flash("Please login to rent items")
        return redirect(url_for('auth.customer_login'))

    product_name = request.form.get('product_name')
    product_id = request.form.get('product_id')

    # Clean the price string (remove '₹' and spaces)
    total_rent_str = request.form.get('total_rent', '0')
    total_rent = ''.join(filter(str.isdigit, total_rent_str))
    
    rent_days = request.form.get('days')
    phone = request.form.get('phone')
    address = request.form.get('address')
    location = request.form.get('location')
    
    # Simple date calculation for demo (Start = Today, End = Today + Days)
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=int(rent_days))
    
    # FORMAT DATES FOR SQL
    today_str = today.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    connection = get_connection()
    cursor = connection.cursor()

    # 1. CHECK AVAILABILITY (Prevent Double Booking) 🛡️
    # Logic: Overlap if (NewStart <= ExistingEnd) AND (NewEnd >= ExistingStart)
    cursor.execute("""
        SELECT b.booking_id FROM bookings b
        JOIN booking_details bd ON b.booking_id = bd.booking_id
        WHERE bd.product_id = :1 
        AND b.status = 'Confirmed' 
        AND (TO_DATE(:2, 'YYYY-MM-DD') <= b.return_date) 
        AND (TO_DATE(:3, 'YYYY-MM-DD') >= b.rent_date)
    """, (product_id, today_str, end_date_str))
    
    conflict = cursor.fetchone()
    if conflict:
        flash(f"⚠️ Sorry! {product_name} is already booked for these dates. Please try another item.")
        cursor.close()
        connection.close()
        return redirect(url_for('products.home'))

    # 2. PROCEED TO BOOK (3NF: Insert into both tables) 🚀
    cursor.execute("""
        INSERT INTO bookings (customer_id, total_price, booking_date, rent_date, return_date, status, phone, address, location)
        VALUES (:1, :2, SYSDATE, TO_DATE(:3, 'YYYY-MM-DD'), TO_DATE(:4, 'YYYY-MM-DD'), 'Confirmed', :5, :6, :7)
        RETURN booking_id INTO :8
    """, [session['customer_id'], total_rent, today_str, end_date_str, phone, address, location, cursor.var(int)])
    
    new_booking_id = cursor.vars[0].getvalue()[0]

    # Insert into booking_details
    cursor.execute("""
        INSERT INTO booking_details (booking_id, product_id, quantity, price)
        VALUES (:1, :2, 1, :3)
    """, (new_booking_id, product_id, total_rent))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    flash(f"Rent Confirmed! {product_name} booked successfully. 🎉")
    session['show_success_modal'] = True  # Trigger modal in my_bookings.html
    return redirect(url_for('user.my_bookings'))

# ---------------- CART ---------------- #

# ---------------- CART (DATABASE BACKED) ---------------- #

@user_bp.route('/cart')
def cart():
    if 'customer_id' not in session:
        flash("Please login to view your cart")
        return redirect(url_for('auth.customer_login'))

    connection = get_connection()
    cursor = connection.cursor()
    
    # Fetch cart items with product details
    cursor.execute("""
        SELECT c.cart_id, p.name, p.price, p.image_path, c.quantity, p.product_id 
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.customer_id = :1
    """, (session['customer_id'],))
    
    # Transform to list of dicts to match template expectation (or update template)
    # Template expects: item.name, item.price, item.image, item.product_id (maybe)
    # Let's see cart.html... usually it iterates. 
    # To be safe, let's pass objects that act like the session dicts but with IDs.
    
    rows = cursor.fetchall()
    cart_items = []
    for r in rows:
        cart_items.append({
            "cart_id": r[0],
            "name": r[1],
            "price": r[2], # numeric
            "image": r[3],
            "quantity": r[4],
            "product_id": r[5]
        })

    cursor.close()
    connection.close()
    
    return render_template('cart.html', cart=cart_items)

@user_bp.route('/add-to-cart-db', methods=['POST'])
def add_to_cart_db():
    if 'customer_id' not in session:
        flash("Please login to add items to cart")
        return redirect(url_for('auth.customer_login'))
        
    product_id = request.form.get('product_id')
    customer_id = session['customer_id']
    
    if customer_id == 99999:
        flash("Guest accounts cannot use the cart. Please register for a unique account.")
        return redirect(url_for('auth.customer_register'))
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Check if already in cart
        cursor.execute("SELECT cart_id, quantity FROM cart WHERE customer_id = :1 AND product_id = :2", (customer_id, product_id))
        existing = cursor.fetchone()
        
        if existing:
            # Update quantity (Optional, for now just notify)
            # cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE cart_id = :1", (existing[0],))
            flash("Item is already in your cart!")
        else:
            cursor.execute("INSERT INTO cart (customer_id, product_id, quantity) VALUES (:1, :2, 1)", (customer_id, product_id))
            flash("Item added to cart 🛒")
            
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        flash(f"Error adding to cart: {e}")
        
    return redirect(url_for('user.cart'))

@user_bp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    if 'customer_id' not in session:
        return redirect(url_for('auth.customer_login'))
        
    # We now expect cart_id or product_id. 
    # If legacy template sends index, we might break. 
    # Let's assume we update template to send cart_id.
    cart_id = request.form.get('cart_id')
    
    if cart_id:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM cart WHERE cart_id = :1", (cart_id,))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            flash(f"Error removing item: {e}")
            
    return redirect(url_for('user.cart'))
