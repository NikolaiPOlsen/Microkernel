import time

from Packages.IPC.Communication import IPCManager
from multiprocessing import Process
import json

class microkernel:
    def __init__(self):
        print("Microkernel init")
        with open("messageContract.json", "r", encoding="utf-8") as f:
            self.contract = json.load(f)

        self.ipc = IPCManager()
        self.plugins = {}
        self.process = {}
        self.running = False

#Starter microkernel
    def start(self):
        print("Microkernel starting")
        self.running = True

#Stopper microkernel
    def stop(self):
        print("Microkernel stopping")
        self.running = False

#Registerer en ny plugin
    def register_plugin(self, plugin_name, plugin_target):
        if plugin_name in self.plugins:
            print(f"Plugin {plugin_name} is already registered.")
            return False

        self.plugins[plugin_name] = {
            'name': plugin_name,
            'target': plugin_target,
            'process': None,
            'queue': None
        }
        print(f"Plugin {plugin_name} registered.")
        return True

#Starter plugin
    def start_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            print(f"Plugin {plugin_name} is not registered.")
            return False

        plugin_info = self.plugins[plugin_name]

        if plugin_info['process'] is not None and plugin_info['process'].is_alive():
            print(f"Plugin {plugin_name} is already running.")
            return False

        queue = self.ipc.start_com(plugin_name)

        process = Process(target=plugin_info['target'], args=(queue,))
        process.start()

        self.plugins[plugin_name]['process'] = process
        self.plugins[plugin_name]['queue'] = queue
        print(f"Plugin {plugin_name} started (PID: {process.pid}).")
        return True

#Stopper plugin
    def stop_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            print(f"Plugin {plugin_name} is not registered.")
            return False

        plugin_info = self.plugins.get(plugin_name)
        process = plugin_info['process']

        if process is None or not process.is_alive():
            print(f"Plugin {plugin_name} is not running.")
            return False

        self.ipc.send_to_plugin(plugin_name, {'type': 'SHUTDOWN'})
        process.join(timeout=5)

        if process.is_alive():
            process.terminate()
            print(f"Plugin {plugin_name} was forcefully stopped.")

        self.ipc.stop_com(plugin_name)
        plugin_info['process'] = None
        plugin_info['queue'] = None
        print(f"Plugin {plugin_name} stopped.")
        return True

#Validering av nestet felter
    def nested_fields(self, message: dict, field_path: str) -> bool:
        fields = field_path.split(".")
        current = message

        for field in fields:
            if not isinstance(current, dict):
                return False
            current = current[field]
        return True

#Melidngs validering
    def validate_message(self, message):
        message_type = message.get("type")
        if message_type is None:
            return False

        spec = self.contract.get(message_type)
        if spec is None:
            return False

        for field_path in spec.get("required_fields", []):
            if not self.nested_fields(message, field_path):
                return False

        message_payload = message.get("payload", {})
        if not isinstance(message_payload, dict):
            return False

        message_schema = spec.get("payload_schema", {})

        for field_name, expected_type in message_schema.items():
            value = message_payload.get(field_name)
            if value is None:
                return False

            if expected_type == "string" and not isinstance(value, str):
                return False
            if expected_type == "number" and not isinstance(value, (int, float)):
                return False

        return True

    def send_user_logged_in_event(self, plugin_name, user_id):
        message = {
            "type": "UserLoggedInEvent",
            "timestamp": time.time(),
            "payload": {
                "user_id": user_id
            }
        }

        if not self.validate_message(message):
            print("Invalid UserLoggedInEvent message format.")
            return False

        self.ipc.send_to_plugin(plugin_name, message)
        print(f"UserLoggedInEvent sent to {plugin_name}.")
        return True

    def send_data_processed_event(self, plugin_name, data_id):
        message = {
            "type": "DataProcessedEvent",
            "timestamp": time.time(),
            "payload": {
                "data_id": data_id,
                "processing_time": time.time() % 1000
            }
        }

        if not self.validate_message(message):
            print("Invalid DataProcessedEvent message format.")
            return False

        self.ipc.send_to_plugin(plugin_name, message)
        print(f"DataProcessedEvent sent to {plugin_name}.")
        return True