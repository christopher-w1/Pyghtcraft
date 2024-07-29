from flask import Blueprint, request, jsonify, render_template
from db.utils import is_action_permitted
from db import get_db
from config import Config
from control_panel.subprocess_manager import MinecraftServerManager

control_panel = Blueprint('control_panel', __name__)
server_manager = MinecraftServerManager()

@control_panel.route('/')
def index():
    if Config.PERM_GETSTATUS < 1:
        server_status = "running" if server_manager.process and server_manager.process.poll() is None else "offline"
        return jsonify({"status": f"Minecraft server is {server_status}."}), 200
    else:
        return jsonify({"error": "GET requests not permitted."}), 401

@control_panel.route('/action', methods=['POST', 'GET'])
def control_minecraft():
    data     = request.json
    username = data.get('username', '')
    api_key  = data.get('api_key', '')
    action   = data.get('action', '')
    command  = data.get('command', '')
    
    if request.method == 'GET':
        if Config.PERM_GETSTATUS < 1:
            server_status = "running" if server_manager.process and server_manager.process.poll() is None else "offline"
            return jsonify({"status": f"Minecraft server is {server_status}."}), 200
        else:
            return jsonify({"error": "GET requests not permitted."}), 401

    # Open database
    with get_db() as db:
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
                    return jsonify({"console_output": list(server_manager.console_output)}), 200
            # Request to run a console command
            case "command":
                if is_action_permitted(db, username, api_key, Config.PERM_RUNCOMMAND):
                    server_manager.send_command(command)
                    return jsonify({"status": f"Command '{command}' sent to Minecraft server."}), 200
            # Any other requests are invalid
            case _:
                    return jsonify({"error": "Invalid action."}), 400
                
        # Message if API key is invalid, unauthorized or non-existent
        return jsonify({"error": "Unauthorized."}), 401

