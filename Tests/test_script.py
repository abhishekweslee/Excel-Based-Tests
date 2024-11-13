import pytest
import logging
import os
from Framework.Sample import ReadingExcel

# Function to set up logging to a file based on the test case name
def setup_logging(testcase_name):
    log_dir = "../logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists
    log_file = os.path.join(log_dir, f"{testcase_name}.log")

    # Create logger
    logger = logging.getLogger(testcase_name)
    logger.setLevel(logging.DEBUG)  # Set log level to DEBUG to capture all messages

    # Remove any existing handlers to avoid duplicate logs
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Create a file handler to log to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Create a stream handler to log to the console (optional)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

@pytest.mark.parametrize("tid", ReadingExcel().get_testIDs())  # Parameterize with all test IDs
def test_booking_details(tid):
    # Initialize logging for this test case
    logger = setup_logging(f"test_case_{tid}")
    logger.info(f"Running test for Test ID: {tid}")
    data = ReadingExcel()

    try:
        # Fetch booking details and expected output based on the test ID (tid)
        booking_details = data.enter_data(tid)
        logger.debug(f"Booking details for Test ID {tid}: {booking_details}")

        expected_output = data.extract_expected_output(tid)
        logger.debug(f"Expected output for Test ID {tid}: {expected_output}")

        # Compare the details and assert the output is "OK"
        output = data.compare(booking_details, expected_output)
        logger.info(f"Comparison result for Test ID {tid}: {output}")

        assert output == "OK", f"Test failed for Test ID {tid}. Expected 'OK' but got {output}"

    except Exception as e:
        logger.error(f"Error occurred while processing Test ID {tid}: {str(e)}")
        raise
