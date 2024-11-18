from Framework.CLI_Automation import CLTAuto
import pytest


def test_case01():
    # command = ["python", "-m", "Core.dev.dev_bus_ticket"]
    # excel_path = r"E:\Qemu\bus_book_subprocess\Tests\test_inputs\Ticket_booking.xlsx"

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
    ticket_file_output = cli.ticket_file_data(f"/home/vlab/ExcelAuto/bus_book_subprocess/Tests/test_outputs/tickets/user_generated_tickets/{test_ids[0]}.txt")
    Output = cli.compare(ticket_file_output, excel_output)
    cli.close_process()
    assert "OK" if "not" not in Output else "NOT OK"
