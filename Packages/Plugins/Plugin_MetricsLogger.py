#Imports
import json
import time
import logging

#class for the Metrics logger plugin
class plugin_MetricsLogger:
    def __init__(self, queue):
        self.queue = queue
        self.running = True
        self.eventCount = 0

#Definerer meldingshåndterere
        self.handlers = {
            "UserLoggedInEvent": self.handle_user_logged_in,
            "DataProcessedEvent": self.handle_data_processed,
        }

#Start funksjon for plugin
    def start(self):
        while self.running:

            message = self.queue.get()

            message_type = message.get("type")

            if message_type is None:
                logging.error("Received invalid message format.")
                continue

            if message_type == "SHUTDOWN":
                logging.info(f"MetricsLogger plugin shutting down. Processed {self.eventCount} events, before shutdown")
                self.running = False
                continue

            handler = self.handlers.get(message_type)
            if handler:
                handler(message)
                self.eventCount += 1
            else:
                print(f"Unknown message type: {message_type}")
                pass

#Håndterer bruker innlogging melding
    def handle_user_logged_in(self, message):
        log_entry = {
            "type": "UserLoggedInEvent",
            "timestamp": message.get("timestamp"),
            "payload": {
                "user_id": message.get("user_id")
            },
            "metadata": {
                "plugin": "MetricsLogger",
                "received_at": time.time()
            }
        }

        logging.info(json.dumps(log_entry))

#Håndterer data prosessert melding
    def handle_data_processed(self, message):
        log_entry = {
            "type": "DataProcessedEvent",
            "timestamp": message.get("timestamp"),
            "payload": {
                "data_id": message.get("data_id"),
                "processing_time": message.get("processing_time")
            },
            "metadata": {
                "plugin": "MetricsLogger",
                "received_at": time.time()
            }
        }
        logging.info(json.dumps(log_entry))