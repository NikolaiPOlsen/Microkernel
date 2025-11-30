from multiprocessing import Process, Queue

class IPCManager:
    def __init__(self):
        self.plugins_queues = {}

#Starter IPC kommunikasjonen for satt plugin
    def start_com(self, plugin_name):
        queue = Queue()
        self.plugins_queues[plugin_name] = queue
        return queue

#Sender melding til plugin
    def send_to_plugin(self, plugin_name, message):
        if plugin_name in self.plugins_queues:
            self.plugins_queues[plugin_name].put(message)
            return True
        else:
            return False

#Sender en melding til alle plugins som kjører
    def broadcast(self, message):
        for queue in self.plugins_queues.values():
            queue.put(message)

#Stopper IPC kommunikasjonen for satt plugin
    def stop_com(self, plugin_name):
        queue = self.plugins_queues.pop(plugin_name, None)
        if queue is None:
            return False
        queue.close()
        return True

#Stopper IPC kommunikasjonen for alle plugins
    def stop_all(self):
        for queue in self.plugins_queues.values():
            queue.close()
        self.plugins_queues.clear()