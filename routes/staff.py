from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import db, User, Trek, Booking

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')



### STEP 1: Staff Dashboard

@staff_bp.route('/dashboard')
def dashboard():

    # Login check
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('auth.login'))

    # Role check
    if session.get('role') != 'staff':
        flash("Access denied!", "danger")
        return redirect(url_for('auth.login'))

    staff_id = session['user_id']

    # Assigned treks
    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=staff_id
    ).all()

    # Dashboard statistics
    total_assigned_treks = len(assigned_treks)

    total_trekkers = 0

    for trek in assigned_treks:
        total_trekkers += Booking.query.filter_by(
            trek_id=trek.id,
            status='Booked'
        ).count()

    return render_template(
        'staff/dashboard.html',
        assigned_treks=assigned_treks,
        total_assigned_treks=total_assigned_treks,
        total_trekkers=total_trekkers
    )



### STEP 2: Trek Details

@staff_bp.route('/trek/<int:trek_id>', methods=['GET', 'POST'])
def trek_details(trek_id):

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'staff':
        flash("Access denied!", "danger")
        return redirect(url_for('auth.login'))

    trek = Trek.query.get_or_404(trek_id)

    # Only assigned staff can manage
    if trek.assigned_staff_id != session['user_id']:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for('staff.dashboard'))

    if request.method == 'POST':

        available_slots = request.form.get('available_slots')
        status = request.form.get('status')

        # Update slots
        if available_slots:

            new_slots = int(available_slots)

            if new_slots < 0:
                flash("Available slots cannot be negative.", "danger")
                return redirect(
                    url_for('staff.trek_details', trek_id=trek.id)
                )

            if new_slots > trek.total_slots:
                flash("Available slots cannot exceed total slots.", "danger")
                return redirect(
                    url_for('staff.trek_details', trek_id=trek.id)
                )

            trek.available_slots = new_slots

        # Update status
        if status:
            trek.status = status

        db.session.commit()

        flash("Trek updated successfully!", "success")

        return redirect(
            url_for('staff.trek_details', trek_id=trek.id)
        )

    return render_template(
        'staff/trek_details.html',
        trek=trek
    )



### STEP 3: Participants

@staff_bp.route('/trek/<int:trek_id>/participants')
def participants(trek_id):

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'staff':
        flash("Access denied!", "danger")
        return redirect(url_for('auth.login'))

    trek = Trek.query.get_or_404(trek_id)

    # Security check
    if trek.assigned_staff_id != session['user_id']:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for('staff.dashboard'))

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    total_participants = Booking.query.filter_by(
        trek_id=trek.id,
        status='Booked'
    ).count()

    return render_template(
        'staff/participants.html',
        trek=trek,
        bookings=bookings,
        total_participants=total_participants
    )



### STEP 4: Staff Profile

@staff_bp.route('/profile')
def profile():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'staff':
        flash("Access denied!", "danger")
        return redirect(url_for('auth.login'))

    staff = User.query.get_or_404(session['user_id'])

    return render_template(
        'staff/profile.html',
        staff=staff
    )



### STEP 5: Edit Profile

@staff_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():

    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'staff':
        flash("Access denied!", "danger")
        return redirect(url_for('auth.login'))

    staff = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':

        # Update phone
        staff.phone = request.form.get('phone')

        # Update experience safely
        exp = request.form.get('experience', '0').strip()
        staff.experience = int(exp) if exp.isdigit() else 0

        # Save changes
        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('staff.profile'))

    return render_template(
        'staff/edit_profile.html',
        staff=staff
    )