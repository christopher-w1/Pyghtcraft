from flask import Blueprint, render_template, session, url_for, redirect
from db.api_key_utils import get_perm_level
from db import get_db

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    perm_lvl = None
    if 'username' in session:
        username = session['username']
        if 'api_key' in session:
            with get_db() as db:
                perm_lvl = get_perm_level(db, session['api_key'], username)
        return render_template('index.html', username=username, perm_level=perm_lvl)
    return render_template('index.html', username=None, perm_level=perm_lvl)

@main_blueprint.route('/register')
def register():
    return render_template('register.html')

@main_blueprint.route('/controlpanel')
def controlpanel():
    if not 'api_key' in session or not 'username' in session:
        return redirect(url_for('main.index'))
    else:
        username = session['username']
        with get_db() as db:
            perm_lvl = get_perm_level(db, session['api_key'], username)
            return render_template('controlpanel.html', perm_level=perm_lvl)
        
@main_blueprint.route('/permissions')
def permissions():
    return render_template('notimplemented.html')

