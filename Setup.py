from Packages.Microkernel.Microkernel import microkernel
from Packages.Plugins.Plugin_MetricsLogger import plugin_MetricsLogger
import logging

#Konfigurer logging for MetricsLogger plugin
logging.basicConfig(
    level=logging.INFO,
    filename="metrics.log",
    filemode="a",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

#Entry point for MetricsLogger plugin
def metrics_entry(queue):
    plugin = plugin_MetricsLogger(queue)
    plugin.start()

#Tilgjengelige plugins
AVAILABLE_PLUGINS = {
    "metrics": metrics_entry,
}

#Main
def main():
    kernel = microkernel()

    while True:
        print("Menu:")
        print("======================")
        print("1. Start Microkernel")
        print("2. Stop Microkernel")
        print("3. Register Plugin")
        print("4. Start Plugin")
        print("5. Stop Plugin")
        print("6. Test UserLoggedInEvent")
        print("7. Test DataProcessedEvent")
        print("8. Exit")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                kernel.start()
            case "2":
                kernel.stop()
            case "3":
                print("Available plugins:", ", ".join(AVAILABLE_PLUGINS.keys()))
                plugin_name = input("Enter plugin name: ").strip()

                plugin_target = AVAILABLE_PLUGINS.get(plugin_name)
                if plugin_target is None:
                    print(f"Plugin {plugin_name} is not available.")
                    continue

                kernel.register_plugin(plugin_name, plugin_target)
            case "4":
                plugin_name = input("Enter plugin name to start: ")
                kernel.start_plugin(plugin_name)
            case "5":
                plugin_name = input("Enter plugin name to stop: ")
                kernel.stop_plugin(plugin_name)
            case "6":
                user_id = input("Enter user ID for UserLoggedInEvent: ")
                kernel.send_user_logged_in_event("metrics", user_id)
            case "7":
                data_id = input("Enter data ID for DataProcessedEvent: ")
                kernel.send_data_processed_event("metrics", data_id)
            case "8":
                break
            case _:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()