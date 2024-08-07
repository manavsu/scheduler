import os
import platform
import logging
import sys

log = logging.getLogger("config")

PRODUCTION = True
VERSION = "1.0.0"

def ensure_dir_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
def get_network_store_path():
    if not PRODUCTION:
        path = "schedules.json"
    elif platform.system() == "Windows":
        appdata = os.getenv('APPDATA')
        if appdata:
            path = os.path.join(appdata, "amber", "schedules.json")
            ensure_dir_exists(path)
        else:
            log.error("APPDATA environment variable is not set.")
            path = "schedules.json"
        ensure_dir_exists(path)
    else:
        path = "schedules.json"
    log.info(f"Using schedules store at {path}")
    return path

DB_PATH = get_network_store_path()
HOST = "127.0.0.1"
PORT = 5000