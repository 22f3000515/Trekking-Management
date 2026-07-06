# STEP 1: Imports
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import User, Trek, Booking, db
from datetime import datetime

# STEP 2: Create Admin Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# STEP 3: Admin Dashboard Route
# URL = /admin/dashboard

@admin_bp.route('/dashboard')
def dashboard():

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    # Check admin access
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    # Count dashboard stats
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='user').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()

    # Render dashboard page
    return render_template(
        'admin/dashboard.html',
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )



# STEP 4: Manage Treks Route
# URL = /admin/treks

# GET = Show page & POST = Add trek
@admin_bp.route('/treks', methods=['GET', 'POST'])  
def manage_treks():

    #  Check login
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    #  Check admin access
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    # If form submitted
    if request.method == 'POST':

        # Get form data
        name = request.form['name']
        location = request.form['location']
        country = request.form['country']
        category = request.form['category']
        difficulty = request.form['difficulty']
        duration_days = int(request.form['duration_days'])
        price = float(request.form['price'])
        total_slots = int(request.form['total_slots'])
        best_season = request.form.get('best_season')
        description = request.form.get('description')

        # Convert international string to boolean
        is_international = True if request.form['is_international'] == 'true' else False

        # Convert dates
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

        # Validation
        if end_date < start_date:
            flash("End date cannot be before start date", "danger")
            return redirect(url_for('admin.manage_treks'))

        # Create trek object
        new_trek = Trek(
            name=name,
            location=location,
            country=country,
            is_international=is_international,
            category=category,
            difficulty=difficulty,
            duration_days=duration_days,
            description=description,
            price=price,
            total_slots=total_slots,
            available_slots=total_slots,
            status='Open',
            start_date=start_date,
            end_date=end_date,
            best_season=best_season
        )

        # Save trek in DB
        db.session.add(new_trek)
        db.session.commit()

        flash("Trek added successfully!", "success")
        return redirect(url_for('admin.manage_treks'))

    # STEP 14: Trek Search
    search = request.args.get('search')
    if search:
        treks = Trek.query.filter(
            (Trek.name.ilike(f"%{search}%")) |
            (Trek.location.ilike(f"%{search}%"))
        ).all()
    else:
        treks = Trek.query.all()

    staffs = User.query.filter_by(role='staff', status='approved').all()

    # Render treks page
    return render_template(
        'admin/treks.html',
        treks=treks,
        staffs=staffs
    )


# STEP 5: Edit Trek

@admin_bp.route('/edit-trek/<int:trek_id>', methods=['GET', 'POST'])
def edit_trek(trek_id):

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    # Check admin access
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    # Get trek by ID
    trek = Trek.query.get_or_404(trek_id)

    #  If form submitted
    if request.method == 'POST':

        trek.name = request.form['name']
        trek.location = request.form['location']
        trek.country = request.form['country']
        trek.category = request.form['category']
        trek.difficulty = request.form['difficulty']
        trek.duration_days = int(request.form['duration_days'])
        trek.price = float(request.form['price'])
        trek.total_slots = int(request.form['total_slots'])
        trek.available_slots = int(request.form['available_slots'])
        trek.status = request.form['status']
        trek.best_season = request.form['best_season']
        trek.description = request.form['description']

        trek.is_international = True if request.form['is_international'] == 'true' else False

        trek.start_date = datetime.strptime(
            request.form['start_date'],
            '%Y-%m-%d'
        )

        trek.end_date = datetime.strptime(
            request.form['end_date'],
            '%Y-%m-%d'
        )

        # Validation
        if trek.end_date < trek.start_date:
            flash("End date cannot be before start date", "danger")
            return redirect(url_for('admin.edit_trek', trek_id=trek.id))

        db.session.commit()

        flash("Trek updated successfully!", "success")
        return redirect(url_for('admin.manage_treks'))

    # Show edit page
    return render_template('admin/edit_trek.html', trek=trek)

    
# STEP 6: Delete Trek
@admin_bp.route('/delete-trek/<int:trek_id>', methods=['POST'])
def delete_trek(trek_id):

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    # Check admin access
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    #Get trek
    trek = Trek.query.get_or_404(trek_id)

    # Delete trek
    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully!", "success")
    return redirect(url_for('admin.manage_treks'))


# STEP 7: Manage Staff

@admin_bp.route('/staff')
def manage_staff():

    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    #: Staff Search
    search = request.args.get('search')

    query = User.query.filter_by(role='staff')

    if search:
        query = query.filter(
            (User.name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    staffs = query.all()

    return render_template('admin/staffs.html', staffs=staffs)

# STEP 8: Approve Staff

@admin_bp.route('/approve-staff/<int:staff_id>', methods=['POST'])
def approve_staff(staff_id):

    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    staff = User.query.get_or_404(staff_id)

    staff.status = "approved"
    db.session.commit()

    flash("Staff approved successfully!", "success")
    return redirect(url_for('admin.manage_staff'))


# STEP 9: Blacklist Staff

@admin_bp.route('/blacklist-staff/<int:staff_id>', methods=['POST'])
def blacklist_staff(staff_id):

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    # Check admin access
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    # Get staff
    staff = User.query.get_or_404(staff_id)

    # Validate role
    if staff.role != 'staff':
        flash("Invalid staff", "danger")
        return redirect(url_for('admin.manage_staff'))

    # Blacklist
    staff.is_blacklisted = True
    db.session.commit()

    flash("Staff blacklisted successfully!", "success")
    return redirect(url_for('admin.manage_staff'))    

# STEP 10: Manage Users
@admin_bp.route('/users')
def manage_users():

    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    # STEP 15: User Search

    search = request.args.get('search')

    query = User.query.filter_by(role='user')

    if search:
        query = query.filter(
          (User.name.ilike(f"%{search}%")) |
           (User.email.ilike(f"%{search}%"))
    )

    users = query.all()

    return render_template('admin/users.html', users=users)

# STEP 11: Block User
@admin_bp.route('/block-user/<int:user_id>', methods=['POST'])
def block_user(user_id):

    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)

    user.is_blacklisted = True
    db.session.commit()

    flash("User blocked successfully!", "success")
    return redirect(url_for('admin.manage_users'))

# STEP 12: Manage Bookings
@admin_bp.route('/bookings')
def manage_bookings():

    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    bookings = Booking.query.all()

    return render_template('admin/bookings.html', bookings=bookings)


# STEP 13: Assign Staff to Trek

@admin_bp.route('/assign-staff/<int:trek_id>', methods=['POST'])
def assign_staff(trek_id):

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    # Check admin access
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    trek = Trek.query.get_or_404(trek_id)

    staff_id = request.form['staff_id']

    # Validate staff
    staff = User.query.get_or_404(int(staff_id))

    if staff.role != 'staff' or staff.status != 'approved':
        flash("Invalid staff selection", "danger")
        return redirect(url_for('admin.manage_treks'))

    # Assign staff
    trek.assigned_staff_id = staff.id
    db.session.commit()

    flash("Staff assigned successfully!", "success")
    return redirect(url_for('admin.manage_treks'))

# STEP 14: Unassign Staff from Trek

@admin_bp.route('/unassign-staff/<int:trek_id>', methods=['POST'])
def unassign_staff(trek_id):

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    # Check admin access
    if session.get('role') != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('auth.login'))

    # Get trek
    trek = Trek.query.get_or_404(trek_id)

    # Remove assigned staff
    trek.assigned_staff_id = None

    db.session.commit()

    flash("Staff unassigned successfully!", "success")
    return redirect(url_for('admin.manage_treks'))    