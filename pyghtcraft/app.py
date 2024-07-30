from flask import Flask
from controllers.auth import auth_blueprint
from controllers.main import main_blueprint
from datetime import timedelta
from config import Config
import logging

app = Flask(__name__, static_url_path='/minecraft/static', static_folder='static')

app.secret_key = '095v457z'  # Für Session Management
app.permanent_session_lifetime = timedelta(minutes=10)

# Konfiguration des Loggers
logging.basicConfig(
    filename='mcservice.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# Registriere die Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/minecraft')
app.register_blueprint(main_blueprint, url_prefix='/minecraft')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=Config.WEB_API_PORT)
