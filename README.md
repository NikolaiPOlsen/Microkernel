# Microkernel

## Overview
This program is a python programmed dummy microkernel (core functions) with an external plugin for metrics logging.
All the plugins runs in issolated processes and communicate via IPC queues
The kernel is tasked to enforce a message contract before sending events. The Metrics logger handles and logs the events according to the specifications

## Directory Structure
/Packages
    /Microkernel        – Kernel implementation
    /Plugins            – All plugins (e.g., MetricsLogger)
    /IPC                – IPCManager for process communication
Setup.py               – CLI entry point
messageContract.json  – Message contract specification

## How to run the pogram
To run the program: start by locating the project folder, then do "python3 Setup.py".

## Usermanual
1. Register plugin - Adds the plugin into the microkernel.
2. Start plugin - Starts the plugin process.
3. Stop plugin - Stops the plugin process.
4. Test UserLoggedInEvents - Sends a UserLoggedInEvent through the kernel → IPC → plugin for testing.
5. Test DataProcessedEvent - Sends a DataProcessedEvent through the kernel → IPC → plugin for testing.
6. Exit - Stops the microkernel and all active plugins, then proceeds closes the program.

## Example Event Message
{
  "type": "UserLoggedInEvent",
  "timestamp": "2025-01-05T12:00:00Z",
  "payload": {
    "user_id": "42"
  }
}
