import re
import subprocess
import pandas as pd
import time

class ReadingExcel:
    def __init__(self):
        print("Initializing ReadingExcel..")
        self.sheet = pd.read_excel('Tests/test_inputs/Ticket_booking.xlsx')

    def get_testIDs(self):
        arr = self.sheet.iloc[:, 0].tolist()
        return arr

    def enter_data(self, tid):
        filtered_row = self.sheet[self.sheet['test_id'] == tid]
        process = subprocess.Popen(
            ['python3', '-m', 'Core.dev.dev_bus_ticket'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Function to send input commands to the process
        def send_input(command):
            print(f"Sending input: {command}")
            process.stdin.write(command + '\n')
            process.stdin.flush()

        # Function to read and print the output as it is generated
        def read_output():
            stdout_line = process.stdout.readline()
            count = 0
            while stdout_line:
                print(f"Output: {stdout_line.strip()}")  # Print the current output
                stdout_line = process.stdout.readline()




        # Sequence of inputs based on the menu
        inputs = [
            "1", "Hyderabad",  # Enter source
            "2", "kkd",  # Enter destination
            "4", "lochu",  # Save entered details
            "6",  # Go to Submenu1
            "6",  # Continue in Submenu1
            "7"  # Go to Submenu2
        ]

        # Capture initial output (first menu)
        print("Initial output from subprocess:")
        #read_output()  # Print the initial output before sending inputs

        # Send each input command to the process and read output immediately
        for user_input in inputs:
            time.sleep(1)  # Allow some time for output to be processed

            # Capture the output after sending the input
            print(f"Reading output after sending input: {user_input}")
            #read_output()
            print(f"Input sent: {user_input}")
            send_input(user_input)
            # Debugging line
            # Capture and print the output immediately after sending the input

        # Capture any remaining output after all inputs are sent
        print("Final output from subprocess:")
        read_output()

        # Capture stderr output if there is any error
        stderr_data = process.stderr.read()
        if stderr_data:
            print("Stderr:\n", stderr_data)

    def extract_expected_output(self, tid):
        filtered_row = self.sheet[self.sheet['test_id'] == tid]
        expected_output = {}
        expected_text = filtered_row['expected_output'].iloc[0]

        # Regular expression to extract each field in the expected output string
        expected_patterns = {
            "Source": r"Source:\s*(.*)",
            "Destination": r"Destination:\s*(.*)",
            "Name": r"Name:\s*(.*)",
            "Date": r"Date:\s*(.*)",
            "Age": r"Age:\s*(\d+)",
            "Phone Number": r"Phone Number:\s*(\d+)"
        }

        for key, pattern in expected_patterns.items():
            match = re.search(pattern, expected_text)
            if match:
                expected_output[key] = match.group(1)

        # Print extracted expected output details
        print("\nExpected Output Details:")
        for key, value in expected_output.items():
            print(f"{key}: {value}")

        return expected_output

    def compare(self, booking_details, expected_output):
        # Compare extracted booking details with expected output
        print("\nComparison with Expected Output:")
        result = "OK"
        for key, expected_value in expected_output.items():
            extracted_value = booking_details.get(key)
            if extracted_value == expected_value:
                print(f"{key}: Match")
            else:
                print(f"{key}: Mismatch (Expected: {expected_value}, Got: {extracted_value})")
                result = "NOT OK"
        return result


if __name__ == "__main__":
    data = ReadingExcel()
    arr = data.get_testIDs()

    # Assuming the first test ID is used for the booking process
    data.enter_data(arr[0])

    # Extract expected output for the first test ID
    expected_output = data.extract_expected_output(arr[0])

    # You would compare the actual output with the expected output here, if you can capture the booking details
    # Compare the results
    # result = data.compare(booking_details, expected_output)
    # print("\nFinal Result:", result)
