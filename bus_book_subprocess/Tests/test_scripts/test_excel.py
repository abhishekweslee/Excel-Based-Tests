import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Framework.CLI_Automation import CLTAuto
import pytest
from Core.dev.Common_opts import Paths


def test_case01():

    cli = CLTAuto()

    # Retrieve test IDs and select the first one for testing
    test_ids = cli.get_test_ids()
    print(f"Test IDs: {test_ids}")

    # Get data for the first test ID
    test_data = cli.get_data(test_ids[0])
    print(f"Test Data: {test_data}")

    # Define the sequence of inputs
    inputs = [
        "1", test_data['Source'],  # Enter source
        "2", test_data['Destination'],  # Enter destination
        "3",  # Save entered source and destination
        "6",
        "1", test_data['Date'],
        "2", test_data['Name'],
        "3",
        "6",
        "1", test_data['Age'],
        "2", test_data['Phone_Number'],
        "3",
        "4", test_ids[0],
        "8"  # Quit
    ]

    cli.enter_data(inputs)

    excel_output = cli.extract_expected_output(test_ids[0])
    ticket_file_output = cli.ticket_file_data(Paths.ticket_dir+f"/{test_ids[0]}.txt")
    Output = cli.compare(ticket_file_output, excel_output)
    cli.close_process()
    assert "OK" if "not" not in Output else "NOT OK"

# test_case01()