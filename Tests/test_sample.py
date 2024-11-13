import pytest
from Framework.Sample import ReadingExcel


@pytest.mark.parametrize("tid", ReadingExcel().get_testIDs())  # Parameterize with all test IDs
def test_booking_details(tid):
    data = ReadingExcel()

    # Fetch booking details and expected output based on the test ID (tid)
    booking_details = data.enter_data(tid)
    expected_output = data.extract_expected_output(tid)

    # Compare the details and assert the output is "OK"
    output = data.compare(booking_details, expected_output)

    assert output is "OK"

