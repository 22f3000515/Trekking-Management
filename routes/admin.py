from flask import Blueprint,url_for,redirect,flash,session
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
@admin_bp.route("/dashboard")

def dashboard():
    if 'user_id' not in session:
        flash("Please Login First!", 'danger')
        return redirect(url_for('auth.login'))
    
    if session.get('role')!='admin':
        flash("Access Denied",'danger')
        return redirect(url_for('auth.login'))
    return 'Admin Dashboard'
