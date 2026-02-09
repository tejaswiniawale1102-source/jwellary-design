from flask import Flask, session
from routes.auth import auth_bp
from routes.products import products_bp
from routes.user import user_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = "renteasy_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/images'

# Register Blueprints
app.register_blueprint(products_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
# Note: Admin blueprint has url_prefix='/admin' in its definition, 
# but some legacy routes might need adjustment. 
# For now, let's keep it clean.
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

