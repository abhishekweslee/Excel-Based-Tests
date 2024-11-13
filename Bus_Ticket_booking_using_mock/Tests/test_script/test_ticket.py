import pytest
from unittest.mock import patch
import pandas as pd
from core.dev.dev_bus_ticket import BusTicketBooking
from core.utils.logging import get_logger
from Tests.test_inputs.file_paths import Paths

def generate_test_cases():
    df = pd.read_excel(Paths.excel_path)
    df.columns = df.columns.str.strip()
    test_cases = []
    for _, row in df.iterrows():
        test_cases.append((
            row['test_id'],
            row['src'],
            row['dest'],
            row['date'],
            row['name'],
            row['age'],
            row['ph no.'],
            row['expected_output'].replace('\\n', '\n')
        ))

    return test_cases

# Parametrize the test function using data from the Excel file
@pytest.mark.parametrize(
    "test_case_id, src, dest, date, name, age, ph_no, expected_output",
    generate_test_cases()
)
def test_ticket_booking(test_case_id, src, dest, date, name, age, ph_no, expected_output):
    print('+' * 50)
    print(f"Processing Test Case ID: {test_case_id}")

    log = get_logger(test_case_id)
    log.info(f"starting test case : {test_case_id}")

    # Mock the input function for each field
    with patch('builtins.input', side_effect=[src, dest, date, name, str(age), str(ph_no)]):
        # Create an instance of the BusTicketBooking class
        bus = BusTicketBooking()

        # Simulate user input by calling the methods
        bus.read_src()
        bus.read_dest()
        bus.read_date()
        bus.read_name()
        bus.read_age()
        bus.read_phone()


        booking_details = bus.print_booking_details()
        print('+' * 50)

        log.info(f"HERE IS YOUR BOOKED TICKET DETAILS of {test_case_id}:\n{booking_details}\n")
        log.info(f"Raw Expected Output from excel for Test Case ID {test_case_id}:\n{expected_output}\n")

        assert booking_details == expected_output, log.error(f"Test Case ID {test_case_id} FAILED: The booking details do not match.")
        log.info(f"Test Case ID {test_case_id} PASSED: The booking details match.\n")
