import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.CLI_Automation import CLTAuto
import pytest
from Core.dev.Common_opts import Paths
from Core.utils.logging import get_logger


cli = CLTAuto()

# Retrieve test IDs and select the first one for testing
test_ids = cli.get_test_ids()
print(f"Test IDs: {test_ids}")

@pytest.mark.parametrize("test_ID", cli.get_test_ids())
def test_case(test_ID):
    log = get_logger(test_ID)
    log.info(f"Starting test with test_id : {test_ID}")

    # Get data for the first test ID
    test_data = cli.get_data(test_ID)
    log.info(f"Test Data: {test_data}")

    # Define the sequence of inputs
    inputs = [
        "1", test_data['Source'],  # Enter source
        "2", test_data['Destination'],  # Enter destination
        "3",  # Save entered source and destination
        "6",
        "1", test_data['Date'],  # Enter date
        "2", test_data['Name'],  # Enter name
        "3",
        "6",
        "1", int(test_data['Age']) if test_data['Age'] != '' else '',  # Enter age
        "2", int(test_data['Phone_Number']) if test_data['Phone_Number'] != '' else '',  # Enter phone number
        "3",
        "4", test_ID,  # Enter test ID
        "7"  # Quit
    ]

    cli.start_process()
    for i in inputs:
        Output = cli.enter_data(i)
        log.info(f"Entered input: {i}")
        log.info(f"Output for the input {i} is:")
        log.info(Output)

    excel_output = cli.extract_expected_output(test_ID)
    ticket_file_output = cli.ticket_file_data(Paths.ticket_dir + f"/{test_ID}.txt")
    Output = cli.compare(ticket_file_output, excel_output)
    cli.close_process()
    assert True if "OK" == Output else False