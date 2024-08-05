import os
import platform
import logging
import sys

log = logging.getLogger("config")
log.setLevel(logging.DEBUG)

PRODUCTION = True
VERSION = "1.0.0"

def ensure_dir_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
def get_network_store_path():
    if not PRODUCTION:
        path = "schedules.json"
    if platform.system() == "Windows":
        path = os.getenv('APPDATA') + "/amber/schedules.json"
        ensure_dir_exists(path)
    else:
        path = "schedules.json"
    log.info(f"Using schedules store at {path}")
    return path

DB_PATH = get_network_store_path()