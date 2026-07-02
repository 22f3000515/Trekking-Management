from flask import Blueprint,url_for,redirect,flash,session
staff_bp=Blueprint("staff",__name__,url_prefix="/staff")

@staff_bp.route('/dashboard')

def dashboard():
    if 'user_id' not in session:
        flash("Please Login First!",'danger')
        return redirect(url_for('auth.login'))
    
    if session.get('role')!='staff':
        flash("Access Denied!",'danger')
        return redirect(url_for('auth.login'))
    return 'Staff Dashboard'