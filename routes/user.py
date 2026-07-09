from flask import Blueprint,url_for,redirect,flash,session,request,render_template
from models import Booking,Trek, db, User
user_bp=Blueprint('user', __name__,url_prefix='/user')

### STEP 1 : User Dashboard

@user_bp.route('/dashboard')
def dashboard():

    # Check Login
    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    # Check User Role
    if session.get("role") != "user":
        flash("Access Denied", "danger")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    # Total Bookings
    total_bookings = Booking.query.filter_by(user_id=user_id).count()

    # Upcoming Treks
    upcoming_treks = (
        Booking.query
        .filter_by(user_id=user_id)
        .order_by(Booking.booking_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'user/dashboard.html',
        total_bookings=total_bookings,
        upcoming_treks=upcoming_treks
    )

# =========================================================
# STEP 2 : Browse All Treks
# =========================================================
@user_bp.route('/treks')
def browse_treks():

    # Check Login
    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    # Check User Role
    if session.get("role") != "user":
        flash("Access Denied", "danger")
        return redirect(url_for('auth.login'))

    # Search
    search = request.args.get('search', '').strip()

    # Filters
    difficulty = request.args.get('difficulty', '')
    location = request.args.get('location', '')

    treks = Trek.query.filter(Trek.status != 'Completed')

    # Search by Name or Location
    if search:
        treks = treks.filter(
            (Trek.name.ilike(f"%{search}%")) |
            (Trek.location.ilike(f"%{search}%"))
        )

    # Difficulty Filter
    if difficulty:
        treks = treks.filter(Trek.difficulty == difficulty)

    # Location Filter
    if location:
        treks = treks.filter(Trek.location == location)

    treks = treks.order_by(Trek.start_date.asc()).all()

    # Dropdown values
    difficulties = [
        row[0] for row in db.session.query(Trek.difficulty).distinct().all()
    ]

    locations = [
        row[0] for row in db.session.query(Trek.location).distinct().all()
    ]

    return render_template(
        'user/treks.html',
        treks=treks,
        difficulties=difficulties,
        locations=locations
    )

### STEP 3 : Trek Details

@user_bp.route('/trek/<int:trek_id>')
def trek_details(trek_id):

    # Check Login
    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    # Check User Role
    if session.get("role") != "user":
        flash("Access Denied", "danger")
        return redirect(url_for('auth.login'))

    trek = Trek.query.get_or_404(trek_id)

    return render_template(
        "user/trek_details.html",
        trek=trek
    )

### STEP 4 : Book Trek

@user_bp.route('/book/<int:trek_id>', methods=['GET', 'POST'])
def book_trek(trek_id):

    # Login Check
    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    # User Check
    if session.get('role') != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('auth.login'))

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":
        flash("This trek is not open for booking!", "danger")
        return redirect(url_for("user.trek_details", trek_id=trek.id))


    if request.method == 'POST':

        participants = int(request.form['participants'])

        existing = Booking.query.filter_by(
        user_id=session['user_id'],
        trek_id=trek.id,
        status="Booked"
        ).first()

        if existing:
            flash("You have already booked this trek.", "warning")
            return redirect(url_for('user.my_bookings'))
        
        # Existing validation
        if participants <= 0:
            flash("Invalid participant count!", "danger")
            return redirect(url_for('user.book_trek', trek_id=trek.id))

        if participants > trek.available_slots:
            flash("Not enough slots available!", "danger")
            return redirect(url_for('user.book_trek', trek_id=trek.id))

        total_price = participants * trek.price

        booking = Booking(
            user_id=session['user_id'],
            trek_id=trek.id,
            participants_count=participants,
            total_price=total_price,
            status="Booked"
        )

        db.session.add(booking)

        trek.available_slots -= participants

        db.session.commit()

        flash("Trek booked successfully!", "success")

        return redirect(url_for('user.my_bookings'))

    return render_template(
        "user/book_trek.html",
        trek=trek
    )


### STEP 5 : My Bookings

@user_bp.route('/my_bookings')
def my_bookings():

    # Check Login
    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    # Check User Role
    if session.get("role") != "user":
        flash("Access Denied!", "danger")
        return redirect(url_for('auth.login'))

    bookings = (
        Booking.query
        .filter_by(user_id=session['user_id'])
        .order_by(Booking.booking_date.desc())
        .all()
    )

    return render_template(
        "user/my_bookings.html",
        bookings=bookings
    )


### STEP 6 : Cancel Booking

@user_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):

    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    if session.get("role") != "user":
        flash("Access Denied!", "danger")
        return redirect(url_for('auth.login'))

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != session['user_id']:
        flash("Access Denied!", "danger")
        return redirect(url_for('user.my_bookings'))

    if booking.status != "Booked":
        flash("Booking already cancelled.", "warning")
        return redirect(url_for('user.my_bookings'))

    booking.status = "Cancelled"

    booking.trek.available_slots += booking.participants_count

    db.session.commit()

    flash("Booking cancelled successfully!", "success")

    return redirect(url_for('user.my_bookings'))


### STEP 7 : User Profile
@user_bp.route('/profile')
def profile():

    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(session['user_id'])

    return render_template(
        'user/profile.html',
        user=user
    )


### STEP 8 : Edit Profile

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():

    # Check Login
    if 'user_id' not in session:
        flash("Please Login First!", "danger")
        return redirect(url_for('auth.login'))

    # Check Role
    if session.get('role') != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':

        user.phone = request.form.get('phone')

        db.session.commit()

        flash("Profile Updated Successfully!", "success")

        return redirect(url_for('user.profile'))

    return render_template(
        'user/edit_profile.html',
        user=user
    )