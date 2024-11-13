import subprocess
import pandas as pd
import re
import time

class ReadingExcel:
    def __init__(self):
        print("Initilizing ReadingExcel..")
        self.sheet = pd.read_excel('../inputs/ExcelDoc.xlsx')

    def get_testIDs(self):
        arr = self.sheet.iloc[:, 0].tolist()
        return arr

    def enter_data(self, tid):
        filtered_row = self.sheet[self.sheet['Test Case ID'] == tid]
        process = subprocess.Popen(
            ['python', '../inputs/dev_bus_ticket.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Function to send input commands to the process
        def send_input(command):
            process.stdin.write(command + '\n')
            process.stdin.flush()
            time.sleep(0.1)

        # Load data from Excel file

        # Sequence of inputs based on the menu
        inputs = [
            "1", filtered_row['Source'].iloc[0],  # Enter source
            "2", filtered_row['Destination'].iloc[0],  # Enter destination
            "3", filtered_row['Date'].iloc[0].strftime('%Y-%m-%d'),  # Enter date in string format
            "4", filtered_row['Name'].iloc[0],  # Enter name
            "5", str(filtered_row['Age'].iloc[0]),  # Enter age
            "6", str(filtered_row['Phone Number'].iloc[0]),  # Enter phone number
            "7"  # Done and show booking details
        ]

        # Send each input command to the process
        for user_input in inputs:
            print(f"Sending: {user_input}")
            send_input(user_input)

        # Now that all inputs are sent, capture all output (stdout and stderr)
        stdout_data, stderr_data = process.communicate()  # Capture output after all inputs

        # Display stdout and stderr for debugging purposes
        print("Stdout:\n", stdout_data)
        print("Stderr:\n", stderr_data)

        # Parse booking details if found in stdout
        booking_details = {}
        patterns = {
            "Source": r"Source:\s*(.*)",
            "Destination": r"Destination:\s*(.*)",
            "Name": r"Name:\s*(.*)",
            "Date": r"Date:\s*(.*)",
            "Age": r"Age:\s*(\d+)",
            "Phone Number": r"Phone Number:\s*(\d+)"
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, stdout_data)
            if match:
                booking_details[key] = match.group(1)

        # Print extracted booking details
        print("\nExtracted Booking Details:")
        for key, value in booking_details.items():
            print(f"{key}: {value}")

        return booking_details

    def extract_expected_output(self, tid):
        filtered_row = self.sheet[self.sheet['Test Case ID'] == tid]
        expected_output = {}
        expected_text = filtered_row['Expected Output'].iloc[0]

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
        for key, expected_value in expected_output.items():
            extracted_value = booking_details.get(key)
            if extracted_value == expected_value:
                print(f"{key}: Match")
                return "OK"
            else:
                print(f"{key}: Mismatch (Expected: {expected_value}, Got: {extracted_value})")
                return "NOT OK"

# if __name__ == "__main__":
#     data = ReadingExcel()
#     arr = data.get_testIDs()
#     booking_details = data.enter_data(arr[0])
#     expected_output = data.extract_expected_output(arr[0])
#     data.compare(booking_details, expected_output)