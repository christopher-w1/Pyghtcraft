from flask import Blueprint, request, jsonify, session
from db import get_db
from db.api_key_utils import is_action_permitted, is_api_key_valid
from db.auth_utils import change_user_password, change_user_email, change_user_username
from config import Config
from modules.servermanager import MinecraftServerManager
import logging

api_blueprint = Blueprint('api', __name__)

server_manager = MinecraftServerManager()

logger = logging.getLogger()

@api_blueprint.route('/api/user', methods=['GET', 'POST'])
def control_user():

    if request.method != 'POST':
        logger.warn("Client sent GET request on /api/user")
        return jsonify({"error": "GET requests are not permitted on this URL."}), 400

    data     = request.json
    username = data.get('username', '')
    password  = data.get('password', '')
    api_key  = data.get('api_key', '')
    action   = data.get('action', '')

    # Open database
    with get_db() as db:

        if is_api_key_valid(db, username, api_key):

            match action:

                case "changepassword":
                    new_password  = data.get('new_password', '')
                    message = change_user_password(db, username, password, new_password)
                    code = 200 if "success" in message else 400
                    return jsonify({"message": message}), code
                    
                case "changeemail":
                    new_email = data.get('new_email', '')
                    message = change_user_email(db, username, password, new_email)
                    code = 200 if "success" in message else 400
                    return jsonify({"message": message}), code

                case "changeusername":
                    new_name = data.get('new_username', '')
                    message = change_user_username(db, username, password, new_name)
                    code = 200 if "success" in message else 400
                    return jsonify({"message": message}), code

                case _:
                    return jsonify({"error": "Invalid action."}), 400
                
        return jsonify({"error": "Invalid API key. Please log in again."}), 401


@api_blueprint.route('/api/server', methods=['GET', 'POST'])
def control_minecraft():

    if request.method != 'POST':
        if Config.PERM_GETSTATUS < 1:
            server_status = "running" if server_manager.process and server_manager.process.poll() is None else "offline"
            return jsonify({"status": f"Minecraft server is {server_status}."}), 200
        else:
            return jsonify({"error": "GET requests not permitted on this URL."}), 401
    
    data     = request.json
    username = data.get('username', '')
    api_key  = data.get('api_key', '')
    action   = data.get('action', '')
    
    # Open database
    with get_db() as db:
        #logger.info(f"User '{username}' sent POST request with action '{action}' to API.")
        match action:
            # Request to ask if server is offline or online
            case "status":
                if is_action_permitted(db, username, api_key, Config.PERM_GETSTATUS):
                    server_status = "running" if server_manager.process and server_manager.process.poll() is None else "offline"
                    return jsonify({"status": f"Minecraft server is {server_status}."}), 200
            # Request to acquire the server address
            case "askaddress":
                if is_action_permitted(db, username, api_key, Config.PERM_GETSTATUS):
                    server_address = request.host_url.rstrip('/')
                    return jsonify({"status": f"Current server address is {server_address}:{Config.MINECRAFT_PORT}"}), 200
            # Request to run the minecraft server
            case "start":
                if is_action_permitted(db, username, api_key, Config.PERM_RUNSERVER):
                    server_manager.start_server()
                    return jsonify({"status": "Minecraft server started."}), 200
            # Request to stop the minecraft server
            case "stop":
                if is_action_permitted(db, username, api_key, Config.PERM_STOPSERVER):
                    server_manager.stop_server()
                    return jsonify({"status": "Minecraft server stopped."}), 200
            # Request to reboot the minecraft server
            case "reboot":
                if is_action_permitted(db, username, api_key, max(Config.PERM_STOPSERVER, Config.PERM_RUNSERVER)):
                    server_manager.stop_server()
                    server_manager.start_server()
                    return jsonify({"status": "Minecraft server restarted."}), 200
            # Request to acquire the latest console output
            case "getconsole":
                if is_action_permitted(db, username, api_key, Config.PERM_SEECONSOLE):
                    console_output = server_manager.get_output_as_list(api_key)
                    if console_output is not None:
                        return jsonify({"console_output": console_output}), 200
                    else:
                        # No content, no update
                        return jsonify({"console_output": []}), 204  
            # Request to run a console command
            case "command":
                if is_action_permitted(db, username, api_key, Config.PERM_RUNCOMMAND):
                    command  = data.get('command', '')
                    server_manager.send_command(command)
                    return jsonify({"status": f"Command '{command}' sent to Minecraft server."}), 200
            # Any other requests are invalid
            case _:
                    return jsonify({"error": "Invalid action."}), 400
                
        # Message if API key is invalid, unauthorized or non-existent
        logger.warn(f"User '{username}' is not authorized to perform '{action}'")
        return jsonify({"error": "Unauthorized."}), 401

@api_blueprint.route('/api/ping', methods=['GET', 'POST'])
def ping():

    # Just answer the PING if its a get
    if request.method != 'POST':
        return jsonify({"status": f"OK"}), 200
    
    data     = request.json
    username = data.get('username', '')
    api_key  = data.get('api_key', '')
    
    # Open database to check API key validity
    with get_db() as db:

        if is_api_key_valid(db, username, api_key):

            return jsonify({"status": f"OK"}), 200
        else:
            if session:
                session.clear()
            return jsonify({"error": f"Session Timeout"}), 401
        

    return jsonify({"error": f"Server error"}), 500