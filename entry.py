from waitress import serve, create_server
from flask_main import app
import logging
import threading
import jupiter_main
import webbrowser
import config
import signal
from time import sleep

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s", datefmt="%d-%m-%y %H:%M:%S")
log = logging.getLogger("main")

cancel_event = threading.Event()

def handle_sigint(signum, frame):
    log.info("SIGINT received, shutting down...")
    cancel_event.set()

signal.signal(signal.SIGINT, handle_sigint)

if __name__ == "__main__":
    server = create_server(app, host=config.HOST, port=config.PORT)
    server_process = threading.Thread(target=server.run, daemon=True)
    jupiter_process = threading.Thread(target=jupiter_main.main_loop, args=(cancel_event,), daemon=True)
    log.info("Starting jupiter API...")
    jupiter_process.start()
    
    log.info("Starting flask...")
    log.info(f"Serving on http://{config.HOST}:{config.PORT}")
    server_process.start()
    
    webbrowser.open(f"http://localhost:5173")
    
    while not cancel_event.wait(5):
        pass

    cancel_event.set()
    log.info("Stopping server...")
    server.close()
    server_process.join()
    
    log.info("Stopping jupiter API...")
    jupiter_process.join()
    