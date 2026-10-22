from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Booking, TourPackage

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/create/<int:package_id>", methods=["GET", "POST"])
@login_required
def create(package_id):
    package = TourPackage.query.get_or_404(package_id)
    if request.method == "POST":
        try:
            travel_date = date.fromisoformat(request.form.get("travel_date", ""))
            travellers = int(request.form.get("travellers", "1"))
            if travel_date < date.today() or not 1 <= travellers <= 20:
                raise ValueError
        except ValueError:
            flash("Choose a valid future date and between 1 and 20 travellers.", "error")
            return render_template("booking_form.html", package=package)
        booking = Booking(
            user_id=current_user.id, package_id=package.id, travel_date=travel_date,
            travellers=travellers, total_price=package.price * travellers,
            notes=request.form.get("notes", "").strip()[:500]
        )
        db.session.add(booking)
        db.session.commit()
        flash("Booking request submitted! The agency will confirm it.", "success")
        return redirect(url_for("bookings.mine"))
    return render_template("booking_form.html", package=package)


@bookings_bp.route("/mine")
@login_required
def mine():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("my_bookings.html", bookings=bookings)
