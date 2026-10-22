from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(80), default="India")
    region = db.Column(db.String(100), default="")
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="Nature")
    activities = db.Column(db.String(255), default="nature")
    climate = db.Column(db.String(50), default="Warm")
    estimated_cost = db.Column(db.Integer, default=5000)
    min_days = db.Column(db.Integer, default=2)
    max_days = db.Column(db.Integer, default=4)
    image_url = db.Column(db.String(500), default="")
    packages = db.relationship("TourPackage", backref="destination", cascade="all, delete-orphan", lazy=True)


class TourPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destination.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    duration_days = db.Column(db.Integer, default=2)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default="")
    inclusions = db.Column(db.String(500), default="")


class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    budget = db.Column(db.Integer, default=10000)
    duration_days = db.Column(db.Integer, default=3)
    interests = db.Column(db.String(255), default="nature")
    climate = db.Column(db.String(50), default="Any")
    travel_style = db.Column(db.String(50), default="Balanced")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey("tour_package.id"), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    travellers = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), default="Pending", nullable=False)
    notes = db.Column(db.String(500), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    package = db.relationship("TourPackage", backref="bookings")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("destination.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
