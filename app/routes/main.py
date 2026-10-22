from flask import Blueprint, render_template, request
from app.models import Destination
from app.services.recommendation import recommend_destinations

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    destinations = Destination.query.order_by(Destination.name).limit(6).all()
    return render_template("index.html", destinations=destinations)


@main_bp.route("/destinations")
def destinations():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    query = Destination.query
    if search:
        query = query.filter(Destination.name.ilike(f"%{search}%") | Destination.region.ilike(f"%{search}%"))
    if category:
        query = query.filter_by(category=category)
    items = query.order_by(Destination.name).all()
    categories = sorted({d.category for d in Destination.query.all()})
    return render_template("destinations.html", destinations=items, categories=categories, search=search, selected_category=category)


@main_bp.route("/destinations/<int:destination_id>")
def destination_detail(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    return render_template("destination_detail.html", destination=destination)


@main_bp.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    results = None
    values = {"budget": "10000", "duration_days": "3", "interests": "nature,photography", "climate": "Any"}
    if request.method == "POST":
        values = {key: request.form.get(key, default) for key, default in values.items()}
        try:
            budget = max(0, min(int(values["budget"]), 10000000))
            duration = max(1, min(int(values["duration_days"]), 60))
        except ValueError:
            budget, duration = 10000, 3
        results = recommend_destinations(
            Destination.query.all(), budget, duration, values["interests"], values["climate"]
        )
    return render_template("recommendations.html", results=results, values=values)
