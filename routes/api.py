from flask import Blueprint, jsonify, request
from models import Trek, Booking, User, db
from datetime import datetime

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/treks", methods=["GET"])
def get_treks():

    treks = Trek.query.all()

    data = []

    for trek in treks:

        data.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "price": trek.price,
            "available_slots": trek.available_slots,
            "status": trek.status
        })

    return jsonify(data)


@api_bp.route("/treks/<int:trek_id>", methods=["GET"])
def get_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    data = {
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "country": trek.country,
        "category": trek.category,
        "difficulty": trek.difficulty,
        "duration_days": trek.duration_days,
        "price": trek.price,
        "available_slots": trek.available_slots,
        "total_slots": trek.total_slots,
        "status": trek.status,
        "description": trek.description
    }

    return jsonify(data)

@api_bp.route("/users", methods=["GET"])
def get_users():

    users = User.query.filter_by(role="user").all()

    data = []

    for user in users:

        data.append({

            "id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status,
            "is_blacklisted": user.is_blacklisted

        })

    return jsonify(data)


@api_bp.route("/bookings", methods=["GET"])
def get_bookings():

    bookings = Booking.query.all()

    data = []

    for booking in bookings:

        data.append({

            "id": booking.id,
            "user": booking.user.name,
            "trek": booking.trek.name,
            "participants": booking.participants_count,
            "total_price": booking.total_price,
            "status": booking.status

        })

    return jsonify(data)


### 2. POST/api/treks- create a new trek
@api_bp.route("/treks", methods=["POST"])
def create_trek():

    # Get JSON data
    data = request.get_json()

    # Check if JSON is valid
    if not data:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    # Required fields
    required_fields = [
        "name",
        "location",
        "country",
        "category",
        "difficulty",
        "duration_days",
        "price",
        "total_slots",
        "start_date",
        "end_date"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    # Check duplicate trek
    existing = Trek.query.filter_by(name=data["name"]).first()

    if existing:
        return jsonify({
            "error": "Trek already exists"
        }), 400

    # Date validation
    try:
        start_date = datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        )

        end_date = datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        )

    except ValueError:
        return jsonify({
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400

    # Logical validation
    if end_date < start_date:
        return jsonify({
            "error": "End date cannot be before start date"
        }), 400

    # Create Trek
    new_trek = Trek(
        name=data["name"],
        location=data["location"],
        country=data["country"],
        is_international=data.get("is_international", False),
        category=data["category"],
        difficulty=data["difficulty"],
        duration_days=data["duration_days"],
        description=data.get("description", ""),
        price=data["price"],
        total_slots=data["total_slots"],
        available_slots=data["total_slots"],
        status="Open",
        start_date=start_date,
        end_date=end_date,
        best_season=data.get("best_season")
    )

    db.session.add(new_trek)
    db.session.commit()

    return jsonify({
        "message": "Trek created successfully",
        "trek_id": new_trek.id
    }), 201  

### PUT/api/treks/<int:trek_id> - update a trek
@api_bp.route("/treks/<int:trek_id>", methods=["PUT"])
def update_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    # Update fields if provided
    if "name" in data:
        trek.name = data["name"]

    if "location" in data:
        trek.location = data["location"]

    if "country" in data:
        trek.country = data["country"]

    if "category" in data:
        trek.category = data["category"]

    if "difficulty" in data:
        trek.difficulty = data["difficulty"]

    if "duration_days" in data:
        trek.duration_days = data["duration_days"]

    if "price" in data:
        trek.price = data["price"]

    if "total_slots" in data:
        trek.total_slots = data["total_slots"]

    if "available_slots" in data:
        trek.available_slots = data["available_slots"]

    # Status Validation
    valid_status = ["Pending", "Open", "Closed", "Completed"]

    if "status" in data:

        if data["status"] not in valid_status:
            return jsonify({
                "error": "Invalid trek status"
            }), 400

        trek.status = data["status"]

    if "description" in data:
        trek.description = data["description"]

    if "best_season" in data:
        trek.best_season = data["best_season"]

    if "is_international" in data:
        trek.is_international = data["is_international"]

    # Date Validation
    if "start_date" in data:
        try:
            trek.start_date = datetime.strptime(
                data["start_date"],
                "%Y-%m-%d"
            )
        except ValueError:
            return jsonify({
                "error": "Invalid start_date format. Use YYYY-MM-DD"
            }), 400

    if "end_date" in data:
        try:
            trek.end_date = datetime.strptime(
                data["end_date"],
                "%Y-%m-%d"
            )
        except ValueError:
            return jsonify({
                "error": "Invalid end_date format. Use YYYY-MM-DD"
            }), 400

    # Logical Validation
    if trek.end_date < trek.start_date:
        return jsonify({
            "error": "End date cannot be before start date"
        }), 400

    # Slot Validation
    if trek.available_slots > trek.total_slots:
        return jsonify({
            "error": "Available slots cannot exceed total slots"
        }), 400

    db.session.commit()

    return jsonify({
        "message": "Trek updated successfully"
    }), 200  


### DELETE/api/treks/<int:trek_id> - delete a trek
@api_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    # Check if any booking exists for this trek
    booking_exists = Booking.query.filter_by(trek_id=trek.id).first()

    if booking_exists:
        return jsonify({
            "error": "Cannot delete trek. Bookings already exist."
        }), 400

    db.session.delete(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek deleted successfully"
    }), 200