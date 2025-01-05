import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Initialize SQLAlchemy instance globally
db = SQLAlchemy()

def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # App configuration (secret key and database URI)
    app.config['SECRET_KEY'] = os.getenv("APP_SECRET", 'some_secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'APP_DATABASE_URI', 
        'sqlite:///db.sqlite'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optionally disable modifications tracking

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    from app.models import User    
    # Ensure that the database tables are created once during app setup
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # Register blueprints for auth and main routes
    from app.routes.auth import auth_bp 
    app.register_blueprint(auth_bp)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.portfolio import portfolio_bp
    app.register_blueprint(portfolio_bp)
    

    return app
