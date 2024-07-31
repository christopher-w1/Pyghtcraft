from flask import Flask
from controllers.auth import auth_blueprint
from controllers.main import main_blueprint
from controllers.api  import api_blueprint
from datetime import timedelta
from config import Config
import logging, argparse, os

app = Flask(__name__, static_url_path=f'/{Config.URL_PREFIX}/static', static_folder='static')

# Set secret key for session management
if not os.path.exists(Config.SECRET_KEY_FILE):
    # Generate new key if necessary
    new_key = os.urandom(32).hex()
    with open(Config.SECRET_KEY_FILE, 'w') as f:
        f.write(new_key)
    app.secret_key = new_key
else:
    # Read key from file
    with open(Config.SECRET_KEY_FILE, 'r') as f:
        app.secret_key = f.read().strip()

# Set session duration
app.permanent_session_lifetime = timedelta(minutes=Config.KEY_VALID_DURATION)

# Initialize logger
logging.basicConfig(
    filename='mcservice.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix=Config.URL_PREFIX)
app.register_blueprint(main_blueprint, url_prefix=Config.URL_PREFIX)
app.register_blueprint(api_blueprint,  url_prefix=Config.URL_PREFIX)

if __name__ == '__main__':
    # Use argument parser
    parser = argparse.ArgumentParser(description='Start the Flask application.')
    parser.add_argument('-debug', action='store_true', help='Run the server in debug mode')
    args = parser.parse_args()

    # Check for debug argument
    if args.debug:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(debug=True, host="0.0.0.0", port=Config.PYGHTCRAFT_PORT)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=Config.PYGHTCRAFT_PORT)
