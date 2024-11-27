import os
import logging
from Core.dev.Common_opts import Paths

def get_logger(filename):
    """
    Create a logger that logs to a specified file and does not print logs to the console.

    Args:
        filename (str): Name of the log file (without path or extension).

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_dir = Paths.Log_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Use a static name for the logger or generate a unique one (e.g., based on timestamp)
    logger = logging.getLogger("simple_logger")  # Static logger name
    logger.setLevel(logging.DEBUG)  # Capture all logs (DEBUG and higher)

    # Ensure no duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a log file
    log_file = os.path.join(log_dir, f"{filename}.log")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)  # Capture all logs in the file

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # No console handler added
    return logger
