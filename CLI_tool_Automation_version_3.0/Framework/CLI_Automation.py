import subprocess
import pandas as pd
import time
import threading
import re
import sys
import os
from Core.dev.Common_opts import Paths
from Core.dev.dev_bus_ticket import *

class CLTAuto:
    def __init__(self):
        print("Initializing CLI Tool...")
        self.sheet = pd.read_excel(Paths.excel_path)
        self.process = None
        self.output_thread = None
        self.str = ""

    def start_process(self):
        self.process = subprocess.Popen(
            ["python3", "-m", "Core.dev.dev_bus_ticket"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def fetch_output(self, pattern):
        """
        Continuously fetch and display output from the subprocess.
        Stops when the pattern is detected or the subprocess ends.
        """
        self.str = ""

        def read_output():
            """Read output from the subprocess."""
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.str += output
                    sys.stdout.write(output)  # Write directly to stdout
                    sys.stdout.flush()  # Ensure immediate output

                    # Stop reading when the pattern is detected
                    if pattern in output:
                        break

        # Start a thread to read and display subprocess output
        self.output_thread = threading.Thread(target=read_output, daemon=True)
        self.output_thread.start()

        # Wait for the output thread to finish
        self.output_thread.join()

        # Return the collected output
        return self.str

    def send_input(self, input_data):
        """
        Send input to the subprocess.
        """
        if self.process:
            self.process.stdin.write(str(input_data) + '\n')
            self.process.stdin.flush()
            sys.stdout.write(str(input_data) + '\n')  # Write directly to stdout
            sys.stdout.flush()  # Ensure immediate output
        else:
            raise Exception("Process not initialized or not running.")

    def enter_data(self, input_data, pattern):
        """
        Combined method: fetch output and send input when the pattern is detected.
        """
        output = self.fetch_output(pattern)  # Fetch output until the pattern is found
        self.send_input(input_data)  # Send input once the pattern is detected
        return output

    def close_process(self):
        if self.process:
            self.process.terminate()
        if self.output_thread and self.output_thread.is_alive():
            self.output_thread.join()
        self.process = None

    def get_test_ids(self):
        """Retrieve all test IDs from the Excel sheet."""
        return self.sheet.iloc[:, 0].tolist()

    def get_data(self, test_id):
        """Retrieve test data for a given test ID."""
        filtered_row = self.sheet[self.sheet['test_id'] == test_id]
        if filtered_row.empty:
            raise ValueError(f"Test ID {test_id} not found in the sheet.")
        data_dict = {
            "Source": (
                filtered_row['src'].iloc[0]
                if 'src' in filtered_row and not filtered_row['src'].empty and pd.notna(filtered_row['src'].iloc[0])
                else ''
            ),
            "Destination": (
                filtered_row['dest'].iloc[0]
                if 'dest' in filtered_row and not filtered_row['dest'].empty and pd.notna(filtered_row['dest'].iloc[0])
                else ''
            ),
            "Date": (
                filtered_row['date'].iloc[0].strftime('%Y-%m-%d')
                if 'date' in filtered_row and not filtered_row['date'].empty and pd.notna(filtered_row['date'].iloc[0])
                else ''
            ),
            "Name": (
                filtered_row['name'].iloc[0]
                if 'name' in filtered_row and not filtered_row['name'].empty and pd.notna(filtered_row['name'].iloc[0])
                else ''
            ),
            "Age": (
                int(filtered_row['age'].iloc[0])
                if 'age' in filtered_row and not filtered_row['age'].empty and pd.notna(filtered_row['age'].iloc[0])
                else ''
            ),
            "Phone_Number": (
                int(filtered_row['ph no.'].iloc[0])
                if 'ph no.' in filtered_row and not filtered_row['ph no.'].empty and pd.notna(
                    filtered_row['ph no.'].iloc[0])
                else ''
            )
        }
        return data_dict

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

    def ticket_file_data(self, file_path):
        result_dict = {}
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    key, value = line.split(':', 1)  # Split only at the first colon
                    key, value = key.strip(), value.strip()
                    # Handle the "Date" key to keep only the date part
                    if key == "Date" and ' ' in value:
                        value = value.split(' ')[0]  # Keep only the date
                    result_dict[key] = value
        return result_dict

    def find_largest_ticket_number(self, folder_path):
        largest_number = -1
        largest_file = None
        ticket_pattern = re.compile(r"ticket(\d+)\.txt")

        # Iterate through all files in the folder
        for file_name in os.listdir(str(folder_path)):
            match = ticket_pattern.match(file_name)
            if match:
                # Extract the number and compare
                number = int(match.group(1))
                if number > largest_number:
                    largest_number = number
                    largest_file = file_name
        return largest_file


    def compare(self, booking_details, expected_output):
        # Compare extracted booking details with expected output
        print("\nComparison with Expected Output:")
        status = "OK"
        print(f"Excel output: {expected_output}")
        print(f"extracted output: {booking_details}")
        for key, expected_value in expected_output.items():
            extracted_value = booking_details.get(key)
            if extracted_value == expected_value:
                print(f"{key}: Match")
            else:
                print(f"{key}: Mismatch (Expected: {expected_value}, Got: {extracted_value})")
                status = "NOT OK"
        return status