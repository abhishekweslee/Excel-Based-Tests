import sys
import os
import json
import pytest
import logging

from openpyxl.styles.builtins import output

# Clear root logger handlers
logging.getLogger().handlers.clear()

# Add project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.CLI_Automation import CLTAuto
from Core.dev.Common_opts import Paths
from Core.utils.logging import get_logger

def load_json(file_path):
    """Load JSON data from a given file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        pytest.fail(f"JSON file not found: {file_path}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Error decoding JSON file: {file_path}\n{str(e)}")

cli = CLTAuto()

# Retrieve test IDs and select the first one for testing
test_ids = cli.get_test_ids()

# Replace print with logging
log = get_logger("initialization")
log.info(f"Test IDs: {test_ids}")

@pytest.mark.parametrize("test_ID", cli.get_test_ids())
def test_case(test_ID):
    log = get_logger(test_ID)

    # Load JSON data
    data = load_json(Paths.pattern_path)

    # Retrieve test data for the first test ID
    test_data = cli.get_data(test_ID)
    if not test_data:
        pytest.fail(f"No test data found for Test ID: {test_ID}")

    # Define the sequence of inputs
    inputs = [
        ("1", data['Main_Menu']['Select']),
        (test_data['Source'], data['Ticket_Details']['Source']),
        ("2", data['Main_Menu']['Select']),
        (test_data['Destination'], data['Ticket_Details']['Destination']),
        ("3", data['Main_Menu']['Select']),
        ("6", data['Main_Menu']['Select']),
        ("1", data['Sub_Menu_1']['Select']),
        (test_data['Date'], data['Ticket_Details']['Date']),
        ("2", data['Sub_Menu_1']['Select']),
        (test_data['Name'], data['Ticket_Details']['Name']),
        ("3", data['Sub_Menu_1']['Select']),
        ("6", data['Sub_Menu_1']['Select']),
        ("1", data['Sub_Menu_2']['Select']),
        (int(test_data['Age']) if test_data['Age'] else '', data['Ticket_Details']['Age']),
        ("2", data['Sub_Menu_2']['Select']),
        (int(test_data['Phone_Number']) if test_data['Phone_Number'] else '', data['Ticket_Details']['Phone_No']),
        ("3", data['Sub_Menu_2']['Select']),
        ("4", data['Sub_Menu_2']['Select']),
        (test_ID, data['Ticket_Details']['File_Name']),
        ("7", data['Sub_Menu_2']['Select'])
    ]

    # Start the CLI process
    cli.start_process()
    try:
        for key, value in inputs:
            # Fetch output and verify the pattern
            output = cli.fetch_output(value)
            if value in output:
                cli.send_input(key)
                log.info(f"\n{output}{key}")
            else:
                log.warning(f"Pattern '{value}' not detected in the output. Skipping input '{key}'.")
                pytest.fail(f"Pattern '{value}' not detected for input '{key}'.")
    except Exception as e:
        log.error(f"Error during input processing: {str(e)}")
        pytest.fail(f"Test failed during input processing: {str(e)}")

    # Extract and compare outputs
    try:
        excel_output = cli.extract_expected_output(test_ID)
        ticket_file_path = os.path.join(Paths.ticket_dir, f"{test_ID}.txt")
        ticket_file_output = cli.ticket_file_data(ticket_file_path)
        comparison_result = cli.compare(ticket_file_output, excel_output)
    except Exception as e:
        log.error(f"Error during output extraction or comparison: {str(e)}")
        pytest.fail("Test failed during output comparison.")

    # Close the CLI process
    cli.close_process()

    # Assert the result
    assert comparison_result == "OK", "Test case failed: Output comparison did not return 'OK'."
