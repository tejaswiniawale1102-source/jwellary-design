from flask import Blueprint, render_template, request, url_for, jsonify, session, flash, redirect
from db import get_connection

products_bp = Blueprint('products', __name__)

# ---------------- HELPER ---------------- #

def get_recommendations(category, current_product_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        # Find 4 items in same category, excluding current
        cursor.execute("SELECT * FROM products WHERE category = :1 AND product_id != :2 FETCH FIRST 4 ROWS ONLY", (category, current_product_id))
        items = cursor.fetchall()
        cursor.close()
        connection.close()
        return items
    except:
        return []

def get_products_by_category(category_name):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE category = :1 ORDER BY product_id ASC", (category_name,))
        products = cursor.fetchall()
        cursor.close()
        connection.close()
        return products
    except:
        return []

# ---------------- ROUTES ---------------- #

@products_bp.route('/')
def home():
    return render_template('index.html')


@products_bp.route('/categories')
def categories():
    return render_template('categories.html')

@products_bp.route('/search')
def search():
    query = request.args.get('q', '')
    products = []
    if query:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            # Case insensitive search
            cursor.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(:1)", ('%' + query + '%',))
            products = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Search error: {e}")
            
    return render_template('search_results.html', products=products, query=query)

@products_bp.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    products = []
    if query:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            # Select specific fields
            cursor.execute("SELECT product_id, name, price, image_path, category, market_price FROM products WHERE LOWER(name) LIKE LOWER(:1)", ('%' + query + '%',))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            
            # Convert to list of dicts
            products = [{'id': r[0], 'name': r[1], 'price': r[2], 'image': r[3], 'category': r[4], 'market_price': r[5]} for r in rows]
        except Exception as e:
            print(f"API Search error: {e}")
            return jsonify({'error': str(e)}), 500
            
    return jsonify(products)

@products_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    # 1. Fetch Product Details
    cursor.execute("SELECT * FROM products WHERE product_id = :1", (product_id,))
    product = cursor.fetchone()

    # 2. Fetch Reviews with Customer Name
    cursor.execute("""
        SELECT r.*, c.customername 
        FROM reviews r 
        JOIN customers c ON r.customer_id = c.customer_id 
        WHERE r.product_id = :1 
        ORDER BY r.created_at DESC
    """, (product_id,))
    reviews = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # 3. Recommendations
    recommendations = get_recommendations(product[2], product_id)

    if product:
        return render_template('product_detail.html', product=product, reviews=reviews, recommendations=recommendations)
    else:
        return "Product not found", 404

@products_bp.route('/add-review/<int:product_id>', methods=['POST'])
def add_review(product_id):
    if 'customer_id' not in session:
        flash("Please login to review products.")
        return redirect(url_for('auth.customer_login'))
    
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    verdict = request.form.get('verdict') # New field
    customer_id = session['customer_id']

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO reviews (product_id, customer_id, rating, comment_text, verdict) VALUES (:1, :2, :3, :4, :5)",
                       (product_id, customer_id, rating, comment, verdict))
        connection.commit()
        cursor.close()
        connection.close()
        flash("Review added successfully! ⭐")
    except Exception as e:
        flash(f"Error adding review: {e}")
        
    return redirect(url_for('products.product_detail', product_id=product_id))

@products_bp.route('/jwelery')
def jewelry():
    products = get_products_by_category('Jewelry')
    return render_template('jwelery.html', products=products)

@products_bp.route('/dresses')
def dresses():
    return render_template('apparel_portal.html')

@products_bp.route('/womens_collection')
def womens_collection():
    products = get_products_by_category('Womens')
    return render_template('womens.html', products=products)

@products_bp.route('/mens')
def mens():
    products = get_products_by_category('Mens')
    return render_template('mens.html', products=products)

@products_bp.route('/womens')
def womens():
    products = get_products_by_category('Womens')
    return render_template('womens.html', products=products)

@products_bp.route('/decor')
def decor():
    products = get_products_by_category('Decor')
    return render_template('decor.html', products=products)

@products_bp.route('/event_tools')
def event_tools():
    products = get_products_by_category('Event Tools')
    return render_template('event_tools.html', products=products)


@products_bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')


@products_bp.route('/about')
def about_us():
    return render_template('about_us.html')


@products_bp.route('/support')
def support():
    return render_template('support.html')


@products_bp.route('/ourstores')
def ourstores():
    return render_template('ourstores.html')
