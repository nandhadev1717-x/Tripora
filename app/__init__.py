import os
from datetime import date
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "tripora.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.bookings import bookings_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        from app import models
        db.create_all()
        seed_demo_data()
        create_demo_admin()

    return app


def seed_demo_data():
    from app.models import Destination, TourPackage
    if Destination.query.count():
        return
    destinations = [
        Destination(name="Munnar", country="India", region="Kerala", description="Rolling tea gardens, misty hills, waterfalls, and peaceful nature trails.", category="Nature", activities="hiking,photography,nature,relaxation", climate="Cool", estimated_cost=6500, min_days=2, max_days=4, image_url="https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80"),
        Destination(name="Goa", country="India", region="Goa", description="Sunny beaches, coastal food, lively markets, and relaxed seaside days.", category="Beach", activities="beach,food,nightlife,relaxation,photography", climate="Warm", estimated_cost=9000, min_days=3, max_days=5, image_url="https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80"),
        Destination(name="Jaipur", country="India", region="Rajasthan", description="Colourful bazaars, historic forts, palaces, and rich local culture.", category="Culture", activities="culture,history,food,shopping,photography", climate="Warm", estimated_cost=8000, min_days=2, max_days=4, image_url="https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1200&q=80"),
        Destination(name="Manali", country="India", region="Himachal Pradesh", description="Mountain scenery, pine forests, scenic drives, and outdoor adventures.", category="Adventure", activities="hiking,adventure,nature,photography", climate="Cold", estimated_cost=12000, min_days=4, max_days=6, image_url="https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80"),
        Destination(name="Alappuzha", country="India", region="Kerala", description="Backwaters, houseboats, village landscapes, and a slow-paced escape.", category="Relaxation", activities="relaxation,nature,food,photography", climate="Warm", estimated_cost=5500, min_days=2, max_days=3, image_url="https://images.unsplash.com/photo-1602934445884-da0fa1c9d3b3?auto=format&fit=crop&w=1200&q=80"),
        Destination(name="Dubai", country="UAE", region="Middle East", description="Modern architecture, desert experiences, shopping, and city attractions.", category="City", activities="shopping,adventure,food,photography,culture", climate="Warm", estimated_cost=35000, min_days=4, max_days=6, image_url="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80"),
        Destination(name="Bali", country="Indonesia", region="Indonesia", description="Tropical beaches, lush landscapes, temples, and wellness experiences.", category="Beach", activities="beach,nature,culture,relaxation,photography", climate="Warm", estimated_cost=42000, min_days=5, max_days=8, image_url="https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80"),
        Destination(name="Ooty", country="India", region="Tamil Nadu", description="Tea estates, gardens, mountain railways, and refreshing hill-station weather.", category="Nature", activities="nature,relaxation,photography,food", climate="Cool", estimated_cost=7000, min_days=2, max_days=4, image_url="https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=80"),
    ]
    db.session.add_all(destinations)
    db.session.flush()
    for d in destinations:
        db.session.add(TourPackage(
            destination_id=d.id,
            title=f"{d.name} Explorer",
            duration_days=d.min_days,
            price=d.estimated_cost,
            description=f"A sample {d.min_days}-day package to explore {d.name}.",
            inclusions="Suggested itinerary, local sightseeing, travel support"
        ))
    db.session.commit()


def create_demo_admin():
    from app.models import User
    admin = User.query.filter_by(email="admin@tripora.local").first()
    if not admin:
        admin = User(name="Tripora Admin", email="admin@tripora.local", is_admin=True)
        admin.set_password("TriporaAdmin123!")
        db.session.add(admin)
        db.session.commit()
