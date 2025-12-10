# Microkernel
## How to run the pogram
To run the program: start by locating the project folder, then do "python3 Setup.py".

## Usermanual
1. Register plugin - Adds the plugin into the microkernel.
2. Start plugin - Starts the plugin process.
3. Stop plugin - Stops the plugin process.
4. Test UserLoggedInEvents - Sends a UserLoggedInEvent through the kernel → IPC → plugin for testing.
5. Test DataProcessedEvent - Sends a DataProcessedEvent through the kernel → IPC → plugin for testing.
6. Exit - Stops the microkernel and all active plugins, then proceeds closes the program.
