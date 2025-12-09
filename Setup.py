from Packages.Microkernel.Microkernel import microkernel
import logging

logging.basicConfig(level=logging.INFO)

def test_function(queue):
    pass  # Dummy funksjon for testing

if __name__ == "__main__":
    kernel = microkernel()
    kernel.register_plugin("test", test_function)
    print(kernel.plugins)