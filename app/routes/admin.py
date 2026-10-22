from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Booking, Destination, TourPackage, User

admin_bp = Blueprint("admin", __name__)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template(
        "admin.html",
        destination_count=Destination.query.count(),
        package_count=TourPackage.query.count(),
        booking_count=Booking.query.count(),
        user_count=User.query.count(),
        bookings=Booking.query.order_by(Booking.created_at.desc()).limit(20).all(),
        destinations=Destination.query.order_by(Destination.name).all()
    )


@admin_bp.route("/booking/<int:booking_id>/status", methods=["POST"])
@admin_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    status = request.form.get("status", "")
    if status not in {"Pending", "Confirmed", "Cancelled"}:
        flash("Invalid booking status.", "error")
    else:
        booking.status = status
        db.session.commit()
        flash(f"Booking #{booking.id} updated.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/destination/add", methods=["POST"])
@admin_required
def add_destination():
    try:
        name = request.form.get("name", "").strip()
        region = request.form.get("region", "").strip()
        category = request.form.get("category", "Nature").strip()
        cost = int(request.form.get("estimated_cost", "5000"))
        days = int(request.form.get("min_days", "2"))
        if not name or not region or cost < 0 or not 1 <= days <= 60:
            raise ValueError
    except ValueError:
        flash("Enter a name, region, non-negative cost, and valid duration.", "error")
        return redirect(url_for("admin.dashboard"))
    destination = Destination(
        name=name, region=region, country=request.form.get("country", "India").strip() or "India",
        description=request.form.get("description", "").strip() or f"Explore {name}.",
        category=category, activities=request.form.get("activities", "nature").strip(),
        climate=request.form.get("climate", "Warm"), estimated_cost=cost,
        min_days=days, max_days=max(days, min(days + 2, 60)),
        image_url=request.form.get("image_url", "").strip()
    )
    db.session.add(destination)
    db.session.flush()
    db.session.add(TourPackage(
        destination_id=destination.id, title=f"{name} Explorer", duration_days=days,
        price=cost, description=f"A sample package to explore {name}.",
        inclusions="Suggested itinerary, sightseeing, travel support"
    ))
    db.session.commit()
    flash(f"{name} and a sample package were added.", "success")
    return redirect(url_for("admin.dashboard"))
