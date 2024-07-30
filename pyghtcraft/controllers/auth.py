from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db
from db.auth_utils import get_user_by_username, verify_password, check_and_insert_user
from db.api_key_utils import gen_api_key, invalidate_api_key, get_perm_level
import logging

auth_blueprint = Blueprint('auth', __name__)

logger = logging.getLogger()

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with get_db() as db:
            user = get_user_by_username(db, username)
            if user and verify_password(user.password, password):
                # Generate API Key
                api_key, perm_level = gen_api_key(db, username)
                # Save session data
                session['username'] = username
                session['api_key'] = api_key
                session['perm_level'] = perm_level
                logger.info(f"User '{username}' logged in with API key '{api_key[:8]}'.")
                return redirect(url_for('main.index'))
            else:
                flash("Login failed.", "errormessage")
                return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    if not 'username' in session:
        return redirect(url_for('main.index'))
    
    if session:
        username = session.get('username')
        api_key = session.get('api_key')

        if api_key:
            with get_db() as db:
                invalidate_api_key(db, api_key)
                logger.info(f"API key for user {username} invalidated.")

        session.pop('username', None)
        session.pop('api_key', None)
        session.pop('perm_level', None)
        logger.info(f"User {username} logged out.")
        return redirect(url_for('main.index'))

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        ip = request.remote_addr
        
        with get_db() as db:
            message = check_and_insert_user(db, username, password, email, ip)
            if "successfully" in message:
                flash(message, "message")
                return redirect(url_for('auth.login'))
            else:
                flash(message, "errormessage")
                return redirect(url_for('auth.register'))
    else:
        return render_template('register.html')

@auth_blueprint.route('/account', methods=['GET', 'POST'])
def update_account():
    if not 'username' in session:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        old_username = request.form.get('old_username')
        new_username = request.form.get('new_username')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        email = request.form.get('email')
        
        #with get_db() as db:
            #result = update_account_in_db(db, old_username, old_password, new_username, new_password, email)
        result = "Not implemented!"

        if result == "Update successful!":
            flash("Account updated successfully!")
        else:
            flash(result)
        return redirect(url_for('auth.update_account'))
    return render_template('account.html')