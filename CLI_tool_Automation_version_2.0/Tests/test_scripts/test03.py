from Framework.CLI_Automation import CLTAuto
import pytest

@pytest.fixture
def cli():
    """Fixture to initialize and clean up the CLI automation instance."""
    cli_instance = CLTAuto()
    yield cli_instance
    cli_instance.close_process()

@pytest.fixture(scope="module")
def all_test_ids(cli):
    """Fixture to retrieve all test IDs once for the module."""
    test_ids = cli.get_test_ids()
    assert test_ids, "No test IDs retrieved; ensure the test setup is correct."
    return test_ids

# Use the test IDs dynamically with parameterization
@pytest.mark.parametrize("test_id", all_test_ids)
def test_ticket_booking(cli, test_id):
    """Test the ticket booking workflow for each test ID."""
    test_data = cli.get_data(test_id)
    assert test_data, f"No test data retrieved for test ID {test_id}."

    # Define the sequence of inputs
    inputs = [
        "1", test_data['Source'],  # Enter source
        "2", test_data['Destination'],  # Enter destination
        "3",  # Save entered source and destination
        "6",
        "1", test_data['Date'],  # Enter date
        "2", test_data['Name'],  # Enter name
        "3",  # Save entered details
        "6",
        "1", test_data['Age'],  # Enter age
        "2", test_data['Phone_Number'],  # Enter phone number
        "3",  # Save entered details
        "4", test_id,  # Use the test ID for the booking
        "8"  # Quit
    ]

    # Enter data into the CLI
    cli.enter_data(inputs)

    # Extract outputs
    excel_output = cli.extract_expected_output(test_id)
    ticket_file_output = cli.ticket_file_data(
        f"/home/vlab/ExcelAuto/bus_book_subprocess/Tests/test_outputs/tickets/user_generated_tickets/{test_id}.txt"
    )

    # Compare outputs and assert results
    Output = cli.compare(ticket_file_output, excel_output)
    assert "not" not in Output, f"Test failed for test ID {test_id}. Comparison output: {Output}"

    print(f"Test case for test ID {test_id} passed.")
