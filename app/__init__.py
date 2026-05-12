from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flasgger import Swagger


swagger = Swagger()
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    swagger.init_app(app)

    # connect extensions to the app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.products import products_bp
    from app.routes.inventory import inventory_bp
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    # simple check route
    @app.route('/')
    def index():
        return jsonify({
            "status": "success",
            "message": "API is running"
        })
    
    # frontend routes
    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')

    return app