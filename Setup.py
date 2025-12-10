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
    kernel.start()

    while True:
        print("Menu:")
        print("======================")
        print("1. Register Plugin")
        print("2. Start Plugin")
        print("3. Stop Plugin")
        print("4. Test UserLoggedInEvent")
        print("5. Test DataProcessedEvent")
        print("6. \033[31mExit\033[0m")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                print("Available plugins:", ", ".join(AVAILABLE_PLUGINS.keys()))
                plugin_name = input("Enter plugin name: ").strip()

                plugin_target = AVAILABLE_PLUGINS.get(plugin_name)
                if plugin_target is None:
                    print(f"\033[33mPlugin {plugin_name} is not available.")
                    continue

                kernel.register_plugin(plugin_name, plugin_target)
            case "2":
                plugin_name = input("Enter plugin name to start: ")
                kernel.start_plugin(plugin_name)
            case "3":
                plugin_name = input("Enter plugin name to stop: ")
                kernel.stop_plugin(plugin_name)
            case "4":
                user_id = input("Enter user ID for UserLoggedInEvent: ")
                kernel.send_user_logged_in_event("metrics", user_id)
            case "5":
                data_id = input("Enter data ID for DataProcessedEvent: ")
                kernel.send_data_processed_event("metrics", data_id)
            case "6":
                kernel.stop()
                break
            case _:
                print("\033[31mInvalid choice. Please try again.\033[32m")

if __name__ == "__main__":
    main()