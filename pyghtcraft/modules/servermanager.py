import subprocess, threading, time, logging
from collections import deque
from config import Config

class MinecraftServerManager:
    def __init__(self):
        self.process = None
        self.console_output = deque(maxlen=32)
        self.logger = logging.getLogger()
        self.updated_clients = []

    def start_server(self):
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(
                [Config.JAVAPATH] + Config.FLAGS + ["-jar", Config.JARFILE, "--nogui"],
                cwd=Config.WORKDIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            threading.Thread(target=self.monitor_output, daemon=True).start()
            for i in range(Config.STARTUP_TIME_LIMIT):
                time.sleep(1)
                if "Done" in self.console_output:
                    self.logger.info("Minecraft server started.")
                    return True
            self.logger.info(f"Server did not start or took longer than {Config.STARTUP_TIME_LIMIT}s.")
                

    def stop_server(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.logger.info("Minecraft server stopped.")
        else:
            self.logger.info("Minecraft server is not running.")
        return True

    def send_command(self, command):
        if self.process:
            self.process.stdin.write(f"{command}\n".encode('utf-8'))
            self.process.stdin.flush()
            self.logger.info(f"Sent command: {command}")
            return True
        else:
            self.logger.error("Cannot send command, Minecraft process is not running.")
            return False
            
    def get_output_as_list(self, api_key):
        """
        Gives new console output for client, but only if output has changed
        since last request.
        """
        if (api_key in self.updated_clients):
            return None
        else:
            self.updated_clients.append(api_key)
            return list(self.console_output)
    

    def monitor_output(self):
        """
        Monitors the subprocesses output and logs it to both logfile and dequeue.
        Empties the list of updated clients.
        """
        if self.process:
            for line in iter(self.process.stdout.readline, b''):
                decoded_line = line.decode('utf-8').strip()
                self.logger.info(decoded_line)
                self.console_output.append(decoded_line)
                self.updated_clients = []
            
            for line in iter(self.process.stderr.readline, b''):
                decoded_line = line.decode('utf-8').strip()
                self.logger.error(decoded_line)
                self.console_output.append(decoded_line)
                self.updated_clients = []
