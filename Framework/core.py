import subprocess
import pandas as pd
import re
import time
import json
import logging

# Set up logging configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # Set the default log level to DEBUG
    handlers=[
        logging.StreamHandler()  # Log to console (you can also log to a file if needed)
    ]
)

logger = logging.getLogger(__name__)

class ReadingExcel:
    def __init__(self):
        logger.info("Initializing ReadingExcel..")
        self.config = self.load_config('../inputs/config.json')  # Load configuration from the JSON file
        self.sheet = pd.read_excel(self.config['paths']['excel_file'])  # Load the Excel file from the config

    def load_config(self, config_path):
        """Loads the configuration from a JSON file."""
        with open(config_path, 'r') as file:
            return json.load(file)

    def get_testIDs(self):
        # Get the Test Case IDs dynamically from the configured column name
        arr = self.sheet[self.config['excel_columns']['test_case_id']].tolist()
        logger.info(f"Test IDs extracted: {arr}")
        return arr

    def enter_data(self, tid):
        filtered_row = self.sheet[self.sheet[self.config['excel_columns']['test_case_id']] == tid]
        process = subprocess.Popen(
            ['python', self.config['paths']['python_script']],  # Load Python script path dynamically from the config
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Function to send input commands to the process
        def send_input(command):
            process.stdin.write(command + '\n')
            process.stdin.flush()
            time.sleep(0.1)

        # Sequence of inputs based on the commands from the config
        inputs = [
            self.config['inputs']['commands'][0], filtered_row[self.config['excel_columns']['source']].iloc[0],  # Enter source
            self.config['inputs']['commands'][1], filtered_row[self.config['excel_columns']['destination']].iloc[0],  # Enter destination
            self.config['inputs']['commands'][2], filtered_row[self.config['excel_columns']['date']].iloc[0].strftime('%Y-%m-%d'),  # Enter date
            self.config['inputs']['commands'][3], filtered_row[self.config['excel_columns']['name']].iloc[0],  # Enter name
            self.config['inputs']['commands'][4], str(filtered_row[self.config['excel_columns']['age']].iloc[0]),  # Enter age
            self.config['inputs']['commands'][5], str(filtered_row[self.config['excel_columns']['phone_number']].iloc[0]),  # Enter phone number
            self.config['inputs']['commands'][6]  # Done and show booking details
        ]

        # Send each input command to the process
        for user_input in inputs:
            logger.debug(f"Sending: {user_input}")
            send_input(user_input)

        # Now that all inputs are sent, capture all output (stdout and stderr)
        stdout_data, stderr_data = process.communicate()  # Capture output after all inputs

        # Display stdout and stderr for debugging purposes
        logger.debug("Stdout:\n" + stdout_data)
        logger.debug("Stderr:\n" + stderr_data)

        # Parse booking details if found in stdout
        booking_details = {}
        for key, pattern in self.config['patterns'].items():
            match = re.search(pattern, stdout_data)
            if match:
                booking_details[key] = match.group(1)

        # Print extracted booking details
        logger.info("\nExtracted Booking Details:")
        for key, value in booking_details.items():
            logger.info(f"{key}: {value}")

        return booking_details

    def extract_expected_output(self, tid):
        filtered_row = self.sheet[self.sheet[self.config['excel_columns']['test_case_id']] == tid]
        expected_output = {}
        expected_text = filtered_row[self.config['excel_columns']['expected_output']].iloc[0]

        # Extract each field in the expected output string based on the pattern from the config
        for key, pattern in self.config['patterns'].items():
            match = re.search(pattern, expected_text)
            if match:
                expected_output[key] = match.group(1)

        # Print extracted expected output details
        logger.info("\nExpected Output Details:")
        for key, value in expected_output.items():
            logger.info(f"{key}: {value}")

        return expected_output

    def compare(self, booking_details, expected_output):
        # Compare extracted booking details with expected output
        logger.info("\nComparison with Expected Output:")
        for key, expected_value in expected_output.items():
            extracted_value = booking_details.get(key)
            if extracted_value == expected_value:
                logger.info(f"{key}: Match")
                return "OK"
            else:
                logger.warning(f"{key}: Mismatch (Expected: {expected_value}, Got: {extracted_value})")
                return "NOT OK"
