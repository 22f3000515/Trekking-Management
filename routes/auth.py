from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
     return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone')
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            flash("Password does not match", "danger")
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        status = "pending" if role == 'staff' else 'approved'

        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role,
            status=status
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')

        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Step 1: Check user exists or not
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found", "danger")
            return redirect(url_for('auth.login'))

        # Step 2: Check password
        if not check_password_hash(user.password, password):
            flash("Invalid email or password", "danger")
            return redirect(url_for('auth.login'))
        
        # STEP 3: Check blacklist
        if user.is_blacklisted:
            flash("Your account has been blocked by admin", "danger")
            return redirect(url_for('auth.login'))

        # Step 4: Staff approval check
        if user.role == 'staff' and user.status != 'approved':
            flash("Waiting for admin approval", "warning")
            return redirect(url_for('auth.login'))
        

        # Step 5: Store session
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['role'] = user.role

        flash("Login successful!", "success")

        # Step 5: Role-based redirect
        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user.role == 'staff':
            return redirect(url_for('staff.dashboard'))
        else:
            return redirect(url_for('user.dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))