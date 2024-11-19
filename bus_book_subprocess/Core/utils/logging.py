import os
import logging
from Core.dev.Common_opts import Paths

def get_logger():
    log_dir = Paths.Log_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Use a static name for the logger or generate a unique one (e.g., based on timestamp)
    logger = logging.getLogger("simple_logger")  # Static logger name
    logger.setLevel(logging.DEBUG)  # Capture all logs (DEBUG and higher)

    # Create a log file with a generic name (e.g., "app.log")
    log_file = os.path.join(log_dir, "test.log")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)  # Capture all logs in the file

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Optional: Add console handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
