from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import get_connection

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            flash("Please login to access this page.")
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------- CUSTOMER REGISTER ---------------- #

@auth_bp.route('/customer-register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        password = request.form.get('password', '').strip()

        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Check for existing user (Case Insensitive Email or Duplicate Phone)
            cursor.execute("SELECT customer_id FROM customers WHERE LOWER(email) = LOWER(:1)", (email,))
            if cursor.fetchone():
                flash("This email is already registered! Please login.")
                return redirect(url_for('auth.customer_login'))

            cursor.execute("SELECT customer_id FROM customers WHERE phone = :1", (phone,))
            if cursor.fetchone():
                flash("This phone number is already registered! Please use another.")
                return redirect(url_for('auth.customer_login'))

            new_id_var = cursor.var(int)
            cursor.execute("""
                INSERT INTO customers (customer_id, customername, phone, email, address, password)
                VALUES (customers_seq.NEXTVAL, :1, :2, :3, :4, :5)
                RETURNING customer_id INTO :6
            """, (name, phone, email, address, generate_password_hash(password), new_id_var))

            new_customer_id = new_id_var.getvalue()[0]

            # ID already retrieved via RETURNING
            
            connection.commit()
        except Exception as e:
            print(f"Registration Error: {e}")
            flash(f"Error during registration: {e}") # Let the user know the real error
            return redirect(url_for('auth.customer_register'))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'connection' in locals(): connection.close()

        # AUTO-LOGIN after registration
        if new_customer_id:
             session['customer_id'] = new_customer_id
             session['customer_name'] = name
             flash(f"Welcome {name}! Registration Successful 🎉")
             return redirect(url_for('products.home'))
        else:
             flash("Registration failed. Please try again or contact support.")
             return redirect(url_for('auth.customer_register'))

    return render_template('customer_register.html')


# ---------------- CUSTOMER LOGIN ---------------- #

@auth_bp.route('/customer-login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        connection = get_connection()
        cursor = connection.cursor()

        # Case-insensitive search
        cursor.execute("""
            SELECT customer_id, customername, password FROM customers
            WHERE LOWER(email) = LOWER(:1)
        """, (email,))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            # Check Password (Hash or Plain Text for legacy)
            stored_pass = user[2]
            is_valid = False
            
            if stored_pass:
                # 1. Try Hash
                try:
                    if check_password_hash(stored_pass, password):
                        is_valid = True
                except:
                    pass # Not a valid hash
                
                # 2. Try Plain Text (Verification for old users)
                if not is_valid and stored_pass == password:
                    is_valid = True

            if is_valid:
                session['customer_id'] = user[0]
                session['customer_name'] = user[1]
                flash(f"Welcome {user[1]}! Login Successful 🎉")
                return redirect(url_for('products.home'))
            else:
                flash("Incorrect Password! Please try again.")
                return redirect(url_for('auth.customer_login'))
        else:
            flash("Account not found. Please register first.")
            return redirect(url_for('auth.customer_register'))

    return render_template('customer_login.html')


# ---------------- LOGOUT ---------------- #

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('products.home'))


# ---------------- ADMIN LOGIN ---------------- #

@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        print(f"Attempting login for: '{username}'") # Debug print

        connection = get_connection()
        cursor = connection.cursor()

        try:
            # Case-insensitive search
            cursor.execute("SELECT admin_id, username, password_hash FROM admins WHERE LOWER(username) = LOWER(:1)", (username,))
            admin_user = cursor.fetchone()
            
            if admin_user:
                print(f"User found: {admin_user[1]}") # Debug print
                stored_hash = admin_user[2]
                if check_password_hash(stored_hash, password):
                    session['admin'] = True
                    session['admin_id'] = admin_user[0]
                    session['admin_name'] = admin_user[1].split('@')[0]
                    flash("Admin Login Successful")
                    return redirect(url_for('admin.admin_dashboard'))
                else:
                    print("Password verification failed") # Debug print
                    flash("Invalid Password")
            else:
                print("User not found in DB") # Debug print
                flash("Admin not found")
                
        except Exception as e:
            print(f"Login Error: {e}")
            flash(f"Error: {e}")
            
        finally:
            cursor.close()
            connection.close()
            
        return redirect(url_for('auth.admin_login'))

    return render_template('admin_login.html')
