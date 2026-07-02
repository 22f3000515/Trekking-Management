from flask import Blueprint,url_for,redirect,flash,session
user_bp=Blueprint('user', __name__,url_prefix='/user')
@user_bp.route('/dashboard')

def dashboard():
    if 'user_id' not in session:
        flash("Please Login First!",'danger')
        return redirect(url_for('auth.login'))
    
    if session.get("role")!="user":
        flash("Access Denied",'danger')
        return redirect(url_for('auth.login'))
    return 'User Dashboard'