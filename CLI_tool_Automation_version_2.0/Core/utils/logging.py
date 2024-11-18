import os
import logging
from Core.dev.Common_opts import Paths

def get_logger(test_case_id):
    log_dir = Paths.log_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


    logger = logging.getLogger(test_case_id)
    logger.setLevel(logging.DEBUG)  # Capture all logs (DEBUG and higher)

    log_file = os.path.join(log_dir, f"test_case_{test_case_id}.log")
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
