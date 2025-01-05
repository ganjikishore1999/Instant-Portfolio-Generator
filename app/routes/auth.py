from flask import redirect, render_template, request, Blueprint, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

from ..models import User, db

# Define the auth blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('full-name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Check if the user already exists
        user_exist = User.query.filter_by(username=username).first()
        if user_exist:
            flash('Username already exists. Please choose another username.', 'error')
            return redirect(url_for('auth.register_user'))

        # Check if password and confirm password match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", 'error')
            return redirect(url_for('auth.register_user'))

        # Hash the password and create the new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, name=name, password=hashed_password)

        # Add the new user to the database and commit
        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully registered! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')  # Render registration form

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    next_page = request.args.get('next')        
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user already exists
        user_exist = User.query.filter_by(username=username).first()
        if not user_exist:
            flash('Username does not exists. Please signup or choose another username.', 'error')
            return redirect(url_for('auth.register_user'))
        if not check_password_hash(user_exist.password, password):
            flash("Invalid credentials! please try again.", "error")
            return redirect(url_for('auth.login'))
        login_user(user_exist, remember=False)
        # Redirect to next page or home page
        return redirect(next_page or url_for('main.home_page'))
    return render_template('login.html', next=next_page)

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("you are logged out successfully....!", "success ")
    return redirect(url_for('main.home_page'))
