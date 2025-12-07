from Packages.IPC.Communication import IPCManager
from multiprocessing import Process

class microkernel:
    def __init__(self):
        print("Microkernel init")
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