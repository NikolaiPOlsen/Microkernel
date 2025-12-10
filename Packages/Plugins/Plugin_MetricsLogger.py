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
                logging.error("\033[31mReceived invalid message format.\033[0m")
                continue

            if message_type == "SHUTDOWN":
                logging.info(f"\033[32mMetricsLogger plugin shutting down. Processed {self.eventCount} events, before shutdown\033[0m")
                self.running = False
                continue

            handler = self.handlers.get(message_type)
            if handler:
                handler(message)
                self.eventCount += 1
            else:
                print(f"\033[31mUnknown message type: {message_type}\033[0m")
                pass

#Håndterer bruker innlogging melding
    def handle_user_logged_in(self, message):
        log_entry = {
            "type": "UserLoggedInEvent",
            "timestamp": message.get("timestamp"),
            "payload": {
                "user_id": message["payload"].get("user_id")
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
                "data_id": message["payload"].get("data_id"),
                "processing_time": message["payload"].get("processing_time")
            },
            "metadata": {
                "plugin": "MetricsLogger",
                "received_at": time.time()
            }
        }
        logging.info(json.dumps(log_entry))