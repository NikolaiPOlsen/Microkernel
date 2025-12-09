#Imports
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
                print("Received invalid message format.")
                continue

            if message_type == "SHUTDOWN":
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
        logging.info("Received user logged in")
        logging.info("User ID: %s", message.get("user_id"))
        logging.info("Timestamp: %s", message.get("timestamp"))

#Håndterer data prosessert melding
    def handle_data_processed(self, message):
        logging.info("Received data processed")
        logging.info("Data ID: %s", message.get("data_id"))
        logging.info("Processing time: %s seconds", message.get("processing_time"))