import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.CLI_Automation import CLTAuto
import pytest
from Core.dev.Common_opts import Paths
from Core.utils.logging import get_logger



def test_case():

    cli = CLTAuto()

    # Retrieve test IDs and select the first one for testing
    test_ids = cli.get_test_ids()
    log = get_logger("outfile")
    log.info(f"Test IDs: {test_ids}")

    # Get data for the first test ID
    test_data = cli.get_data(test_ids[9])
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
        "7"  # Quit
    ]

    cli.start_process()
    for i in inputs:
        Output = cli.enter_data(i)
        log.info(f"Entered input: {i}")
        log.info(f"Output for the input {i} is:")
        log.info(Output)

    excel_output = cli.extract_expected_output(test_ids[9])
    file = cli.find_largest_ticket_number(Paths.automatic_ticket_dir)
    ticket_file_output = cli.ticket_file_data(Paths.automatic_ticket_dir+f"/{file}")
    Output = cli.compare(ticket_file_output, excel_output)
    cli.close_process()
    assert True if "OK" == Output else False