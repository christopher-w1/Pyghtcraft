from flask import Flask
from config import Config
from control_panel.routes import control_panel
import logging

# Setting up flask
app = Flask(__name__, static_url_path=f'{Config.URL_PREFIX}/static', static_folder='static')
app.register_blueprint(control_panel, url_prefix = Config.URL_PREFIX)

# Setting up logger
logging.basicConfig(
    filename=Config.LOGFILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=Config.WEB_API_PORT)
