import pandas as pd
from datetime import datetime
import sys


class BusTicketBooking:
    def __init__(self):
        self.src = ''
        self.dest = ''
        self.d = ''
        self.nm = ''
        self.age = 0
        self.ph = ''

    def read_src(self):
        self.src = input("Enter source : ")
        return self.src

    def read_dest(self):
        self.dest = input("Enter destination : ")
        return self.dest

    def read_name(self):
        self.nm = input("Enter name : ")
        return self.nm

    def read_date(self):
        date = input("Enter travel date (YYYY-MM-DD): ")
        if isinstance(date, pd.Timestamp):
            date = date.strftime('%Y-%m-%d')  # Convert Timestamp to string

        try:
            travel_date = datetime.strptime(date, '%Y-%m-%d')
            if travel_date < datetime.now():
                print("Travel date cannot be in the past.")
                return
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
            return
        self.d = date
        return self.d

    def read_age(self):
        # Validate age input
        try:
            self.age = int(input("Enter your age: "))
            if self.age <= 0:
                raise ValueError
        except ValueError:
            print("Invalid age. Please enter a positive integer.")
        return self.age

    def read_phone(self):
        self.ph = input("Enter your phone number: ")

        # Simple phone number validation
        if not self.ph.isdigit() or len(self.ph) < 10:
            print("Invalid phone number. It should contain at least 10 digits.")
            return
        return self.ph

    def read_excel_data(self, file_path):
        df = pd.read_excel(file_path)
        return df

    def print_booking_details(self):

        return (
            f"Source: {self.src}\n"
            f"Destination: {self.dest}\n"
            f"Date: {self.d}\n"
            f"Name: {self.nm}\n"
            f"Age: {self.age}\n"
            f"Phone Number: {self.ph}"
        )

    def menu(self):
        print("\n--- Bus Ticket Booking ---")
        print("1. Enter source")
        print("2. Enter destination")
        print("3. Enter Date")
        print("4. Enter name")
        print("5. Enter age")
        print("6. Enter phone number")
        print("7. Done")

    def run(self):
        self.menu()

        while True:
            choice = input("Select an option between 1 to 7 : ")

            if choice == '1':
                self.read_src()
            elif choice == '2':
                self.read_dest()
            elif choice == '3':
                self.read_date()
            elif choice == '4':
                self.read_name()
            elif choice == '5':
                self.read_age()
            elif choice == '6':
                self.read_phone()
            elif choice == '7':
                self.print_booking_details()
                return


if __name__ == "__main__":
    booking = BusTicketBooking()
    booking.run()
