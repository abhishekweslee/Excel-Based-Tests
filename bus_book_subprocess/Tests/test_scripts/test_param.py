import sys
import os
from venv import logger

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.CLI_Automation import CLTAuto
import pytest
from Core.dev.Common_opts import Paths
from Core.utils.logging import get_logger


cli = CLTAuto()
log = get_logger()

# Retrieve test IDs and select the first one for testing
test_ids = cli.get_test_ids()
print(f"Test IDs: {test_ids}")

@pytest.mark.parametrize("test_id", cli.get_test_ids())
def test_case01(test_id):
    log.info(f"Starting test with test_id : {test_id}")

    # Get data for the first test ID
    test_data = cli.get_data(test_id)
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
        "4", test_id,  # Enter test ID
        "7"  # Quit
    ]
    cli.start_process()
    log.info(f"Sending inputs: {inputs}")
    cli.enter_data(inputs)

    excel_output = cli.extract_expected_output(test_id)
    log.info(f"Expected output from excel : {excel_output}")
    file = cli.find_largest_ticket_number(Paths.automatic_ticket_dir)
    ticket_file_output = cli.ticket_file_data(Paths.ticket_dir+f"/{test_id}.txt")
    log.info(f"Ticket File Output: {ticket_file_output}")
    #ticket_file_output = cli.ticket_file_data(Paths.ticket_dir + f"/{file}")


    Output = cli.compare(ticket_file_output, excel_output)
    log.info(f"Comparison Output: {Output}\n\n")
    cli.close_process()
    assert True if "OK" == Output else False