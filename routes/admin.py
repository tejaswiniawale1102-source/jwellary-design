from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
import os
from db import get_connection
from routes.auth import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Note: Some routes were not strictly under /admin in the original app (like admin-dashboard),
# but I will keep them consistent or adapt. 
# Original: /admin-dashboard -> I will keep it as /admin-dashboard by registering it on the app strictly or using root route here if needed, 
# BUT blueprint prefix is safer for /admin/xyz. 
# Let's handle top-level admin routes separately or just be careful. 
# I'll stick to 'admin_bp' handling anything related to admin.

# ---------------- ADMIN DASHBOARD ---------------- #

@admin_bp.route('/dashboard') # Becomes /admin/dashboard
@admin_required
def admin_dashboard():

    connection = get_connection()
    cursor = connection.cursor()
    
    # 1. Total Revenue (Approximate based on confirmed/returned bookings)
    cursor.execute("SELECT SUM(total_price) FROM bookings WHERE status IN ('Confirmed', 'Returned')")
    total_revenue = cursor.fetchone()[0] or 0

    # 2. Total Active Bookings
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Confirmed'")
    active_bookings = cursor.fetchone()[0] or 0

    # 3. Bookings by Category (For Pie Chart)
    cursor.execute("""
        SELECT p.category, COUNT(b.booking_id) 
        FROM bookings b
        JOIN booking_details bd ON b.booking_id = bd.booking_id
        JOIN products p ON bd.product_id = p.product_id
        GROUP BY p.category
    """)
    category_data = cursor.fetchall()
    
    # 4. Revenue by Category (For Bar Chart)
    cursor.execute("""
        SELECT p.category, SUM(b.total_price) 
        FROM bookings b
        JOIN booking_details bd ON b.booking_id = bd.booking_id
        JOIN products p ON bd.product_id = p.product_id
        WHERE b.status IN ('Confirmed', 'Returned')
        GROUP BY p.category
    """)
    revenue_data = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    # Convert data for Chart.js
    categories = [row[0] for row in category_data]
    booking_counts = [row[1] for row in category_data]
    revenue_counts = [row[1] for row in revenue_data]

    return render_template('admin_dashboard.html', 
                         total_revenue=total_revenue, 
                         active_bookings=active_bookings,
                         categories=categories,
                         booking_counts=booking_counts,
                         revenue_counts=revenue_counts)


# ---------------- ADMIN ADD ITEM ---------------- #

@admin_bp.route('/add-item', methods=['GET', 'POST'])
@admin_required
def add_new_item():

    if request.method == 'POST':
        try:
            name = request.form['name']
            category = request.form['category']
            price = request.form['price']
            description = request.form['description']
            image = request.files['image']

            if image:
                filename = secure_filename(image.filename)
                # Ensure using current_app to get config
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_path = url_for('static', filename='images/' + filename)
            else:
                image_path = ""

            connection = get_connection()
            cursor = connection.cursor()
            
            # Fix for ORA-00001: Get the next ID manually to ensure no conflict
            cursor.execute("SELECT COALESCE(MAX(product_id), 0) + 1 FROM products")
            new_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO products (product_id, name, category, price, image_path, description)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, (new_id, name, category, price, image_path, description))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            flash("Product added successfully!")
            return redirect(url_for('admin.admin_dashboard'))

        except Exception as e:
            flash(f"Error adding product: {e}")
            return redirect(url_for('admin.add_new_item'))

    return render_template('add_item.html')


# ---------------- ADMIN - DELETE ITEM ---------------- #

@admin_bp.route('/delete-items')
@admin_required
def view_delete_items():
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT product_id, name, price, image_path, category FROM products ORDER BY product_id DESC")
        products = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error fetching products: {e}")
        products = []
        
    return render_template('delete_items.html', products=products)

@admin_bp.route('/delete-item/<int:product_id>', methods=['POST'])
@admin_required
def delete_item(product_id):

    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # 1. Delete related reviews
        cursor.execute("DELETE FROM reviews WHERE product_id = :1", (product_id,))
        
        # 2. Delete related cart items
        cursor.execute("DELETE FROM cart WHERE product_id = :1", (product_id,))
        
        # 3. Delete related booking details
        cursor.execute("DELETE FROM booking_details WHERE product_id = :1", (product_id,))
        
        # 4. Delete the product itself
        cursor.execute("DELETE FROM products WHERE product_id = :1", (product_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        flash("Item and related records deleted successfully.")
    except Exception as e:
        print(f"Error deleting product: {e}")
        flash(f"Error deleting item: {e}")

    return redirect(url_for('admin.view_delete_items'))


# ---------------- ADMIN VIEW BOOKINGS ---------------- #

@admin_bp.route('/view-bookings')
@admin_required
def view_all_bookings():

    try:
        connection = get_connection()
        cursor = connection.cursor()
        # Join bookings with customers and booking_details to get the customer and product name
        cursor.execute("""
            SELECT b.booking_id, NVL(c.customername, 'Guest/Unknown'), NVL(p.name, 'Product Removed/Unknown'), b.total_price, b.rent_date, b.return_date, b.status, bd.product_id 
            FROM bookings b 
            LEFT JOIN customers c ON b.customer_id = c.customer_id 
            LEFT JOIN booking_details bd ON b.booking_id = bd.booking_id
            LEFT JOIN products p ON bd.product_id = p.product_id
            ORDER BY b.booking_id DESC
        """)
        bookings = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        bookings = []

    return render_template('admin_bookings.html', bookings=bookings)

@admin_bp.route('/mark-returned/<int:booking_id>', methods=['POST'])
@admin_required
def mark_returned(booking_id):
        
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("UPDATE bookings SET status = 'Returned' WHERE booking_id = :1", (booking_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        flash(f"Booking #{booking_id} marked as Returned! ✅")
        return redirect(url_for('admin.view_all_bookings'))
        
    except Exception as e:
        return f"Error: {e}"

@admin_bp.route('/cancel-booking-admin/<int:booking_id>', methods=['POST'])
@admin_required
def cancel_booking_admin(booking_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_id = :1", (booking_id,))
        connection.commit()
        cursor.close()
        connection.close()
        flash(f"Booking #{booking_id} has been Cancelled.")
    except Exception as e:
        flash(f"Error cancelling booking: {e}")
    return redirect(url_for('admin.view_all_bookings'))

@admin_bp.route('/delete-booking-admin/<int:booking_id>', methods=['POST'])
@admin_required
def delete_booking_admin(booking_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM bookings WHERE booking_id = :1", (booking_id,))
        connection.commit()
        cursor.close()
        connection.close()
        flash(f"Booking #{booking_id} DELETED permanently.")
    except Exception as e:
        flash(f"Error deleting booking: {e}")
    return redirect(url_for('admin.view_all_bookings'))
