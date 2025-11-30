from Packages.IPC.Communication import IPCManager

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
    def register_plugin(self, plugin_name):
        pass

#Starter plugin
    def start_plugin(self, plugin_name):
        queue = self.ipc.start_com(plugin_name)
        #Må ha en start process method

#Stopper plugin
    def stop_plugin(self, plugin_name):
        self.ipc.stop_com(plugin_name)
        #Må ha en stop process method
        #Må ha en slett process method